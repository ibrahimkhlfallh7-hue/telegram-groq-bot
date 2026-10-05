import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

SYSTEM_PROMPT = """أنت مساعد مبيعات وخبير ذكي لكتاب 'قسوة النبلاء'. أجب عن أسئلة المستخدم بأسلوب إقناعي، ودود، واحترافي باللغة العربية."""

def get_groq_response(user_text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "عذراً، حدث خطأ أثناء الاتصال بنظام الذكاء الاصطناعي."
    except Exception as e:
        return "عذراً، حدث خطأ في الاتصال بالشبكة."

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]

        if user_text.strip() == "/start":
            reply_text = "أهلاً بك! أنا مساعدك الذكي لكتاب قسوة النبلاء. كيف يمكنني مساعدتك اليوم؟"
        else:
            reply_text = get_groq_response(user_text)

        send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(send_url, json={"chat_id": chat_id, "text": reply_text})

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
