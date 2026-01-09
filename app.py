import os
import random
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# تفعيل CORS الشامل ضروري جداً لربط GitHub Pages بـ Render
CORS(app, resources={r"/*": {"origins": "*"}})

# تهيئة Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

BOT_TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
CHAT_ID = "6695916631"

@app.route('/')
def home():
    return "سيرفر الجيش يعمل بنجاح!", 200

@app.route('/send_order', methods=['POST', 'OPTIONS'])
def send_order():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        data = request.json
        u_uid = data.get('user_uid')
        u_name = data.get('user_name', 'عميل')
        o_type = data.get('type')
        details = data.get('details', {})
        o_id = f"{random.randint(1000, 9999)}"

        text = f"📦 طلب #{o_id} جديد\n👤 العميل: {u_name}\n🆔 UID: {u_uid}\n"
        text += "------------------------\n"
        for key, value in details.items():
            text += f"🔹 {key}: {value}\n"

        if o_type == 'شحن رصيد':
            amt = str(details.get('المبلغ', '0')).replace('$', '')
            buttons = [[
                {"text": "✅ قبول وشحن", "callback_data": f"add_{u_uid}_{amt}_{o_id}"},
                {"text": "❌ رفض", "callback_data": f"rej_{o_id}"}
            ]]
        else:
            prc = str(details.get('السعر', '0')).replace('$', '')
            buttons = [
                [{"text": "✅ تم التنفيذ", "callback_data": f"done_{o_id}"}],
                [{"text": f"❌ رفض وإرجاع {prc}$", "callback_data": f"ref_{u_uid}_{prc}_{o_id}"}]
            ]

        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
            "chat_id": CHAT_ID,
            "text": text,
            "reply_markup": {"inline_keyboard": buttons}
        })
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.json
    if "callback_query" in update:
        query = update["callback_query"]
        callback_data = query["data"]
        msg_id = query["message"]["message_id"]
        chat_id = query["message"]["chat"]["id"]
        parts = callback_data.split('_')
        
        try:
            action = parts[0]
            if action == "add": 
                uid, amt = parts[1], float(parts[2])
                db.collection('users').document(uid).update({'balance': firestore.Increment(amt)})
                res_txt = "✅ تم الشحن"
            elif action == "ref": 
                uid, prc = parts[1], float(parts[2])
                db.collection('users').document(uid).update({'balance': firestore.Increment(prc)})
                res_txt = "💰 تم الإرجاع"
            else: res_txt = "⚙️ نُفذ الإجراء"

            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", json={
                "chat_id": chat_id, "message_id": msg_id,
                "text": f"{query['message']['text']}\n\n⚙️ النتيجة: {res_txt}"
            })
        except: pass
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
