import os
import logging
import fnmatch
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import yaml

logger = logging.getLogger(__name__)

class RemediationPolicy(BaseModel):
    name: str
    description: str = ""
    match_alerts: List[str] = Field(default_factory=list)
    match_exit_codes: List[int] = Field(default_factory=list)
    action: str = "MANUAL_INVESTIGATION"
    allowed_namespaces: List[str] = Field(default_factory=lambda: ["*"])
    excluded_namespaces: List[str] = Field(default_factory=lambda: ["kube-system", "kube-node-lease", "kube-public"])
    cooldown_seconds: int = 300
    max_retries: int = 3
    require_human_approval: bool = False
    scale_increment: int = 2
    max_replicas: int = 10

class PolicyEngine:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.getenv("POLICIES_CONFIG_PATH", "config/policies.yaml")
        self.policies: List[RemediationPolicy] = []
        self.load_policies()

    def load_policies(self):
        """Loads declarative YAML policies from disk or falls back to built-ins."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    raw_policies = data.get("policies", [])
                    self.policies = [RemediationPolicy(**p) for p in raw_policies]
                    logger.info(f"Loaded {len(self.policies)} declarative remediation policies from '{self.config_path}'.")
                    return
            except Exception as e:
                logger.error(f"Failed to load policies from {self.config_path}: {e}")

        logger.info("Using embedded default enterprise policies.")
        self.policies = [
            RemediationPolicy(
                name="default-oom-policy",
                match_alerts=["*OOM*", "*OutOfMemory*", "PodOOMKilled"],
                match_exit_codes=[137],
                action="RESTART_POD",
                cooldown_seconds=300
            ),
            RemediationPolicy(
                name="default-crashloop-policy",
                match_alerts=["*CrashLoop*", "PodCrashLooping"],
                match_exit_codes=[1, 127],
                action="ROLLBACK_DEPLOYMENT",
                cooldown_seconds=600
            ),
            RemediationPolicy(
                name="default-traffic-scaling",
                match_alerts=["*HighTraffic*", "*LatencyP99*", "*NodeMemoryHighUtilization*"],
                action="SCALE_DEPLOYMENT",
                cooldown_seconds=300
            )
        ]

    def find_matching_policy(
        self,
        alert_name: str,
        namespace: str,
        exit_code: Optional[int] = None
    ) -> Optional[RemediationPolicy]:
        """
        Finds the highest-priority matching policy for a given alert, namespace, and exit code.
        Enforces namespace isolation and system protection guardrails.
        """
        for policy in self.policies:
            # Guardrail 1: Protected System Namespaces
            if any(fnmatch.fnmatch(namespace, ex) for ex in policy.excluded_namespaces):
                logger.warning(f"Namespace '{namespace}' is excluded by policy '{policy.name}'. Automated actions blocked.")
                continue

            # Guardrail 2: Allowed Namespaces check
            if not any(fnmatch.fnmatch(namespace, al) for al in policy.allowed_namespaces):
                continue

            # Check Alert Name matching (supports wildcards like *OOM*)
            alert_matched = any(fnmatch.fnmatch(alert_name, pattern) for pattern in policy.match_alerts)

            # Check Exit Code matching if defined
            exit_code_matched = True
            if policy.match_exit_codes and exit_code is not None:
                exit_code_matched = exit_code in policy.match_exit_codes

            if alert_matched and exit_code_matched:
                logger.info(f"Alert '{alert_name}' in '{namespace}' matched Policy: '{policy.name}' (Action: {policy.action})")
                return policy

        logger.info(f"No automated policy matched alert '{alert_name}'. Escalating to manual investigation.")
        return None

policy_engine = PolicyEngine()
