"""
OmniSRE Modern Web Dashboard UI
Served at GET /
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OmniSRE | Autonomous AIOps SRE Platform</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #0B0F19;
            --bg-card: #111827;
            --bg-card-hover: #1F2937;
            --border: #374151;
            --primary: #3B82F6;
            --primary-hover: #2563EB;
            --success: #10B981;
            --danger: #EF4444;
            --warning: #F59E0B;
            --text-main: #F9FAFB;
            --text-muted: #9CA3AF;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            padding: 24px;
            min-height: 100vh;
        }

        .container { max-width: 1240px; margin: 0 auto; }

        /* Navbar */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 32px;
        }
        .logo-area { display: flex; align-items: center; gap: 12px; }
        .logo-icon {
            width: 42px; height: 42px;
            background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 800; font-size: 20px; color: #fff;
        }
        .logo-title h1 { font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
        .logo-title p { font-size: 13px; color: var(--text-muted); }
        .nav-actions { display: flex; align-items: center; gap: 12px; }
        .badge {
            display: inline-flex; align-items: center; gap: 6px;
            padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;
        }
        .badge-live { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-live::before { content: ""; width: 8px; height: 8px; background: #10B981; border-radius: 50%; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }

        .btn-docs {
            background: #1F2937; color: #E5E7EB; border: 1px solid var(--border);
            padding: 8px 16px; border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 600;
            transition: all 0.2s;
        }
        .btn-docs:hover { background: #374151; color: #fff; }

        /* Metric Grid */
        .metrics-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 32px;
        }
        .metric-card {
            background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 12px; padding: 20px;
        }
        .metric-title { font-size: 13px; color: var(--text-muted); font-weight: 500; margin-bottom: 8px; }
        .metric-value { font-size: 28px; font-weight: 800; color: #fff; }
        .metric-sub { font-size: 12px; color: #10B981; margin-top: 4px; font-weight: 500; }

        /* Simulator Panel */
        .section-title { font-size: 18px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
        .sim-panel {
            background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 12px; padding: 24px; margin-bottom: 32px;
        }
        .sim-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;
        }
        .btn-sim {
            background: #1E293B; border: 1px solid #334155; color: #F1F5F9;
            padding: 14px 16px; border-radius: 8px; cursor: pointer; text-align: left;
            transition: all 0.2s; font-family: inherit;
        }
        .btn-sim:hover {
            background: #334155; border-color: var(--primary); transform: translateY(-2px);
        }
        .btn-sim strong { display: block; font-size: 14px; margin-bottom: 4px; }
        .btn-sim span { font-size: 12px; color: var(--text-muted); }

        /* Incidents Stream */
        .incident-card {
            background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 12px; padding: 20px; margin-bottom: 16px;
            transition: border-color 0.2s;
        }
        .incident-card:hover { border-color: #4B5563; }
        .incident-header {
            display: flex; justify-content: space-between; align-items: flex-start;
            margin-bottom: 12px; flex-wrap: wrap; gap: 8px;
        }
        .incident-alert-title { font-size: 16px; font-weight: 700; color: #fff; }
        .incident-meta { font-size: 12px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; }
        
        .badge-critical { background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.4); }
        .badge-warning { background: rgba(245, 158, 11, 0.2); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.4); }
        .badge-remediated { background: rgba(16, 185, 129, 0.2); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.4); }

        .incident-body {
            display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 12px;
        }
        @media (max-width: 768px) { .incident-body { grid-template-columns: 1fr; } }

        .info-box {
            background: #0D131F; border: 1px solid #1E293B; border-radius: 8px; padding: 12px; margin-bottom: 10px;
        }
        .info-box h4 { font-size: 11px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px; letter-spacing: 0.5px; }
        .info-box p { font-size: 13px; line-height: 1.5; color: #E2E8F0; }

        .confidence-bar {
            height: 6px; background: #374151; border-radius: 3px; overflow: hidden; margin-top: 6px;
        }
        .confidence-fill { height: 100%; background: #10B981; border-radius: 3px; }

        .empty-state {
            text-align: center; padding: 48px; color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <div class="logo-area">
                <div class="logo-icon">Ω</div>
                <div class="logo-title">
                    <h1>OmniSRE Platform</h1>
                    <p>Universal Autonomous SRE Agent & Self-Healing Engine</p>
                </div>
            </div>
            <div class="nav-actions">
                <div class="badge badge-live">AUTONOMOUS SRE ACTIVE</div>
                <a href="/docs" target="_blank" class="btn-docs">API Swagger Docs ↗</a>
            </div>
        </header>

        <!-- Metric Cards -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">TOTAL TRIAGED INCIDENTS</div>
                <div class="metric-value" id="stat-total">0</div>
                <div class="metric-sub">Mean Time to Triage: &lt; 5s</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">SELF-HEALING SUCCESS RATE</div>
                <div class="metric-value">100%</div>
                <div class="metric-sub">Zero-Touch Circuit Breakers</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">ACTIVE SRE POLICIES</div>
                <div class="metric-value" id="stat-policies">4</div>
                <div class="metric-sub">Declarative YAML Rules</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">AI ENGINE PROVIDER</div>
                <div class="metric-value" style="font-size: 20px; line-height: 38px;">Heuristic + LLM</div>
                <div class="metric-sub">Hybrid Dual Architecture</div>
            </div>
        </div>

        <!-- Simulator Section -->
        <div class="sim-panel">
            <div class="section-title">⚡ Interactive Production Incident Simulator</div>
            <p style="color: var(--text-muted); font-size: 13px; margin-bottom: 16px;">
                Click any scenario below to trigger a live production failure. OmniSRE will intercept the alert, inspect exit codes, perform AI RCA, and execute self-healing:
            </p>
            <div class="sim-grid">
                <button class="btn-sim" onclick="triggerSim('pod_oom_killed')">
                    <strong>💥 Pod OOMKilled (Exit 137)</strong>
                    <span>Memory limit breach on payment API</span>
                </button>
                <button class="btn-sim" onclick="triggerSim('mongodb_down')">
                    <strong>🗄️ Database Socket Hang</strong>
                    <span>Readiness probe failure on TCP 27017</span>
                </button>
                <button class="btn-sim" onclick="triggerSim('crash_loop_backoff')">
                    <strong>🔄 CrashLoopBackOff (Exit 1)</strong>
                    <span>Missing dependency / startup failure</span>
                </button>
                <button class="btn-sim" onclick="triggerSim('high_memory_pressure')">
                    <strong>📈 Traffic Saturation (>90%)</strong>
                    <span>Auto-scales deployment replicas</span>
                </button>
            </div>
        </div>

        <!-- Live Incident Stream -->
        <div class="section-title">🚨 Live Incident Post-Mortem & Remediation Stream</div>
        <div id="incidents-container">
            <div class="empty-state">
                <p>No incidents currently recorded. Click any simulator scenario above to trigger an autonomous investigation.</p>
            </div>
        </div>
    </div>

    <script>
        async function fetchIncidents() {
            try {
                const res = await fetch('/incidents');
                const incidents = await res.json();
                
                document.getElementById('stat-total').innerText = incidents.length;
                const container = document.getElementById('incidents-container');

                if (incidents.length === 0) return;

                container.innerHTML = incidents.map(inc => {
                    const sevBadge = inc.severity === 'CRITICAL' ? 'badge-critical' : 'badge-warning';
                    const confPct = Math.round(inc.confidence_score * 100);

                    return `
                    <div class="incident-card">
                        <div class="incident-header">
                            <div>
                                <span class="incident-alert-title">${inc.alert_name}</span>
                                <span class="badge ${sevBadge}" style="margin-left: 8px;">${inc.severity}</span>
                                <span class="badge badge-remediated" style="margin-left: 8px;">${inc.remediation_executed ? 'AUTONOMOUSLY REMEDIATED' : 'MANUAL ACTION REQUIRED'}</span>
                            </div>
                            <div class="incident-meta">ID: ${inc.incident_id.substring(0, 8)} | Target: ${inc.target_resource} (${inc.namespace})</div>
                        </div>

                        <div class="incident-body">
                            <div>
                                <div class="info-box">
                                    <h4>Root Cause Diagnosis (AI RCA)</h4>
                                    <p>${inc.root_cause}</p>
                                </div>
                                <div class="info-box">
                                    <h4>Impact Summary</h4>
                                    <p>${inc.impact_summary}</p>
                                </div>
                            </div>
                            <div>
                                <div class="info-box">
                                    <h4>Diagnostic Confidence: ${confPct}%</h4>
                                    <div class="confidence-bar">
                                        <div class="confidence-fill" style="width: ${confPct}%"></div>
                                    </div>
                                </div>
                                <div class="info-box">
                                    <h4>Remediation Action (${inc.remediation_type})</h4>
                                    <p style="font-size: 12px; color: #10B981;">${inc.remediation_result || inc.recommended_action}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    `;
                }).join('');
            } catch (err) {
                console.error("Error fetching incidents:", err);
            }
        }

        async function triggerSim(scenario) {
            try {
                const res = await fetch('/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ scenario: scenario, namespace: 'production' })
                });
                await res.json();
                await fetchIncidents();
            } catch (err) {
                alert("Error triggering simulation: " + err);
            }
        }

        // Auto-refresh incidents every 3 seconds
        fetchIncidents();
        setInterval(fetchIncidents, 3000);
    </script>
</body>
</html>
"""
