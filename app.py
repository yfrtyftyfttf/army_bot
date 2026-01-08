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
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

def send_to_tele(endpoint, data):
    return requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/{endpoint}", json=data)

@app.route('/send_order', methods=['POST'])
def send_order():
    data = request.json
    u_name = data.get('user_name')
    o_type = data.get('type')
    details = data.get('details', {})
    acc_code = details.get('كود_الحساب', '---')
    
    msg = f"🔔 طلب جديد من: {u_name} (ID: {acc_code})\nنوع الطلب: {o_type}\n"
    for k, v in details.items(): msg += f"🔹 {k}: {v}\n"
    
    # أزرار الطلبات العادية
    if o_type == 'شحن رصيد':
        btn = [[{"text": "✅ قبول وشحن", "callback_data": f"add_{data['user_uid']}_{details['المبلغ']}"}]]
    else:
        btn = [[{"text": "✅ تم التنفيذ", "callback_data": "done"}]]

    send_to_tele("sendMessage", {"chat_id": CHAT_ID, "text": msg, "reply_markup": {"inline_keyboard": btn}})
    return jsonify({"status": "ok"})

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    
    # 1. نظام البحث (إذا أرسل الأدمن 6 أرقام)
    if "message" in update:
        text = update["message"].get("text", "")
        if text.isdigit() and len(text) == 6:
            users = db.collection('users').where('accountCode', '==', int(text)).stream()
            found = False
            for u in users:
                found = True
                user = u.to_dict()
                msg = f"👤 مستخدم موجود:\nالاسم: {user['name']}\nالرصيد: {user['balance']}$\nكود الحساب: {user['accountCode']}"
                btn = [[{"text": "➕ إضافة 5$", "callback_data": f"add_{user['uid']}_5"}, 
                        {"text": "➕ إضافة 10$", "callback_data": f"add_{user['uid']}_10"}]]
                send_to_tele("sendMessage", {"chat_id": CHAT_ID, "text": msg, "reply_markup": {"inline_keyboard": btn}})
            if not found:
                send_to_tele("sendMessage", {"chat_id": CHAT_ID, "text": "❌ لا يوجد حساب بهذا الكود."})

    # 2. تنفيذ العمليات (أزرار القبول)
    if "callback_query" in update:
        call = update["callback_query"]
        data = call["data"]
        if data.startswith("add_"):
            _, uid, amt = data.split("_")
            db.collection('users').document(uid).update({'balance': firestore.Increment(float(amt))})
            send_to_tele("answerCallbackQuery", {"callback_query_id": call["id"], "text": f"تم إضافة {amt}$"})
            send_to_tele("editMessageText", {"chat_id": CHAT_ID, "message_id": call["message"]["message_id"], "text": call["message"]["text"] + f"\n\n✅ تم الشحن بنجاح!"})

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
