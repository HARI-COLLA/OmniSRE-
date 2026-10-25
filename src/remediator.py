import logging
import time
from typing import Dict, Tuple
from .models import RCAReport, RemediationActionType
from .k8s_client import k8s_client
from .config import settings

logger = logging.getLogger(__name__)

class RemediationEngine:
    def __init__(self):
        # Target -> last remediation timestamp
        self.cooldown_tracker: Dict[str, float] = {}
        # Target -> count of remediations
        self.remediation_counts: Dict[str, int] = {}

    def execute_remediation(self, rca: RCAReport) -> Tuple[bool, str]:
        """
        Executes self-healing action based on RCA recommendations with strict safety guardrails.
        """
        if not settings.auto_remediation_enabled:
            msg = "Auto-remediation is DISABLED by configuration. Skipping automatic execution."
            logger.info(msg)
            return False, msg

        action_type = rca.remediation_type
        target = rca.target_resource
        namespace = rca.namespace

        # Safety Check 1: Actionable type
        if action_type in [RemediationActionType.MANUAL_INVESTIGATION, RemediationActionType.NONE]:
            msg = f"No automated remediation action defined for type '{action_type}'. Escalating to on-call engineer."
            logger.info(msg)
            return False, msg

        # Safety Check 2: Cooldown timer
        now = time.time()
        last_action_time = self.cooldown_tracker.get(target, 0)
        cooldown = settings.remediation_cooldown_seconds
        if (now - last_action_time) < cooldown:
            remaining = int(cooldown - (now - last_action_time))
            msg = f"Safety Cooldown active for target '{target}'. {remaining}s remaining before another automated action is permitted."
            logger.warning(msg)
            return False, msg

        # Safety Check 3: Max retry caps
        attempts = self.remediation_counts.get(target, 0)
        if attempts >= settings.max_remediations_per_target:
            msg = f"Remediation limit exceeded ({attempts}/{settings.max_remediations_per_target}) for '{target}'. Suspending automation to prevent flapping."
            logger.error(msg)
            return False, msg

        # Execute Actions
        success = False
        exec_summary = ""

        try:
            if action_type == RemediationActionType.RESTART_POD:
                logger.info(f"Executing self-healing: Restarting pod '{target}' in '{namespace}'...")
                success = k8s_client.restart_pod(namespace, target)
                exec_summary = f"Triggered pod eviction and recreation for '{target}' in namespace '{namespace}'."

            elif action_type == RemediationActionType.SCALE_DEPLOYMENT:
                target_deployment = target.split("-")[0] if "-" in target else target
                new_replicas = 3
                logger.info(f"Executing self-healing: Horizontally scaling deployment '{target_deployment}' to {new_replicas}...")
                success = k8s_client.scale_deployment(namespace, target_deployment, new_replicas)
                exec_summary = f"Horizontally scaled deployment '{target_deployment}' to {new_replicas} replicas to handle traffic surge."

            elif action_type == RemediationActionType.ROLLBACK_DEPLOYMENT:
                target_deployment = target.split("-")[0] if "-" in target else target
                logger.info(f"Executing self-healing: Triggering rolling restart on '{target_deployment}'...")
                success = k8s_client.restart_deployment(namespace, target_deployment)
                exec_summary = f"Triggered deployment rollout restart for '{target_deployment}'."

            else:
                msg = f"Unimplemented remediation type '{action_type}'."
                return False, msg

            if success:
                self.cooldown_tracker[target] = now
                self.remediation_counts[target] = attempts + 1
                logger.info(f"Remediation successful: {exec_summary}")
                return True, exec_summary
            else:
                return False, f"Failed to execute remediation action on '{target}'."

        except Exception as e:
            err_msg = f"Exception during remediation execution: {e}"
            logger.error(err_msg)
            return False, err_msg

remediation_engine = RemediationEngine()
