import os
import sqlite3
import logging
from typing import List, Optional
from datetime import datetime, timezone
from .models import RCAReport, RemediationActionType

logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DATABASE_PATH", "data/omnisre.db")

class IncidentDatabase:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initializes the persistent SOC2 audit log schema."""
        conn = self._get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS incidents (
                        incident_id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        alert_name TEXT NOT NULL,
                        target_resource TEXT NOT NULL,
                        namespace TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        root_cause TEXT NOT NULL,
                        impact_summary TEXT NOT NULL,
                        confidence_score REAL NOT NULL,
                        recommended_action TEXT NOT NULL,
                        remediation_type TEXT NOT NULL,
                        remediation_executed INTEGER NOT NULL,
                        remediation_result TEXT,
                        created_at TEXT NOT NULL,
                        exit_code INTEGER,
                        policy_matched TEXT,
                        execution_duration_ms INTEGER,
                        verification_status TEXT,
                        raw_logs TEXT
                    )
                """)
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_incidents_timestamp ON incidents(timestamp DESC)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_incidents_namespace ON incidents(namespace)")

                # Automatic safe migration for existing databases
                for col_name, col_type in [
                    ("exit_code", "INTEGER"),
                    ("policy_matched", "TEXT"),
                    ("execution_duration_ms", "INTEGER"),
                    ("verification_status", "TEXT"),
                    ("raw_logs", "TEXT")
                ]:
                    try:
                        cursor.execute(f"ALTER TABLE incidents ADD COLUMN {col_name} {col_type}")
                    except sqlite3.OperationalError:
                        pass

                logger.info(f"Initialized persistent SOC2 incident audit storage at '{self.db_path}'.")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
        finally:
            conn.close()

    def save_incident(self, rca: RCAReport):
        """Persists an incident post-mortem report to the database."""
        conn = self._get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO incidents (
                        incident_id, timestamp, alert_name, target_resource, namespace,
                        severity, root_cause, impact_summary, confidence_score,
                        recommended_action, remediation_type, remediation_executed,
                        remediation_result, created_at, exit_code, policy_matched,
                        execution_duration_ms, verification_status, raw_logs
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rca.incident_id,
                    rca.timestamp,
                    rca.alert_name,
                    rca.target_resource,
                    rca.namespace,
                    rca.severity,
                    rca.root_cause,
                    rca.impact_summary,
                    rca.confidence_score,
                    rca.recommended_action,
                    rca.remediation_type.value if hasattr(rca.remediation_type, 'value') else str(rca.remediation_type),
                    1 if rca.remediation_executed else 0,
                    rca.remediation_result,
                    datetime.now().astimezone().isoformat(),
                    rca.exit_code,
                    rca.policy_matched,
                    rca.execution_duration_ms,
                    rca.verification_status,
                    rca.raw_logs
                ))
                logger.info(f"Persisted incident '{rca.incident_id}' to audit storage.")
        except Exception as e:
            logger.error(f"Failed to persist incident {rca.incident_id}: {e}")
        finally:
            conn.close()

    def get_recent_incidents(self, limit: int = 50) -> List[RCAReport]:
        """Fetches the latest incidents ordered by timestamp descending."""
        incidents = []
        conn = self._get_connection()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM incidents ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            for row in rows:
                keys = row.keys()
                incidents.append(RCAReport(
                    incident_id=row["incident_id"],
                    timestamp=row["timestamp"],
                    alert_name=row["alert_name"],
                    target_resource=row["target_resource"],
                    namespace=row["namespace"],
                    severity=row["severity"],
                    root_cause=row["root_cause"],
                    impact_summary=row["impact_summary"],
                    confidence_score=row["confidence_score"],
                    recommended_action=row["recommended_action"],
                    remediation_type=RemediationActionType(row["remediation_type"]),
                    remediation_executed=bool(row["remediation_executed"]),
                    remediation_result=row["remediation_result"],
                    exit_code=row["exit_code"] if "exit_code" in keys else None,
                    policy_matched=row["policy_matched"] if "policy_matched" in keys else None,
                    execution_duration_ms=row["execution_duration_ms"] if "execution_duration_ms" in keys else None,
                    verification_status=row["verification_status"] if "verification_status" in keys else "Healthy (Running 1/1)",
                    raw_logs=row["raw_logs"] if "raw_logs" in keys else ""
                ))
        except Exception as e:
            logger.error(f"Failed to query incidents from database: {e}")
        finally:
            conn.close()
        return incidents

    def clear_all_incidents(self):
        """Clears all audit logs from the database for fresh simulation cycles."""
        conn = self._get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM incidents")
                logger.info("Cleared all incident records from audit storage.")
        except Exception as e:
            logger.error(f"Failed to clear incidents: {e}")
        finally:
            conn.close()

incident_db = IncidentDatabase()
