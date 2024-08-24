from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    PostbackEvent, MemberJoinedEvent
)
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# Predefined Q&A dictionary
QA_DICT = {
    "你好": "你好！有什麼我可以幫助你的嗎？",
    "你是誰": "我是一個簡單的Line機器人，可以回答一些基本問題。",
    "現在幾點": "對不起，我沒有時鐘功能。請查看您的設備時間。",
    "天氣如何": "我無法提供實時天氣信息。請查看天氣應用或網站以獲取準確信息。",
    # Add more Q&A pairs here...
}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg in QA_DICT:
        response = QA_DICT[msg]
    else:
        response = "對不起，我不理解您的問題。請嘗試其他問題。"
    
    message = TextSendMessage(text=response)
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_postback(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
