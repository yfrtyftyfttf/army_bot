import os
import sqlite3
import telebot
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
app.secret_key = "super_secret_key_123"

# ================= DATABASE =================
def get_db():
    return sqlite3.connect("database.db")

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        telegram_id INTEGER
    )
    """)
    db.commit()
    db.close()

init_db()

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect("/dashboard")

        return "بيانات خطأ"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= BOT =================
@bot.message_handler(commands=["start"])
def start(message):
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE telegram_id = ?", (message.from_user.id,)
    ).fetchone()

    if user:
        bot.reply_to(message, "✅ حسابك مربوط بالموقع")
    else:
        bot.reply_to(
            message,
            "❌ حسابك غير مسجل\nسجّل من الموقع أولاً"
        )
    db.close()

# ================= RUN =================
if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: bot.infinity_polling(skip_pending=True)).start()
    app.run(host="0.0.0.0", port=5000)
