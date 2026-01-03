from flask import Flask, render_template_string, jsonify, request
import threading
import time

app = Flask(__name__)

# إعدادات النظام
PASSWORD_ACCESS = "hx5"
ADMIN_NAME = "Mohamed Security"

# بيانات وهمية لمحاكاة نتائج التخمين (ستتغير عند ربط بوتك الحقيقي)
guessing_results = []
active_units = 0

# واجهة المستخدم (HTML + CSS + JS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>{{ admin_name }} - Terminal</title>
    <style>
        body {
            background-color: black;
            color: #0f0;
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        canvas {
            position: absolute;
            top: 0;
            left: 0;
            z-index: -1;
        }
        .login-box, .dashboard {
            background: rgba(0, 20, 0, 0.9);
            border: 2px solid #0f0;
            padding: 20px;
            box-shadow: 0 0 20px #0f0;
            text-align: center;
            width: 80%;
            max-width: 600px;
            z-index: 10;
        }
        input {
            background: black;
            border: 1px solid #0f0;
            color: #0f0;
            padding: 10px;
            margin: 10px;
            text-align: center;
        }
        button {
            background: #0f0;
            color: black;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: bold;
            margin: 5px;
        }
        button:hover { background: #0c0; }
        .results-table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        .results-table th, .results-table td {
            border: 1px solid #0f0;
            padding: 8px;
            font-size: 12px;
        }
        .hidden { display: none; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>

    <div id="login-screen" class="login-box">
        <h2>{{ admin_name }}</h2>
        <p>ENTER ACCESS CODE</p>
        <input type="password" id="passInput" placeholder="Password...">
        <br>
        <button onclick="checkPass()">ACCESS</button>
    </div>

    <div id="main-dashboard" class="dashboard hidden">
        <h1 style="text-shadow: 0 0 10px #0f0;">{{ admin_name }} SYSTEM</h1>
        <div style="margin-bottom: 20px;">
            <button onclick="startUnit()" style="background: #28a745; color: white;">⚡ EXECUTE_START</button>
            <button onclick="stopAll()" style="background: #dc3545; color: white;">🛑 TERMINATE</button>
        </div>
        <div id="unit-count">ACTIVE UNITS: 0</div>
        
        <table class="results-table">
            <thead>
                <tr>
                    <th>Target</th>
                    <th>Result</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody id="results-body">
                </tbody>
        </table>
    </div>

    <script>
        // تأثير الماتريكس المتحرك
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        function drawMatrix() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#0f0";
            ctx.font = fontSize + "px arial";
            drops.forEach((y, i) => {
                const text = letters[Math.floor(Math.random() * letters.length)];
                ctx.fillText(text, i * fontSize, y * fontSize);
                if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;});
        }
        setInterval(drawMatrix, 50);

        // وظائف التحكم
        function checkPass() {
            const val = document.getElementById('passInput').value;
            if (val === "{{ password }}") {
                document.getElementById('login-screen').classList.add('hidden');
                document.getElementById('main-dashboard').classList.remove('hidden');
            } else {
                alert("ACCESS DENIED");
            }
        }

        function startUnit() {
            fetch('/api/start').then(res => res.json()).then(data => {
                document.getElementById('unit-count').innerText = "ACTIVE UNITS: " + data.units;
                updateTable(data.new_result);
            });
        }

        function stopAll() {
            fetch('/api/stop').then(res => res.json()).then(data => {
                document.getElementById('unit-count').innerText = "ACTIVE UNITS: 0";
                document.getElementById('results-body').innerHTML = "";
            });
        }

        function updateTable(res) {
            if(!res) return;
            const row = <tr><td>${res.target}</td><td>${res.pass}</td><td>✅ SUCCESS</td></tr>;
            document.getElementById('results-body').innerHTML += row;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, admin_name=ADMIN_NAME, password=PASSWORD_ACCESS)

@app.route('/api/start')
def api_start():
    global active_units
    active_units += 1
    # محاكاة لنتيجة تخمين
    new_res = {"target": f"User_{active_units}", "pass": f"Pass_***{active_units}"}
    return jsonify(units=active_units, new_result=new_res)

@app.route('/api/stop')
def api_stop():
    global active_units
    active_units = 0
    return jsonify(units=0)

if name == '__main__':
    app.run(host='0.0.0.0', port=10000)
