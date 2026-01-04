import telebot, requests, os, random, time, threading
from flask import Flask, render_template_string, jsonify
from datetime import datetime

# --- [ الإعدادات الأساسية ] ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- [ قسم البروكسيات ] ---
RAW_PROXIES = """
82.24.249.101:5938:njhuvsdz:wp92l0dkdkoc 
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
82.23.204.254:7086:njhuvsdz:wp92l0dkdkoc
"""
PROXIES_LIST = [p.strip() for p in RAW_PROXIES.strip().split('\n') if p.strip()]

# --- [ تخزين البيانات ] ---
stats = {"checked": 0, "found": 0, "errors": 0, "logs": []}
found_accounts = [] 
hunting_active = False

# --- [ واجهة النظام - HTML_TEMPLATE ] ---
# (لقد تركت كود الـ HTML كما هو لأنه سليم برمجياً)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>KAIL.911 OPERATOR</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { margin: 0; background: #000; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: 'Courier New', monospace; overflow: hidden; color: #00f2ff; }
        .main-container { position: relative; width: 950px; height: 650px; border: 2px solid #00f2ff; border-radius: 15px; box-shadow: 0 0 25px #00f2ff55; display: none; background: #000; overflow: hidden; }
        #matrix { position: absolute; inset: 0; z-index: 1; opacity: 0.3; }
        .ui-element { position: relative; z-index: 3; }
        .header-panel { position: absolute; top: 20px; width: 100%; display: flex; justify-content: space-around; align-items: center; }
        .insta-link { color: #fff; text-decoration: none; background: rgba(225,48,108,0.2); border: 1px solid #e1306c; padding: 8px 15px; border-radius: 20px; font-size: 14px; box-shadow: 0 0 10px #e1306c; }
        .stats-row { position: absolute; top: 120px; width: 100%; display: flex; justify-content: center; gap: 25px; }
        .stat-box { background: rgba(0, 20, 40, 0.8); border: 1px solid #00f2ff; padding: 15px; border-radius: 10px; width: 150px; text-align: center; }
        .stat-box b { font-size: 32px; display: block; margin-top: 5px; }
        .controls { position: absolute; bottom: 260px; width: 100%; display: flex; justify-content: center; gap: 15px; }
        .btn { background: rgba(0,242,255,0.1); border: 1px solid #00f2ff; color: #00f2ff; padding: 12px 30px; cursor: pointer; border-radius: 5px; font-weight: bold; transition: 0.3s; text-transform: uppercase; }
        .btn:hover { background: #00f2ff; color: #000; box-shadow: 0 0 20px #00f2ff; }
        .log-screen { position: absolute; bottom: 30px; left: 5%; width: 90%; height: 200px; background: rgba(0,10,20,0.9); border: 1px solid #00f2ff; padding: 10px; overflow-y: auto; font-size: 13px; color: #00ffaa; text-align: left; direction: ltr; }
        #hits-panel { display: none; position: absolute; inset: 30px; background: #000; border: 2px solid #0f0; z-index: 100; border-radius: 15px; padding: 20px; box-shadow: 0 0 40px #0f05; }
        .hits-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #0f0; padding-bottom: 10px; }
        .hits-list { margin-top: 15px; height: 450px; overflow-y: auto; }
        .hit-row { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px dashed #0f03; color: #0f0; }
        .gate { position: fixed; inset: 0; background: #000; z-index: 999; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .gate input { background: transparent; border: 1px solid #00f2ff; color: #00f2ff; padding: 15px; font-size: 20px; text-align: center; border-radius: 8px; outline: none; }
    </style>
</head>
<body>
<div class="gate" id="gate">
    <h2 style="letter-spacing: 8px;">SYSTEM ENCRYPTION</h2>
    <input type="password" id="pass" placeholder="ENTER ACCESS KEY">
    <br>
    <button class="btn" onclick="login()">AUTHORIZE</button>
</div>
<div class="main-container" id="mainApp">
    <canvas id="matrix"></canvas>
    <div class="header-panel ui-element">
        <div style="font-weight: bold;">STATUS: <span id="status-text" style="color:red;">OFFLINE</span></div>
        <a href="https://www.instagram.com/kail.911" target="_blank" class="insta-link"><i class="fab fa-instagram"></i> kail.911</a>
    </div>
    <div class="stats-row ui-element">
        <div class="stat-box">CHECKED<b id="c">0</b></div>
        <div class="stat-box" style="border-color:#0f0;">FOUND<b id="f" style="color:#0f0;">0</b></div>
        <div class="stat-box" style="border-color:red;">ERRORS<b id="e" style="color:red;">0</b></div>
    </div>
    <div class="controls ui-element">
        <button class="btn" onclick="action('start')"><i class="fas fa-bolt"></i> START</button>
        <button class="btn" onclick="action('stop')" style="color:red; border-color:red;"><i class="fas fa-power-off"></i> STOP</button>
        <button class="btn" onclick="showHits()" style="color:#0f0; border-color:#0f0;"><i class="fas fa-crosshairs"></i> HITS</button>
    </div>
    <div class="log-screen ui-element" id="logs"></div>
    <div id="hits-panel">
        <div class="hits-header">
            <h2 style="margin:0; color:#0f0;">SUCCESSFUL CAPTURES</h2>
            <button class="btn" onclick="closeHits()" style="color:red; border-color:red;">CLOSE</button>
        </div>
        <div class="hits-list" id="hits-body"></div>
    </div>
</div>
<script>
    const canvas = document.getElementById("matrix");
    const ctx = canvas.getContext("2d");
    canvas.width = 950; canvas.height = 650;
    const columns = Array(Math.floor(canvas.width/15)).fill(0);
    function drawMatrix() {
        ctx.fillStyle = "rgba(0,0,0,0.05)"; ctx.fillRect(0,0,canvas.width,canvas.height);
        ctx.fillStyle = "#00f2ff"; ctx.font = "15px monospace";
        columns.forEach((y, i) => {
            ctx.fillText(String.fromCharCode(0x30A0 + Math.random()*96), i*15, y);
            columns[i] = y > canvas.height || y > Math.random()*10000 ? 0 : y + 15;
        });
    }
    setInterval(drawMatrix, 50);
    function login() { if(document.getElementById("pass").value === "hx888") { $("#gate").hide(); $("#mainApp").show(); } else { alert("ACCESS DENIED"); } }
    function action(c) { 
        $.getJSON("/cmd/"+c); 
        $("#status-text").text(c === 'start' ? 'RUNNING' : 'OFFLINE').css('color', c === 'start' ? '#0f0' : 'red');
    }
    function showHits() {
        $.getJSON("/api/hits", (data) => {
            let h = data.length ? "" : "<div style='text-align:center; padding:50px;'>No targets captured yet.</div>";
            data.forEach(x => h += `<div class="hit-row"><span>@${x.user}</span><span>${x.time}</span></div>`);
            $("#hits-body").html(h);
            $("#hits-panel").fadeIn();
        });
    }
    function closeHits() { $("#hits-panel").fadeOut(); }
    setInterval(() => {
        $.getJSON("/api/stats", (d) => {
            $("#c").text(d.checked); $("#f").text(d.found); $("#e").text(d.errors);
            let l = ""; d.logs.forEach(msg => l += `<div>> ${msg}</div>`);
            $("#logs").html(l).scrollTop(9999);
        });
    }, 1000);
</script>
</body>
</html>
"""

@app.route("/")
def index(): 
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/stats")
def stats_api(): 
    return jsonify(stats)

@app.route("/api/hits")
def hits_api(): 
    return jsonify(found_accounts)

@app.route("/cmd/<c>")
def cmd(c):
    global hunting_active
    if c == "start" and not hunting_active:
        hunting_active = True
        threading.Thread(target=hunt, daemon=True).start()
    elif c == "stop": 
        hunting_active = False
    return jsonify(ok=True)

def hunt():
    global hunting_active
    while hunting_active:
        # توليد اسم مستخدم عشوائي
        user = "".join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890._") for _ in range(4))
        url = f"https://www.instagram.com/{user}/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        px = {}
        if PROXIES_LIST:
            p = random.choice(PROXIES_LIST)
            if not p.startswith('http'): 
                p = 'http://' + p
            px = {"http": p, "https": p}
        
        try:
            res = requests.get(url, headers=headers, proxies=px, timeout=5)
            stats["checked"] += 1
            if res.status_code == 404:
                stats["found"] += 1
                now = datetime.now().strftime("%H:%M:%S")
                found_accounts.append({"user": user, "time": now})
                try:
                    bot.send_message("-1002361139454", f"🔥 [HIT] Available: @{user}")
                except:
                    pass
                stats["logs"].append(f"SUCCESS: @{user} is available!")
            else:
                stats["logs"].append(f"Checked: @{user} (Taken)")
        except:
            stats["errors"] += 1
            stats["logs"].append("Proxy link failed. Rotating...")
        
        if len(stats["logs"]) > 15: 
            stats["logs"].pop(0)
        time.sleep(0.7)

if __name__ == "__main__":
    # تم تصحيح name لتصبح __name__
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
