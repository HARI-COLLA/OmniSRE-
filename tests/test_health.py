from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"
    assert "ai_provider" in data

def test_dashboard_ui_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "OmniSRE Platform" in response.text
    assert "Autonomous SRE" in response.text
