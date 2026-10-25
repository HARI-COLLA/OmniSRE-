import logging
from typing import Optional, List
from .models import PodContext
from .config import settings

logger = logging.getLogger(__name__)

class KubernetesClient:
    def __init__(self):
        self.client_initialized = False
        self.mock_mode = settings.k8s_mock_mode
        self._init_client()

    def _init_client(self):
        if self.mock_mode:
            logger.info("KubernetesClient running in MOCK mode (simulated cluster).")
            self.client_initialized = True
            return

        try:
            from kubernetes import client, config
            if settings.k8s_in_cluster:
                config.load_incluster_config()
                logger.info("Loaded in-cluster Kubernetes configuration.")
            else:
                config.load_kube_config()
                logger.info("Loaded local ~/.kube/config.")

            self.v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
            self.client_initialized = True
        except Exception as e:
            logger.warning(f"Could not initialize Kubernetes client ({e}). Falling back to MOCK mode.")
            self.mock_mode = True
            self.client_initialized = True

    def get_pod_diagnostics(self, namespace: str, pod_name: str, scenario: Optional[str] = None) -> PodContext:
        """
        Extracts pod state, container status, last exit code, events, and recent crash logs.
        """
        if self.mock_mode:
            return self._mock_pod_diagnostics(namespace, pod_name, scenario)

        try:
            # Query real k8s API
            pod = self.v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            events = self.v1.list_namespaced_event(namespace=namespace, field_selector=f"involvedObject.name={pod_name}")
            event_msgs = [f"[{e.type}] {e.reason}: {e.message}" for e in events.items[-5:]]

            # Container exit details
            exit_code = None
            exit_reason = None
            restart_count = 0
            if pod.status and pod.status.container_statuses:
                cs = pod.status.container_statuses[0]
                restart_count = cs.restart_count
                if cs.last_state and cs.last_state.terminated:
                    exit_code = cs.last_state.terminated.exit_code
                    exit_reason = cs.last_state.terminated.reason

            # Logs
            recent_logs = ""
            try:
                recent_logs = self.v1.read_namespaced_pod_log(
                    name=pod_name, namespace=namespace, previous=True, tail_lines=50
                )
            except Exception:
                try:
                    recent_logs = self.v1.read_namespaced_pod_log(
                        name=pod_name, namespace=namespace, tail_lines=50
                    )
                except Exception as log_err:
                    recent_logs = f"Logs unavailable: {log_err}"

            return PodContext(
                pod_name=pod_name,
                namespace=namespace,
                phase=pod.status.phase if pod.status else "Unknown",
                restart_count=restart_count,
                exit_code=exit_code,
                exit_reason=exit_reason,
                recent_logs=recent_logs,
                k8s_events=event_msgs
            )
        except Exception as e:
            logger.error(f"Failed to fetch live K8s pod diagnostics: {e}")
            return self._mock_pod_diagnostics(namespace, pod_name, target_scenario)

    def _mock_pod_diagnostics(self, namespace: str, pod_name: str, scenario: Optional[str] = None) -> PodContext:
        """Generates realistic telemetry context based on common failure scenarios."""
        scenario = scenario or "generic"

        if "oom" in scenario.lower():
            return PodContext(
                pod_name=pod_name,
                namespace=namespace,
                phase="Failed",
                restart_count=4,
                exit_code=137,
                exit_reason="OOMKilled",
                recent_logs="FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory\n1: 0xb09c10 node::Abort() [node]\nCommand terminated by signal 9 (SIGKILL)",
                k8s_events=[
                    "[Warning] Unhealthy: Liveness probe failed: Get http://10.244.1.4:3500/ok: dial tcp: connection refused",
                    "[Warning] BackOff: Back-off restarting failed container mon in pod",
                    "[Warning] OOMKilled: Container api in pod exceeded memory limit 256Mi"
                ]
            )
        elif "pressure" in scenario.lower() or "memory" in scenario.lower():
            return PodContext(
                pod_name=pod_name,
                namespace=namespace,
                phase="Running",
                restart_count=0,
                exit_code=0,
                exit_reason=None,
                recent_logs="Incoming GET /api/tasks 200 OK (Latency: 450ms)\nIncoming POST /api/tasks 201 Created (Concurrency spike detected)",
                k8s_events=[
                    "[Normal] ScalingReplicaSet: Deployment is operating near resource saturation threshold",
                    "[Warning] HighResourceUsage: Memory usage at 94.1%"
                ]
            )
        elif "mongo" in scenario.lower():
            return PodContext(
                pod_name=pod_name,
                namespace=namespace,
                phase="Running",
                restart_count=1,
                exit_code=1,
                exit_reason="Error",
                recent_logs="[conn142] end connection 10.244.0.12:48190 (0 connections now open)\n[initandlisten] waiting for connections on port 27017\nE [storage] WiredTiger error (28) [1792847224:128912][1:0x7f9a1]: No space left on device",
                k8s_events=[
                    "[Warning] FailedMount: MountVolume.SetUp failed for volume mongo-volume: volume is read-only",
                    "[Warning] Unhealthy: Readiness probe failed: nc -z localhost 27017 returned code 1"
                ]
            )
        elif "crash" in scenario.lower():
            return PodContext(
                pod_name=pod_name,
                namespace=namespace,
                phase="CrashLoopBackOff",
                restart_count=6,
                exit_code=1,
                exit_reason="CrashLoopBackOff",
                recent_logs="Error: Cannot find module '/app/server.js'\nat Function.Module._resolveFilename (node:internal/modules/cjs/loader:1144:15)\nat startup (node:internal/bootstrap/switches/is_main:137:12)",
                k8s_events=[
                    "[Warning] BackOff: Back-off 5m0s restarting failed container in pod",
                    "[Normal] Pulled: Container image already present on machine"
                ]
            )
        else:
            return PodContext(
                pod_name=pod_name,
                namespace=namespace,
                phase="Running",
                restart_count=0,
                exit_code=0,
                exit_reason=None,
                recent_logs="Server listening on port 3500\nDatabase connected successfully\nIncoming GET /api/tasks 200 OK",
                k8s_events=["[Normal] Started: Started container"]
            )

    def restart_pod(self, namespace: str, pod_name: str) -> bool:
        """Deletes a pod to trigger Kubernetes ReplicaSet / Deployment recreation."""
        logger.info(f"Remediation action: Restarting pod '{pod_name}' in namespace '{namespace}'...")
        if self.mock_mode:
            logger.info(f"[MOCK] Pod '{pod_name}' successfully evicted and recreated by Deployment controller.")
            return True

        try:
            self.v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
            logger.info(f"Successfully deleted pod {pod_name} for recreation.")
            return True
        except Exception as e:
            logger.error(f"Failed to delete pod {pod_name}: {e}")
            return False

    def restart_deployment(self, namespace: str, deployment_name: str) -> bool:
        """Performs a zero-downtime rolling restart on a deployment."""
        import datetime
        logger.info(f"Remediation action: Triggering rolling restart on Deployment '{deployment_name}' in namespace '{namespace}'...")
        if self.mock_mode:
            logger.info(f"[MOCK] Rolling restart patch applied to Deployment '{deployment_name}'. New replica rollout in progress.")
            return True

        try:
            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            body = {
                'spec': {
                    'template': {
                        'metadata': {
                            'annotations': {
                                'kubectl.kubernetes.io/restartedAt': now
                            }
                        }
                    }
                }
            }
            self.apps_v1.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=body)
            logger.info(f"Deployment {deployment_name} rolling restart triggered.")
            return True
        except Exception as e:
            logger.error(f"Failed to patch deployment {deployment_name}: {e}")
            return False

    def scale_deployment(self, namespace: str, deployment_name: str, target_replicas: int) -> bool:
        """Scales a deployment up or down."""
        logger.info(f"Remediation action: Scaling deployment '{deployment_name}' in '{namespace}' to {target_replicas} replicas...")
        if self.mock_mode:
            logger.info(f"[MOCK] Deployment '{deployment_name}' scaled to {target_replicas} replicas.")
            return True

        try:
            body = {'spec': {'replicas': target_replicas}}
            self.apps_v1.patch_namespaced_deployment_scale(name=deployment_name, namespace=namespace, body=body)
            logger.info(f"Deployment {deployment_name} scaled to {target_replicas}.")
            return True
        except Exception as e:
            logger.error(f"Failed to scale deployment {deployment_name}: {e}")
            return False

k8s_client = KubernetesClient()
