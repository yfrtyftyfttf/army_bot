import telebot, os, requests
from flask import Flask, render_template_string, request, jsonify

# --- [ إعدادات محمد - نسخة السرعة الصافية ] ---
ADMIN_PASS = "hx2026"
INSTA_URL = "https://instagram.com/kail.911"

app = Flask(__name__)

# دالة الذكاء الاصطناعي أصبحت الآن الأولوية الوحيدة
def get_fast_reply(text):
    try:
        # محرك مباشر بدون وسيط
        r = requests.get(f"https://api.simsimi.net/v2/?text={text}&lc=ar", timeout=2)
        return r.json().get('success', "أمرك مطاع سيدي.")
    except:
        return "النظام مستعد.."

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MUHAMMAD FAST OS</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { margin:0; background:#000; color:#00ffcc; font-family:sans-serif; overflow:hidden; height:100vh; }
        .nav { position:fixed; top:0; width:100%; height:50px; background:rgba(0,0,0,0.95); display:flex; justify-content:space-between; align-items:center; padding:0 15px; border-bottom:1px solid #00ffcc44; z-index:1000; box-sizing:border-box; }
        #dash { display:none; flex-direction:column; height:100vh; padding-top:50px; }
        .map { height:20%; border-bottom:1px solid #00ffcc22; opacity:0.6; }
        .chat { flex:1; display:flex; flex-direction:column; background:#050505; position:relative; overflow:hidden; }
        .msgs { flex:1; padding:15px; overflow-y:auto; display:flex; flex-direction:column; gap:10px; padding-bottom:80px; }
        .m { padding:12px 18px; border-radius:18px; font-size:16px; max-width:85%; box-shadow: 0 2px 5px rgba(0,0,0,0.5); }
        .u { background:#00ffcc; color:#000; align-self:flex-start; font-weight:bold; }
        .a { background:#111; color:#00ffcc; border:1px solid #00ffcc22; align-self:flex-end; }
        .box { position:absolute; bottom:0; width:100%; padding:15px; background:#000; display:flex; box-sizing:border-box; border-top:1px solid #1a1a1a; }
        input { flex:1; background:#000; border:1px solid #00ffcc77; color:#00ffcc; padding:12px; border-radius:25px; outline:none; text-align:center; font-size:16px; }
        #login { height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; }
        .btn { margin-top:15px; background:#00ffcc; color:#000; border:none; padding:12px 50px; font-weight:bold; border-radius:30px; cursor:pointer; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="{{ insta }}" target="_blank" style="color:#00ffcc; text-decoration:none; font-size:12px; border:1px solid #00ffcc; padding:3px 10px; border-radius:15px;">@kail.911</a>
        <div style="font-size:12px; font-weight:bold;">MUHAMMAD TURBO</div>
    </div>
    <div id="login">
        <h2 style="letter-spacing:2px;">نظام السرعة القصوى</h2>
        <input type="password" id="p" placeholder="PASSWORD" style="width:230px; padding:15px; background:none; border:1px solid #00ffcc; color:#00ffcc; border-radius:10px; text-align:center;">
        <button onclick="auth()" class="btn">دخول</button>
    </div>
    <div id="dash">
        <div class="map"><iframe src="https://cybermap.kaspersky.com/en/widget/map" style="width:100%; height:100%; border:none; filter:hue-rotate(150deg);"></iframe></div>
        <div class="chat">
            <div class="msgs" id="ms"><div class="m a">مرحباً سيدي محمد. تم تحويل كافة موارد السيرفر للذكاء الاصطناعي لضمان أسرع رد ممكن.</div></div>
            <div class="box"><input type="text" id="ui" placeholder="اكتب رسالتك..." onkeypress="if(event.which==13)send()"></div>
        </div>
    </div>
    <script>
        function auth(){ if($("#p").val()==="{{pass}}"){$("#login").hide();$("#dash").css("display","flex");}else{alert("ERROR");} }
        function send(){ 
            let t=$("#ui").val(); if(!t)return;
            $("#ms").append(`<div class="m u">${t}</div>`); $("#ui").val("");
            $.ajax({
                url: '/ai', type: 'POST', contentType: 'application/json',
                data: JSON.stringify({ msg: t }),
                success: function(r) {
                    $("#ms").append(`<div class="m a">${r.ans}</div>`);
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

@app.route("/ai", methods=['POST'])
def ai():
    data = request.get_json()
    reply = get_fast_reply(data.get('msg', ''))
    return jsonify(ans=reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
            $("#ms").scrollTop($("#ms")[0].scrollHeight);
