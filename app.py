from flask import Flask, request, render_template
import telebot
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ========= Telegram Handlers =========
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 البوت شغال ومربوط بالموقع")

# ========= Webhook =========
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# ========= Pages =========
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", user="User")

# ========= Set Webhook =========
@app.before_first_request
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://army-bot-3y9o.onrender.com/{BOT_TOKEN}")

# ========= Run =========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
