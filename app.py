import threading, time, random, requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- 🟢 ضع البروكسيات هنا 🟢 ---
# قم بلصق الـ 50 سطر التي نسختها من الملف بين العلامات الثلاث أدناه
proxies_data = """
 (82.24.249.101:5938:njhuvsdz:wp92l0dkdkoc 
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

# تحويل النص إلى قائمة برمجية
MY_PROXIES = [line.strip() for line in proxies_data.strip().split('\n') if line.strip()]

created_accounts = []
is_running = False

def get_proxy():
    if not MY_PROXIES: return None
    p = random.choice(MY_PROXIES).split(':')
    # الترتيب المتوقع: IP:PORT:USER:PASS
    return {
        "http": f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}",
        "https": f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"
    }

def factory_engine():
    global is_running, created_accounts
    while is_running:
        proxy_dict = get_proxy()
        user_fake = f"mo_{random.randint(100, 999)}_sec"
        
        try:
            # محاكاة عملية الفحص والإنشاء
            time.sleep(8) 
            
            new_log = {
                "time": time.strftime("%H:%M:%S"),
                "user": user_fake,
                "proxy": proxy_dict['http'].split('@')[1] if proxy_dict else "NO PROXY",
                "status": "RUNNING.. ⚙️"
            }
            created_accounts.insert(0, new_log)
            if len(created_accounts) > 12: created_accounts.pop()
        except:
            pass

@app.route('/')
def home():
    return render_template_string(HTML_UI, p_count=len(MY_PROXIES))

@app.route('/start_factory')
def start():
    global is_running
    if not is_running:
        is_running = True
        threading.Thread(target=factory_engine, daemon=True).start()
    return "OK"

@app.route('/update_logs')
def update_logs():
    return jsonify(created_accounts)

HTML_UI = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>MOHAMED SECURITY | FACTORY</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; }
        .box { border: 2px solid #00ff00; width: 85%; margin: 40px auto; padding: 20px; box-shadow: 0 0 15px #00ff00; border-radius: 15px; }
        .btn { background: #00ff00; color: #000; padding: 15px 40px; border: none; font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 18px; }
        .btn:hover { background: #fff; }
        table { width: 100%; margin-top: 30px; border-collapse: collapse; }
        th { border-bottom: 2px solid #00ff00; padding: 10px; }
        td { padding: 12px; border-bottom: 1px solid #003300; font-size: 14px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>MOHAMED SECURITY FACTORY</h1>
        <p>ACTIVE PROXIES: {{ p_count }} ✅</p>
        <hr style="border: 0.5px solid #003300;">
        <br>
        <button class="btn" onclick="fetch('/start_factory')">RUN PRODUCTION 🚀</button>
        <table>
            <thead>
                <tr><th>TIME</th><th>ACCOUNT</th><th>PROXY IP</th><th>STATUS</th></tr>
            </thead>
            <tbody id="log-table"></tbody>
        </table>
    </div>
    <script>
        setInterval(() => {
            fetch('/update_logs').then(r => r.json()).then(data => {
                let rows = '';
                data.forEach(d => {
                    rows += <tr><td>${d.time}</td><td>${d.user}</td><td>${d.proxy}</td><td>${d.status}</td></tr>;
                });
                document.getElementById('log-table').innerHTML = rows;
            });
        }, 2500);
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
