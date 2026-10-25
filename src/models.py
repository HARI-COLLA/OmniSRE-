from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field

class RemediationActionType(str, Enum):
    RESTART_POD = "RESTART_POD"
    SCALE_DEPLOYMENT = "SCALE_DEPLOYMENT"
    ROLLBACK_DEPLOYMENT = "ROLLBACK_DEPLOYMENT"
    CONFIG_UPDATE = "CONFIG_UPDATE"
    MANUAL_INVESTIGATION = "MANUAL_INVESTIGATION"
    NONE = "NONE"

class AlertItem(BaseModel):
    status: str = "firing"
    labels: Dict[str, str] = Field(default_factory=dict)
    annotations: Dict[str, str] = Field(default_factory=dict)
    startsAt: Optional[str] = None
    endsAt: Optional[str] = None
    generatorURL: Optional[str] = None

class AlertmanagerWebhook(BaseModel):
    receiver: Optional[str] = "ai-incident-engine"
    status: str = "firing"
    alerts: List[AlertItem] = Field(default_factory=list)
    groupLabels: Dict[str, str] = Field(default_factory=dict)
    commonLabels: Dict[str, str] = Field(default_factory=dict)
    commonAnnotations: Dict[str, str] = Field(default_factory=dict)

class PodContext(BaseModel):
    pod_name: str
    namespace: str
    phase: str = "Unknown"
    restart_count: int = 0
    exit_code: Optional[int] = None
    exit_reason: Optional[str] = None
    recent_logs: str = ""
    k8s_events: List[str] = Field(default_factory=list)

class TelemetryContext(BaseModel):
    cpu_utilization_pct: Optional[float] = None
    memory_utilization_pct: Optional[float] = None
    custom_metrics: Dict[str, Any] = Field(default_factory=dict)

class IncidentContext(BaseModel):
    incident_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now().astimezone().isoformat())
    alert: AlertItem
    pod_context: Optional[PodContext] = None
    telemetry: Optional[TelemetryContext] = None

class RCAReport(BaseModel):
    incident_id: str
    timestamp: str
    alert_name: str
    target_resource: str
    namespace: str
    severity: str
    root_cause: str
    impact_summary: str
    confidence_score: float
    recommended_action: str
    remediation_type: RemediationActionType
    remediation_executed: bool = False
    remediation_result: Optional[str] = None
    exit_code: Optional[int] = None
    policy_matched: Optional[str] = None
    execution_duration_ms: Optional[int] = None
    verification_status: Optional[str] = "Healthy (Running 1/1)"
    raw_logs: Optional[str] = ""
    k8s_events: List[str] = Field(default_factory=list)


class SimulationRequest(BaseModel):
    scenario: str = Field(
        default="mongodb_down",
        description="Scenario to simulate: 'mongodb_down', 'pod_oom_killed', 'crash_loop_backoff', 'high_memory_pressure'"
    )
    namespace: str = "three-tier"
    target_service: Optional[str] = None
