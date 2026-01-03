from flask import Flask, render_template_string, jsonify
import threading
import time
import random

app = Flask(__name__)

# --- إعدادات النظام COMMAND CENTER ---
PASSWORD_ACCESS = "hx5"
ADMIN_NAME = "Mohamed Security"
USER_TAG = "kail.911"

# متغيرات للتحكم في عملية الفحص داخل السيرفر
is_running = False
results_list = [] # مخزن النتائج داخل السيرفر

# دالة الفحص (المحرك الداخلي)
def hacking_engine():
    global is_running, results_list
    targets = ["admin", "user", "root", "manager", "support"]
    
    while is_running:
        # هنا يتم وضع كود الفحص الحقيقي (تخمين، فحص متاح، إلخ)
        current_target = random.choice(targets) + str(random.randint(10, 99))
        status = random.choice(["SUCCESS ✅", "FAILED ❌", "RETRYING ⏳"])
        
        # إضافة النتيجة للمخزن
        new_entry = {
            "id": len(results_list) + 1,
            "target": current_target,
            "status": status,
            "time": time.strftime("%H:%M:%S")
        }
        results_list.insert(0, new_entry) # إضافة النتيجة في البداية
        
        # التحكم في سرعة الفحص (مثلاً فحص كل ثانيتين)
        time.sleep(2)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>{{ admin_name }} | Mainframe</title>
    <style>
        :root { --main-color: #00ff41; }
        body { background: #000; color: var(--main-color); font-family: monospace; margin: 0; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; }
        canvas { position: absolute; top: 0; left: 0; z-index: -1; }
        .container { background: rgba(0, 15, 0, 0.9); border: 1px solid var(--main-color); padding: 30px; border-radius: 10px; box-shadow: 0 0 20px var(--main-color); width: 90%; max-width: 700px; z-index: 10; text-align: center; }
        input { background: transparent; border: 1px solid var(--main-color); color: #fff; padding: 10px; width: 200px; text-align: center; margin-bottom: 20px; }
        button { background: var(--main-color); color: #000; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; margin: 5px; }
        .hidden { display: none; }
        .log-container { max-height: 300px; overflow-y: auto; border: 1px solid #004400; margin-top: 20px; background: #000500; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #004400; padding: 8px; font-size: 0.9em; }
        .success { color: #fff; font-weight: bold; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>

    <div id="login-screen" class="container">
        <h1>{{ admin_name }}</h1>
        <div style="color:#fff; margin-bottom:10px;">@{{ user_tag }}</div>
        <input type="password" id="passInput" placeholder="ACCESS KEY">
        <br>
        <button onclick="checkPass()">BOOT SYSTEM</button>
    </div>

    <div id="main-dashboard" class="container hidden">
        <h1 style="text-shadow: 0 0 10px var(--main-color);">SYSTEM ACTIVE</h1>
        <p>OPERATOR: {{ admin_name }}</p>
        
        <button onclick="startAction()" style="background: #28a745; color: #fff;">⚡ START ENGINE</button>
        <button onclick="stopAction()" style="background: #dc3545; color: #fff;">🛑 KILL ALL</button>

        <div class="log-container">
            <table>
                <thead>
                    <tr>
                        <th>TIME</th>
                        <th>TARGET</th>
                        <th>STATUS</th>
                    </tr>
                </thead>
                <tbody id="logs"></tbody>
            </table>
        </div>
    </div>

    <script>
        // Matrix Effect
        const c = document.querySelector('canvas');
        const ctx = c.getContext('2d');
        c.width = window.innerWidth; c.height = window.innerHeight;
        const letters = "01"; const fontSize = 16; const columns = c.width/fontSize;
        const drops = Array(Math.floor(columns)).fill(1);
        function draw() {
            ctx.fillStyle = "rgba(0,0,0,0.05)"; ctx.fillRect(0,0,c.width,c.height);
            ctx.fillStyle = "#0f0"; ctx.
            font = fontSize + "px arial";
            drops.forEach((y, i) => {
                ctx.fillText(letters[Math.floor(Math.random()*letters.length)], i*fontSize, y*fontSize);
                if(y*fontSize > c.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 33);

        function checkPass() {
            if(document.getElementById('passInput').value === "{{ password }}") {
                document.getElementById('login-screen').classList.add('hidden');
                document.getElementById('main-dashboard').classList.remove('hidden');
                setInterval(refreshLogs, 2000); // تحديث الجدول كل ثانيتين تلقائياً
            }
        }

        function startAction() { fetch('/api/start'); }
        function stopAction() { fetch('/api/stop').then(() => location.reload()); }

        function refreshLogs() {
            fetch('/api/logs').then(res => res.json()).then(data => {
                let html = '';
                data.forEach(item => {
                    html += <tr><td>${item.time}</td><td>${item.target}</td><td class="success">${item.status}</td></tr>;
                });
                document.getElementById('logs').innerHTML = html;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, admin_name=ADMIN_NAME, user_tag=USER_TAG, password=PASSWORD_ACCESS)

@app.route('/api/start')
def start():
    global is_running
    if not is_running:
        is_running = True
        threading.Thread(target=hacking_engine, daemon=True).start()
    return jsonify(status="started")

@app.route('/api/stop')
def stop():
    global is_running, results_list
    is_running = False
    results_list = []
    return jsonify(status="stopped")

@app.route('/api/logs')
def get_logs():
    return jsonify(results_list[:20]) # عرض آخر 20 نتيجة فقط

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
