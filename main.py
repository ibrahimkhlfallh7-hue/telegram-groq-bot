import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

SYSTEM_PROMPT = """أنت مساعد مبيعات وخدمة عملاء ذكي لكتاب 'قسوة النبلاء'. 
مهمتك الإجابة على استفسارات العميل بلباقة وتشويق، ومساعدته في شراء الكتاب عبر النجوم أو موقع Getly.
كن محفزاً ومختصراً."""

def get_groq_response(user_text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    }
    try:
        res = requests.post(url, json=payload, headers=headers).json()
        return res['choices'][0]['message']['content']
    except Exception as e:
        return "أهلاً بك! أنا مساعد كتاب قسوة النبلاء، كيف يمكنني مساعدتك اليوم؟"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        
        reply = get_groq_response(text)
        
        send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(send_url, json={"chat_id": chat_id, "text": reply})
        
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
  
