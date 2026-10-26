import pytest
from src.ai_engine import ai_engine
from src.models import IncidentContext, AlertItem, PodContext, TelemetryContext, RemediationActionType

@pytest.mark.asyncio
async def test_oom_killed_analysis():
    alert = AlertItem(
        status="firing",
        labels={"alertname": "PodOOMKilled", "pod": "api-pod", "namespace": "three-tier"}
    )
    pod_ctx = PodContext(
        pod_name="api-pod",
        namespace="three-tier",
        phase="Failed",
        exit_code=137,
        exit_reason="OOMKilled",
        recent_logs="Allocation failed - JavaScript heap out of memory"
    )
    ctx = IncidentContext(alert=alert, pod_context=pod_ctx)
    rca = await ai_engine.analyze_incident(ctx)

    assert rca.severity == "CRITICAL"
    assert "137" in rca.root_cause or "OOMKilled" in rca.root_cause or "Out-Of-Memory" in rca.root_cause
    assert rca.remediation_type == RemediationActionType.RESTART_POD
    assert rca.confidence_score >= 0.9

@pytest.mark.asyncio
async def test_mongodb_down_analysis():
    alert = AlertItem(
        status="firing",
        labels={"alertname": "MongoDbDown", "pod": "mongodb-pod", "namespace": "three-tier"}
    )
    pod_ctx = PodContext(
        pod_name="mongodb-pod",
        namespace="three-tier",
        phase="Running",
        exit_code=1,
        recent_logs="WiredTiger error: No space left on device"
    )
    ctx = IncidentContext(alert=alert, pod_context=pod_ctx)
    rca = await ai_engine.analyze_incident(ctx)

    assert rca.severity == "CRITICAL"
    assert "MongoDB" in rca.root_cause or "storage" in rca.root_cause.lower()
    assert rca.remediation_type == RemediationActionType.RESTART_POD

@pytest.mark.asyncio
async def test_high_memory_pressure_analysis():
    alert = AlertItem(
        status="firing",
        labels={"alertname": "NodeMemoryHighUtilization", "deployment": "api-deployment", "namespace": "three-tier"}
    )
    telemetry = TelemetryContext(memory_utilization_pct=95.0, cpu_utilization_pct=88.0)
    ctx = IncidentContext(alert=alert, telemetry=telemetry)
    rca = await ai_engine.analyze_incident(ctx)

    assert rca.severity == "WARNING"
    assert "saturation" in rca.root_cause.lower() or "memory" in rca.root_cause.lower()
    assert rca.remediation_type == RemediationActionType.SCALE_DEPLOYMENT

@pytest.mark.asyncio
async def test_imagepullbackoff_analysis():
    alert = AlertItem(
        status="firing",
        labels={"alertname": "ImagePullBackOff", "pod": "frontend-web-9a8b", "namespace": "three-tier"}
    )
    pod_ctx = PodContext(
        pod_name="frontend-web-9a8b",
        namespace="three-tier",
        phase="Pending",
        exit_reason="ImagePullBackOff",
        image="myrepo/app:invalid-tag-v9",
        k8s_events=["[Warning] Failed to pull image: rpc error: code = NotFound"]
    )
    ctx = IncidentContext(alert=alert, pod_context=pod_ctx)
    rca = await ai_engine.analyze_incident(ctx)

    assert rca.severity == "CRITICAL"
    assert "ImagePullBackOff" in rca.root_cause
    assert "myrepo/app:invalid-tag-v9" in rca.root_cause
    assert rca.remediation_type == RemediationActionType.ROLLBACK_DEPLOYMENT
