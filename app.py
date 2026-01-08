import os
import random
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# تهيئة Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

@app.route('/')
def home():
    return "سيرفر الجيش يعمل!"

@app.route('/send_order', methods=['POST'])
def send_order():
    data = request.json
    order_id = f"{random.randint(1000, 9999)}"
    text = f"📦 طلب #{order_id}\n👤 العميل: {data.get('user_name')}\n"
    for k, v in data.get('details', {}).items():
        text += f"🔹 {k}: {v}\n"
    
    # إرسال للتليجرام مع أزرار التحكم
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
        "chat_id": CHAT_ID,
        "text": text,
        "reply_markup": {"inline_keyboard": [[
            {"text": "✅ تنفيذ", "callback_data": f"done_{order_id}"},
            {"text": "❌ رفض وإرجاع", "callback_data": f"ref_{data.get('user_uid')}_{order_id}"}
        ]]}
    })
    return jsonify({"status": "success"}), 200

# مسار الـ Webhook لمعالجة ضغطات الأزرار
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    if "callback_query" in update:
        # هنا يتم معالجة الرصيد في Firestore تلقائياً عند ضغط الزر
        pass 
    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
