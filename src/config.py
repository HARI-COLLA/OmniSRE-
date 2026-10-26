import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    app_name: str = "AIOps SRE Incident Agent"
    version: str = "1.0.0"
    app_env: str = os.getenv("APP_ENV", "development")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # AI Configuration
    # Options: "mock_heuristic", "gemini", "openai"
    ai_provider: str = os.getenv("AI_PROVIDER", "mock_heuristic")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Kubernetes Configuration
    k8s_in_cluster: bool = os.getenv("K8S_IN_CLUSTER", "false").lower() == "true"
    k8s_mock_mode: bool = os.getenv("K8S_MOCK_MODE", "true").lower() == "true"
    cluster_name: str = os.getenv("CLUSTER_NAME", "auto-detect")

    # Prometheus Configuration
    prometheus_url: str = os.getenv("PROMETHEUS_URL", "http://prometheus-kube-prometheus-prometheus.monitoring.svc:9090")

    # Auto-Remediation Controls
    auto_remediation_enabled: bool = os.getenv("AUTO_REMEDIATION_ENABLED", "true").lower() == "true"
    remediation_cooldown_seconds: int = int(os.getenv("REMEDIATION_COOLDOWN_SECONDS", "300"))
    max_remediations_per_target: int = int(os.getenv("MAX_REMEDIATIONS_PER_TARGET", "3"))

    # Notification Webhooks
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")
    discord_webhook_url: str = os.getenv("DISCORD_WEBHOOK_URL", "")

settings = Settings()
