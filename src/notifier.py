import logging
import httpx
from .models import RCAReport
from .config import settings

logger = logging.getLogger(__name__)

class IncidentNotifier:
    async def dispatch_incident_report(self, rca: RCAReport):
        """Dispatches the RCA report to configured notification sinks."""
        self._print_terminal_banner(rca)

        if settings.slack_webhook_url:
            await self._send_slack_notification(rca)

        if settings.discord_webhook_url:
            await self._send_discord_notification(rca)

    def _print_terminal_banner(self, rca: RCAReport):
        """Prints a human-readable SRE Incident card to the terminal."""
        separator = "=" * 78
        status_symbol = "[REMEDIATED]" if rca.remediation_executed else "[MANUAL ACTION REQUIRED]"
        
        banner = f"""
{separator}
>>> [AIOps SRE AGENT] INCIDENT ROOT CAUSE ANALYSIS REPORT
{separator}
Incident ID     : {rca.incident_id}
Timestamp       : {rca.timestamp}
Alert Triggered : {rca.alert_name} ({rca.severity})
Target Resource : {rca.target_resource} (Namespace: {rca.namespace})
Confidence Score: {rca.confidence_score * 100:.1f}%

[*] ROOT CAUSE DIAGNOSIS:
{rca.root_cause}

[*] IMPACT ASSESSMENT:
{rca.impact_summary}

[*] RECOMMENDED ACTION:
{rca.recommended_action}

[*] AUTO-REMEDIATION STATUS:
Status          : {status_symbol}
Action Type     : {rca.remediation_type}
Execution Log   : {rca.remediation_result or 'None'}
{separator}
"""
        try:
            print(banner)
        except UnicodeEncodeError:
            print(banner.encode("ascii", "replace").decode("ascii"))

    async def _send_slack_notification(self, rca: RCAReport):
        """Sends a rich Block Kit notification to Slack."""
        try:
            color = "#FF0000" if rca.severity == "CRITICAL" else "#FFA500"
            payload = {
                "attachments": [
                    {
                        "color": color,
                        "title": f"🚨 [AIOps Alert] {rca.alert_name} - {rca.target_resource}",
                        "fields": [
                            {"title": "Severity", "value": rca.severity, "short": True},
                            {"title": "Confidence", "value": f"{rca.confidence_score * 100:.0f}%", "short": True},
                            {"title": "Root Cause", "value": rca.root_cause, "short": False},
                            {"title": "Impact", "value": rca.impact_summary, "short": False},
                            {"title": "Remediation Executed", "value": str(rca.remediation_executed), "short": True},
                            {"title": "Action Result", "value": rca.remediation_result or "N/A", "short": False}
                        ],
                        "footer": "AIOps SRE Autonomous Agent"
                    }
                ]
            }
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(settings.slack_webhook_url, json=payload)
        except Exception as e:
            logger.warning(f"Failed to post to Slack: {e}")

    async def _send_discord_notification(self, rca: RCAReport):
        """Sends an embed notification to Discord."""
        try:
            payload = {
                "embeds": [
                    {
                        "title": f"🚨 AIOps Incident Report: {rca.alert_name}",
                        "description": rca.root_cause,
                        "color": 15158332 if rca.severity == "CRITICAL" else 15105570,
                        "fields": [
                            {"name": "Target", "value": f"`{rca.target_resource}`", "inline": True},
                            {"name": "Severity", "value": rca.severity, "inline": True},
                            {"name": "Auto-Remediated", "value": "Yes ✅" if rca.remediation_executed else "No ❌", "inline": True},
                            {"name": "Action Summary", "value": rca.remediation_result or "None", "inline": False}
                        ]
                    }
                ]
            }
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(settings.discord_webhook_url, json=payload)
        except Exception as e:
            logger.warning(f"Failed to post to Discord: {e}")

notifier = IncidentNotifier()
