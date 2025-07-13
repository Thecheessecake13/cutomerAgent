from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_roundtrip_complaint():
    payload = {"user_id": "u1", "subject": "Test", "description": "Desc"}
    post = client.post("/api/complaints", json=payload)
    assert post.status_code == 200
    data = post.json()
    assert data["user_id"] == "u1"
    cid = data["id"]
    get = client.get(f"/api/complaints/{cid}")
    assert get.status_code == 200
    assert get.json()["id"] == cid