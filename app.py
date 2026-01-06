from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from telebot import types
import uuid
import os
from threading import Thread

# ================== الإعدادات ==================
BOT_TOKEN = os.environ.get("6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k")     # توكن البوت (من Render)
ADMIN_ID = os.environ.get("6695916631")       # ايدي الأدمن (من Render)
PRICE_PER_1000 = 3.0

if not BOT_TOKEN or not ADMIN_ID:
    raise Exception("❌ BOT_TOKEN أو ADMIN_ID غير موجودين في Environment Variables")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# اسم موقعك على GitHub Pages
CORS(app, origins=["https://yfrtyftyfttf.github.io"])

# ================== بيانات مؤقتة ==================
users = {}
orders = {}

# ================== دوال ==================
def calc_price(qty: int) -> float:
    return round((qty / 1000) * PRICE_PER_1000, 2)

# ================== API ==================

@app.route("/api/register", methods=["POST"])
def register():
    uid = str(uuid.uuid4())[:8]
    users[uid] = {
        "balance": 0.0,
        "orders": []
    }
    return jsonify({"user_id": uid})


@app.route("/api/balance/<uid>", methods=["GET"])
def get_balance(uid):
    if uid not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[uid])


@app.route("/api/deposit", methods=["POST"])
def deposit():
    data = request.json
    uid = data.get("user_id")
    amount = float(data.get("amount", 0))

    if uid not in users:
        return jsonify({"error": "User not found"}), 404

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ قبول", callback_data=f"dep_ok_{uid}_{amount}"),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"dep_no_{uid}")
    )

    bot.send_message(
        ADMIN_ID,
        f"💳 طلب شحن\n"
        f"👤 المستخدم: {uid}\n"
        f"💰 المبلغ: ${amount}",
        reply_markup=markup
    )

    return jsonify({"status": "sent"})


@app.route("/api/order", methods=["POST"])
def create_order():
    data = request.json
    uid = data.get("user_id")
    qty = int(data.get("qty", 0))
    platform = data.get("platform")
    link = data.get("link")

    if uid not in users:
        return jsonify({"error": "User not found"}), 404

    cost = calc_price(qty)

    if users[uid]["balance"] < cost:
        return jsonify({"error": "رصيد غير كافي"}), 400

    users[uid]["balance"] -= cost

    order_id = str(uuid.uuid4())[:8]
    orders[order_id] = {
        "user": uid,
        "platform": platform,
        "qty": qty,
        "link": link,
        "cost": cost,
        "status": "pending"
    }

    users[uid]["orders"].append(order_id)

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔄 قيد التنفيذ", callback_data=f"ord_proc_{order_id}"),
        types.InlineKeyboardButton("✅ مكتمل", callback_data=f"ord_done_{order_id}")
    )

    bot.send_message(
        ADMIN_ID,
        f"🚀 طلب رشق جديد\n"
        f"🆔 {order_id}\n"
        f"📱 {platform}\n"
        f"🔢 {qty}\n"
        f"🔗 {link}\n"
        f"💵 ${cost}",
        reply_markup=markup
    )

    return jsonify({"order_id": order_id, "cost": cost})


@app.route("/api/order/<order_id>", methods=["GET"])
def track_order(order_id):
    if order_id not in orders:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(orders[order_id])

# ================== Telegram Callbacks ==================

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    data = call.data.split("_")

    # شحن
    if data[0] == "dep":
        uid = data[2]
        if data[1] == "ok":
            amount = float(data[3])
            users[uid]["balance"] += amount
            bot.edit_message_text(
                f"✅ تم شحن ${amount} للمستخدم {uid}",
                call.message.chat.id,
                call.message.message_id
            )
        else:
            bot.edit_message_text(
                "❌ تم رفض طلب الشحن",
                call.message.chat.id,
                call.message.message_id
            )

    # الطلبات
    if data[0] == "ord":
        order_id = data[2]
        if order_id not in orders:
            return

        if data[1] == "proc":
            orders[order_id]["status"] = "processing"
            bot.answer_callback_query(call.id, "تم تحويل الطلب إلى قيد التنفيذ")
        elif data[1] == "done":
            orders[order_id]["status"] = "completed"
            bot.edit_message_text(
                f"✅ الطلب {order_id} مكتمل",
                call.message.chat.id,
                call.message.message_id
            )

# ================== تشغيل البوت ==================
Thread(target=bot.infinity_polling, daemon=True).start()
