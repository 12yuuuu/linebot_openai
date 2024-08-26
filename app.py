from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    PostbackEvent, MemberJoinedEvent
)
import os
app = Flask(name)
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# Predefined Q&A dictionary
QA_DICT = {
    # 基本對話
    "你好": "你好！我是你的日常助手。需要記錄今天的活動，查看帳戶信息，或只是聊聊天嗎？",
    "你是誰": "我是一個設計用來幫助你記錄日常活動和管理帳戶的聊天機器人。",
    "再見": "再見！希望今天過得愉快。別忘了記錄今天的精彩時刻哦！",
    "謝謝": "不客氣！很高興能幫到你。",
    # 日常記錄
    "如何記錄活動": "要記錄活動，只需要說「記錄」，然後告訴我你做了什麼。例如：「記錄：今天去公園跑步30分鐘」。",
    "查看今日記錄": "好的，我會為你顯示今天的所有記錄。請注意，這是一個示例回覆，實際功能需要與後端數據庫集成。",
    "本週總結": "我可以為你總結本週的活動。這個功能可以幫助你回顧一週的成就和進展。",
    # 帳戶管理
    "查看帳戶餘額": "抱歉，我現在無法顯示實際的帳戶餘額。這個功能需要與真實的帳戶系統集成。",
    "記錄支出": "要記錄支出，請說「支出」，然後告訴我金額和類別。例如：「支出50元，午餐」。",
    "記錄收入": "要記錄收入，請說「收入」，然後告訴我金額和來源。例如：「收入1000元，薪水」。",
    "查看本月支出": "我可以幫你統計本月的支出情況。這可以幫助你更好地管理財務。",
    # 提醒功能
    "設置提醒": "要設置提醒，請說「提醒」，然後告訴我內容和時間。例如：「提醒下午3點開會」。",
    "查看所有提醒": "好的，我會列出你所有的提醒事項。請注意，這需要與日曆或提醒系統集成。",
    # 其他功能
    "今天天氣": "抱歉，我沒有實時天氣信息。你可以查看天氣 app 或網站獲取準確信息。",
    "幫助": "我可以幫你記錄日常活動、管理帳戶、設置提醒。需要了解具體功能可以問我「如何記錄活動」、「如何記錄支出」等。也可以叫我講個笑話！",
    # 閒聊
    "今天過得怎麼樣": "作為一個 AI 助手，我沒有個人的一天。但我很高興能夠幫助你！你今天過得如何？",
    "講個笑話": "好的，這是一個笑話：為什麼電腦會累？因為它要常常運行。",
    "我感到沮喪": "我理解你現在感到沮喪。記住，這只是暫時的感受。也許做一些你喜歡的事情會讓心情好一些？",
    # 默認回覆
    "default": "？"
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
    msg = event.message.text.strip().lower()

    if msg in QA_DICT:
        response = QA_DICT[msg]
    else:
        # Check if the message starts with specific keywords
        if msg.startswith("記錄"):
            response = "好的，我已經記錄下來了：" + msg[2:]
        elif msg.startswith("今天"):
            response = "已記錄今天" + msg[2:] + "，哈哈"
        elif msg.startswith("支出"):
            response = "已記錄支出：" + msg[2:]
        elif msg.startswith("收入"):
            response = "已記錄收入：" + msg[2:]
        elif msg.startswith("提醒"):
            response = "好的，我會提醒你：" + msg[2:]
        elif msg.startswith("刪除"):
            response = "不能刪喔，哈哈"
        else:
            response = QA_DICT["default"]

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
if name == "main":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
