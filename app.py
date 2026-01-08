import os
import random
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. إعداد Firebase
# تأكد من رفع ملف serviceAccountKey.json على GitHub
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. إعدادات تليجرام
BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

# --- مسار استقبال الطلبات من الموقع ---
@app.route('/send_order', methods=['POST'])
def send_order():
    try:
        data = request.json
        order_type = data.get('type')
        details = data.get('details')
        user_uid = data.get('user_uid')
        user_name = data.get('user_name', 'عميل غير معروف')
        
        order_id = f"{random.randint(1000, 9999)}"

        # بناء نص الرسالة للبوت
        text = f"📦 طلب جديد #{order_id}\n"
        text += f"👤 العميل: {user_name}\n"
        text += f"🆔 معرف المستخدم: {user_uid}\n"
        text += "------------------------\n"
        for key, value in details.items():
            text += f"🔹 {key}: {value}\n"

        # إعداد الأزرار التفاعلية
        buttons = []
        if order_type == 'شحن رصيد':
            amount = details.get('المبلغ', '0')
            buttons = [[
                {"text": "✅ قبول وشحن الرصيد", "callback_data": f"add_{user_uid}_{amount}_{order_id}"},
                {"text": "❌ رفض الطلب", "callback_data": f"msg_{user_uid}_عذراً، كود الشحن غير صحيح"}
            ]]
        else:
            # استخراج السعر لإرجاعه في حال الرفض
            price = details.get('السعر', '0').replace('$', '')
            buttons = [
                [{"text": "✅ تم التنفيذ", "callback_data": f"done_{order_id}"}],
                [{"text": "❌ رفض وإرجاع المال", "callback_data": f"ref_{user_uid}_{price}_{order_id}"}]
            ]

        # إرسال الرسالة مع الأزرار إلى تليجرام
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text,
            "reply_markup": {"inline_keyboard": buttons}
        }
        requests.post(url, json=payload)
        
        return jsonify({"status": "success", "order_id": order_id}), 200
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

# --- مسار الـ Webhook لمعالجة ردود أفعال البوت (الأزرار) ---
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.json
    
    if "callback_query" in update:
        query = update["callback_query"]
        callback_data = query["data"]
        msg_id = query["message"]["message_id"]
        
        parts = callback_data.split('_')
        action = parts[0]
        
        response_msg = ""
        
        try:
            if action == "add": # قبول شحن رصيد
                uid, amount, oid = parts[1], float(parts[2]), parts[3]
                user_ref = db.collection('users').doc(uid)
                user_ref.update({'balance': firestore.Increment(amount)})
                response_msg = f"✅ تم شحن {amount}$ للحساب بنجاح (طلب #{oid})"
                
            elif action == "ref": # رفض طلب رشق وإرجاع الأموال
                uid, price, oid = parts[1], float(parts[2]), parts[3]
                user_ref = db.collection('users').doc(uid)
                user_ref.update({'balance': firestore.Increment(price)})
                response_msg = f"💰 تم رفض طلب #{oid} وإعادة {price}$ للرصيد"
                
            elif action == "done": # تأكيد تنفيذ فقط
                oid = parts[1]
                response_msg = f"🎉 تم تحديث حالة الطلب #{oid} إلى: مكتمل"

            elif action == "msg": # إرسال رسالة تنبيه فقط
                uid, note = parts[1], parts[2]
                response_msg = f"⚠️ تم إرسال تنبيه للمستخدم: {note}"

            # تحديث الرسالة في تليجرام لإزالة الأزرار وتأكيد العملية
            update_url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
            requests.post(update_url, json={
                "chat_id": CHAT_ID,
                "message_id": msg_id,
                "text": f"{query['message']['text']}\n\n⚙️ الإجراء: {response_msg}"
            })

        except Exception as e:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                          json={"chat_id": CHAT_ID, "text": f"❌ خطأ في النظام: {str(e)}"})

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
