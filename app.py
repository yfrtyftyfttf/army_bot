import telebot
import requests
import time

# --- [1] إعدادات البوت ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
ADMIN_ID = 6695916631 

bot = telebot.TeleBot(BOT_TOKEN)

# --- [2] قائمة البروكسيات المدمجة ---
# ضع البروكسيات الخاصة بك هنا (مثال: IP:PORT أو USER:PASS@IP:PORT)
PROXIES = [
    "123.456.789.01:8080",
    "987.654.321.01:3128",
    # أضف بقية الـ 50 بروكسي هنا بنفس التنسي82.24.249.101:5938:njhuvsdz:wp92l0dkdkoc 
82.29.244.57:5880:njhuvsdz:wp92l0dkdkoc 
198.89.123.107:6649:njhuvsdz:wp92l0dkdkoc 
206.206.71.75:5715:njhuvsdz:wp92l0dkdkoc 
23.27.210.135:6505:njhuvsdz:wp92l0dkdkoc 
64.137.49.9:6550:njhuvsdz:wp92l0dkdkoc 
66.63.180.174:5698:njhuvsdz:wp92l0dkdkoc 
149.57.17.176:5644:njhuvsdz:wp92l0dkdkoc 
154.6.59.162:6630:njhuvsdz:wp92l0dkdkoc 
91.211.87.224:7214:njhuvsdz:wp92l0dkdkoc 
199.180.8.177:5888:njhuvsdz:wp92l0dkdkoc 
82.24.247.128:6962:njhuvsdz:wp92l0dkdkoc 
198.105.119.196:5445:njhuvsdz:wp92l0dkdkoc 
82.21.244.100:5423:njhuvsdz:wp92l0dkdkoc 
82.25.213.249:5601:njhuvsdz:wp92l0dkdkoc 
31.59.27.107:6684:njhuvsdz:wp92l0dkdkoc 
45.43.87.128:7877:njhuvsdz:wp92l0dkdkoc 
64.137.89.162:6235:njhuvsdz:wp92l0dkdkoc 
142.147.245.203:5894:njhuvsdz:wp92l0dkdkoc 
23.229.125.169:5438:njhuvsdz:wp92l0dkdkoc 
31.223.189.234:6500:njhuvsdz:wp92l0dkdkoc 
45.41.171.41:6077:njhuvsdz:wp92l0dkdkoc 
205.164.57.143:5718:njhuvsdz:wp92l0dkdkoc 
82.23.222.10:6316:njhuvsdz:wp92l0dkdkoc 
209.242.203.117:6832:njhuvsdz:wp92l0dkdkoc 
64.137.8.175:6857:njhuvsdz:wp92l0dkdkoc 
23.27.138.82:6183:njhuvsdz:wp92l0dkdkoc 
142.147.244.113:6357:njhuvsdz:wp92l0dkdkoc 
82.23.222.38:6344:njhuvsdz:wp92l0dkdkoc 
23.27.208.117:5827:njhuvsdz:wp92l0dkdkoc 
31.59.33.141:6717:njhuvsdz:wp92l0dkdkoc 
142.202.254.57:6035:njhuvsdz:wp92l0dkdkoc 
82.22.235.92:6898:njhuvsdz:wp92l0dkdkoc 
195.40.187.2:5184:njhuvsdz:wp92l0dkdkoc 
66.63.180.153:5677:njhuvsdz:wp92l0dkdkoc 
82.29.249.54:7891:njhuvsdz:wp92l0dkdkoc 
108.165.227.16:5257:njhuvsdz:wp92l0dkdkoc 
82.24.217.12:5342:njhuvsdz:wp92l0dkdkoc 
45.131.92.195:6806:njhuvsdz:wp92l0dkdkoc 
104.245.244.5:6445:njhuvsdz:wp92l0dkdkoc 
145.223.47.135:6717:njhuvsdz:wp92l0dkdkoc 
64.137.99.193:5826:njhuvsdz:wp92l0dkdkoc 
204.217.161.171:6743:njhuvsdz:wp92l0dkdkoc 
107.181.148.69:5929:njhuvsdz:wp92l0dkdkoc 
173.211.30.43:6477:njhuvsdz:wp92l0dkdkoc 
181.214.13.96:5937:njhuvsdz:wp92l0dkdkoc 
104.252.41.95:7032:njhuvsdz:wp92l0dkdkoc 
45.41.171.35:6071:njhuvsdz:wp92l0dkdkoc 
46.203.154.160:5603:njhuvsdz:wp92l0dkdkoc 
82.23.204.254:7086:njhuvsdz:wp92l0dkdkocق
]

def check_email_availability(email):
    """فحص هل الإيميل متاح (محذوف من الشركة)"""
    # ملاحظة: فحص الإيميل يتطلب API خاص بكل شركة (Outlook/Yahoo)
    # سنضع هنا منطقاً بسيطاً للفحص كمثال
    try:
        response = requests.get(f"https://api.test-email.com/check?email={email}", timeout=5)
        return response.json().get("available", False)
    except:
        return False

def check_instagram_user(username, proxy):
    """فحص هل اليوزر متاح في انستقرام باستخدام بروكسي"""
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        url = f"https://www.instagram.com/{username}/"
        res = requests.get(url, proxies=proxy_dict, timeout=5)
        # إذا كانت النتيجة 404 يعني الحساب متاح أو محذوف
        return res.status_code == 404
    except:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 أداة صيد (انستا + إيميل) جاهزة!\n\nأرسل اليوزر الذي تريد فحصه:")

@bot.message_handler(func=lambda m: True)
def hunt(message):
    target = message.text
    bot.send_message(ADMIN_ID, f"🔍 بدأنا فحص اليوزر: @{target}")
    
    # استخدام أول بروكسي متاح
    current_proxy = PROXIES[0] if PROXIES else None
    
    is_insta_available = check_instagram_user(target, current_proxy)
    
    if is_insta_available:
        # إذا كان متاح، نفحص الإيميل المرتبط (افتراضاً أنه بنفس الاسم)
        email_to_check = f"{target}@hotmail.com"
        is_email_available = check_email_availability(email_to_check)
        
        if is_email_available:
            bot.send_message(ADMIN_ID, f"🎯 صيد ثمين!\n👤 يوزر: @{target}\n📧 إيميل متاح: {email_to_check}\n🔗 الحالة: متاح للربط!")
        else:
            bot.send_message(ADMIN_ID, f"⚠️ اليوزر @{target} متاح، لكن الإيميل غير متاح.")
    else:
        bot.send_message(ADMIN_ID, f"❌ اليوزر @{target} غير متاح في انستقرام.")

bot.infinity_polling()
