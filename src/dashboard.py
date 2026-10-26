"""
OmniSRE Modern Enterprise Web Dashboard UI
Served at GET /
Enterprise SRE Control Plane with Multi-Cluster Context, Dynamic Health Hierarchy, and Forensic Investigation
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OmniSRE Platform | Autonomous SRE & Self-Healing Control Plane</title>
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
            padding: 24px 20px;
            background-image: 
                radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 20%, rgba(6, 182, 212, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 50% 90%, rgba(139, 92, 246, 0.08) 0%, transparent 50%);
            background-attachment: fixed;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 1320px;
            margin: 0 auto;
        }

        /* Ambient Topbar */
        .ambient-topbar {
            height: 2px;
            width: 100%;
            background: linear-gradient(90deg, transparent 0%, var(--primary) 30%, var(--accent-cyan) 70%, transparent 100%);
            margin-bottom: 20px;
            border-radius: 2px;
            opacity: 0.8;
        }

        /* Navbar */
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
            margin-bottom: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            flex-wrap: wrap;
            gap: 14px;
        }

        .logo-group {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .logo-box {
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #4F46E5, #06B6D4);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
        }

        .logo-title h1 {
            font-size: 20px;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo-title p {
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 2px;
        }

        .nav-right {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .cluster-live-badge {
            background: rgba(6, 182, 212, 0.12);
            border: 1px solid rgba(6, 182, 212, 0.35);
            color: #38BDF8;
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: var(--font-mono);
        }

        .cluster-live-badge .badge-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #06B6D4;
            box-shadow: 0 0 10px #06B6D4;
            animation: pulseGlow 2s infinite;
        }

        .status-pill {
            background: var(--success-bg);
            border: 1px solid var(--success-border);
            color: #34D399;
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: 0.3px;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 10px var(--success);
            animation: pulseGlow 2s infinite;
        }

        @keyframes pulseGlow {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }

        .nav-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-subtle);
            color: var(--text-body);
            padding: 7px 14px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .nav-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            border-color: rgba(255, 255, 255, 0.2);
        }

        .nav-btn.btn-auth-active {
            border-color: rgba(16, 185, 129, 0.4);
            color: #34D399;
            background: rgba(16, 185, 129, 0.1);
        }

        /* Infra Bar */
        .infra-status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
            background: rgba(10, 16, 30, 0.5);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
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

        /* Multi-Cluster Switcher Bar */
        .cluster-bar {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            overflow-x: auto;
            padding-bottom: 4px;
        }

        .cluster-tab {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-subtle);
            color: var(--text-body);
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .cluster-tab:hover {
            background: rgba(30, 41, 59, 0.8);
            border-color: rgba(255, 255, 255, 0.2);
            color: #fff;
        }

        .cluster-tab.active {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(6, 182, 212, 0.15));
            border-color: var(--accent-cyan);
            color: #fff;
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
        }

        /* Hero Cluster Health Banner */
        .hero-banner {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.14) 0%, rgba(6, 182, 212, 0.08) 100%);
            border: 1px solid rgba(16, 185, 129, 0.35);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 30px -10px rgba(16, 185, 129, 0.2);
            transition: all 0.3s ease;
            flex-wrap: wrap;
            gap: 16px;
        }

        .hero-banner.alert-state {
            background: linear-gradient(135deg, rgba(244, 63, 94, 0.15) 0%, rgba(245, 158, 11, 0.08) 100%);
            border-color: rgba(244, 63, 94, 0.4);
            box-shadow: 0 10px 30px -10px rgba(244, 63, 94, 0.25);
        }

        .hero-title-group {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .hero-icon-box {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #34D399;
            flex-shrink: 0;
        }

        .hero-banner.alert-state .hero-icon-box {
            background: rgba(244, 63, 94, 0.15);
            border-color: rgba(244, 63, 94, 0.3);
            color: #FB7185;
        }

        .hero-title-text h2 {
            font-size: 17px;
            font-weight: 800;
            color: var(--text-title);
            letter-spacing: -0.3px;
        }

        .hero-title-text p {
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 3px;
        }

        .hero-meta-badges {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .hero-badge {
            font-size: 11px;
            font-weight: 700;
            padding: 5px 12px;
            border-radius: 8px;
            font-family: var(--font-mono);
            letter-spacing: 0.3px;
        }

        .badge-green { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); color: #34D399; }
        .badge-blue { background: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.35); color: #38BDF8; }
        .badge-red { background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.35); color: #FB7185; }

        /* Topology Grid */
        .topology-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 14px;
            margin-bottom: 24px;
        }

        .topo-card {
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 16px;
            transition: all 0.2s ease;
        }

        .topo-card:hover {
            border-color: var(--border-focus);
            transform: translateY(-2px);
        }

        .topo-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .topo-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-title);
        }

        .topo-status-tag {
            font-size: 10px;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: var(--font-mono);
        }

        .status-ok { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .status-err { background: rgba(244, 63, 94, 0.15); color: #FB7185; border: 1px solid rgba(244, 63, 94, 0.3); }

        .topo-val {
            font-family: var(--font-mono);
            font-size: 12px;
            color: #38BDF8;
            margin-bottom: 6px;
            word-break: break-all;
        }

        .topo-sub {
            font-size: 11px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
        }

        /* Section Heading */
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .section-title {
            font-size: 16px;
            font-weight: 800;
            color: var(--text-title);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Simulators Grid */
        .simulators-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 12px;
            margin-bottom: 24px;
        }

        .sim-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 14px 16px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
            position: relative;
            overflow: hidden;
        }

        .sim-card:hover {
            border-color: rgba(99, 102, 241, 0.4);
            background: rgba(30, 41, 59, 0.8);
            transform: translateY(-2px);
        }

        .sim-card.executing {
            border-color: var(--warning);
            background: rgba(245, 158, 11, 0.1);
        }

        .sim-card-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 6px;
        }

        .sim-card-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-title);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .sim-badge {
            font-size: 10px;
            font-family: var(--font-mono);
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-muted);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .sim-card-desc {
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.4;
        }

        /* Filter & Search Bar */
        .filter-bar {
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 12px 18px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .search-box {
            flex: 1;
            min-width: 220px;
            position: relative;
        }

        .search-box input {
            width: 100%;
            background: rgba(10, 16, 30, 0.7);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 8px 12px 8px 34px;
            color: #fff;
            font-family: var(--font-main);
            font-size: 12px;
            outline: none;
            transition: all 0.2s ease;
        }

        .search-box input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.2);
        }

        .search-icon {
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
            display: flex;
        }

        .filter-select {
            background: rgba(10, 16, 30, 0.7);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 8px 12px;
            color: var(--text-body);
            font-family: var(--font-main);
            font-size: 12px;
            outline: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .filter-select:focus {
            border-color: var(--primary);
        }

        .filter-btn-clear {
            background: transparent;
            border: 1px solid var(--border-subtle);
            color: var(--text-muted);
            padding: 7px 12px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .filter-btn-clear:hover {
            color: #fff;
            border-color: rgba(255, 255, 255, 0.2);
        }

        /* Incident Post-Mortem Stream */
        .incident-card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 18px;
            transition: all 0.25s ease;
            position: relative;
        }

        .incident-card.card-unresolved {
            border-color: rgba(244, 63, 94, 0.4);
            box-shadow: 0 0 25px rgba(244, 63, 94, 0.15);
        }

        .incident-card:hover {
            border-color: var(--border-focus);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }

        /* Failure Location Breadcrumbs */
        .error-location-bar {
            background: rgba(10, 16, 30, 0.6);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 8px 14px;
            margin-bottom: 14px;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            font-family: var(--font-mono);
        }

        .location-label {
            color: var(--text-muted);
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.5px;
        }

        .loc-crumb strong {
            color: var(--text-title);
        }

        .loc-sep {
            color: var(--text-muted);
            opacity: 0.6;
        }

        .text-cyan { color: #38BDF8 !important; }
        .text-indigo { color: #A5B4FC !important; }
        .text-warning { color: #FCD34D !important; }
        .text-emerald { color: #34D399 !important; }

        /* Resolution Status Banner */
        .resolution-status-banner {
            padding: 12px 16px;
            border-radius: 10px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 14px;
            border: 1px solid transparent;
        }

        .res-solved {
            background: rgba(16, 185, 129, 0.1);
            border-color: rgba(16, 185, 129, 0.25);
            color: #34D399;
        }

        .res-pending {
            background: rgba(245, 158, 11, 0.1);
            border-color: rgba(245, 158, 11, 0.25);
            color: #FCD34D;
        }

        .res-rejected {
            background: rgba(244, 63, 94, 0.1);
            border-color: rgba(244, 63, 94, 0.25);
            color: #FB7185;
        }

        .incident-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 12px;
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

        .tag-badge {
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            font-family: var(--font-mono);
            letter-spacing: 0.3px;
        }

        .tag-critical { background: var(--danger-bg); border: 1px solid var(--danger-border); color: #FB7185; }
        .tag-warning { background: var(--warning-bg); border: 1px solid var(--warning-border); color: #FCD34D; }
        .tag-healed { background: var(--success-bg); border: 1px solid var(--success-border); color: #34D399; }
        .tag-remedy { background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); color: #A5B4FC; }
        .tag-live-state { background: rgba(6, 182, 212, 0.12); border: 1px solid rgba(6, 182, 212, 0.3); color: #38BDF8; }

        .incident-timestamp {
            font-size: 12px;
            color: var(--text-muted);
            font-family: var(--font-mono);
        }

        .code-pill {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-subtle);
            padding: 2px 6px;
            border-radius: 4px;
            color: #CBD5E1;
            font-family: var(--font-mono);
            font-size: 11px;
        }

        .incident-grid {
            display: grid;
            grid-template-columns: 3fr 2fr;
            gap: 18px;
            margin-bottom: 16px;
        }

        @media (max-width: 900px) {
            .incident-grid { grid-template-columns: 1fr; }
        }

        .info-panel {
            background: rgba(10, 16, 30, 0.5);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }

        .info-label {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .info-content {
            font-size: 13px;
            line-height: 1.5;
            color: var(--text-body);
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
            background: linear-gradient(90deg, #10B981, #06B6D4);
            border-radius: 3px;
            transition: width 0.5s ease;
        }

        .incident-footer-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 14px;
            border-top: 1px solid var(--border-subtle);
            flex-wrap: wrap;
            gap: 12px;
        }

        .btn-inspect {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-subtle);
            color: var(--text-body);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-inspect:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            border-color: rgba(255, 255, 255, 0.2);
        }

        .btn-action-approve {
            background: linear-gradient(135deg, #10B981, #059669);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-action-approve:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
        }

        .btn-action-deny {
            background: rgba(244, 63, 94, 0.15);
            border: 1px solid rgba(244, 63, 94, 0.35);
            color: #FB7185;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-action-deny:hover {
            background: rgba(244, 63, 94, 0.25);
            color: #fff;
        }

        .proof-tag {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--text-muted);
        }

        /* Empty Card */
        .empty-card {
            background: var(--bg-card);
            border: 1px dashed var(--border-subtle);
            border-radius: 16px;
            padding: 48px 24px;
            text-align: center;
            color: var(--text-muted);
        }

        .empty-icon {
            font-size: 36px;
            margin-bottom: 12px;
            color: #34D399;
        }

        /* Load More */
        .load-more-container {
            text-align: center;
            margin: 20px 0;
        }

        .btn-load-more {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border-subtle);
            color: var(--text-body);
            padding: 10px 24px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-load-more:hover {
            background: rgba(30, 41, 59, 0.9);
            border-color: var(--border-focus);
            color: #fff;
        }

        /* Forensic Modal */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(3, 7, 18, 0.82);
            backdrop-filter: blur(10px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding: 20px;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal-card {
            background: #0B1120;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 18px;
            width: 100%;
            max-width: 820px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7);
            padding: 24px 28px;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 14px;
            border-bottom: 1px solid var(--border-subtle);
        }

        .modal-title {
            font-size: 17px;
            font-weight: 800;
            color: var(--text-title);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .btn-close {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 20px;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 6px;
            transition: all 0.2s ease;
        }

        .btn-close:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.1);
        }

        .modal-metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 12px;
            margin-bottom: 18px;
        }

        .modal-metric-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 12px;
        }

        .m-lbl { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }
        .m-val { font-size: 14px; font-weight: 700; color: #fff; font-family: var(--font-mono); margin-top: 4px; }

        .terminal-container {
            background: #020617;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 14px;
            font-family: var(--font-mono);
            font-size: 12px;
            color: #94A3B8;
            max-height: 240px;
            overflow-y: auto;
            white-space: pre-wrap;
            line-height: 1.5;
            margin-bottom: 18px;
        }

        .modal-actions-bar {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            flex-wrap: wrap;
            padding-top: 14px;
            border-top: 1px solid var(--border-subtle);
        }

        .btn-modal-action {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--border-subtle);
            color: var(--text-body);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-modal-action:hover {
            background: rgba(255, 255, 255, 0.15);
            color: #fff;
        }

        /* Toast */
        #toast-box {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 2000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .toast {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(99, 102, 241, 0.35);
            color: #fff;
            padding: 12px 18px;
            border-radius: 10px;
            font-size: 13px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideIn 0.3s ease;
            transition: all 0.3s ease;
            max-width: 420px;
        }

        @keyframes slideIn {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .rotating {
            animation: rotateIcon 1s linear infinite;
        }

        @keyframes rotateIcon {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="ambient-topbar"></div>

        <!-- Glassmorphism Navbar -->
        <header>
            <div class="logo-group">
                <div class="logo-box">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        <path d="m9 12 2 2 4-4"/>
                    </svg>
                </div>
                <div class="logo-title">
                    <h1>OmniSRE Platform Control Plane</h1>
                    <p>Universal Autonomous SRE & Self-Healing Engine</p>
                </div>
            </div>

            <div class="nav-right">
                <div class="cluster-live-badge">
                    <span class="badge-dot"></span>
                    <span id="nav-cluster-name">Cluster: omnisre-prod-eks</span>
                </div>

                <div class="status-pill">
                    <span class="pulse-dot" id="ws-dot"></span>
                    <span id="ws-status">Real-Time WebSocket (0ms)</span>
                </div>

                <button class="nav-btn" id="btn-api-key" onclick="openAuthModal()" title="Configure API Authentication Key">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="7.5" cy="15.5" r="5.5"/>
                        <path d="m21 2-9.6 9.6"/>
                        <path d="m15.5 7.5 3 3L22 7l-3-3"/>
                    </svg>
                    <span id="auth-btn-label">API Key</span>
                </button>

                <button class="nav-btn" id="btn-refresh" onclick="handleManualRefresh()" title="Synchronize with live cluster telemetry">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                        <path d="M3 3v5h5"/>
                        <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
                        <path d="M16 21h5v-5"/>
                    </svg>
                    <span>Sync</span>
                </button>

                <a href="/docs" target="_blank" class="nav-btn" title="OpenAPI Swagger Documentation">
                    <span>API Docs</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                        <polyline points="15 3 21 3 21 9"/>
                        <line x1="10" y1="14" x2="21" y2="3"/>
                    </svg>
                </a>
            </div>
        </header>

        <!-- Live Infrastructure Topology Telemetry Bar -->
        <div class="infra-status-grid">
            <div class="infra-status-item">
                <span class="infra-dot"></span>
                <span class="infra-name">Control Plane:</span>
                <span class="infra-val" id="k8s-ver-pill">v1.31 (EKS Active)</span>
            </div>
            <div class="infra-status-item">
                <span class="infra-dot"></span>
                <span class="infra-name">Cluster Nodes:</span>
                <span class="infra-val" id="infra-nodes">2/2 Nodes Ready (t3.small)</span>
            </div>
            <div class="infra-status-item">
                <span class="infra-dot"></span>
                <span class="infra-name">Workloads:</span>
                <span class="infra-val" id="infra-workloads">7/7 Pods Nominal (100%)</span>
            </div>
            <div class="infra-status-item">
                <span class="infra-dot"></span>
                <span class="infra-name">Cluster Time (UTC):</span>
                <span class="infra-val" id="live-cluster-clock">00:00:00 UTC</span>
            </div>
        </div>

        <!-- Multi-Cluster Context Switcher -->
        <div class="cluster-bar">
            <span style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-right: 4px;">Context:</span>
            <button class="cluster-tab active" onclick="switchCluster('omnisre-prod-eks', this)">
                <span>AWS EKS (Production)</span>
            </button>
            <button class="cluster-tab" onclick="switchCluster('gke-primary-us', this)">
                <span>Google GKE (Primary)</span>
            </button>
            <button class="cluster-tab" onclick="switchCluster('aks-staging-eu', this)">
                <span>Azure AKS (Staging)</span>
            </button>
            <button class="cluster-tab" onclick="switchCluster('onprem-baremetal-01', this)">
                <span>Bare-Metal (Edge/NOC)</span>
            </button>
        </div>

        <!-- Dynamic Hero Health Banner -->
        <div class="hero-banner" id="hero-banner">
            <div class="hero-title-group">
                <div class="hero-icon-box" id="hero-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        <path d="m9 12 2 2 4-4"/>
                    </svg>
                </div>
                <div class="hero-title-text">
                    <h2 id="hero-title">CLUSTER HEALTH: 100% OPERATIONAL</h2>
                    <p id="hero-sub">Connected to AWS EKS cluster <strong>omnisre-prod-eks</strong>. 0 active firing alerts. All nodes and workloads healthy.</p>
                </div>
            </div>
            <div class="hero-meta-badges">
                <span class="hero-badge badge-green" id="hero-status-pill">● 0 FIRING ALERTS</span>
                <span class="hero-badge badge-blue">● 2/2 NODES READY</span>
                <span class="hero-badge badge-blue">● SOC2 AUDIT ACTIVE</span>
            </div>
        </div>

        <!-- Live Node Topology Grid -->
        <div class="topology-grid" id="topology-grid">
            <div class="topo-card">
                <div class="topo-header">
                    <span class="topo-title">EKS Control Plane</span>
                    <span class="topo-status-tag status-ok">ACTIVE</span>
                </div>
                <div class="topo-val">omnisre-prod-eks</div>
                <div class="topo-sub">
                    <span>Provider: AWS EKS</span>
                    <span>Region: ap-south-1</span>
                </div>
            </div>

            <div class="topo-card">
                <div class="topo-header">
                    <span class="topo-title">Worker Node 1</span>
                    <span class="topo-status-tag status-ok">READY</span>
                </div>
                <div class="topo-val">ip-192-168-41-75</div>
                <div class="topo-sub">
                    <span>Type: t3.small</span>
                    <span>Runtime: containerd</span>
                </div>
            </div>

            <div class="topo-card">
                <div class="topo-header">
                    <span class="topo-title">Worker Node 2</span>
                    <span class="topo-status-tag status-ok">READY</span>
                </div>
                <div class="topo-val">ip-192-168-73-36</div>
                <div class="topo-sub">
                    <span>Type: t3.small</span>
                    <span>Runtime: containerd</span>
                </div>
            </div>
        </div>

        <!-- Live Chaos & Scenario Injector Section -->
        <div class="section-header">
            <div class="section-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
                <span>Production Failure Scenarios & Interactive Chaos Triage</span>
            </div>
            <span style="font-size: 12px; color: var(--text-muted);">Simulate real-world outages & test autonomous resolution</span>
        </div>

        <div class="simulators-grid">
            <button class="sim-card" id="btn-sim-oom" onclick="triggerSim('pod_oom_killed', 'btn-sim-oom')">
                <div class="sim-card-top">
                    <span class="sim-card-title">Pod OOMKilled</span>
                    <span class="sim-badge">Exit 137</span>
                </div>
                <p class="sim-card-desc">Cgroup memory breach. Intercepts SIGKILL, harvests container dump, restarts pod.</p>
            </button>

            <button class="sim-card" id="btn-sim-db" onclick="triggerSim('mongodb_down', 'btn-sim-db')">
                <div class="sim-card-top">
                    <span class="sim-card-title">Database Socket Hang</span>
                    <span class="sim-badge">Probe Fail</span>
                </div>
                <p class="sim-card-desc">Liveness probe timeout on MongoDB TCP 27017. Triggers stateful controller recovery.</p>
            </button>

            <button class="sim-card" id="btn-sim-crash" onclick="triggerSim('crash_loop_backoff', 'btn-sim-crash')">
                <div class="sim-card-top">
                    <span class="sim-card-title">CrashLoopBackOff</span>
                    <span class="sim-badge">Exit 1 / 127</span>
                </div>
                <p class="sim-card-desc">Startup entrypoint failure. Triages previous logs, rolls back faulty deployment.</p>
            </button>

            <button class="sim-card" id="btn-sim-traffic" onclick="triggerSim('high_memory_pressure', 'btn-sim-traffic')">
                <div class="sim-card-top">
                    <span class="sim-card-title">Traffic Saturation</span>
                    <span class="sim-badge">Scale +2</span>
                </div>
                <p class="sim-card-desc">CPU/Memory spike &gt;90%. Horizontally scales deployment replicas via HPA.</p>
            </button>
        </div>

        <!-- Incident Post-Mortem Stream Header -->
        <div class="section-header">
            <div class="section-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6366F1" stroke-width="2">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                    <line x1="8" y1="21" x2="16" y2="21"/>
                    <line x1="12" y1="17" x2="12" y2="21"/>
                </svg>
                <span>Incident Post-Mortem & Autonomous Remediation Stream</span>
                <span class="sim-badge" id="incident-counter-badge">0 Incidents</span>
            </div>
            <div style="display: flex; gap: 8px;">
                <button class="nav-btn" onclick="clearStream()" title="Clear audit history for fresh tests">
                    <span>Clear Stream</span>
                </button>
            </div>
        </div>

        <!-- Filter & Search Controls Bar -->
        <div class="filter-bar">
            <div class="search-box">
                <span class="search-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"/>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                </span>
                <input type="text" id="filter-search" placeholder="Search alert, pod, namespace, or root cause..." oninput="handleFilterChange()">
            </div>

            <select class="filter-select" id="filter-severity" onchange="handleFilterChange()">
                <option value="ALL">All Severities</option>
                <option value="CRITICAL">Critical Only</option>
                <option value="WARNING">Warning Only</option>
            </select>

            <select class="filter-select" id="filter-namespace" onchange="handleFilterChange()">
                <option value="ALL">All Namespaces</option>
            </select>

            <select class="filter-select" id="filter-status" onchange="handleFilterChange()">
                <option value="ALL">All Statuses</option>
                <option value="UNRESOLVED">Unresolved First</option>
                <option value="RESOLVED">Resolved Only</option>
                <option value="APPROVAL">Awaiting Approval</option>
            </select>

            <select class="filter-select" id="filter-sort" onchange="handleFilterChange()">
                <option value="NEWEST">Newest First</option>
                <option value="OLDEST">Oldest First</option>
                <option value="CONFIDENCE">Highest Confidence</option>
            </select>

            <button class="filter-btn-clear" onclick="resetFilters()">Reset</button>
        </div>

        <!-- Container for Live Cards -->
        <div id="incidents-container">
            <div class="empty-card">
                <div class="empty-icon">
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        <path d="m9 12 2 2 4-4"/>
                    </svg>
                </div>
                <h3 style="font-size: 15px; color: var(--text-title); margin-bottom: 6px;">Cluster Workloads Healthy & Monitored</h3>
                <p style="font-size: 13px;">No active firing incidents. The autonomous AIOps agent is actively monitoring Prometheus and Kubernetes telemetry.</p>
            </div>
        </div>

        <!-- Load More Container -->
        <div class="load-more-container" id="load-more-box" style="display: none;">
            <button class="btn-load-more" id="btn-load-more" onclick="loadMoreIncidents()">
                Load More Incidents
            </button>
        </div>
    </div>

    <!-- API Key Authentication Modal -->
    <div class="modal-overlay" id="auth-modal" role="dialog" aria-modal="true" aria-labelledby="auth-modal-title">
        <div class="modal-card" style="max-width: 480px;">
            <div class="modal-header">
                <div class="modal-title" id="auth-modal-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6366F1" stroke-width="2">
                        <circle cx="7.5" cy="15.5" r="5.5"/>
                        <path d="m21 2-9.6 9.6"/>
                        <path d="m15.5 7.5 3 3L22 7l-3-3"/>
                    </svg>
                    <span>OmniSRE API Authentication</span>
                </div>
                <button class="btn-close" onclick="closeAuthModal()" aria-label="Close dialog">&times;</button>
            </div>
            <p style="font-size: 13px; color: var(--text-body); margin-bottom: 16px; line-height: 1.5;">
                Enter your configured <code>API_KEY</code> to authorize remediation executions and privileged control plane actions. Stored securely in your current browser session.
            </p>
            <div style="margin-bottom: 16px;">
                <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">API Token / Key</label>
                <input type="password" id="input-api-key" placeholder="Enter X-API-Key..." style="width: 100%; margin-top: 6px; background: #020617; border: 1px solid var(--border-subtle); border-radius: 8px; padding: 10px 12px; color: #fff; font-family: var(--font-mono); font-size: 13px; outline: none;">
            </div>
            <div class="modal-actions-bar">
                <button class="btn-modal-action" onclick="clearApiKey()">Clear Key</button>
                <button class="btn-action-approve" onclick="saveApiKey()">Save & Connect</button>
            </div>
        </div>
    </div>

    <!-- Forensic Details Modal with A11y Focus Trap -->
    <div class="modal-overlay" id="forensic-modal" role="dialog" aria-modal="true" aria-labelledby="forensic-modal-title">
        <div class="modal-card" id="forensic-modal-card">
            <div class="modal-header">
                <div class="modal-title" id="forensic-modal-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2">
                        <polyline points="4 17 10 11 4 5"/>
                        <line x1="12" y1="19" x2="20" y2="19"/>
                    </svg>
                    <span>Kubernetes Diagnostic Forensics & Terminal Logs</span>
                </div>
                <button class="btn-close" onclick="closeForensicModal()" aria-label="Close modal">&times;</button>
            </div>

            <div class="modal-metric-grid">
                <div class="modal-metric-card">
                    <div class="m-lbl">POSIX Exit Code</div>
                    <div class="m-val" id="m-exit-code">—</div>
                </div>
                <div class="modal-metric-card">
                    <div class="m-lbl">Replica Status</div>
                    <div class="m-val" id="m-status" style="color: #34D399; font-size: 12px;">—</div>
                </div>
                <div class="modal-metric-card">
                    <div class="m-lbl">Policy Matched</div>
                    <div class="m-val" id="m-policy" style="font-size: 12px;">—</div>
                </div>
                <div class="modal-metric-card">
                    <div class="m-lbl">Execution Duration</div>
                    <div class="m-val" id="m-duration">—</div>
                </div>
            </div>

            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px;">
                Raw Container Crash Logs (previous=True)
            </div>
            <div class="terminal-container" id="m-logs">No log data recorded.</div>

            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px;">
                Cryptographic Audit Proof (SOC2 CC7.3 / ISO 27001)
            </div>
            <div class="terminal-container" id="m-audit-proof" style="max-height: 140px; color: #38BDF8;">
                Audit Proof
            </div>

            <div class="modal-actions-bar">
                <button class="btn-modal-action" id="btn-copy-id" onclick="copyCurrentIncidentId()">
                    <span>Copy Incident ID</span>
                </button>
                <button class="btn-modal-action" id="btn-copy-hash" onclick="copyCurrentAuditHash()">
                    <span>Copy SHA-256 Hash</span>
                </button>
                <button class="btn-modal-action" id="btn-copy-json" onclick="copyCurrentIncidentJSON()">
                    <span>Copy Audit JSON</span>
                </button>
                <button class="btn-modal-action" onclick="closeForensicModal()">Close</button>
            </div>
        </div>
    </div>

    <!-- Toast Notifications -->
    <div id="toast-box"></div>

    <script>
        let currentFilter = 'omnisre-prod-eks';
        let cachedIncidents = [];
        let filteredIncidents = [];
        let displayLimit = 20;
        let wsSocket = null;
        let selectedIncident = null;
        let lastFocusedElement = null;

        // API Key Auth Management
        function getAuthHeaders() {
            const key = sessionStorage.getItem('omnisre_api_key');
            const headers = { 'Content-Type': 'application/json' };
            if (key) {
                headers['X-API-Key'] = key;
                headers['Authorization'] = `Bearer ${key}`;
            }
            return headers;
        }

        function checkAuthStatus() {
            const key = sessionStorage.getItem('omnisre_api_key');
            const btn = document.getElementById('btn-api-key');
            const lbl = document.getElementById('auth-btn-label');
            if (key) {
                if (btn) btn.classList.add('btn-auth-active');
                if (lbl) lbl.innerText = 'Key Set';
            } else {
                if (btn) btn.classList.remove('btn-auth-active');
                if (lbl) lbl.innerText = 'API Key';
            }
        }

        function openAuthModal() {
            const key = sessionStorage.getItem('omnisre_api_key') || '';
            document.getElementById('input-api-key').value = key;
            document.getElementById('auth-modal').classList.add('active');
            setTimeout(() => document.getElementById('input-api-key').focus(), 100);
        }

        function closeAuthModal() {
            document.getElementById('auth-modal').classList.remove('active');
        }

        function saveApiKey() {
            const key = document.getElementById('input-api-key').value.trim();
            if (key) {
                sessionStorage.setItem('omnisre_api_key', key);
                showToast('API Key saved to session');
            } else {
                sessionStorage.removeItem('omnisre_api_key');
                showToast('API Key cleared');
            }
            checkAuthStatus();
            closeAuthModal();
            fetchIncidents();
        }

        function clearApiKey() {
            sessionStorage.removeItem('omnisre_api_key');
            document.getElementById('input-api-key').value = '';
            checkAuthStatus();
            closeAuthModal();
            showToast('API Key removed');
        }

        // WebSocket with Polling Fallback
        function connectWebSocket() {
            try {
                const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${proto}//${location.host}/ws/events`;
                wsSocket = new WebSocket(wsUrl);

                wsSocket.onopen = () => {
                    const st = document.getElementById('ws-status');
                    if (st) st.innerText = 'Real-Time WebSocket (0ms)';
                    const dot = document.getElementById('ws-dot');
                    if (dot) dot.style.background = '#10B981';
                };

                wsSocket.onmessage = (event) => {
                    try {
                        const msg = JSON.parse(event.data);
                        if (msg.type === 'INCIDENT_RESOLVED' || msg.type === 'INCIDENT_RECORDED') {
                            showToast(`Live update: ${msg.data.alert_name} (${msg.data.remediation_executed ? 'Resolved' : 'Pending'})`);
                            fetchIncidents();
                            fetchClusterOverview();
                        } else if (msg.type === 'INCIDENTS_CLEARED') {
                            fetchIncidents();
                            fetchClusterOverview();
                        }
                    } catch (e) {
                        console.debug("WS parse error:", e);
                    }
                };

                wsSocket.onclose = () => {
                    const st = document.getElementById('ws-status');
                    if (st) st.innerText = 'Auto-Polling (5s)';
                    const dot = document.getElementById('ws-dot');
                    if (dot) dot.style.background = '#F59E0B';
                    setTimeout(connectWebSocket, 5000);
                };
            } catch (err) {
                console.error("WebSocket connection error:", err);
            }
        }

        function showToast(msg) {
            const box = document.getElementById('toast-box');
            if (!box) return;
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" style="flex-shrink:0;">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
                <span>${msg}</span>
            `;
            box.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(10px)';
                setTimeout(() => toast.remove(), 300);
            }, 3800);
        }

        // Safe UTC Time Parser and Formatter
        function formatIncidentTime(ts) {
            if (!ts) return 'Just now';
            try {
                // Ensure timestamp with no timezone suffix parses as UTC
                let safeTs = ts;
                if (!safeTs.endsWith('Z') && !safeTs.includes('+') && !safeTs.includes('-')) {
                    safeTs += 'Z';
                }
                const date = new Date(safeTs);
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
                if (diffSec < 60) {
                    rel = `${diffSec}s ago`;
                } else if (diffSec < 3600) {
                    const mins = Math.floor(diffSec / 60);
                    const secs = diffSec % 60;
                    rel = `${mins}m ${String(secs).padStart(2, '0')}s ago`;
                } else {
                    const hrs = Math.floor(diffSec / 3600);
                    const mins = Math.floor((diffSec % 3600) / 60);
                    const secs = diffSec % 60;
                    rel = `${hrs}h ${mins}m ${String(secs).padStart(2, '0')}s ago`;
                }
                
                return `${timeStr} (${rel})`;
            } catch (err) {
                return ts;
            }
        }

        async function fetchClusterOverview() {
            try {
                const res = await fetch('/cluster/overview', { headers: getAuthHeaders() });
                if (!res.ok) {
                    if (res.status === 401) openAuthModal();
                    return;
                }
                const data = await res.json();
                if (data.cluster_name) {
                    document.getElementById('nav-cluster-name').innerText = `Cluster: ${data.cluster_name}`;
                }
                if (data.k8s_version) {
                    document.getElementById('k8s-ver-pill').innerText = data.k8s_version;
                }
                if (data.total_nodes) {
                    const instType = data.nodes && data.nodes[0] ? data.nodes[0].instance_type : 't3.small';
                    document.getElementById('infra-nodes').innerText = `${data.ready_nodes}/${data.total_nodes} Ready (${instType})`;
                }
                if (data.total_pods !== undefined) {
                    const healthyPct = data.total_pods > 0 ? Math.round((data.healthy_pods / data.total_pods) * 100) : 100;
                    document.getElementById('infra-workloads').innerText = `${data.healthy_pods}/${data.total_pods} Healthy (${healthyPct}%)`;
                }

                if (data.nodes && data.nodes.length > 0) {
                    const topoGrid = document.getElementById('topology-grid');
                    let html = `
                    <div class="topo-card">
                        <div class="topo-header">
                            <span class="topo-title">EKS Control Plane</span>
                            <span class="topo-status-tag status-ok">ACTIVE</span>
                        </div>
                        <div class="topo-val">${data.cluster_name}</div>
                        <div class="topo-sub">
                            <span>Provider: ${data.cloud_provider || 'AWS EKS'}</span>
                            <span>Region: ${data.region || 'ap-south-1'}</span>
                        </div>
                    </div>`;

                    data.nodes.forEach((n, idx) => {
                        const isReady = n.status === 'Ready';
                        html += `
                        <div class="topo-card">
                            <div class="topo-header">
                                <span class="topo-title">Worker Node ${idx + 1}</span>
                                <span class="topo-status-tag ${isReady ? 'status-ok' : 'status-err'}">${n.status.toUpperCase()}</span>
                            </div>
                            <div class="topo-val">${n.name}</div>
                            <div class="topo-sub">
                                <span>Type: ${n.instance_type || 't3.small'}</span>
                                <span>IP: ${n.ip || 'Private'}</span>
                            </div>
                        </div>`;
                    });

                    topoGrid.innerHTML = html;
                }
            } catch (err) {
                console.error("Cluster overview fetch error:", err);
            }
        }

        async function clearStream() {
            try {
                const res = await fetch('/incidents', { method: 'DELETE', headers: getAuthHeaders() });
                if (!res.ok) {
                    if (res.status === 401) { openAuthModal(); return; }
                    throw new Error(`HTTP ${res.status}`);
                }
                showToast('Audit stream cleared successfully');
                await fetchIncidents();
            } catch (err) {
                showToast('Error clearing stream: ' + err.message);
            }
        }

        function switchCluster(cluster, el) {
            document.querySelectorAll('.cluster-tab').forEach(t => t.classList.remove('active'));
            el.classList.add('active');
            currentFilter = cluster;
            showToast(`Target Cluster: ${cluster}`);
            fetchIncidents();
        }

        // Filter and Search Handlers
        function handleFilterChange() {
            renderIncidentsList();
        }

        function resetFilters() {
            document.getElementById('filter-search').value = '';
            document.getElementById('filter-severity').value = 'ALL';
            document.getElementById('filter-namespace').value = 'ALL';
            document.getElementById('filter-status').value = 'ALL';
            document.getElementById('filter-sort').value = 'NEWEST';
            renderIncidentsList();
        }

        function updateNamespaceDropdown(incidents) {
            const select = document.getElementById('filter-namespace');
            const currentVal = select.value;
            const namespaces = new Set();
            incidents.forEach(i => { if (i.namespace) namespaces.add(i.namespace); });
            
            let html = '<option value="ALL">All Namespaces</option>';
            namespaces.forEach(ns => {
                html += `<option value="${ns}">${ns}</option>`;
            });
            select.innerHTML = html;
            if (namespaces.has(currentVal)) {
                select.value = currentVal;
            }
        }

        async function fetchIncidents() {
            try {
                const res = await fetch('/incidents', { headers: getAuthHeaders() });
                if (!res.ok) {
                    if (res.status === 401) { openAuthModal(); return; }
                    throw new Error(`HTTP ${res.status}`);
                }
                cachedIncidents = await res.json();
                updateNamespaceDropdown(cachedIncidents);
                renderIncidentsList();
            } catch (err) {
                console.error("Error updating incident stream:", err);
            }
        }

        function renderIncidentsList() {
            const searchTerm = (document.getElementById('filter-search').value || '').toLowerCase().trim();
            const sevFilter = document.getElementById('filter-severity').value;
            const nsFilter = document.getElementById('filter-namespace').value;
            const statusFilter = document.getElementById('filter-status').value;
            const sortVal = document.getElementById('filter-sort').value;

            // 1. Cluster Filter
            let list = cachedIncidents.filter(inc => {
                if (!currentFilter || currentFilter === 'all' || currentFilter === 'omnisre-prod-eks') {
                    return (inc.cluster_name || 'omnisre-prod-eks') === 'omnisre-prod-eks';
                }
                return (inc.cluster_name || '') === currentFilter;
            });

            // 2. Search Filter
            if (searchTerm) {
                list = list.filter(i => 
                    (i.alert_name && i.alert_name.toLowerCase().includes(searchTerm)) ||
                    (i.target_resource && i.target_resource.toLowerCase().includes(searchTerm)) ||
                    (i.namespace && i.namespace.toLowerCase().includes(searchTerm)) ||
                    (i.root_cause && i.root_cause.toLowerCase().includes(searchTerm))
                );
            }

            // 3. Severity Filter
            if (sevFilter !== 'ALL') {
                list = list.filter(i => (i.severity || '').toUpperCase() === sevFilter);
            }

            // 4. Namespace Filter
            if (nsFilter !== 'ALL') {
                list = list.filter(i => i.namespace === nsFilter);
            }

            // 5. Status Filter
            if (statusFilter === 'UNRESOLVED') {
                list = list.filter(i => !i.remediation_executed);
            } else if (statusFilter === 'RESOLVED') {
                list = list.filter(i => i.remediation_executed);
            } else if (statusFilter === 'APPROVAL') {
                list = list.filter(i => !i.remediation_executed && i.approval_token);
            }

            // 6. Sorting
            list.sort((a, b) => {
                if (sortVal === 'NEWEST') {
                    // Unresolved pinned to top unless specified otherwise
                    if (!a.remediation_executed && b.remediation_executed) return -1;
                    if (a.remediation_executed && !b.remediation_executed) return 1;
                    return new Date(b.timestamp) - new Date(a.timestamp);
                } else if (sortVal === 'OLDEST') {
                    return new Date(a.timestamp) - new Date(b.timestamp);
                } else if (sortVal === 'CONFIDENCE') {
                    return (b.confidence_score || 0) - (a.confidence_score || 0);
                }
                return 0;
            });

            filteredIncidents = list;
            document.getElementById('incident-counter-badge').innerText = `${list.length} Incident(s)`;

            const container = document.getElementById('incidents-container');
            const heroBanner = document.getElementById('hero-banner');
            const heroIcon = document.getElementById('hero-icon');
            const heroTitle = document.getElementById('hero-title');
            const heroSub = document.getElementById('hero-sub');
            const heroPill = document.getElementById('hero-status-pill');

            const activeUnresolved = cachedIncidents.filter(i => !i.remediation_executed);

            // Dynamic Hero State
            if (cachedIncidents.length === 0) {
                heroBanner.classList.remove('alert-state');
                heroIcon.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>`;
                heroTitle.innerText = 'CLUSTER HEALTH: 100% OPERATIONAL';
                heroSub.innerHTML = `Connected to AWS EKS cluster <strong>${currentFilter}</strong>. 0 active firing alerts. All nodes and workloads healthy.`;
                heroPill.className = 'hero-badge badge-green';
                heroPill.innerText = '● 0 FIRING ALERTS';
            } else if (activeUnresolved.length > 0) {
                heroBanner.classList.add('alert-state');
                heroIcon.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
                heroTitle.innerText = `CRITICAL ALERT: ${activeUnresolved.length} UNRESOLVED INCIDENT(S)`;
                const unresolvedNames = activeUnresolved.map(u => `<strong>${u.target_resource}</strong> (${u.alert_name})`).join(', ');
                heroSub.innerHTML = `Active failure on: ${unresolvedNames} in cluster <strong>${currentFilter}</strong>. Review triage and execute remediation below.`;
                heroPill.className = 'hero-badge badge-red';
                heroPill.innerText = `● ${activeUnresolved.length} ACTIVE INCIDENT(S)`;
            } else {
                heroBanner.classList.remove('alert-state');
                heroIcon.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="20 6 9 17 4 12"/></svg>`;
                heroTitle.innerText = 'CLUSTER HEALTH: 100% OPERATIONAL (ALL INCIDENTS RESOLVED)';
                heroSub.innerHTML = `All <strong>${cachedIncidents.length} incident(s)</strong> autonomously triaged and healed in AWS EKS cluster <strong>${currentFilter}</strong>. Zero failing workloads. Replacement pods verified passing probes.`;
                heroPill.className = 'hero-badge badge-green';
                heroPill.innerText = `● ALL ${cachedIncidents.length} INCIDENT(S) RESOLVED`;
            }

            if (list.length === 0) {
                container.innerHTML = `
                <div class="empty-card">
                    <div class="empty-icon">
                        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                            <path d="m9 12 2 2 4-4"/>
                        </svg>
                    </div>
                    <h3 style="font-size: 15px; color: var(--text-title); margin-bottom: 6px;">No Matching Incidents</h3>
                    <p style="font-size: 13px;">No incidents matched your search or active filter criteria.</p>
                </div>`;
                document.getElementById('load-more-box').style.display = 'none';
                return;
            }

            const visibleList = list.slice(0, displayLimit);
            const loadMoreBox = document.getElementById('load-more-box');
            if (list.length > displayLimit) {
                loadMoreBox.style.display = 'block';
                document.getElementById('btn-load-more').innerText = `Load More Incidents (${visibleList.length} of ${list.length} shown)`;
            } else {
                loadMoreBox.style.display = 'none';
            }

            container.innerHTML = visibleList.map((inc, idx) => {
                const isCritical = inc.severity === 'CRITICAL';
                const sevClass = isCritical ? 'tag-critical' : 'tag-warning';
                const confPct = Math.round((inc.confidence_score || 0) * 100);
                const formattedDate = formatIncidentTime(inc.timestamp);
                const durationMs = inc.execution_duration_ms !== null && inc.execution_duration_ms !== undefined ? inc.execution_duration_ms + 'ms' : '—';
                const clusterName = inc.cluster_name || 'omnisre-prod-eks';
                const nodeName = inc.node_name || '—';
                const containerName = inc.container_name || '—';
                const auditHashShort = inc.audit_hash ? `sha256:${inc.audit_hash.substring(0, 16)}...` : '—';
                const exitCodeDisp = inc.exit_code !== null && inc.exit_code !== undefined ? `Exit ${inc.exit_code}` : '—';

                return `
                <div class="incident-card ${!inc.remediation_executed ? 'card-unresolved' : ''}">
                    <!-- FAILURE LOCATION BREADCRUMBS -->
                    <div class="error-location-bar">
                        <span class="location-label">📍 FAILURE LOCATION:</span>
                        <span class="loc-crumb">Cluster: <strong class="text-cyan">${clusterName}</strong></span>
                        <span class="loc-sep">➔</span>
                        <span class="loc-crumb">Node: <strong class="text-indigo">${nodeName}</strong></span>
                        <span class="loc-sep">➔</span>
                        <span class="loc-crumb">Namespace: <strong class="text-warning">${inc.namespace}</strong></span>
                        <span class="loc-sep">➔</span>
                        <span class="loc-crumb">Pod: <strong class="text-emerald">${inc.target_resource}</strong></span>
                        <span class="loc-sep">➔</span>
                        <span class="loc-crumb">Container: <strong>${containerName}</strong></span>
                    </div>

                    <!-- RESOLUTION PROOF BANNER -->
                    <div class="resolution-status-banner ${inc.remediation_executed ? 'res-solved' : (inc.remediation_result && inc.remediation_result.startsWith('REJECTED') ? 'res-rejected' : 'res-pending')}">
                        <span style="font-size: 20px; flex-shrink: 0; display: flex;">
                            ${inc.remediation_executed ? `
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                            ` : (inc.remediation_result && inc.remediation_result.startsWith('REJECTED') ? `
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#F43F5E" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
                            ` : `
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                            `)}
                        </span>
                        <div>
                            <div style="font-weight: 800; font-size: 14px; letter-spacing: 0.2px;">
                                ${inc.remediation_executed 
                                    ? 'ISSUE AUTONOMOUSLY RESOLVED & REPLICA HEALTH VERIFIED (' + durationMs + ')' 
                                    : (inc.remediation_result && inc.remediation_result.startsWith('REJECTED') 
                                        ? 'REMEDIATION REJECTED BY HUMAN OPERATOR' 
                                        : 'INCIDENT DETECTED — REMEDIATION PENDING HUMAN APPROVAL / TRIGGER')}
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; opacity: 0.95;">
                                ${inc.remediation_executed 
                                    ? `Action: <strong>${inc.remediation_type}</strong> | ${inc.remediation_result || 'Evicted failing pod and verified healthy replacement replica passing readiness probes.'}`
                                    : (inc.remediation_result || 'Policy requires review before executing self-healing action.')}
                            </div>
                        </div>
                    </div>

                    <div class="incident-header">
                        <div class="incident-title-left">
                            <span class="incident-alert-name">${inc.alert_name}</span>
                            <span class="tag-badge ${sevClass}">SEVERITY: ${inc.severity}</span>
                            <span class="tag-badge tag-healed">
                                <span>${inc.remediation_executed ? 'STATUS: ✔ RESOLVED (' + durationMs + ')' : 'STATUS: ⏳ PENDING'}</span>
                            </span>
                            <span class="tag-badge tag-remedy">REMEDY: ${inc.remediation_type}</span>
                            <span class="tag-badge tag-live-state">
                                LIVE STATE: ${inc.verification_status || '—'}
                            </span>
                        </div>
                        <div class="incident-timestamp">
                            <span class="live-timestamp" data-ts="${inc.timestamp}">${formattedDate}</span> | <span class="code-pill">ID: ${inc.incident_id.substring(0, 8)}</span>
                        </div>
                    </div>

                    <div class="incident-grid">
                        <div>
                            <div class="info-panel">
                                <div class="info-label">
                                    <span>AI Root Cause Diagnosis</span>
                                    <span class="code-pill">Exit Code: ${exitCodeDisp}</span>
                                </div>
                                <p class="info-content">${inc.root_cause}</p>
                                <details style="margin-top: 10px; cursor: pointer;">
                                    <summary style="font-size: 11px; color: #38BDF8; font-weight: 600; font-family: var(--font-mono); outline: none;">
                                        📄 View Raw Error & Terminal Logs ▼
                                    </summary>
                                    <div class="terminal-container" style="max-height: 120px; margin-top: 8px; font-size: 11px; white-space: pre-wrap;">${inc.raw_logs && inc.raw_logs.trim().length > 0 ? inc.raw_logs : 'No container stdout/stderr logs recorded for this event.'}</div>
                                </details>
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
                                    <span>Remediation Plan & Policy</span>
                                    <span style="color: var(--accent-cyan);">${inc.policy_matched || '—'}</span>
                                </div>
                                <p class="info-content" style="color: #34D399; font-size: 12px; font-weight: 500;">
                                    ${inc.remediation_result || inc.recommended_action}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div class="incident-footer-bar">
                        <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                            <button class="btn-inspect" onclick="openForensicModal('${inc.incident_id}', this)">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"/>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                                </svg>
                                <span>Inspect Forensics & Audit</span>
                            </button>

                            ${!inc.remediation_executed && inc.approval_token ? `
                            <button class="btn-action-approve" onclick="handleApprove('${inc.approval_token}', this)">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                                <span>Approve Remediation</span>
                            </button>
                            <button class="btn-action-deny" onclick="handleDeny('${inc.approval_token}', this)">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                                <span>Reject</span>
                            </button>
                            ` : (!inc.remediation_executed ? `
                            <button class="btn-action-approve" onclick="triggerIncidentRemediate('${inc.incident_id}', this)">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                                <span>Execute Autonomous Healing</span>
                            </button>
                            ` : '')}
                        </div>
                        <span class="proof-tag">✔ SOC2 Audit Hash: ${auditHashShort}</span>
                    </div>
                </div>
                `;
            }).join('');
        }

        function loadMoreIncidents() {
            displayLimit += 20;
            renderIncidentsList();
        }

        // Action Handlers
        async function triggerSim(scenario, btnId) {
            const btn = document.getElementById(btnId);
            const originalHTML = btn.innerHTML;
            btn.classList.add('executing');
            btn.innerHTML = `<div class="sim-card-top"><span class="sim-card-title">⚡ Intercepting & Self-Healing...</span></div><p class="sim-card-desc">Triage in progress via OmniSRE Agent...</p>`;

            try {
                const res = await fetch('/simulate', {
                    method: 'POST',
                    headers: getAuthHeaders(),
                    body: JSON.stringify({ scenario: scenario, namespace: 'default' })
                });
                if (!res.ok) {
                    if (res.status === 401) { openAuthModal(); return; }
                    throw new Error(`HTTP ${res.status}`);
                }
                const data = await res.json();
                showToast(`Remediated: ${data.alert_name} in namespace "${data.namespace}"`);
                await fetchIncidents();
                await fetchClusterOverview();
            } catch (err) {
                showToast(`Simulation error: ${err.message}`);
            } finally {
                setTimeout(() => {
                    btn.classList.remove('executing');
                    btn.innerHTML = originalHTML;
                }, 800);
            }
        }

        async function triggerIncidentRemediate(id, btn) {
            if (btn) {
                btn.innerText = 'Healing Replica...';
                btn.style.opacity = '0.7';
            }
            showToast(`Executing self-healing for ${id.substring(0, 8)}...`);
            try {
                const res = await fetch(`/remediate/${id}`, { method: 'POST', headers: getAuthHeaders() });
                if (!res.ok) {
                    if (res.status === 401) { openAuthModal(); return; }
                    throw new Error(`HTTP ${res.status}`);
                }
                const data = await res.json();
                showToast(`✔ Issue Resolved: ${data.remediation_result}`);
                await fetchIncidents();
                await fetchClusterOverview();
            } catch (e) {
                showToast(`Remediation error: ${e.message}`);
            }
        }

        async function handleApprove(token, btn) {
            if (btn) {
                btn.innerText = 'Approving...';
                btn.style.opacity = '0.7';
            }
            try {
                const res = await fetch(`/approval/${token}`, { method: 'POST', headers: getAuthHeaders() });
                if (!res.ok) {
                    if (res.status === 401) { openAuthModal(); return; }
                    throw new Error(`HTTP ${res.status}`);
                }
                const data = await res.json();
                showToast(`✔ Action Approved: ${data.result}`);
                await fetchIncidents();
                await fetchClusterOverview();
            } catch (e) {
                showToast(`Approval error: ${e.message}`);
            }
        }

        async function handleDeny(token, btn) {
            if (btn) {
                btn.innerText = 'Rejecting...';
                btn.style.opacity = '0.7';
            }
            try {
                const res = await fetch(`/approval/${token}/deny`, { method: 'POST', headers: getAuthHeaders() });
                if (!res.ok) {
                    if (res.status === 401) { openAuthModal(); return; }
                    throw new Error(`HTTP ${res.status}`);
                }
                const data = await res.json();
                showToast(`Action Denied: ${data.result}`);
                await fetchIncidents();
                await fetchClusterOverview();
            } catch (e) {
                showToast(`Denial error: ${e.message}`);
            }
        }

        // Forensic Modal with A11y Focus Trap & Copy Buttons
        function openForensicModal(incidentId, triggerEl) {
            lastFocusedElement = triggerEl || document.activeElement;
            const inc = cachedIncidents.find(i => i.incident_id === incidentId);
            if (!inc) return;
            selectedIncident = inc;

            document.getElementById('m-exit-code').innerText = inc.exit_code !== null && inc.exit_code !== undefined ? `Exit ${inc.exit_code}` : '—';
            document.getElementById('m-status').innerText = inc.verification_status || '—';
            document.getElementById('m-policy').innerText = inc.policy_matched || '—';
            document.getElementById('m-duration').innerText = inc.execution_duration_ms ? `${inc.execution_duration_ms} ms` : '—';

            const logsBox = document.getElementById('m-logs');
            logsBox.innerText = inc.raw_logs && inc.raw_logs.trim().length > 0 ? inc.raw_logs : 'No container stdout/stderr logs recorded for this event.';

            const auditBox = document.getElementById('m-audit-proof');
            auditBox.innerText = `API Action: ${inc.remediation_type} -> Target: ${inc.target_resource}
Cluster: ${inc.cluster_name || 'omnisre-prod-eks'} | Node: ${inc.node_name || '—'}
Namespace: ${inc.namespace} | Incident ID: ${inc.incident_id}
Audit Hash: ${inc.audit_hash ? 'sha256:' + inc.audit_hash : '—'}
Result: ${inc.remediation_result || 'Triage completed.'}
Verification: ${inc.verification_status || '—'}
Standard: SOC2 CC7.3 / ISO 27001 Automated Recovery Logged.`;

            const modal = document.getElementById('forensic-modal');
            modal.classList.add('active');
            
            // Focus first focusable element inside modal
            setTimeout(() => {
                const firstBtn = modal.querySelector('button');
                if (firstBtn) firstBtn.focus();
            }, 100);
        }

        function closeForensicModal() {
            const modal = document.getElementById('forensic-modal');
            modal.classList.remove('active');
            selectedIncident = null;
            if (lastFocusedElement) {
                lastFocusedElement.focus();
                lastFocusedElement = null;
            }
        }

        function copyCurrentIncidentId() {
            if (!selectedIncident) return;
            navigator.clipboard.writeText(selectedIncident.incident_id);
            const btn = document.getElementById('btn-copy-id');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span>✔ Copied ID!</span>';
            setTimeout(() => btn.innerHTML = originalText, 1800);
            showToast('Incident ID copied to clipboard');
        }

        function copyCurrentAuditHash() {
            if (!selectedIncident || !selectedIncident.audit_hash) return;
            navigator.clipboard.writeText(selectedIncident.audit_hash);
            const btn = document.getElementById('btn-copy-hash');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span>✔ Copied Hash!</span>';
            setTimeout(() => btn.innerHTML = originalText, 1800);
            showToast('SHA-256 Audit Hash copied to clipboard');
        }

        function copyCurrentIncidentJSON() {
            if (!selectedIncident) return;
            navigator.clipboard.writeText(JSON.stringify(selectedIncident, null, 2));
            const btn = document.getElementById('btn-copy-json');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span>✔ Copied JSON!</span>';
            setTimeout(() => btn.innerHTML = originalText, 1800);
            showToast('Full incident JSON copied to clipboard');
        }

        // Accessibility & Keyboard Listeners
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (document.getElementById('forensic-modal').classList.contains('active')) {
                    closeForensicModal();
                } else if (document.getElementById('auth-modal').classList.contains('active')) {
                    closeAuthModal();
                }
            }
            // Trap focus within active modal
            const activeModal = document.querySelector('.modal-overlay.active');
            if (activeModal && e.key === 'Tab') {
                const focusables = activeModal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
                if (focusables.length === 0) return;
                const first = focusables[0];
                const last = focusables[focusables.length - 1];
                if (e.shiftKey) {
                    if (document.activeElement === first) {
                        last.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === last) {
                        first.focus();
                        e.preventDefault();
                    }
                }
            }
        });

        // 1-Second Dynamic Live Ticker
        function tickTimestamps() {
            document.querySelectorAll('.live-timestamp').forEach(el => {
                const ts = el.getAttribute('data-ts');
                if (ts) el.innerText = formatIncidentTime(ts);
            });
            const clockEl = document.getElementById('live-cluster-clock');
            if (clockEl) {
                const now = new Date();
                clockEl.innerText = now.toTimeString().split(' ')[0] + ' UTC';
            }
        }

        async function handleManualRefresh() {
            const btn = document.getElementById('btn-refresh');
            if (btn) btn.classList.add('rotating');
            await fetchIncidents();
            await fetchClusterOverview();
            tickTimestamps();
            showToast('Stream synchronized with live cluster');
            setTimeout(() => { if (btn) btn.classList.remove('rotating'); }, 600);
        }

        // Initialization
        checkAuthStatus();
        connectWebSocket();
        fetchClusterOverview();
        fetchIncidents();
        tickTimestamps();
        setInterval(tickTimestamps, 1000);
        setInterval(fetchIncidents, 5000);
        setInterval(fetchClusterOverview, 10000);
    </script>
</body>
</html>
"""
