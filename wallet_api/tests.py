from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_get_wallet():
    response = client.get("/api/v1/wallets/test_wallet")
    assert response.status_code == 404

def test_deposit():
    response = client.post("/api/v1/wallets/test_wallet/operation", json={"operation_type": "DEPOSIT", "amount": 100})
    assert response.status_code == 200

