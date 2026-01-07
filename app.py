import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

@app.route('/')
def home():
    return "سيرفر الجيش يعمل بنجاح!"

@app.route('/send_order', methods=['POST'])
def send_order():
    try:
        data = request.json
        order_type = data.get('type')
        details = data.get('details')

        message = f"🚨 {order_type} جديد\n"
        message += "------------------------\n"
        for key, value in details.items():
            message += f"🔹 {key}: {value}\n"
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == '__main__':
    # مهم جداً لعمل الرابط أونلاين
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
