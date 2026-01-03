import telebot
import requests
import os
import random
import time

# --- [1] إعدادات الهوية ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
ADMIN_ID = 6695916631 

bot = telebot.TeleBot(BOT_TOKEN)
hunting_active = False
found_accounts_file = "hunted.txt" # ملف حفظ الصيد

# إحصائيات الفحص
stats = {"checked": 0, "found": 0, "errors": 0}

def generate_random_user():
    length = random.randint(4, 8)
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890._'
    return ''.join(random.choice(chars) for i in range(length))

def get_random_proxy():
    try:
        if os.path.exists('m2.txt'):
            with open('m2.txt', 'r') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
                if proxies:
                    p = random.choice(proxies).split(':')
                    return {"http": f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}", "https": f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"}
    except: return None
    return None

def check_email_available(email):
    try:
        url = f"https://login.live.com/CheckIdp.srf?sdk=1&uaid=dbe&u={email}"
        res = requests.get(url, timeout=5)
        return '"IfExistsResult":1' in res.text
    except: return False

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("1️⃣ صيد", "2️⃣ وقف الصيد استاذ محمد")
    markup.add("3️⃣ أعرض الحسابات التي تم صيدها")
    
    welcome_msg = (
        "👋 أهلاً بك أستاذ محمد في لوحة التحكم\n\n"
        "📊 **شاشة تفاصيل الفحص:**\n"
        f"━━━━━━━━━━━━━━\n"
        f"✅ تم فحص: {stats['checked']}\n"
        f"🎯 تم صيد: {stats['found']}\n"
        f"⚠️ أخطاء البروكسي: {stats['errors']}\n"
        f"━━━━━━━━━━━━━━\n"
        "اختر أحد الأوامر من الأزرار بالأسفل بالأسفل:"
    )
    bot.reply_to(message, welcome_msg, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "1️⃣ صيد")
def start_hunting(message):
    global hunting_active
    if hunting_active:
        bot.reply_to(message, "⚠️ الصيد يعمل بالفعل أستاذ محمد.")
        return
    
    hunting_active = True
    bot.reply_to(message, "🚀 انطلق الصيد التلقائي... سأوافيك بالنتائج فوراً.")
    
    while hunting_active:
        user = generate_random_user()
        proxy = get_random_proxy()
        email = f"{user}@hotmail.com"
        stats['checked'] += 1
        
        try:
            res_insta = requests.get(f"https://www.instagram.com/{user}/", proxies=proxy, timeout=5)
            if res_insta.status_code == 404:
                if check_email_available(email):
                    stats['found'] += 1
                    account_info = f"👤 @{user} | 📧 {email}"
                    
                    # حفظ في الملف
                    with open(found_accounts_file, "a") as f:
                        f.write(account_info + "\n")
                    
                    text = (f"🎯 **صيد جديد ومؤكد!**\n\n"
                            f"{account_info}\n\n"
                            f"✅ اليوزر والإيميل متاحان للإنشاء.")
                    bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
        except:
            stats['errors'] += 1
        
        # تحديث شاشة الفحص كل 50 محاولة (للحفاظ على سرعة السيرفر)
        if stats['checked'] % 50 == 0:
            print(f"Status: Checked {stats['checked']} accounts...")
            
        time.sleep(0.4)

@bot.message_handler(func=lambda m: m.text == "2️⃣ وقف الصيد استاذ محمد")
def stop_hunting(message):
    global hunting_active
    hunting_active = False
    bot.reply_to(message, "🛑 حاضر أستاذ محمد، تم إيقاف الصيد بنجاح.")

@bot.message_handler(func=lambda m: m.text == "3️⃣ أعرض الحسابات التي تم صيدها")
def show_hunted(message):
    if os.path.exists(found_accounts_file):
        with open(found_accounts_file, "r") as f:
            data = f.read()
        if data:
            bot.reply_to(message, f"📋 **قائمة الصيد الثمين:**\n\n{data}")
        else:
            bot.reply_to(message, "📁 الملف فارغ، لم يتم صيد حسابات بعد.")
    else:
        bot.reply_to(message, "❌ لا يوجد سجل صيد حالياً.")

bot.infinity_polling()
