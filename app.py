import threading, time, random, requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- 🟢 ضع البروكسيات هنا 🟢 ---
proxies_data = """
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
# ------------------------------

MY_PROXIES = [line.strip() for line in proxies_data.strip().split('\n') if line.strip()]
created_accounts = []
is_running = False

def factory_engine():
    global is_running, created_accounts
    created_accounts.insert(0, {"time": time.strftime("%H:%M:%S"), "user": "SYSTEM", "proxy": "LOCAL", "status": "STARTING FACTORY... 🚀"})
    while is_running:
        p = random.choice(MY_PROXIES).split(':') if MY_PROXIES else ["127.0.0.1", "8080"]
        user_fake = f"mo_{random.randint(100, 999)}_sec"
        new_log = {"time": time.strftime("%H:%M:%S"), "user": user_fake, "proxy": p[0], "status": "CONNECTING.. ⚙️"}
        created_accounts.insert(0, new_log)
        if len(created_accounts) > 10: created_accounts.pop()
        time.sleep(5)

@app.route('/')
def home():
    return render_template_string(HTML_UI, p_count=len(MY_PROXIES))

@app.route('/start_factory')
def start():
    global is_running
    if not is_running:
        is_running = True
        threading.Thread(target=factory_engine, daemon=True).start()
    return jsonify({"status": "success"})

@app.route('/update_logs')
def update_logs():
    return jsonify(created_accounts)

HTML_UI = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>MOHAMED SECURITY FACTORY</title>
    
    <link rel="icon" href="https://i.ibb.co/m5YfM5y/image.png" type="image/png">
    <link rel="shortcut icon" href="https://i.ibb.co/m5YfM5y/image.png" type="image/png">

    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; margin: 0; padding: 20px; }
        .box { border: 2px solid #00ff00; max-width: 850px; margin: auto; padding: 30px; box-shadow: 0 0 25px #00ff00; border-radius: 15px; background: rgba(0,10,0,0.8); }
        .btn { background: #00ff00; color: #000; padding: 15px 45px; border: none; font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 20px; box-shadow: 0 0 15px #00ff00; transition: 0.3s; }
        .btn:hover { background: #fff; box-shadow: 0 0 25px #fff; }
        table { width: 100%; margin-top: 30px; border-collapse: collapse; }
        th { color: #fff; border-bottom: 2px solid #00ff00; padding: 10px; }
        td { padding: 12px; border-bottom: 1px solid #003300; font-size: 14px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>MOHAMED SECURITY FACTORY</h1>
        <p style="font-size: 18px;">ACTIVE PROXIES: <span style="color: #fff;">{{ p_count }}</span> ✅</p>
        <hr style="border: 0; border-top: 1px solid #004400; margin: 20px 0;">
        <button class="btn" onclick="fetch('/start_factory')">RUN PRODUCTION 🚀</button>
        <table>
            <thead><tr><th>TIME</th><th>ACCOUNT</th><th>PROXY IP</th><th>STATUS</th></tr></thead>
            <tbody id="log-table"></tbody>
        </table>
    </div>
    <script>
        setInterval(() => {
            fetch('/update_logs').then(r => r.json()).then(data => {
                let rows = '';
                data.forEach(d => { rows += <tr><td>${d.time}</td><td>${d.user}</td><td>${d.proxy}</td><td>${d.status}</td></tr>; });
                document.getElementById('log-table').innerHTML = rows;
            });
        }, 2000);
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
