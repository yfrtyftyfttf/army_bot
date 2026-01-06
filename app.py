from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from telebot import types
import uuid, os
from threading import Thread

# ====== إعدادات ======
TOKEN = os.environ.get"6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
ADMIN_ID = os.environ.get"6695916631"
PRICE_PER_1000 = 3.0

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app, origins=["https://yfrtyftyfttf.github.io"])

users = {}
orders = {}

def calc_price(qty):
    return round((qty / 1000) * PRICE_PER_1000, 2)

@app.route("/api/register", methods=["POST"])
def register():
    uid = str(uuid.uuid4())[:8]
    users[uid] = {"balance": 0.0, "orders": []}
    return jsonify({"user_id": uid})

@app.route("/api/balance/<uid>")
def balance(uid):
    if uid not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[uid])

@app.route("/api/deposit", methods=["POST"])
def deposit():
    data = request.json
    uid = data["user_id"]
    amount = float(data["amount"])

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ قبول", callback_data=f"dep_ok_{uid}_{amount}"),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"dep_no_{uid}")
    )

    bot.send_message(
        ADMIN_ID,
        f"💳 طلب شحن\n👤 {uid}\n💰 ${amount}",
        reply_markup=markup
    )
    return jsonify({"status": "sent"})

@app.route("/api/order", methods=["POST"])
def order():
    data = request.json
    uid = data["user_id"]

    if uid not in users:
        return jsonify({"error": "User not found"}), 404

    qty = int(data["qty"])
    cost = calc_price(qty)

    if users[uid]["balance"] < cost:
        return jsonify({"error": "رصيد غير كافي"}), 400

    users[uid]["balance"] -= cost
    oid = str(uuid.uuid4())[:8]

    orders[oid] = {"user": uid, "status": "pending"}
    users[uid]["orders"].append(oid)

    bot.send_message(ADMIN_ID, f"🚀 طلب جديد\nID: {oid}\nQty: {qty}")
    return jsonify({"order_id": oid, "cost": cost})

@bot.callback_query_handler(func=lambda c: True)
def callbacks(call):
    d = call.data.split("_")

    if d[0] == "dep":
        uid = d[2]
        if d[1] == "ok":
            amount = float(d[3])
            users[uid]["balance"] += amount
            bot.edit_message_text("✅ تم الشحن", call.message.chat.id, call.message.message_id)
        else:
            bot.edit_message_text("❌ مرفوض", call.message.chat.id, call.message.message_id)

Thread(target=bot.infinity_polling, daemon=True).start()
