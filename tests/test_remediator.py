import time
from src.remediator import RemediationEngine
from src.models import RCAReport, RemediationActionType
from src.config import settings

def test_remediation_cooldown_and_safety():
    engine = RemediationEngine()
    rca = RCAReport(
        incident_id="inc-123",
        timestamp="2026-10-25T12:00:00Z",
        alert_name="PodOOMKilled",
        target_resource="api-pod-1",
        namespace="three-tier",
        severity="CRITICAL",
        root_cause="OOMKilled",
        impact_summary="Pod dead",
        confidence_score=0.95,
        recommended_action="Restart pod",
        remediation_type=RemediationActionType.RESTART_POD
    )

    # First execution should succeed
    success1, msg1 = engine.execute_remediation(rca)
    assert success1 is True
    assert "Triggered pod eviction" in msg1

    # Immediate second execution on same target should be blocked by cooldown
    success2, msg2 = engine.execute_remediation(rca)
    assert success2 is False
    assert "Safety Cooldown active" in msg2

def test_remediation_disabled_flag():
    engine = RemediationEngine()
    original_state = settings.auto_remediation_enabled
    try:
        settings.auto_remediation_enabled = False
        rca = RCAReport(
            incident_id="inc-456",
            timestamp="2026-10-25T12:00:00Z",
            alert_name="MongoDbDown",
            target_resource="mongo-pod-99",
            namespace="three-tier",
            severity="CRITICAL",
            root_cause="Mongo down",
            impact_summary="Service down",
            confidence_score=0.92,
            recommended_action="Restart pod",
            remediation_type=RemediationActionType.RESTART_POD
        )
        success, msg = engine.execute_remediation(rca)
        assert success is False
        assert "DISABLED" in msg
    finally:
        settings.auto_remediation_enabled = original_state
