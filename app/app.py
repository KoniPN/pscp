from flask import Flask
import os

app = Flask(__name__)

# ข้อความที่จะแสดง - สามารถเปลี่ยนได้ผ่าน Jenkins CI
MESSAGE = os.getenv("HELLO_MESSAGE", "Hello from Jenkins CI/CD Pipeline!")

@app.route('/')
def hello():
    return f"""
    <html>
        <head>
            <title>Hello World Service</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    text-align: center;
                    padding: 40px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }}
                h1 {{ font-size: 3em; margin-bottom: 20px; }}
                p {{ font-size: 1.2em; opacity: 0.8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 {MESSAGE}</h1>
                <p>Deployed on Minikube with ArgoCD</p>
                <p>Pod: {os.getenv('HOSTNAME', 'unknown')}</p>
            </div>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

@app.route('/metrics')
def metrics():
    """Simple metrics endpoint for monitoring"""
    return "hello_world_requests_total 1\n", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
