from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)

def test_simulate_mongodb_down():
    payload = {"scenario": "mongodb_down", "namespace": "three-tier"}
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["alert_name"] == "MongoDbDown"
    assert data["severity"] == "CRITICAL"
    assert data["remediation_type"] == "RESTART_POD"
    assert data["confidence_score"] > 0.8

def test_simulate_pod_oom_killed():
    payload = {"scenario": "pod_oom_killed", "namespace": "three-tier", "target_service": "api-worker-test"}
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["alert_name"] == "PodOOMKilled"
    assert "137" in data["root_cause"] or "OOMKilled" in data["root_cause"]
    assert data["remediation_type"] == "RESTART_POD"

def test_simulate_high_memory_pressure():
    payload = {"scenario": "high_memory_pressure", "namespace": "three-tier"}
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["alert_name"] == "NodeMemoryHighUtilization"
    assert data["remediation_type"] == "SCALE_DEPLOYMENT"

def test_alertmanager_webhook_ingest():
    webhook_payload = {
        "receiver": "ai-incident-engine",
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {
                    "alertname": "PodCrashLooping",
                    "severity": "critical",
                    "namespace": "three-tier",
                    "pod": "api-service-test-1"
                },
                "annotations": {
                    "summary": "Container restarting in CrashLoopBackOff",
                    "description": "Process exited with code 1."
                }
            }
        ]
    }
    response = client.post("/webhook", json=webhook_payload)
    assert response.status_code == 202
    assert response.json()["alerts_count"] == 1

def test_incidents_list():
    response = client.get("/incidents")
    assert response.status_code == 200
    incidents = response.json()
    assert isinstance(incidents, list)
    assert len(incidents) >= 1
