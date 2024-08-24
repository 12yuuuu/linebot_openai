import requests
import os

def test_hugging_face_api():
    HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
    HF_API_TOKEN = os.getenv('HUGGING_FACE_API_KEY')

    if HF_API_TOKEN is None:
        print("Hugging Face API Token 未設置。請檢查環境變數。")
        return

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": "Hello, how are you?"}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        print(f"狀態碼: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("回應內容:", result)
        else:
            print("錯誤訊息:", response.text)
    except Exception as e:
        print("請求發生錯誤:", str(e))

if __name__ == "__main__":
    test_hugging_face_api()

