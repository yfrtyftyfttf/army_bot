import telebot, requests, os, random, time, threading
from flask import Flask, render_template_string, jsonify
from datetime import datetime

# --- [ إعدادات البوت والقناة ] ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
MY_ID = "6190753066"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- [ البروكسيات الـ 50 الخاصة بك ] ---
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

# --- [ النظام ] ---
stats = {"checked": 0, "found": 0, "errors": 0, "logs": []}
found_accounts = [] 
already_checked = set() 
hunting_active = False

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
        .main-container { position: relative; width: 950px; height: 650px; border: 2px solid #00f2ff; border-radius: 15px; box-shadow: 0 0 25px #00f2ff55; display: block; background: #000; }
        #matrix { position: absolute; inset: 0; z-index: 1; opacity: 0.2; }
        .ui-element { position: relative; z-index: 3; }
        .stats-row { position: absolute; top: 100px; width: 100%; display: flex; justify-content: center; gap: 20px; }
        .stat-box { background: rgba(0, 15, 30, 0.9); border: 1px solid #00f2ff; padding: 20px; border-radius: 10px; width: 160px; text-align: center; }
        .stat-box b { font-size: 35px; display: block; }
        .controls { position: absolute; bottom: 250px; width: 100%; display: flex; justify-content: center; gap: 15px; }
        .btn { background: rgba(0,242,255,0.1); border: 1px solid #00f2ff; color: #00f2ff; padding: 12px 35px; cursor: pointer; border-radius: 5px; font-weight: bold; }
        .btn:hover { background: #00f2ff; color: #000; box-shadow: 0 0 15px #00f2ff; }
        .log-screen { position: absolute; bottom: 30px; left: 5%; width: 90%; height: 180px; background: rgba(0,0,0,0.9); border: 1px solid #00f2ff; padding: 10px; overflow-y: auto; font-size: 13px; color: #00ffaa; text-align: left; }
        #hits-panel { display: none; position: absolute; inset: 20px; background: #000; border: 2px solid #0f0; z-index: 100; border-radius: 15px; padding: 20px; }
        .hit-row { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px dashed #0f03; color: #0f0; }
    </style>
</head>
<body>
<div class="main-container">
    <canvas id="matrix"></canvas>
    <div class="stats-row ui-element">
        <div class="stat-box">CHECKED<b id="c">0</b></div>
        <div class="stat-box" style="border-color:#0f0;">FOUND<b id="f" style="color:#0f0;">0</b></div>
        <div class="stat-box" style="border-color:red;">ERRORS<b id="e" style="color:red;">0</b></div>
    </div>
    <div class="controls ui-element">
        <button class="btn" onclick="action('start')">START</button>
        <button class="btn" onclick="action('stop')" style="color:red; border-color:red;">STOP</button>
        <button class="btn" onclick="showHits()" style="color:#0f0; border-color:#0f0;">HITS</button>
    </div>
    <div class="log-screen ui-element" id="logs"></div>
    <div id="hits-panel">
        <div style="display:flex; justify-content:space-between; border-bottom:1px solid #0f0;">
            <h2 style="color:#0f0;">CAPTURED</h2>
            <button class="btn" onclick="closeHits()" style="color:red;">CLOSE</button>
        </div>
        <div id="hits-body" style="height:450px; overflow-y:auto; margin-top:10px;"></div>
    </div>
</div>
<script>
    function action(c) { $.getJSON("/cmd/"+c); }
    function showHits() {
        $.getJSON("/api/hits", (data) => {
            let h = data.map(x => `<div class="hit-row"><span>@${x.user}</span><span>${x.time}</span></div>`).join('');
            $("#hits-body").html(h || "No Hits Yet"); $("#hits-panel").fadeIn();
        });
    }
    function closeHits() { $("#hits-panel").fadeOut(); }
    setInterval(() => {
        $.getJSON("/api/stats", (d) => {
            $("#c").text(d.checked); $("#f").text(d.found); $("#e").text(d.errors);
            $("#logs").html(d.logs.map(m => `<div>> ${m}</div>`).join('')).scrollTop(9999);
        });
    }, 1000);
</script>
</body>
</html>
"""

@app.route("/")
def index(): return render_template_string(HTML_TEMPLATE)

@app.route("/api/stats")
def stats_api(): return jsonify(stats)

@app.route("/api/hits")
def hits_api(): return jsonify(found_accounts)

@app.route("/cmd/<c>")
def cmd(c):
    global hunting_active
    if c == "start" and not hunting_active:
        hunting_active = True
        for _ in range(5): threading.Thread(target=hunt, daemon=True).start()
    elif c == "stop": hunting_active = False
    return jsonify(ok=True)

def hunt():
    while hunting_active:
        user = "".join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890._") for _ in range(5))
        if user in already_checked: continue
        already_checked.add(user)
        
        px = {}
        if PROXIES_LIST:
            p = random.choice(PROXIES_LIST).split(':')
            if len(p) == 4:
                formatted = f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"
                px = {"http": formatted, "https": formatted}

        try:
            res = requests.get(f"https://www.instagram.com/{user}/", timeout=10, proxies=px)
            stats["checked"] += 1
            if res.status_code == 404:
                stats["found"] += 1
                now = datetime.now().strftime("%H:%M:%S")
                found_accounts.append({"user": user, "time": now})
                bot.send_message(MY_ID, f"🔥 [HIT] @{user}")
                stats["logs"].append(f"SUCCESS: @{user}")
            else:
                stats["logs"].append(f"Checked: @{user}")
        except:
            stats["errors"] += 1
            stats["logs"].append("Proxy Error...")
        
        if len(stats["logs"]) > 10: stats["logs"].pop(0)
        time.sleep(0.3)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
