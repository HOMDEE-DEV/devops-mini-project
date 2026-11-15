import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)

# ดึงค่า Config จาก Environment Variables (ตามหลัก 12-Factor App)
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# เชื่อมต่อกับ Redis Database
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, socket_connect_timeout=2)
except Exception:
    r = None

@app.route("/")
def hello():
    visits = "N/A"
    redis_status = "Disconnected"
    
    if r:
        try:
            visits = r.incr("page_views")
            redis_status = "Connected"
        except redis.exceptions.ConnectionError:
            redis_status = "Connection Failed"

    return jsonify({
        "message": "Hello from DevOps Pipeline! Version 1.1 by Oran is LIVE!",
        "status": "success",
        "redis_status": redis_status,
        "page_views": visits
    })

# Endpoint สำหรับ Health Check (ตรวจสอบสถานะแอป และ Database)
@app.route("/health")
def health_check():
    redis_alive = False
    if r:
        try:
            redis_alive = r.ping()
        except Exception:
            redis_alive = False

    return jsonify({
        "status": "healthy",
        "service": "devops-mini-project",
        "dependencies": {
            "redis": "healthy" if redis_alive else "unhealthy"
        }
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
