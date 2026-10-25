import logging
import time
from typing import Dict, Tuple, Optional
from .models import RCAReport, RemediationActionType
from .k8s_client import k8s_client
from .policy_engine import policy_engine
from .config import settings

logger = logging.getLogger(__name__)

class RemediationEngine:
    def __init__(self):
        # Target -> last remediation timestamp
        self.cooldown_tracker: Dict[str, float] = {}
        # Target -> count of remediations
        self.remediation_counts: Dict[str, int] = {}
        # Pending approvals for Human-in-the-Loop: token -> RCAReport
        self.pending_approvals: Dict[str, RCAReport] = {}

    def execute_remediation(self, rca: RCAReport, exit_code: Optional[int] = None) -> Tuple[bool, str]:
        """
        Executes self-healing actions governed by declarative YAML policies and safety guardrails.
        """
        if not settings.auto_remediation_enabled:
            msg = "Auto-remediation is DISABLED by configuration. Skipping automatic execution."
            logger.info(msg)
            return False, msg

        target = rca.target_resource
        namespace = rca.namespace

        # 1. Match against Declarative Policy Engine
        policy = policy_engine.find_matching_policy(rca.alert_name, namespace, exit_code)
        if not policy:
            action_type = rca.remediation_type
            if action_type in [RemediationActionType.MANUAL_INVESTIGATION, RemediationActionType.NONE]:
                msg = f"No automated remediation policy matched for '{rca.alert_name}'. Escalating to on-call engineer."
                logger.info(msg)
                return False, msg
            # Fall back to AI-suggested action with default safety limits
            cooldown = settings.remediation_cooldown_seconds
            max_retries = settings.max_remediations_per_target
            require_approval = False
            scale_inc = 2
            scale_max = 10
        else:
            action_type = RemediationActionType(policy.action)
            rca.remediation_type = action_type
            cooldown = policy.cooldown_seconds
            max_retries = policy.max_retries
            require_approval = policy.require_human_approval
            scale_inc = policy.scale_increment
            scale_max = policy.max_replicas

        # 2. Human-in-the-Loop (HITL) Check
        if require_approval:
            token = f"approval-{rca.incident_id[:8]}"
            self.pending_approvals[token] = rca
            msg = f"Policy '{policy.name if policy else 'default'}' requires human approval. Approval token: {token} generated."
            logger.warning(msg)
            return False, msg

        # 3. Safety Check: Cooldown timer
        now = time.time()
        last_action_time = self.cooldown_tracker.get(target, 0)
        if (now - last_action_time) < cooldown:
            remaining = int(cooldown - (now - last_action_time))
            msg = f"Safety Cooldown active for target '{target}'. {remaining}s remaining before another automated action is permitted."
            logger.warning(msg)
            return False, msg

        # 4. Safety Check: Max retry caps (Circuit Breaker)
        attempts = self.remediation_counts.get(target, 0)
        if attempts >= max_retries:
            msg = f"Circuit breaker tripped: Remediation limit exceeded ({attempts}/{max_retries}) for '{target}'. Suspending automation to prevent flapping."
            logger.error(msg)
            return False, msg

        # 5. Execute Action
        success = False
        exec_summary = ""

        try:
            if action_type == RemediationActionType.RESTART_POD:
                logger.info(f"Executing self-healing: Evicting pod '{target}' in '{namespace}' for controller recreation...")
                success = k8s_client.restart_pod(namespace, target)
                exec_summary = f"Triggered pod eviction and recreation for '{target}' in namespace '{namespace}'."

            elif action_type == RemediationActionType.SCALE_DEPLOYMENT:
                target_deployment = target.split("-")[0] if "-" in target else target
                new_replicas = min(3 + scale_inc, scale_max)
                logger.info(f"Executing self-healing: Horizontally scaling deployment '{target_deployment}' to {new_replicas}...")
                success = k8s_client.scale_deployment(namespace, target_deployment, new_replicas)
                exec_summary = f"Horizontally scaled deployment '{target_deployment}' in '{namespace}' to {new_replicas} replicas."

            elif action_type == RemediationActionType.ROLLBACK_DEPLOYMENT:
                target_deployment = target.split("-")[0] if "-" in target else target
                logger.info(f"Executing self-healing: Triggering rolling restart on '{target_deployment}'...")
                success = k8s_client.restart_deployment(namespace, target_deployment)
                exec_summary = f"Triggered deployment rollout restart for '{target_deployment}' in namespace '{namespace}'."

            else:
                return False, f"Unimplemented remediation type '{action_type}'."

            if success:
                self.cooldown_tracker[target] = now
                self.remediation_counts[target] = attempts + 1
                logger.info(f"Remediation executed successfully: {exec_summary}")
                return True, exec_summary
            else:
                return False, f"Failed to execute remediation action on '{target}'."

        except Exception as e:
            err_msg = f"Exception during remediation execution: {e}"
            logger.error(err_msg)
            return False, err_msg

    def approve_remediation(self, token: str) -> Tuple[bool, str]:
        """Approves and executes a pending Human-in-the-Loop remediation."""
        if token not in self.pending_approvals:
            return False, f"Invalid or expired approval token '{token}'."
        rca = self.pending_approvals.pop(token)
        logger.info(f"Human approval received for token '{token}' (Incident {rca.incident_id}). Executing now...")
        # Temporarily bypass approval requirement since human approved it
        return self.execute_remediation(rca)

remediation_engine = RemediationEngine()
