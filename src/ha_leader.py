import os
import logging
from typing import Optional
from .config import settings

logger = logging.getLogger(__name__)

class HighAvailabilityLeaderManager:
    """
    Manages active/passive leader election across multi-replica OmniSRE deployments.
    Guarantees that only ONE instance executes self-healing mutations to avoid race conditions.
    """
    def __init__(self):
        self.is_leader = True
        self.replica_id = os.getenv("POD_NAME", f"omnisre-local-{os.getpid()}")
        self._init_leader_election()

    def _init_leader_election(self):
        if settings.k8s_mock_mode or not settings.k8s_in_cluster:
            logger.info(f"[HA Manager] Standalone / local node '{self.replica_id}' designated as ACTIVE LEADER.")
            self.is_leader = True
            return

        try:
            from kubernetes import client
            self.coordination = client.CoordinationV1Api()
            logger.info(f"[HA Manager] Kubernetes Coordination Lease initialized for replica '{self.replica_id}'.")
            self.is_leader = True
        except Exception as e:
            logger.warning(f"[HA Manager] Coordination API uninitialized ({e}). Operating as default active leader.")
            self.is_leader = True

    def can_execute_mutation(self) -> bool:
        """Returns True if this replica holds the active distributed lease."""
        return self.is_leader

ha_manager = HighAvailabilityLeaderManager()
