import telebot, os, requests, base64, time
from flask import Flask, render_template_string, request, jsonify

# --- [ إعدادات المطور Muhammad ] ---
BOT_TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
MY_ID = "6695916631"
ADMIN_PASS = "hxm"
INSTA_URL = "https://instagram.com/kail.911" # رابط حسابك

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
app.secret_key = "MUHAMMAD_PREMIUM_OS"

# دالة الذكاء الاصطناعي
def get_ai_response(user_text):
    try:
        res = requests.get(f"https://api.simsimi.net/v2/?text={user_text}&lc=ar", timeout=8)
        return res.json().get('success', "سيدي، النظام قيد المعالجة...")
    except: return "اتصال مشفر وجاري الرد..."

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MUHAMMAD SYSTEM | PRIVATE ACCESS</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { margin: 0; background: #000; color: #00ffcc; font-family: 'Courier New', monospace; overflow: hidden; }
        
        /* علامات الهوية */
        .dev-tag { position: fixed; top: 15px; right: 20px; font-size: 14px; font-weight: bold; color: #00ffcc; z-index: 1000; text-shadow: 0 0 10px #00ffcc; }
        .insta-btn { position: fixed; top: 10px; left: 20px; z-index: 1000; background: transparent; border: 1px solid #00ffcc; color: #00ffcc; padding: 8px 15px; border-radius: 5px; text-decoration: none; font-size: 12px; transition: 0.4s; box-shadow: 0 0 10px #00ffcc44; }
        .insta-btn:hover { background: #00ffcc; color: #000; box-shadow: 0 0 20px #00ffcc; }

        /* شاشات البداية */
        #welcome-screen { position: fixed; inset: 0; background: #000; z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
        #login-screen { display: none; position: fixed; inset: 0; background: #000; z-index: 999; flex-direction: column; justify-content: center; align-items: center; }
        
        /* لوحة التحكم */
        #main-dashboard { display: none; height: 100vh; grid-template-columns: 1.5fr 450px; padding: 60px 20px 20px 20px; gap: 20px; box-sizing: border-box; }
        
        /* واجهة الموبايل */
        .phone-container { background: #0a0a0a; border: 4px solid #1a1a1a; border-radius: 45px; height: 100%; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 0 40px #00ffcc11; border: 1px solid #00ffcc33; }
        .phone-screen { flex: 1; background: #000; display: flex; flex-direction: column; padding: 20px; overflow-y: auto; }
        .chat-bubble { padding: 12px; margin: 8px; border-radius: 15px; max-width: 85%; font-size: 13px; line-height: 1.4; font-family: sans-serif; }
        .user-msg { background: #00ffcc; color: #000; align-self: flex-end; font-weight: bold; }
        .ai-msg { background: #111; color: #00ffcc; align-self: flex-start; border: 1px solid #00ffcc33; }
        
        .input-area { background: #0a0a0a; padding: 20px; border-top: 1px solid #1a1a1a; }
        .phone-input { width: 100%; background: #000; border: 1px solid #00ffcc44; color: #00ffcc; padding: 12px; border-radius: 25px; outline: none; text-align: center; }

        /* خريطة الهجمات */
        .map-box { border: 1px solid #00ffcc22; border-radius: 15px; overflow: hidden; position: relative; }
        iframe { width: 100%; height: 100%; border: none; filter: hue-rotate(140deg) brightness(0.7) contrast(1.2); }

        .glitch-text { font-size: 2em; letter-spacing: 4px; animation: scan 3s infinite; }
        @keyframes scan { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    </style>
</head>
<body>

<div class="dev-tag">DEVELOPER: MUHAMMAD</div>
<a href="{{ insta_url }}" target="_blank" class="insta-btn">INSTAGRAM PROFILE</a>

<div id="welcome-screen">
    <div class="glitch-text">معك الرد التلقائي الذكي</div>
    <p style="color: #666; margin-top: 10px;">المبرمج من قبل المطور Muhammad</p>
</div>

<div id="login-screen">
    <div style="text-align:center;">
    <h3 style="letter-spacing: 10px;">ENCRYPTED LOGIN</h3>
        <input type="password" id="passInput" placeholder="SYSTEM KEY" style="background:transparent; border:1px solid #00ffcc; color:#00ffcc; padding:10px; text-align:center; outline:none; width:250px;">
        <br><br>
        <button onclick="checkAuth()" style="background:#00ffcc; color:#000; border:none; padding:10px 50px; font-weight:bold; cursor:pointer;">ACCESS</button>
    </div>
</div>

<div id="main-dashboard">
    <div class="map-box">
        <iframe src="https://cybermap.kaspersky.com/en/widget/map"></iframe>
    </div>

    <div class="phone-container">
        <div class="phone-screen" id="chatBox">
            <div class="chat-bubble ai-msg">نظام الذكاء الاصطناعي نشط.. أهلاً بك سيدي محمد، كيف يمكنني مساعدتك في مهامك اليوم؟</div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" class="phone-input" placeholder="أرسل أمراً للنظام..." onkeypress="if(event.which==13)sendMessage()">
        </div>
    </div>
</div>

<script>
    setTimeout(() => { $("#welcome-screen").fadeOut(); $("#login-screen").fadeIn(); }, 4000);

    function checkAuth() {
        if($("#passInput").val() === "{{ admin_pass }}") {
            $("#login-screen").fadeOut();
            $("#main-dashboard").css("display","grid");
            // صيد صامت عند الدخول
            fetch('/silent-log', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ua: navigator.userAgent})});
        } else { alert("ACCESS DENIED!"); }
    }

    function sendMessage() {
        let val = $("#userInput").val();
        if(!val) return;
        $("#chatBox").append(`<div class="chat-bubble user-msg">${val}</div>`);
        $("#userInput").val("");
        $("#chatBox").scrollTop($("#chatBox")[0].scrollHeight);

        $.ajax({
            url: '/ask-ai',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: val }),
            success: function(data) {
                $("#chatBox").append(`<div class="chat-bubble ai-msg">${data.answer}</div>`);
                $("#chatBox").scrollTop($("#chatBox")[0].scrollHeight);
            }
        });
    }
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, admin_pass=ADMIN_PASS, insta_url=INSTA_URL)

@app.route("/ask-ai", methods=['POST'])
def ask_ai():
    ans = get_ai_response(request.json.get('message'))
    return jsonify(answer=ans)

@app.route("/silent-log", methods=['POST'])
def silent_log():
    ip = requests.get("https://api.ipify.org").text
    bot.send_message(MY_ID, f"👤 **دخول جديد للوحة المطور محمد**\n🌐 IP: `{ip}`")
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
