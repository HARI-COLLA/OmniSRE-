import logging
from typing import List
from fastapi import FastAPI, BackgroundTasks, status
from .config import settings
from .models import (
    AlertmanagerWebhook,
    IncidentContext,
    RCAReport,
    SimulationRequest,
    AlertItem
)
from .k8s_client import k8s_client
from .prometheus_client import prom_client
from .ai_engine import ai_engine
from .remediator import remediation_engine
from .notifier import notifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("AIOpsServer")

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Autonomous AI-Powered Incident Response & Auto-Remediation Engine for Kubernetes SRE"
)

# In-memory history of analyzed incidents
incident_history: List[RCAReport] = []

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Liveness & readiness probe."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.version,
        "environment": settings.app_env,
        "ai_provider": settings.ai_provider,
        "auto_remediation_enabled": settings.auto_remediation_enabled,
        "k8s_mock_mode": settings.k8s_mock_mode
    }

async def process_incident(alert: AlertItem, target_scenario: str = None) -> RCAReport:
    """Core incident pipeline: Ingest -> Context Gather -> AI RCA -> Remediate -> Notify."""
    namespace = alert.labels.get("namespace", "three-tier")
    target_pod = (
        alert.labels.get("pod")
        or alert.labels.get("instance")
        or alert.labels.get("service")
        or "target-service-pod"
    )

    # 1. Context Gathering: Pod Diagnostics & Prometheus Metrics
    pod_ctx = k8s_client.get_pod_diagnostics(namespace, target_pod, scenario=target_scenario)
    telemetry_ctx = await prom_client.get_resource_telemetry(namespace, target_pod)

    incident_ctx = IncidentContext(
        alert=alert,
        pod_context=pod_ctx,
        telemetry=telemetry_ctx
    )

    # 2. AI Root Cause Analysis
    rca = await ai_engine.analyze_incident(incident_ctx)

    # 3. Auto-Remediation Execution
    executed, exec_result = remediation_engine.execute_remediation(rca)
    rca.remediation_executed = executed
    rca.remediation_result = exec_result

    # 4. Dispatch Notifications
    await notifier.dispatch_incident_report(rca)

    # 5. Save History
    incident_history.insert(0, rca)
    return rca

@app.post("/webhook", status_code=status.HTTP_202_ACCEPTED)
async def alertmanager_webhook(webhook: AlertmanagerWebhook, background_tasks: BackgroundTasks):
    """
    Ingests Prometheus Alertmanager alerts and triggers autonomous AI investigation.
    """
    logger.info(f"Received Alertmanager webhook with {len(webhook.alerts)} alert(s).")
    for alert in webhook.alerts:
        if alert.status == "firing":
            background_tasks.add_task(process_incident, alert)
    return {"message": "Alertmanager webhook ingested successfully", "alerts_count": len(webhook.alerts)}

@app.post("/simulate", response_model=RCAReport, status_code=status.HTTP_200_OK)
async def simulate_incident(req: SimulationRequest):
    """
    Simulates real-world production incident scenarios to demonstrate AI RCA & auto-healing.
    Scenarios: 'mongodb_down', 'pod_oom_killed', 'crash_loop_backoff', 'high_memory_pressure'
    """
    logger.info(f"Triggering incident simulation for scenario: '{req.scenario}'...")

    scenario_map = {
        "mongodb_down": {
            "alertname": "MongoDbDown",
            "severity": "critical",
            "pod": "mongodb-55d4c585b-x52r8",
            "summary": "MongoDB instance is DOWN and unreachable",
            "description": "Readiness probe failed on TCP port 27017. Storage read-only detected."
        },
        "pod_oom_killed": {
            "alertname": "PodOOMKilled",
            "severity": "critical",
            "pod": req.target_service or "api-7db95f877d-w2k4p",
            "summary": "Pod container terminated with exit code 137 (OOMKilled)",
            "description": "V8 memory cgroup limit 256Mi exceeded during heap allocation spike."
        },
        "crash_loop_backoff": {
            "alertname": "PodCrashLooping",
            "severity": "critical",
            "pod": req.target_service or "api-7db95f877d-k9lp2",
            "summary": "Pod container restarting repeatedly in CrashLoopBackOff",
            "description": "Container process exited with status 1 on initialization."
        },
        "high_memory_pressure": {
            "alertname": "NodeMemoryHighUtilization",
            "severity": "warning",
            "pod": "api-deployment",
            "summary": "High memory saturation (>85%) on backend pods",
            "description": "Traffic surge elevated memory usage to 94.1%."
        }
    }

    config = scenario_map.get(req.scenario, scenario_map["mongodb_down"])

    alert = AlertItem(
        status="firing",
        labels={
            "alertname": config["alertname"],
            "severity": config["severity"],
            "namespace": req.namespace,
            "pod": config["pod"],
            "service": req.scenario.split("_")[0]
        },
        annotations={
            "summary": config["summary"],
            "description": config["description"]
        }
    )

    rca = await process_incident(alert, target_scenario=req.scenario)
    return rca

@app.get("/incidents", response_model=List[RCAReport])
def list_incidents():
    """Lists history of all evaluated incidents and generated RCAs."""
    return incident_history
