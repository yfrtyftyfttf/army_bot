import os
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

BOT_TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
CHAT_ID = "6695916631"

@app.route('/send_order', methods=['POST', 'OPTIONS'])
def send_order():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    try:
        data = request.json
        msg = f"🔔 طلب جديد: {data['type']}\n👤 الاسم: {data['user_name']}\n🆔 الكود: {data.get('acc_code', '---')}\n"
        for k, v in data.get('details', {}).items(): msg += f"🔹 {k}: {v}\n"
        
        kb = [[{"text": "✅ تنفيذ", "callback_data": f"add_{data['user_uid']}_{data['details'].get('المبلغ', 0)}"}]] if data['type'] == 'شحن رصيد' else [[{"text": "✅ تم", "callback_data": "done"}]]
        
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "reply_markup": {"inline_keyboard": kb}})
        return jsonify({"status": "success"}), 200
    except: return jsonify({"status": "error"}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    if "message" in update:
        text = update["message"].get("text", "")
        if text.isdigit() and len(text) == 6: # البحث عن الكود
            users = db.collection('users').where('accountCode', '==', int(text)).stream()
            found = False
            for u in users:
                found = True
                user = u.to_dict()
                msg = f"👤 مستخدم: {user['name']}\n💰 الرصيد: {user['balance']}$\n🆔 الكود: {user['accountCode']}"
                kb = [[{"text": "➕ إضافة 5$", "callback_data": f"add_{user['uid']}_5"}, {"text": "➕ إضافة 10$", "callback_data": f"add_{user['uid']}_10"}]]
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "reply_markup": {"inline_keyboard": kb}})
            if not found: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": "❌ لا يوجد مستخدم."})

    if "callback_query" in update:
        call = update["callback_query"]
        if call["data"].startswith("add_"):
            _, uid, amt = call["data"].split("_")
            db.collection('users').document(uid).update({'balance': firestore.Increment(float(amt))})
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", json={"chat_id": CHAT_ID, "message_id": call["message"]["message_id"], "text": call["message"]["text"] + f"\n\n✅ تم شحن {amt}$"})

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
