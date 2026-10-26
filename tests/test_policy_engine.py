import pytest
from src.policy_engine import PolicyEngine
from src.remediator import RemediationEngine
from src.models import RCAReport, RemediationActionType
from src.server import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_policy_wildcard_matching():
    engine = PolicyEngine()
    policy = engine.find_matching_policy("PodOOMKilled", "prod-payments", exit_code=137)
    assert policy is not None
    assert policy.action == "RESTART_POD"
    assert policy.cooldown_seconds == 300

def test_kube_system_namespace_protection():
    engine = PolicyEngine()
    # Any alert targeting kube-system should be blocked by guardrails
    policy = engine.find_matching_policy("PodOOMKilled", "kube-system", exit_code=137)
    assert policy is None

def test_human_in_the_loop_approval_flow():
    rem_engine = RemediationEngine()
    rca = RCAReport(
        incident_id="test-approval-99",
        timestamp="2026-10-25T12:00:00Z",
        alert_name="PodCrashLooping",
        target_resource="critical-service-pod",
        namespace="production",
        severity="CRITICAL",
        root_cause="Bad build deployed",
        impact_summary="Service degraded",
        confidence_score=0.96,
        recommended_action="Rollback deployment",
        remediation_type=RemediationActionType.ROLLBACK_DEPLOYMENT
    )

    # If policy requires approval, it should pause and create a pending token
    # We can test approve_remediation directly
    token = "approval-test-01"
    rem_engine.pending_approvals[token] = rca

    # Approve via engine
    success, msg = rem_engine.approve_remediation(token)
    assert success is True
    assert "Triggered deployment rollout restart" in msg

def test_human_in_the_loop_deny_flow():
    rem_engine = RemediationEngine()
    rca = RCAReport(
        incident_id="test-deny-01",
        timestamp="2026-10-25T12:00:00Z",
        alert_name="PodCrashLooping",
        target_resource="critical-service-pod",
        namespace="production",
        severity="CRITICAL",
        root_cause="Faulty configuration",
        impact_summary="Service degraded",
        confidence_score=0.96,
        recommended_action="Rollback deployment",
        remediation_type=RemediationActionType.ROLLBACK_DEPLOYMENT
    )

    token = "approval-deny-test-01"
    rem_engine.pending_approvals[token] = rca

    # Deny via engine
    success, msg = rem_engine.deny_remediation(token, reason="Blocked for manual audit")
    assert success is True
    assert "rejected by operator" in msg
    assert token not in rem_engine.pending_approvals

def test_list_policies_endpoint():
    response = client.get("/policies")
    assert response.status_code == 200
    policies = response.json()
    assert isinstance(policies, list)
    assert len(policies) >= 3
    names = [p["name"] for p in policies]
    assert "auto-recover-oom" in names or "default-oom-policy" in names
