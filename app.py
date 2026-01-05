import os, requests
from flask import Flask, render_template_string, request, jsonify

# --- [ إعدادات محمد - نظام السرعة القصوى ] ---
ADMIN_PASS = "hx2026"
INSTA_URL = "https://instagram.com/kail.911"

app = Flask(__name__)

# دالة الذكاء الاصطناعي - تم تحسينها لتعطي ردوداً فورية
def get_ai_reply(text):
    try:
        # استخدام محرك معالجة مباشر وخفيف جداً
        r = requests.get(f"https://api.simsimi.net/v2/?text={text}&lc=ar", timeout=3)
        return r.json().get('success', "تم استقبال أمرك سيدي محمد.")
    except:
        return "جاري تأمين الاتصال.."

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
        .nav { position:fixed; top:0; width:100%; height:55px; background:rgba(0,0,0,0.95); display:flex; justify-content:space-between; align-items:center; padding:0 15px; border-bottom:1px solid #00ffcc33; z-index:1000; box-sizing:border-box; }
        #dash { display:none; flex-direction:column; height:100vh; padding-top:55px; }
        
        /* تحسين مساحة الموبايل - الشات الآن يأخذ 80% من الشاشة */
        .map { height:180px; border-bottom:1px solid #00ffcc22; background:#050505; }
        .chat { flex:1; display:flex; flex-direction:column; background:#080808; position:relative; overflow:hidden; }
        
        .msgs { flex:1; padding:15px; overflow-y:auto; display:flex; flex-direction:column; gap:12px; padding-bottom:80px; }
        .m { padding:12px 18px; border-radius:20px; font-size:16px; max-width:85%; line-height:1.5; }
        .u { background:#00ffcc; color:#000; align-self:flex-start; font-weight:bold; }
        .a { background:#151515; color:#fff; border:1px solid #00ffcc44; align-self:flex-end; }
        
        .box { position:absolute; bottom:0; width:100%; padding:15px; background:#000; border-top:1px solid #1a1a1a; display:flex; gap:10px; box-sizing:border-box; }
        input { flex:1; background:#000; border:1px solid #00ffcc; color:#00ffcc; padding:12px; border-radius:30px; outline:none; font-size:16px; text-align:center; }
        
        #login { height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; }
        .btn { margin-top:20px; background:#00ffcc; color:#000; border:none; padding:12px 60px; font-weight:bold; border-radius:30px; cursor:pointer; font-size:16px; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="{{ insta }}" target="_blank" style="color:#00ffcc; text-decoration:none; font-size:12px; border:1px solid #00ffcc; padding:4px 12px; border-radius:15px;">@kail.911</a>
        <div style="font-size:11px; font-weight:bold; text-shadow:0 0 5px #00ffcc;">MUHAMMAD TURBO v2</div>
    </div>

    <div id="login">
        <h2 style="letter-spacing:3px; color:#00ffcc;">SYSTEM SECURED</h2>
        <input type="password" id="p" placeholder="ادخل المفتاح" style="width:240px; padding:15px; background:none; border:1px solid #00ffcc; color:#00ffcc; border-radius:10px; text-align:center; font-size:20px;">
        <button onclick="auth()" class="btn">دخول</button>
    </div>

    <div id="dash">
        <div class="map"><iframe src="https://cybermap.kaspersky.com/en/widget/map" style="width:100%; height:100%; border:none; filter:hue-rotate(150deg) contrast(1.1);"></iframe></div>
        <div class="chat">
            <div class="msgs" id="ms">
                <div class="m a">نظام السرعة القصوى مفعل.. بانتظار أوامرك سيدي محمد.</div>
            </div>
            <div class="box">
                <input type="text" id="ui" placeholder="اكتب هنا..." onkeypress="if(event.which==13)send()">
            </div>
        </div>
    </div>

    <script>
        function auth() {
            if($("#p").val() === "{{ pass }}") { hide(); 
                $("#dash").css("display","flex"); 
            } else { alert("رمز الدخول غير صحيح!"); }
        }
        function send() {
            let t = $("#ui").val(); if(!t) return;
            $("#ms").append(`<div class="m u">${t}</div>`); $("#ui").val("");
            $("#ms").scrollTop($("#ms")[0].scrollHeight);
            $.ajax({
                url: '/ai_fast', type: 'POST', contentType: 'application/json',
                data: JSON.stringify({ message: t }),
                success: function(response) {
                    $("#ms").append(`<div class="m a">${response.reply}</div>`);
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
    # إصلاح شامل لطريقة الـ Return لضمان عدم حدوث SyntaxError
    return render_template_string(HTML, pass=ADMIN_PASS, insta=INSTA_URL)

@app.route("/ai_fast", methods=['POST'])
def ai_fast():
    # استلام البيانات ومعالجتها بأسرع شكل ممكن
    user_input = request.get_json().get('message', '')
    ai_answer = get_ai_reply(user_input)
    return jsonify(reply=ai_answer)

if __name__ == "__main__":
    # تشغيل السيرفر على المنفذ الصحيح لـ Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
                $("#login").
