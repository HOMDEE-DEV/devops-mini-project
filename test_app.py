import pytest
from app import app

@pytest.fixture
def client():
    # จำลอง client สำหรับยิงทดสอบ Flask app โดยไม่ต้องรัน server จริง
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_root_endpoint(client):
    """ทดสอบหน้าแรก / ต้องได้ HTTP 200 และข้อความถูกต้อง"""
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert "Hello from DevOps Pipeline" in json_data["message"]

def test_health_check(client):
    """ทดสอบหน้า /health ต้องได้ HTTP 200 และสถานะ healthy"""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert json_data["service"] == "devops-mini-project"
