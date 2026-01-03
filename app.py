import telebot
import requests
import os
import threading

# --- إعدادات أساسية ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
ADMIN_ID = 6695916631  # آيدي حسابك

bot = telebot.TeleBot(BOT_TOKEN)

# دالة لجلب البروكسيات
def load_proxies():
    if os.path.exists('m2.txt'):
        with open('m2.txt', 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

@bot.message_handler(commands=['start'])
def welcome(message):
    proxies = load_proxies()
    msg = (f"🚀 **مرحباً بك في أداة الصيد المطورة**\n\n"
           f"📦 عدد البروكسيات: {len(proxies)}\n"
           f"⚙️ الحالة: جاهز للعمل\n\n"
           f"أرسل اسم المستخدم (User) الذي تريد بدء الصيد عليه:")
    bot.reply_to(message, msg, parse_mode="Markdown")

# هنا تبدأ عملية الصيد عند استقبال أي نص (اليوزر)
@bot.message_handler(func=lambda message: True)
def start_hunting(message):
    target_user = message.text
    proxies = load_proxies()
    
    if not proxies:
        bot.reply_to(message, "❌ خطأ: ملف البروكسيات فارغ!")
        return

    bot.send_message(message.chat.id, f"🔍 جاري محاولة صيد اليوزر: @{target_user}")
    
    # تجربة فحص باستخدام أول بروكسي كمثال
    proxy = proxies[0]
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    
    try:
        # مثال لطلب فحص (يمكنك تعديل الرابط حسب الموقع المستهدف)
        response = requests.get(f"https://www.instagram.com/{target_user}/", proxies=proxy_dict, timeout=5)
        if response.status_code == 404:
            bot.send_message(ADMIN_ID, f"🎯 صيد ثمين! اليوزر @{target_user} متاح.")
        else:
            bot.send_message(ADMIN_ID, f"Status: {response.status_code} | اليوزر غير متاح حالياً.")
    except:
        bot.send_message(ADMIN_ID, "⚠️ البروكسي الحالي بطيء أو لا يعمل، جرب بروكسي آخر.")

bot.infinity_polling()
