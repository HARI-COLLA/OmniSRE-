import logging
import json
import httpx
from datetime import datetime, timezone
from typing import Optional
from .models import IncidentContext, RCAReport, RemediationActionType
from .config import settings

logger = logging.getLogger(__name__)

SRE_SYSTEM_PROMPT = """
You are a Principal Site Reliability Engineer (SRE) and Autonomous Incident Response Agent for a production Kubernetes 3-Tier cloud application (React Frontend, Node.js API, MongoDB).

Your task is to analyze the provided Incident Context (Alert metadata, Pod exit codes, crash logs, Kubernetes events, and Prometheus telemetry) and output a rigorous Root Cause Analysis (RCA) and an actionable remediation plan.

You must respond ONLY with a valid JSON object matching the following structure:
{
  "severity": "CRITICAL" | "WARNING" | "INFO",
  "root_cause": "Detailed, highly specific explanation of why this component failed based on the evidence.",
  "impact_summary": "User-facing and architectural impact of this incident.",
  "confidence_score": float between 0.0 and 1.0,
  "recommended_action": "Clear human-readable remediation recommendation.",
  "remediation_type": "RESTART_POD" | "SCALE_DEPLOYMENT" | "ROLLBACK_DEPLOYMENT" | "CONFIG_UPDATE" | "MANUAL_INVESTIGATION"
}
"""

class AIEngine:
    def __init__(self):
        self.provider = settings.ai_provider

    async def analyze_incident(self, context: IncidentContext) -> RCAReport:
        """Analyzes an incident context and returns a structured RCA report."""
        alert_name = context.alert.labels.get("alertname", "UnknownAlert")
        target_resource = (
            context.alert.labels.get("pod")
            or context.alert.labels.get("deployment")
            or context.alert.labels.get("instance")
            or context.alert.labels.get("service")
            or "unknown-resource"
        )
        namespace = context.alert.labels.get("namespace", "three-tier")
        severity = context.alert.labels.get("severity", "warning").upper()

        logger.info(f"Analyzing incident {context.incident_id} ({alert_name}) targeting '{target_resource}' via provider '{self.provider}'...")

        # Select provider
        if self.provider == "gemini" and settings.gemini_api_key:
            rca_data = await self._call_gemini(context)
        elif self.provider == "openai" and settings.openai_api_key:
            rca_data = await self._call_openai(context)
        else:
            rca_data = self._rule_based_sre_analyzer(context)

        return RCAReport(
            incident_id=context.incident_id,
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            alert_name=alert_name,
            target_resource=target_resource,
            namespace=namespace,
            severity=rca_data.get("severity", severity),
            root_cause=rca_data.get("root_cause", "Unspecified failure detected by telemetry."),
            impact_summary=rca_data.get("impact_summary", "Service functionality may be degraded."),
            confidence_score=float(rca_data.get("confidence_score", 0.85)),
            recommended_action=rca_data.get("recommended_action", "Inspect container logs and restart."),
            remediation_type=RemediationActionType(rca_data.get("remediation_type", RemediationActionType.MANUAL_INVESTIGATION))
        )

    async def _call_gemini(self, context: IncidentContext) -> dict:
        """Invokes Google Gemini API with SRE context."""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.gemini_api_key}"
            user_content = json.dumps(context.model_dump(), indent=2)
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": SRE_SYSTEM_PROMPT},
                            {"text": f"Incident Context Data:\n{user_content}"}
                        ]
                    }
                ],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
        except Exception as e:
            logger.warning(f"Gemini API call failed ({e}). Falling back to SRE Heuristic Engine.")
            return self._rule_based_sre_analyzer(context)

    async def _call_openai(self, context: IncidentContext) -> dict:
        """Invokes OpenAI Chat Completion API."""
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {settings.openai_api_key}", "Content-Type": "application/json"}
            user_content = json.dumps(context.model_dump(), indent=2)
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": SRE_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Incident Context Data:\n{user_content}"}
                ],
                "response_format": {"type": "json_object"}
            }
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload, headers=headers)
                data = res.json()
                text = data["choices"][0]["message"]["content"]
                return json.loads(text)
        except Exception as e:
            logger.warning(f"OpenAI API call failed ({e}). Falling back to SRE Heuristic Engine.")
            return self._rule_based_sre_analyzer(context)

    def _rule_based_sre_analyzer(self, context: IncidentContext) -> dict:
        """
        Deterministic SRE Expert System.
        Analyzes exit codes, log patterns, and metrics to produce high-precision RCA.
        """
        alert_name = (context.alert.labels.get("alertname") or "") if context.alert.labels else ""
        summary = (context.alert.annotations.get("summary") or "") if context.alert.annotations else ""
        pod_ctx = context.pod_context
        exit_code = pod_ctx.exit_code if pod_ctx else None
        exit_reason = (pod_ctx.exit_reason or "") if pod_ctx else ""
        logs = (pod_ctx.recent_logs or "") if pod_ctx else ""
        events = " ".join(pod_ctx.k8s_events) if (pod_ctx and pod_ctx.k8s_events) else ""

        # Case 1: OOMKilled / Heap Exhaustion
        if exit_code == 137 or "OOMKilled" in exit_reason or "heap out of memory" in logs or "OOMKilled" in events:
            image_name = (pod_ctx.image or "") if pod_ctx else ""
            target_res = (context.alert.labels.get("pod") or "") if context.alert.labels else ""
            
            runtime_name = "container process"
            if "python" in logs.lower() or "python" in image_name.lower():
                runtime_name = "Python application runtime"
            elif "node" in logs.lower() or "javascript" in logs.lower() or "v8" in logs.lower():
                runtime_name = "Node.js V8 runtime"
            elif "jvm" in logs.lower() or "java" in logs.lower():
                runtime_name = "Java JVM"
            elif "go" in logs.lower() or "golang" in logs.lower():
                runtime_name = "Go binary"

            return {
                "severity": "CRITICAL",
                "root_cause": (
                    f"Process terminated with Linux kernel SIGKILL (Exit Code 137) triggered by cgroup OOM Killer. "
                    f"The {runtime_name} exceeded configured container memory limits under load."
                ),
                "impact_summary": "Service replica terminated abruptly, causing active HTTP connections to drop.",
                "confidence_score": 0.98,
                "recommended_action": "Evict failing container, trigger immediate pod restart with clean memory, and scale memory limits in deployment spec.",
                "remediation_type": "RESTART_POD"
            }

        # Case 2: MongoDB Down / Storage Failure
        if "Mongo" in alert_name or "mongodb" in logs.lower() or "mongo" in summary.lower():
            if "read-only" in events or "No space left on device" in logs:
                return {
                    "severity": "CRITICAL",
                    "root_cause": "MongoDB crashed because the underlying EBS Persistent Volume reached 100% capacity and was remounted read-only by the kernel.",
                    "impact_summary": "All stateful write and update operations to the application database are completely blocked.",
                    "confidence_score": 0.95,
                    "recommended_action": "Trigger automated temporary pod recreation and expand EBS PersistentVolumeClaim storage quota.",
                    "remediation_type": "RESTART_POD"
                }
            return {
                "severity": "CRITICAL",
                "root_cause": "MongoDB server instance is unreachable or failing readiness probes on TCP port 27017.",
                "impact_summary": "3-Tier Backend API cannot persist or query task objects; client facing read/writes failing.",
                "confidence_score": 0.92,
                "recommended_action": "Restart the MongoDB pod to reset listener sockets and verify PVC volume mount integrity.",
                "remediation_type": "RESTART_POD"
            }

        # Case: ImagePullBackOff / ErrImagePull
        if "imagepull" in alert_name.lower() or "imagepull" in exit_reason.lower() or "errimagepull" in events.lower() or "imagepullbackoff" in events.lower():
            target_img = (pod_ctx.image or "") if pod_ctx else "configured image"
            return {
                "severity": "CRITICAL",
                "root_cause": f"Container failed to start due to ImagePullBackOff. Kubernetes Kubelet was unable to pull image '{target_img}'. Either the image tag does not exist in registry or ECR/DockerHub pull credentials are misconfigured.",
                "impact_summary": "Replica cannot initialize; deployment cannot scale or replace pods.",
                "confidence_score": 0.98,
                "recommended_action": "Roll back deployment image tag to previous stable GitOps digest or verify image pull secret permissions.",
                "remediation_type": "ROLLBACK_DEPLOYMENT"
            }

        # Case 3: CrashLoopBackOff / Missing Modules / Application Stack Traces
        if "CrashLoop" in alert_name or exit_code in [1, 2, 127] or "Cannot find module" in logs or "CrashLoopBackOff" in exit_reason or "traceback" in logs.lower() or "panic:" in logs.lower():
            # Extract application crash details from logs
            app_err = ""
            for line in reversed(logs.splitlines()):
                line_str = line.strip()
                if any(kw in line_str.lower() for kw in ["error", "exception", "cannot find", "fatal", "syntax", "panic"]):
                    app_err = line_str[:120]
                    break

            if app_err:
                root_msg = f"Application code crashed inside container with exit code {exit_code or 1}. Stack Trace: '{app_err}'."
            else:
                root_msg = f"Container repeatedly failing with non-zero exit code {exit_code or 1} during initialization."

            return {
                "severity": "CRITICAL",
                "root_cause": root_msg,
                "impact_summary": "Deployment replica enters CrashLoopBackOff back-off cycles; active customer requests drop or fail with HTTP 502/503.",
                "confidence_score": 0.96,
                "recommended_action": "Inspect captured stderr stack trace in Forensics, roll back to previous stable release, or apply hotfix to application entrypoint.",
                "remediation_type": "ROLLBACK_DEPLOYMENT" if "cannot find" in logs.lower() or "syntax" in logs.lower() else "RESTART_POD"
            }

        # Case 4: High Traffic / CPU Throttling / Resource Saturation
        if "Memory" in alert_name or "CPU" in alert_name or "throttl" in alert_name.lower() or (context.telemetry and context.telemetry.memory_utilization_pct and context.telemetry.memory_utilization_pct > 85):
            cpu_pct = context.telemetry.cpu_utilization_pct if context.telemetry else 92.4
            mem_pct = context.telemetry.memory_utilization_pct if context.telemetry else 89.1
            is_cpu = "CPU" in alert_name or "throttl" in alert_name.lower()
            return {
                "severity": "WARNING",
                "root_cause": (
                    f"Severe CPU saturation and CFS quota throttling detected ({cpu_pct}% utilization). Process execution throttled by Linux cgroup controller."
                    if is_cpu else
                    f"Sustained traffic surge causing memory saturation ({mem_pct}% utilization >85% threshold)."
                ),
                "impact_summary": "Increased request latency (p99 degradation) and elevated risk of node thrashing.",
                "confidence_score": 0.92,
                "recommended_action": "Scale deployment replicas horizontally (+2) to distribute compute saturation across worker nodes.",
                "remediation_type": "SCALE_DEPLOYMENT"
            }

        # Default fallback
        return {
            "severity": "WARNING",
            "root_cause": f"Observed anomaly in telemetry pattern corresponding to alert '{alert_name}'.",
            "impact_summary": "Service degradation possible.",
            "confidence_score": 0.75,
            "recommended_action": "Inspect cluster logs and verify endpoint responsiveness.",
            "remediation_type": "MANUAL_INVESTIGATION"
        }

ai_engine = AIEngine()
