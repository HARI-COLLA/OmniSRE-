import os
import pytest
from src.database import IncidentDatabase
from src.models import RCAReport, RemediationActionType

TEST_DB_PATH = "data/test_omnisre.db"

def test_database_persistence():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    db = IncidentDatabase(db_path=TEST_DB_PATH)

    rca = RCAReport(
        incident_id="inc-soc2-audit-001",
        timestamp="2026-10-25T14:00:00Z",
        alert_name="PodOOMKilled",
        target_resource="payment-worker-1",
        namespace="prod-payments",
        severity="CRITICAL",
        root_cause="V8 heap allocation breach (Exit code 137)",
        impact_summary="Service degraded",
        confidence_score=0.98,
        recommended_action="Restart pod",
        remediation_type=RemediationActionType.RESTART_POD,
        remediation_executed=True,
        remediation_result="Pod restarted successfully"
    )

    db.save_incident(rca)

    # Query from database
    results = db.get_recent_incidents(limit=10)
    assert len(results) == 1
    stored = results[0]
    assert stored.incident_id == "inc-soc2-audit-001"
    assert stored.severity == "CRITICAL"
    assert stored.remediation_executed is True
    assert stored.confidence_score == 0.98

    # Clean up test DB
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
