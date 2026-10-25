"""
Interactive Incident Simulation CLI
Run with: py examples/simulate_incident.py
"""
import sys
import os

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.server import app

def main():
    if sys.stdout.encoding and "utf" not in sys.stdout.encoding.lower():
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    client = TestClient(app)
    
    print("\n" + "=" * 60)
    print(">>> [AIOps SRE AGENT] INTERACTIVE INCIDENT SIMULATOR")
    print("=" * 60)
    print("Choose an incident scenario to simulate:\n")
    print("  1) MongoDB Down / Storage Failure (exit code 1, WiredTiger read-only)")
    print("  2) Pod OOMKilled / Memory Limit Breach (exit code 137)")
    print("  3) Pod CrashLoopBackOff / Missing Dependency (exit code 1)")
    print("  4) High Resource Saturation / Traffic Spike (>90% RAM)")
    print("  5) Run ALL scenarios sequentially\n")

    choice = input("Enter choice [1-5] (default: 1): ").strip() or "1"

    scenarios = {
        "1": ["mongodb_down"],
        "2": ["pod_oom_killed"],
        "3": ["crash_loop_backoff"],
        "4": ["high_memory_pressure"],
        "5": ["mongodb_down", "pod_oom_killed", "crash_loop_backoff", "high_memory_pressure"]
    }

    selected = scenarios.get(choice, ["mongodb_down"])

    for s in selected:
        print(f"\n[Triggering Scenario: {s}]...")
        resp = client.post("/simulate", json={"scenario": s, "namespace": "three-tier"})
        if resp.status_code == 200:
            data = resp.json()
            print(f"[SUCCESS] Analysis Complete! Incident ID: {data['incident_id']}")
        else:
            print(f"[ERROR]: {resp.text}")

if __name__ == "__main__":
    main()
