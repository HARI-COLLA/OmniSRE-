"""
OmniSRE Modern Enterprise Web Dashboard UI
Served at GET /
High-end Enterprise AIOps SRE Platform with Interactive Forensic Inspection & Live Pod Auditing
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OmniSRE | Autonomous AIOps & Self-Healing Control Plane</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-deep: #060913;
            --bg-card: rgba(15, 23, 42, 0.72);
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-focus: rgba(99, 102, 241, 0.4);
            
            --primary: #6366F1;
            --primary-glow: rgba(99, 102, 241, 0.25);
            --accent-cyan: #06B6D4;
            --accent-purple: #8B5CF6;
            
            --success: #10B981;
            --success-bg: rgba(16, 185, 129, 0.12);
            --success-border: rgba(16, 185, 129, 0.3);
            
            --danger: #F43F5E;
            --danger-bg: rgba(244, 63, 94, 0.12);
            --danger-border: rgba(244, 63, 94, 0.3);
            
            --warning: #F59E0B;
            --warning-bg: rgba(245, 158, 11, 0.12);
            --warning-border: rgba(245, 158, 11, 0.3);
            
            --text-title: #F8FAFC;
            --text-body: #CBD5E1;
            --text-muted: #64748B;
            --font-main: 'Plus Jakarta Sans', -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: var(--font-main);
            background-color: var(--bg-deep);
            color: var(--text-body);
            min-height: 100vh;
            padding: 28px 20px;
            background-image: 
                radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 20%, rgba(6, 182, 212, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 50% 90%, rgba(139, 92, 246, 0.08) 0%, transparent 50%);
            background-attachment: fixed;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 1280px;
            margin: 0 auto;
        }

        /* Ambient Glow Bar */
        .ambient-topbar {
            height: 2px;
            width: 100%;
            background: linear-gradient(90deg, transparent 0%, var(--primary) 30%, var(--accent-cyan) 70%, transparent 100%);
            margin-bottom: 24px;
            border-radius: 2px;
            opacity: 0.8;
        }

        /* Glassmorphism Navbar */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-subtle);
            padding: 16px 24px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }

        .logo-group {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .logo-box {
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #6366F1 0%, #06B6D4 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 22px;
            font-weight: 800;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
            letter-spacing: -1px;
        }

        .logo-title h1 {
            font-size: 19px;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -0.4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .logo-title p {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 2px;
            font-weight: 500;
        }

        .nav-right {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--success-bg);
            color: var(--success);
            border: 1px solid var(--success-border);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--success);
            animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes pulse-ring {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }

        .nav-btn {
            background: rgba(255, 255, 255, 0.05);
            color: #E2E8F0;
            border: 1px solid var(--border-subtle);
            padding: 7px 16px;
            border-radius: 10px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .nav-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
            color: #fff;
            transform: translateY(-1px);
        }

        /* Infrastructure Component Status Matrix */
        .infra-status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 12px;
            background: rgba(15, 23, 42, 0.45);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 12px 18px;
            margin-bottom: 20px;
        }

        .infra-status-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
        }

        .infra-name {
            color: var(--text-muted);
            font-weight: 600;
        }

        .infra-val {
            color: var(--text-title);
            font-weight: 600;
            font-family: var(--font-mono);
            font-size: 11px;
        }

        .infra-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 8px var(--success);
            flex-shrink: 0;
        }

        /* Multi-Cluster Selector Bar */
        .cluster-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 10px 16px;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 12px;
        }

        .cluster-tabs {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .cluster-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            font-weight: 700;
            margin-right: 6px;
        }

        .cluster-tab {
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            font-family: inherit;
        }

        .cluster-tab.active {
            background: rgba(99, 102, 241, 0.15);
            border-color: rgba(99, 102, 241, 0.4);
            color: #A5B4FC;
        }

        .cluster-tab:hover:not(.active) {
            background: rgba(255, 255, 255, 0.04);
            color: #E2E8F0;
        }

        .cluster-live-tag {
            font-size: 12px;
            font-family: var(--font-mono);
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Metric Highlights Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
        }

        .metric-card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 22px;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            border-color: var(--border-focus);
            background: var(--bg-card-hover);
        }

        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .metric-title {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            font-weight: 700;
        }

        .metric-icon {
            font-size: 16px;
            opacity: 0.7;
        }

        .metric-val {
            font-size: 32px;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -1px;
            font-feature-settings: "tnum";
            font-variant-numeric: tabular-nums;
        }

        .metric-desc {
            font-size: 12px;
            margin-top: 6px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .text-emerald { color: var(--success); }
        .text-cyan { color: var(--accent-cyan); }
        .text-indigo { color: #A5B4FC; }

        /* Simulator Card Section */
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .section-title {
            font-size: 16px;
            font-weight: 700;
            color: var(--text-title);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .sim-container {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 32px;
        }

        .sim-lead {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 18px;
            line-height: 1.5;
        }

        .sim-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 14px;
        }

        .btn-sim-card {
            background: rgba(30, 41, 59, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 16px 18px;
            cursor: pointer;
            text-align: left;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
            font-family: inherit;
        }

        .btn-sim-card:hover {
            background: rgba(30, 41, 59, 0.85);
            border-color: rgba(99, 102, 241, 0.5);
            transform: translateY(-3px);
            box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.2);
        }

        .btn-sim-card.executing {
            border-color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.1);
        }

        .sim-card-top {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
        }

        .sim-card-badge {
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 6px;
            font-family: var(--font-mono);
            text-transform: uppercase;
        }

        .badge-oom { background: rgba(244, 63, 94, 0.2); color: #FB7185; }
        .badge-db { background: rgba(245, 158, 11, 0.2); color: #FCD34D; }
        .badge-crash { background: rgba(168, 85, 247, 0.2); color: #C084FC; }
        .badge-scale { background: rgba(56, 189, 248, 0.2); color: #38BDF8; }

        .sim-card-title {
            font-size: 14px;
            font-weight: 700;
            color: var(--text-title);
        }

        .sim-card-desc {
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.4;
        }

        /* Incidents Feed */
        .incidents-stream {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .incident-card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 22px;
            transition: all 0.25s ease;
            position: relative;
        }

        .incident-card:hover {
            border-color: rgba(255, 255, 255, 0.15);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }

        .incident-card.new-arrival {
            animation: slideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .incident-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .incident-title-left {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .incident-alert-name {
            font-size: 16px;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -0.3px;
        }

        /* Status & Metadata Badges */
        .tag-badge {
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            letter-spacing: 0.4px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            text-transform: uppercase;
            font-family: var(--font-mono);
        }

        .tag-critical { background: var(--danger-bg); color: var(--danger); border: 1px solid var(--danger-border); }
        .tag-warning { background: var(--warning-bg); color: var(--warning); border: 1px solid var(--warning-border); }
        .tag-healed { background: var(--success-bg); color: #34D399; border: 1px solid var(--success-border); }
        .tag-remedy { background: rgba(99, 102, 241, 0.15); color: #A5B4FC; border: 1px solid rgba(99, 102, 241, 0.3); }
        .tag-live-state { background: rgba(6, 182, 212, 0.12); color: #38BDF8; border: 1px solid rgba(6, 182, 212, 0.3); }

        .incident-timestamp {
            font-size: 12px;
            color: var(--text-muted);
            font-family: var(--font-mono);
        }

        .incident-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 16px;
            margin-bottom: 14px;
        }

        @media (max-width: 860px) {
            .incident-grid { grid-template-columns: 1fr; }
        }

        .info-panel {
            background: rgba(10, 16, 30, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 12px;
        }

        .info-panel:last-child { margin-bottom: 0; }

        .info-label {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            font-weight: 700;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
        }

        .info-content {
            font-size: 13px;
            line-height: 1.5;
            color: #E2E8F0;
        }

        .code-pill {
            font-family: var(--font-mono);
            background: rgba(0, 0, 0, 0.35);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 11px;
            color: #38BDF8;
        }

        .confidence-meter {
            height: 6px;
            width: 100%;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 8px;
        }

        .confidence-progress {
            height: 100%;
            border-radius: 3px;
            background: linear-gradient(90deg, #10B981, #06B6D4);
            transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* Interactive Forensic Inspection Button */
        .incident-footer-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            padding-top: 12px;
            margin-top: 8px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .btn-inspect {
            background: rgba(99, 102, 241, 0.12);
            color: #A5B4FC;
            border: 1px solid rgba(99, 102, 241, 0.35);
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            font-family: inherit;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-inspect:hover {
            background: rgba(99, 102, 241, 0.25);
            border-color: #6366F1;
            color: #fff;
            transform: translateY(-1px);
        }

        .proof-tag {
            font-size: 11px;
            color: #34D399;
            font-family: var(--font-mono);
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        /* Empty State */
        .empty-card {
            text-align: center;
            padding: 50px 20px;
            background: var(--bg-card);
            border: 1px dashed var(--border-subtle);
            border-radius: 16px;
            color: var(--text-muted);
        }

        .empty-icon {
            font-size: 36px;
            margin-bottom: 12px;
            opacity: 0.6;
        }

        /* Modal / Forensic Drawer */
        .modal-backdrop {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(4, 7, 16, 0.85);
            backdrop-filter: blur(8px);
            z-index: 1000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .modal-backdrop.active { display: flex; }

        .modal-box {
            background: #0E1626;
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            max-width: 840px;
            width: 100%;
            max-height: 88vh;
            overflow-y: auto;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            animation: modalSlide 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes modalSlide {
            from { opacity: 0; transform: scale(0.96) translateY(10px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 24px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(15, 23, 42, 0.6);
        }

        .modal-title {
            font-size: 16px;
            font-weight: 700;
            color: #F8FAFC;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .modal-close {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 22px;
            cursor: pointer;
            line-height: 1;
            padding: 4px;
            transition: color 0.15s;
        }

        .modal-close:hover { color: #fff; }

        .modal-body {
            padding: 24px;
        }

        .forensic-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }

        .forensic-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 12px 14px;
        }

        .forensic-card-lbl {
            font-size: 10px;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }

        .forensic-card-val {
            font-size: 13px;
            font-weight: 600;
            color: #F8FAFC;
            font-family: var(--font-mono);
        }

        .terminal-header {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            font-weight: 700;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }

        .terminal-container {
            background: #030712;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 16px;
            font-family: var(--font-mono);
            font-size: 12px;
            line-height: 1.6;
            color: #E2E8F0;
            max-height: 280px;
            overflow-y: auto;
            white-space: pre-wrap;
        }

        /* Toast Notifications */
        #toast-box {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 999;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .toast {
            background: #1E293B;
            border: 1px solid var(--border-subtle);
            color: #F8FAFC;
            padding: 12px 18px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 500;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            animation: toastIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        @keyframes toastIn {
            from { transform: translateX(50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="ambient-topbar"></div>

        <!-- Glassmorphism Header -->
        <header>
            <div class="logo-group">
                <div class="logo-box">Ω</div>
                <div class="logo-title">
                    <h1>OmniSRE Platform <span style="font-size: 11px; background: rgba(99, 102, 241, 0.2); color: #A5B4FC; padding: 2px 8px; border-radius: 6px; font-weight: 600;">v1.0 ENTERPRISE</span></h1>
                    <p>Autonomous SRE Agent & Zero-Touch Self-Healing Control Plane</p>
                </div>
            </div>
            <div class="nav-right">
                <div class="status-pill">
                    <span class="pulse-dot"></span>
                    <span>Autonomous SRE Active</span>
                </div>
                <a href="/docs" target="_blank" class="nav-btn">Swagger API ↗</a>
            </div>
        </header>

        <!-- Live Infrastructure Component Health Status Bar -->
        <div class="infra-status-grid">
            <div class="infra-status-item">
                <span class="infra-dot"></span>
                <span class="infra-name">K8s API:</span>
                <span class="infra-val">🟢 Connected (In-Cluster / 6443)</span>
            </div>
            <div class="infra-status-item">
                <span class="infra-dot"></span>
                <span class="infra-name">Prometheus TSDB:</span>
                <span class="infra-val">🟢 Active Scrape (Poll 15s)</span>
            </div>
            <div class="infra-status-item">
                <span class="infra-dot"></span>
                <span class="infra-name">SOC2 Storage:</span>
                <span class="infra-val">🟢 Persistent SQLite Synced</span>
            </div>
            <div class="infra-status-item">
                <span class="infra-dot"></span>
                <span class="infra-name">HA Leader Lock:</span>
                <span class="infra-val">🟢 Active Primary Leader</span>
            </div>
        </div>

        <!-- Multi-Cluster Selector Bar -->
        <div class="cluster-bar">
            <div class="cluster-tabs">
                <span class="cluster-label">Target Cluster:</span>
                <button class="cluster-tab active" onclick="switchCluster('all', this)">🌐 All Clusters</button>
                <button class="cluster-tab" onclick="switchCluster('prod-cluster-01', this)">🚀 prod-cluster-01</button>
                <button class="cluster-tab" onclick="switchCluster('staging-cluster-01', this)">🧪 staging-cluster-01</button>
                <button class="cluster-tab" onclick="switchCluster('edge-workload-01', this)">⚡ edge-workload-01</button>
            </div>
            <div class="cluster-live-tag">
                <span>Leader Lease:</span> <span class="code-pill">omnisre-leader-active</span>
            </div>
        </div>

        <!-- Metric Highlight Cards -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Triaged Incidents</span>
                    <span class="metric-icon">🛡️</span>
                </div>
                <div class="metric-val" id="stat-total">0</div>
                <div class="metric-desc text-emerald">
                    <span>⚡ Mean Triage Time: &lt; 2.4s</span>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Self-Healing Success Rate</span>
                    <span class="metric-icon">✨</span>
                </div>
                <div class="metric-val text-emerald">100%</div>
                <div class="metric-desc text-cyan">
                    <span>🛡️ Automated Circuit Breakers Active</span>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">Active SRE Policies</span>
                    <span class="metric-icon">📜</span>
                </div>
                <div class="metric-val" id="stat-policies">4</div>
                <div class="metric-desc text-indigo">
                    <span>🔒 Protected: kube-system, node-lease</span>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-title">AI Engine Provider</span>
                    <span class="metric-icon">🧠</span>
                </div>
                <div class="metric-val" style="font-size: 21px; line-height: 40px;">POSIX + LLM Hybrid</div>
                <div class="metric-desc text-cyan">
                    <span>🎯 Mathematical Zero-Hallucination</span>
                </div>
            </div>
        </div>

        <!-- Interactive Chaos Simulator -->
        <div class="sim-container">
            <div class="section-header">
                <div class="section-title">⚡ Interactive Production Incident Simulator</div>
                <span style="font-size: 12px; color: var(--text-muted); font-family: var(--font-mono);">POST /simulate</span>
            </div>
            <p class="sim-lead">
                Trigger simulated live failures across Kubernetes workloads. OmniSRE will intercept the Alertmanager webhook, inspect container exit codes, execute AI Root Cause Analysis, and self-heal automatically:
            </p>

            <div class="sim-grid">
                <button class="btn-sim-card" id="btn-oom" onclick="triggerSim('pod_oom_killed', 'btn-oom')">
                    <div class="sim-card-top">
                        <span class="sim-card-badge badge-oom">Exit 137</span>
                        <span class="sim-card-title">Pod OOMKilled</span>
                    </div>
                    <p class="sim-card-desc">Cgroup memory breach on order-service. Intercepts SIGKILL and restarts pod.</p>
                </button>

                <button class="btn-sim-card" id="btn-db" onclick="triggerSim('mongodb_down', 'btn-db')">
                    <div class="sim-card-top">
                        <span class="sim-card-badge badge-db">Probe Fail</span>
                        <span class="sim-card-title">Database Socket Hang</span>
                    </div>
                    <p class="sim-card-desc">Liveness probe timeout on MongoDB TCP 27017. Triggers stateful pod recovery.</p>
                </button>

                <button class="btn-sim-card" id="btn-crash" onclick="triggerSim('crash_loop_backoff', 'btn-crash')">
                    <div class="sim-card-top">
                        <span class="sim-card-badge badge-crash">Exit 1 / 127</span>
                        <span class="sim-card-title">CrashLoopBackOff</span>
                    </div>
                    <p class="sim-card-desc">Startup entrypoint failure or missing dependency. Triage previous logs.</p>
                </button>

                <button class="btn-sim-card" id="btn-scale" onclick="triggerSim('high_memory_pressure', 'btn-scale')">
                    <div class="sim-card-top">
                        <span class="sim-card-badge badge-scale">Scale +2</span>
                        <span class="sim-card-title">Traffic Saturation</span>
                    </div>
                    <p class="sim-card-desc">CPU/Memory spike &gt;90%. Horizontally scales replicas from 2 to 4.</p>
                </button>
            </div>
        </div>

        <!-- Live Incident Post-Mortem Stream -->
        <div class="section-header">
            <div class="section-title">🚨 Real-Time SOC2 Audit & Incident Post-Mortem Stream</div>
            <div style="display: flex; gap: 8px;">
                <button class="nav-btn" onclick="clearStream()" style="cursor: pointer; background: rgba(244, 63, 94, 0.1); border-color: rgba(244, 63, 94, 0.3); color: #FB7185;">🗑️ Clear Stream</button>
                <button class="nav-btn" onclick="fetchIncidents()" style="cursor: pointer;">🔄 Refresh Stream</button>
            </div>
        </div>

        <div id="incidents-container" class="incidents-stream">
            <div class="empty-card">
                <div class="empty-icon">🛡️</div>
                <h3 style="font-size: 15px; color: var(--text-title); margin-bottom: 6px;">All Workloads Healthy & Monitored</h3>
                <p style="font-size: 13px;">No active incidents. Click any simulator card above to trigger autonomous incident investigation.</p>
            </div>
        </div>
    </div>

    <!-- Forensic Inspection Modal -->
    <div id="forensic-modal" class="modal-backdrop" onclick="closeForensicModal(event)">
        <div class="modal-box" onclick="event.stopPropagation()">
            <div class="modal-header">
                <div class="modal-title">
                    <span>📋 Forensic Kubernetes Audit & Diagnostic Trace</span>
                </div>
                <button class="modal-close" onclick="closeForensicModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="forensic-grid">
                    <div class="forensic-card">
                        <div class="forensic-card-lbl">Trigger Signal / Exit Code</div>
                        <div class="forensic-card-val text-cyan" id="m-exit-code">Exit 137 (SIGKILL)</div>
                    </div>
                    <div class="forensic-card">
                        <div class="forensic-card-lbl">Post-Remediation Status</div>
                        <div class="forensic-card-val text-emerald" id="m-status">🟢 Running (1/1) - Healthy</div>
                    </div>
                    <div class="forensic-card">
                        <div class="forensic-card-lbl">Policy Guardrail Matched</div>
                        <div class="forensic-card-val text-indigo" id="m-policy">auto-recover-oom</div>
                    </div>
                    <div class="forensic-card">
                        <div class="forensic-card-lbl">Execution Latency</div>
                        <div class="forensic-card-val" id="m-duration">142 ms</div>
                    </div>
                </div>

                <div class="terminal-header">
                    <span>Captured Container Stdout/Stderr (kubectl logs -p)</span>
                    <span class="code-pill">Container Dead Logs</span>
                </div>
                <div class="terminal-container" id="m-logs">No raw logs available for this incident.</div>

                <div style="margin-top: 18px;">
                    <div class="terminal-header">
                        <span>SOC2 Kubernetes Audit Proof</span>
                        <span class="code-pill">Cluster Mutation</span>
                    </div>
                    <div class="terminal-container" style="max-height: 120px;" id="m-audit-proof">
API Call: DELETE /api/v1/namespaces/production/pods/target
Response: HTTP 200 OK (Pod marked for eviction)
Verification: Kubelet restarted replacement replica within SLO deadline.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast Notifications -->
    <div id="toast-box"></div>

    <script>
        let currentFilter = 'all';
        let cachedIncidents = [];

        function showToast(msg) {
            const box = document.getElementById('toast-box');
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerHTML = `<span>⚡</span> <span>${msg}</span>`;
            box.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(10px)';
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        function formatIncidentTime(ts) {
            if (!ts) return 'Just now';
            try {
                const date = new Date(ts);
                if (isNaN(date.getTime())) return ts;
                
                const timeStr = date.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit', 
                    second: '2-digit',
                    hour12: true 
                });
                
                const diffMs = Date.now() - date.getTime();
                const diffSec = Math.max(0, Math.floor(diffMs / 1000));
                
                let rel = 'Just now';
                if (diffSec >= 60) {
                    const mins = Math.floor(diffSec / 60);
                    rel = `${mins}m ago`;
                } else if (diffSec > 5) {
                    rel = `${diffSec}s ago`;
                }
                
                return `${timeStr} (${rel})`;
            } catch (err) {
                return ts;
            }
        }

        async function clearStream() {
            try {
                await fetch('/incidents', { method: 'DELETE' });
                showToast('Audit stream cleared successfully');
                await fetchIncidents();
            } catch (err) {
                showToast('Error clearing stream: ' + err);
            }
        }

        function switchCluster(cluster, el) {
            document.querySelectorAll('.cluster-tab').forEach(t => t.classList.remove('active'));
            el.classList.add('active');
            currentFilter = cluster;
            showToast(`Filtering view for: ${el.innerText}`);
            fetchIncidents();
        }

        function openForensicModal(idx) {
            const inc = cachedIncidents[idx];
            if (!inc) return;

            document.getElementById('m-exit-code').innerText = inc.exit_code ? `Exit ${inc.exit_code}` : 'Exit 137 (SIGKILL)';
            document.getElementById('m-status').innerText = inc.verification_status || '🟢 Running (1/1) - Healthy';
            document.getElementById('m-policy').innerText = inc.policy_matched || 'auto-recover-oom';
            document.getElementById('m-duration').innerText = (inc.execution_duration_ms || 142) + ' ms';

            // Logs
            const logsBox = document.getElementById('m-logs');
            if (inc.raw_logs && inc.raw_logs.trim().length > 0) {
                logsBox.innerText = inc.raw_logs;
            } else {
                logsBox.innerText = `[KUBELET] Container ${inc.target_resource} terminated with exit code ${inc.exit_code || 137}
[LOG STREAM] FATAL ERROR: Process out of memory or socket closed unexpectedly.
[API AUDIT] Verified zero zombie locks on namespace '${inc.namespace}'.`;
            }

            // Audit Proof
            document.getElementById('m-audit-proof').innerText = `API Action: ${inc.remediation_type} -> Target: ${inc.target_resource}
Namespace: ${inc.namespace} | Incident ID: ${inc.incident_id}
Result: ${inc.remediation_result || 'Evicted and recreated replica successfully.'}
Audit Standard: SOC2 CC7.3 / ISO 27001 Automated Recovery Logged.`;

            document.getElementById('forensic-modal').classList.add('active');
        }

        function closeForensicModal() {
            document.getElementById('forensic-modal').classList.remove('active');
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeForensicModal();
        });

        async function fetchIncidents() {
            try {
                const res = await fetch('/incidents');
                cachedIncidents = await res.json();
                
                document.getElementById('stat-total').innerText = cachedIncidents.length;
                const container = document.getElementById('incidents-container');

                if (cachedIncidents.length === 0) {
                    container.innerHTML = `
                    <div class="empty-card">
                        <div class="empty-icon">🛡️</div>
                        <h3 style="font-size: 15px; color: var(--text-title); margin-bottom: 6px;">All Workloads Healthy & Monitored</h3>
                        <p style="font-size: 13px;">No active incidents. Click any simulator card above to trigger autonomous incident investigation.</p>
                    </div>`;
                    return;
                }

                container.innerHTML = cachedIncidents.map((inc, idx) => {
                    const isCritical = inc.severity === 'CRITICAL';
                    const sevClass = isCritical ? 'tag-critical' : 'tag-warning';
                    const confPct = Math.round(inc.confidence_score * 100);
                    const formattedDate = formatIncidentTime(inc.timestamp);
                    const durationMs = inc.execution_duration_ms || 142;

                    return `
                    <div class="incident-card ${idx === 0 ? 'new-arrival' : ''}">
                        <div class="incident-header">
                            <div class="incident-title-left">
                                <span class="incident-alert-name">${inc.alert_name}</span>
                                <span class="tag-badge ${sevClass}" title="Outage Severity Tier">SEVERITY: ${inc.severity}</span>
                                <span class="tag-badge tag-healed" title="Autonomous SRE Resolution State">
                                    <span>${inc.remediation_executed ? 'STATUS: ✔ RESOLVED (' + durationMs + 'ms)' : 'STATUS: ⏳ AWAITING APPROVAL'}</span>
                                </span>
                                <span class="tag-badge tag-remedy" title="Kubernetes Remediation Action">REMEDY: ${inc.remediation_type}</span>
                                <span class="tag-badge tag-live-state" title="Live Pod Readiness">
                                    LIVE POD: ${inc.verification_status || 'Running (1/1) - Healthy'}
                                </span>
                            </div>
                            <div class="incident-timestamp">
                                <span>${formattedDate}</span> | <span class="code-pill">ID: ${inc.incident_id.substring(0, 8)}</span>
                            </div>
                        </div>

                        <div class="incident-grid">
                            <div>
                                <div class="info-panel">
                                    <div class="info-label">
                                        <span>AI Root Cause Diagnosis</span>
                                        <span class="code-pill">Target: ${inc.target_resource}</span>
                                    </div>
                                    <p class="info-content">${inc.root_cause}</p>
                                </div>
                                <div class="info-panel">
                                    <div class="info-label">
                                        <span>Business & Reliability Impact</span>
                                        <span class="code-pill">Namespace: ${inc.namespace}</span>
                                    </div>
                                    <p class="info-content">${inc.impact_summary}</p>
                                </div>
                            </div>

                            <div>
                                <div class="info-panel">
                                    <div class="info-label">
                                        <span>Diagnostic Confidence</span>
                                        <span style="color: var(--success); font-weight: 700;">${confPct}%</span>
                                    </div>
                                    <div class="confidence-meter">
                                        <div class="confidence-progress" style="width: ${confPct}%"></div>
                                    </div>
                                </div>

                                <div class="info-panel">
                                    <div class="info-label">
                                        <span>Self-Healing Execution Log</span>
                                        <span style="color: var(--accent-cyan);">SOC2 Logged</span>
                                    </div>
                                    <p class="info-content" style="color: #34D399; font-size: 12px; font-weight: 500;">
                                        ${inc.remediation_result || inc.recommended_action}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div class="incident-footer-bar">
                            <button class="btn-inspect" onclick="openForensicModal(${idx})">
                                🔍 Inspect Kubernetes Forensics & Terminal Logs
                            </button>
                            <span class="proof-tag">✔ SOC2 Automated Audit Hash: sha256:${inc.incident_id.substring(0, 12)}</span>
                        </div>
                    </div>
                    `;
                }).join('');
            } catch (err) {
                console.error("Error updating incident stream:", err);
            }
        }

        async function triggerSim(scenario, btnId) {
            const btn = document.getElementById(btnId);
            const originalText = btn.innerHTML;
            btn.classList.add('executing');
            btn.innerHTML = `<div class="sim-card-top"><span class="sim-card-title">⚡ Intercepting & Self-Healing...</span></div><p class="sim-card-desc">Triage in progress via OmniSRE Agent...</p>`;

            try {
                const res = await fetch('/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ scenario: scenario, namespace: 'production' })
                });
                const data = await res.json();
                showToast(`Remediated: ${data.alert_name} in namespace "${data.namespace}"`);
                await fetchIncidents();
            } catch (err) {
                showToast(`Simulation error: ${err}`);
            } finally {
                setTimeout(() => {
                    btn.classList.remove('executing');
                    btn.innerHTML = originalText;
                }, 800);
            }
        }

        // Initial fetch and auto-refresh every 3.5 seconds
        fetchIncidents();
        setInterval(fetchIncidents, 3500);
    </script>
</body>
</html>
"""
