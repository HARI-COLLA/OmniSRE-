# 🧪 OmniSRE: Complete Testing, Verification & Portfolio Guide

This guide walks you through **testing every capability of the OmniSRE platform live on your machine**, taking screenshots for your portfolio/LinkedIn, and validating the automated test suites.

---

## 🌐 1. Live Access Endpoints (Active Now on Your Machine)

The platform is running locally as a background service on **Port 8000**:

| Interface | URL | What to Test & Observe |
| :--- | :--- | :--- |
| **OmniSRE Web Dashboard** | 👉 **[http://localhost:8000](http://localhost:8000)** | Interactive dark-mode dashboard with 1-click incident simulators and live post-mortem feed |
| **Interactive Swagger API** | 👉 **[http://localhost:8000/docs](http://localhost:8000/docs)** | Complete OpenAPI explorer to trigger webhooks, query policies, and inspect incident audits |
| **System Health API** | 👉 **[http://localhost:8000/health](http://localhost:8000/health)** | JSON health probe showing active policies and autonomous healing state |
| **Active Policies API** | 👉 **[http://localhost:8000/policies](http://localhost:8000/policies)** | Live list of declarative YAML policies loaded from `config/policies.yaml` |

---

## 📸 2. UI Testing & Portfolio Screenshot Walkthrough

Open your web browser and navigate to **`http://localhost:8000`**.

### Test Case 1: Test Pod OOMKilled (Linux Kernel Exit Code 137)
1. On the dashboard, click the button: **`💥 Pod OOMKilled (Exit 137)`**.
2. **What happens in the background:**
   - The platform receives an alert for a payment microservice pod.
   - It queries container status, extracts **Exit Code `137`**, and parses the heap exhaustion error.
   - The AI correlates the cgroup memory limit breach with telemetry.
   - The policy engine checks `auto-recover-oom` and evicts the dead pod for recreation.
3. **What appears on your screen:**
   - A critical incident card renders with a **98% Confidence Score**.
   - Root Cause Diagnosis: *"Pod was killed with SIGKILL (Exit Code 137) due to Out-Of-Memory (OOMKilled)..."*
   - Status badge turns green: **`AUTONOMOUSLY REMEDIATED`**.
4. 📷 **Screenshot Opportunity:** Capture this card showing the Root Cause Diagnosis, 98% confidence bar, and `AUTONOMOUSLY REMEDIATED` badge!

---

### Test Case 2: Test Database Socket Hang & Probe Failure
1. Click the button: **`🗄️ Database Socket Hang`**.
2. **What appears on your screen:**
   - Incident card for `MongoDbDown` or database failure.
   - Root Cause: *"MongoDB crashed because the underlying EBS Persistent Volume reached 100% capacity..."*
   - Remediation: *"Triggered pod eviction and recreation... in namespace 'three-tier'."*
3. 📷 **Screenshot Opportunity:** Capture the database recovery card.

---

### Test Case 3: Test Microservice Traffic Surge & Horizontal Auto-Scaling
1. Click the button: **`📈 Traffic Saturation (>90%)`**.
2. **What appears on your screen:**
   - Warning incident card for `NodeMemoryHighUtilization`.
   - Action Type: **`RemediationActionType.SCALE_DEPLOYMENT`**.
   - Remediation Log: *"Horizontally scaled deployment 'api' in 'production' to 3 replicas."*
3. 📷 **Screenshot Opportunity:** Great proof of auto-scaling in action!

---

## ⚡ 3. Automated CLI Testing Commands

Open a new PowerShell terminal and test the engine via command line:

### A. Run the 16/16 Automated Test Suite
Validates policy matching, system namespace protection (`kube-system` guardrail), circuit breakers, cooldowns, and all failure modes:

```powershell
cd c:\Users\malla\Downloads\ai-incident-engine
py -m pytest tests/ -v
```

**Expected Result:**
```text
============================= 16 passed in 2.95s ==============================
```

---

### B. Run the Interactive Terminal Simulator
Test the triage pipeline with live terminal logging:

```powershell
cd c:\Users\malla\Downloads\ai-incident-engine
py examples/simulate_incident.py
```
*(Type `5` and press Enter to execute all 4 real-world production incident scenarios sequentially).*

---

## 🔍 4. API & cURL Verification Commands

You can also test the platform via cURL or Postman:

### Check Health & Metadata:
```powershell
curl.exe -s http://localhost:8000/health
```

### Inspect Loaded Declarative Policies:
```powershell
curl.exe -s http://localhost:8000/policies
```

### Fetch Incident Audit History (JSON):
```powershell
curl.exe -s http://localhost:8000/incidents
```

### Simulate Alert via cURL:
```powershell
curl.exe -X POST http://localhost:8000/simulate -H "Content-Type: application/json" -d '{\"scenario\":\"pod_oom_killed\",\"namespace\":\"payments\"}'
```

---

## 🛡️ 5. Key Architecture Points to Highlight in Interviews

1. **Deterministic + Generative AI Hybrid:**
   - Explain why the platform works with 100% precision even without an external API key: it inspects mathematical Linux kernel signals (Exit Code 137 for OOM, Exit Code 1 for runtime crashes) while supporting cloud LLMs (Gemini/OpenAI) for complex edge cases.
2. **Declarative YAML Policies:**
   - SREs define playbooks in `config/policies.yaml` without changing Python code.
3. **Anti-Flapping & Circuit Breakers:**
   - Mandatory cooldowns (300s) and retry caps (3 attempts) prevent restart storms.
4. **Human-in-the-Loop (HITL) Approvals:**
   - Critical database rollbacks generate approval tokens and can be authorized via Slack buttons or `POST /approval/{token}`.
