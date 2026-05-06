import streamlit as st

_GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg:           #F7F8FA;
    --card:         #FFFFFF;
    --surface-2:    #F8FAFC;
    --divider:      #F1F5F9;
    --border:       #E5E7EB;
    --border-strong:#CBD5E1;
    --text:         #0F172A;
    --text-2:       #475569;
    --text-3:       #64748B;
    --primary:      #6366F1;
    --primary-2:    #8B5CF6;
    --gradient-ai:  linear-gradient(90deg,#6366F1,#8B5CF6);
    --dark:         #0F172A;
    --info:         #2563EB;  --info-bg:    #EFF6FF;
    --success:      #059669;  --success-bg: #ECFDF5;
    --warn:         #B45309;  --warn-bg:    #FEF3C7;
    --danger:       #DC2626;  --danger-bg:  #FEF2F2;
    --purple:       #7C3AED;  --purple-bg:  #F5F3FF;
    --p0: #B91C1C; --p0-bg: #FEE2E2;
    --p1: #B45309; --p1-bg: #FEF3C7;
    --p2: #1D4ED8; --p2-bg: #EFF6FF;
    --p3: #475569; --p3-bg: #F1F5F9;
    --chart-bar:    #3B82F6;
    --chart-grid:   #E5E7EB;
    --chart-anxiety:#F59E0B;
    --chart-confuse:#3B82F6;
    --chart-expect: #10B981;
    --chart-stress: #EF4444;
    --r-sm:6px; --r:8px; --r-md:10px; --r-lg:12px; --r-pill:999px;
    --shadow-card: 0 1px 2px rgba(15,23,42,.04);
    --font: "PingFang SC","Microsoft YaHei","Inter",system-ui,-apple-system,sans-serif;
}

/* ==================== Page ==================== */
.stApp { background:var(--bg); font-family:var(--font); color:var(--text); }
.block-container { max-width:1200px; padding-top:2rem; padding-bottom:2rem; }

/* ==================== Sidebar ==================== */
section[data-testid="stSidebar"] {
    background: var(--surface-2) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] { display: none; }
/* Fix: sidebar always visible, not collapsible */
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] { display: none !important; }
button[kind="header"] { display: none !important; }
.sidebar-logo {
    font-size:18px; font-weight:700; color:var(--text);
    padding:24px 16px 16px; display:flex; align-items:center; gap:8px;
}
.sidebar-logo::before { content:"🔍"; font-size:22px; }
.sidebar-divider { border:none; border-top:1px solid var(--border); margin:0 16px 16px; }
section[data-testid="stSidebar"] label[data-baseweb="radio"] {
    color:var(--text-2) !important; font-size:14px; font-weight:400;
    padding:10px 16px; border-radius:var(--r); transition:all 0.15s ease;
    margin:2px 0; position:relative;
}
section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
    background:var(--divider); color:var(--text) !important;
}
section[data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"] label {
    background:linear-gradient(90deg, rgba(99,102,241,.08), rgba(139,92,246,.08)) !important;
    color:var(--primary) !important; font-weight:600;
    border-left:3px solid var(--primary);
}
section[data-testid="stSidebar"] .stRadio > div { gap:2px; }
/* Fix: header not covering content */
header[data-testid="stHeader"] {
    position: relative !important;
    background: transparent !important;
}
.block-container {
    padding-top: 2rem !important;
}

/* ==================== Cards ==================== */
.if-card {
    background:var(--card); border:1px solid var(--border);
    border-radius:var(--r-lg); padding:20px; box-shadow:var(--shadow-card);
    transition:transform 0.2s ease, box-shadow 0.2s ease;
}
.if-card:hover {
    transform:translateY(-2px);
    box-shadow:0 6px 16px rgba(15,23,42,.10);
}
.if-section {
    background:#fff; border:1px solid var(--border);
    border-radius:var(--r-lg); padding:24px; margin-bottom:20px;
}
.if-section-title {
    font-size:16px; font-weight:600; color:var(--text); margin-bottom:16px;
}
.if-section-title.danger::before { content:"⊘"; color:var(--danger); margin-right:8px; }

/* ==================== Buttons ==================== */
.stButton > button {
    background:var(--dark); color:#fff; border:none;
    border-radius:var(--r-md); height:40px; padding:0 18px; font-weight:500;
}
.stButton > button:hover { background:#1e293b; }
.stButton > button:focus {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}
.stButton > button:active { background:#0f172a; }
.if-btn-ai {
    display:inline-flex; align-items:center; gap:8px;
    background:var(--gradient-ai); color:#fff !important;
    padding:10px 20px; border-radius:var(--r-md);
    font-weight:600; text-decoration:none;
}
.if-btn-ai:hover { opacity:.92; }
.if-btn-ai:focus {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}
.if-btn-ai:active { opacity:.8; }
.if-btn-secondary {
    display:flex; align-items:center; justify-content:center; gap:8px;
    width:100%; height:38px; background:var(--divider); color:var(--text-2);
    border-radius:var(--r); font-size:14px; font-weight:500; text-decoration:none;
}
.if-btn-secondary:hover { background:var(--border); }
.if-btn-secondary:focus {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}
.if-btn-secondary:active { background:var(--border-strong); }
.if-icon-btn {
    display:inline-flex; align-items:center; justify-content:center;
    width:24px; height:24px; border-radius:6px; color:var(--text-3); cursor:pointer;
}
.if-icon-btn:hover { background:var(--divider); color:var(--text); }
.if-icon-btn:focus {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}
.if-icon-btn:active { background:var(--border); }

/* ==================== Metrics ==================== */
.if-metric { display:flex; justify-content:space-between; align-items:flex-start; }
.if-metric .label { color:var(--text-2); font-size:14px; font-weight:500; }
.if-metric .value { font-size:30px; font-weight:700; margin-top:8px; color:var(--text); font-variant-numeric:tabular-nums; }
.if-metric .unit { font-size:16px; font-weight:400; margin-left:4px; }
.if-metric .icon {
    width:40px; height:40px; border-radius:var(--r-md);
    display:flex; align-items:center; justify-content:center; font-size:20px;
}
.icon.blue { background:var(--info-bg); color:var(--info); }
.icon.red { background:var(--danger-bg); color:var(--danger); }
.icon.green { background:var(--success-bg); color:var(--success); }
.icon.purple { background:var(--purple-bg); color:var(--purple); }

/* ==================== Tags / Pills ==================== */
.if-tag {
    display:inline-block; padding:2px 10px; border-radius:var(--r);
    font-size:12px; font-weight:500;
}
.tag-done { background:var(--success-bg); color:var(--success); }
.tag-running { background:var(--purple-bg); color:var(--purple); }
.tag-info { background:var(--info-bg); color:var(--info); }
.tag-warn { background:var(--danger-bg); color:var(--danger); }
.if-count {
    display:inline-block; padding:2px 10px; border-radius:var(--r-pill);
    background:var(--info-bg); color:#4F46E5; font-size:12px; font-weight:500;
}
.if-pill {
    display:inline-block; padding:4px 12px; border-radius:var(--r-pill);
    background:#EEF2FF; color:#4F46E5; font-size:13px; font-weight:500;
    margin:0 8px 8px 0;
}
.if-pill.sm { padding:4px 12px; font-size:13px; }
.if-pill.md { padding:6px 16px; font-size:15px; font-weight:600; }
.if-pill.lg { padding:8px 20px; font-size:17px; font-weight:600; }
.if-priority {
    display:inline-block; padding:2px 10px; border-radius:var(--r-pill);
    font-size:12px; font-weight:500;
}
.if-priority.p0 { background:var(--p0-bg); color:var(--p0); }
.if-priority.p1 { background:var(--p1-bg); color:var(--p1); }
.if-priority.p2 { background:var(--p2-bg); color:var(--p2); }
.if-priority.p3 { background:var(--p3-bg); color:var(--p3); }

/* ==================== Quote / Opportunity ==================== */
.if-quote {
    background:#EFF4FF; border-left:4px solid var(--primary);
    border-radius:var(--r); padding:12px 14px; color:var(--text-2);
    font-size:14px; margin:12px 0;
}
.if-quote::before { content:"❝ "; color:var(--primary); font-weight:600; }
.if-opp-inline {
    background:var(--success-bg); border-left:4px solid #10B981;
    border-radius:var(--r); padding:12px 14px;
}
.if-opp-inline .t { font-size:12px; font-weight:600; color:#047857; margin-bottom:4px; }
.if-opp-inline .d { font-size:14px; color:#065F46; }
.if-opp {
    border-radius:var(--r-md); padding:16px 18px; margin-bottom:12px;
    border-left:4px solid;
}
.if-opp .t {
    font-size:15px; font-weight:600; margin-bottom:4px;
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
    text-overflow: ellipsis;
}
.if-opp .d { font-size:14px; line-height:1.6; }
.if-opp.green { background:var(--success-bg); border-color:#10B981; }
.if-opp.green .t { color:#047857; } .if-opp.green .d { color:#065F46; }
.if-opp.blue { background:var(--info-bg); border-color:#3B82F6; }
.if-opp.blue .t { color:#1D4ED8; } .if-opp.blue .d { color:#1E3A8A; }
.if-opp.purple { background:var(--purple-bg); border-color:#8B5CF6; }
.if-opp.purple .t { color:#6D28D9; } .if-opp.purple .d { color:#4C1D95; }

/* ==================== Pain card ==================== */
.if-pain {
    border:1px solid var(--border); border-radius:var(--r-lg);
    padding:20px; margin-bottom:16px;
}
.if-pain.embedded { border:none; padding:8px 0 16px; margin-bottom:0; }
.if-pain-head {
    display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;
}
.if-pain-title {
    font-size:15px; font-weight:600;
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
    text-overflow: ellipsis;
}
.if-severity {
    display:inline-flex; align-items:center; gap:6px;
    font-size:12px; color:var(--text-3);
}
.if-severity .dots { display:inline-flex; gap:3px; }
.if-severity .dot {
    width:10px; height:10px; border-radius:var(--r-pill); background:#FEE2E2;
}
.if-severity .dot.on { background:#EF4444; }
.if-severity .score { color:#EF4444; font-weight:500; }

/* ==================== Lists & needs ==================== */
.if-scene {
    background:var(--surface-2); border:1px solid var(--border);
    border-radius:var(--r-md); padding:14px 16px; font-size:14px;
    color:var(--text-2); margin-bottom:12px;
}
.if-need-list { list-style:none; padding:0; margin:0; }
.if-need-list li {
    position:relative; padding-left:16px; margin-bottom:8px;
    font-size:14px; color:var(--text-2); line-height:1.8;
}
.if-need-list li::before {
    content:""; position:absolute; left:0; top:11px;
    width:5px; height:5px; border-radius:var(--r-pill); background:var(--text);
}
.if-need-list.implicit li::before { background:var(--purple); }

/* ==================== Profile ==================== */
.if-profile {
    display:grid; grid-template-columns:1fr 1fr; row-gap:20px; column-gap:32px;
}
.if-profile .k { font-size:13px; font-weight:500; color:var(--text-3); margin-bottom:6px; }
.if-profile .v { font-size:14px; font-weight:500; color:var(--text); }

/* ==================== Emotion ==================== */
.if-emotion-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
.if-emotion { border-radius:var(--r-md); padding:16px; text-align:center; }
.if-emotion .l { font-size:13px; font-weight:500; }
.if-emotion .v { font-size:22px; font-weight:700; margin-top:4px; }
.if-emotion.anxiety { background:var(--warn-bg); color:var(--warn); }
.if-emotion.confused { background:var(--info-bg); color:var(--info); }
.if-emotion.expect { background:var(--success-bg); color:var(--success); }
.if-emotion.stress { background:var(--danger-bg); color:var(--danger); }

/* ==================== Stage bar ==================== */
.if-stage { display:flex; align-items:center; gap:12px; margin-bottom:16px; }
.if-stage .label { width:80px; font-size:14px; font-weight:500; color:var(--text-2); }
.if-stage .track {
    flex:1; height:8px; background:var(--divider);
    border-radius:var(--r-pill); overflow:hidden;
}
.if-stage .fill { height:100%; background:var(--dark); border-radius:var(--r-pill); }
.if-stage .num { width:48px; text-align:right; font-size:13px; font-weight:500; color:var(--text-2); }

/* ==================== Cluster + opportunity list ==================== */
.if-cluster-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.if-cluster {
    border:1px solid var(--border); border-radius:var(--r-lg);
    padding:16px; background:#fff;
}
.if-cluster-head {
    display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;
}
.if-cluster-title {
    font-size:15px; font-weight:600;
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
    text-overflow: ellipsis;
}
.if-opp-item { border-radius:var(--r); padding:12px 14px; margin-bottom:10px; }
.if-opp-item .t { font-size:15px; font-weight:600; }
.if-opp-item .meta { font-size:12px; font-weight:500; margin-top:2px; }
.if-opp-item.p0 { background:var(--p0-bg); }
.if-opp-item.p0 .t { color:var(--p0); } .if-opp-item.p0 .meta { color:#DC2626; }
.if-opp-item.p1 { background:var(--p1-bg); }
.if-opp-item.p1 .t { color:var(--p1); } .if-opp-item.p1 .meta { color:#D97706; }
.if-opp-item.p2 { background:var(--p2-bg); }
.if-opp-item.p2 .t { color:var(--p2); } .if-opp-item.p2 .meta { color:#2563EB; }

/* ==================== Numeric table ==================== */
.if-table-numeric {
    width:100%; border-collapse:separate; border-spacing:0;
    background:#fff; border:1px solid var(--border);
    border-radius:var(--r-lg); overflow:hidden; font-size:14px;
}
.if-table-numeric thead th {
    background:var(--surface-2); color:var(--text-2);
    font-weight:500; font-size:13px; padding:12px 16px;
    text-align:left; border-bottom:1px solid var(--border);
    position: sticky; top:0; z-index:1;
}
.if-table-numeric tbody td {
    padding:0 16px; height:56px;
    border-bottom:1px solid var(--divider);
    font-variant-numeric:tabular-nums;
}
.if-table-numeric tbody tr:last-child td { border-bottom:none; }
.if-table-numeric .num { text-align:right; }
.if-table-numeric .muted { color:var(--text-2); }
.if-table-numeric .center { text-align:center; }
.if-table-numeric thead th:hover { background:var(--border); }
.if-table-numeric tbody tr:hover { background:var(--surface-2); transition:background 0.15s ease; }
.if-table-numeric .sort-indicator {
    font-size:11px; color:var(--primary); margin-left:4px;
}
.if-table-numeric td.truncate {
    max-width:200px; white-space:nowrap; overflow:hidden;
    text-overflow:ellipsis; cursor:help;
}
.if-table-numeric th:nth-child(3),
.if-table-numeric th:nth-child(4),
.if-table-numeric th:nth-child(5),
.if-table-numeric th:nth-child(6),
.if-table-numeric td:nth-child(3),
.if-table-numeric td:nth-child(4),
.if-table-numeric td:nth-child(5),
.if-table-numeric td:nth-child(6) {
    min-width:80px; white-space:nowrap;
}
.if-table-numeric th:nth-child(7),
.if-table-numeric td:nth-child(7) {
    min-width:100px; white-space:nowrap;
}
.if-table-wrapper {
    position:relative; overflow-x:auto; border-radius:var(--r-lg);
    border:1px solid var(--border); background:#fff;
    -webkit-overflow-scrolling:touch;
}
.if-table-wrapper .if-table-numeric {
    border:none; border-radius:0;
}
.if-table-scroll-hint {
    display:none; position:absolute; bottom:8px; left:50%;
    transform:translateX(-50%); padding:4px 12px; background:rgba(0,0,0,.6);
    color:#fff; font-size:11px; border-radius:var(--r-pill); pointer-events:none;
    z-index:2; animation:fadeHint 3s ease forwards;
}
@keyframes fadeHint { 0%,70%{opacity:1} 100%{opacity:0} }
@media (max-width: 1024px) {
    .if-table-scroll-hint { display:block; }
}
.if-table-caption {
    display:flex; justify-content:space-between; align-items:baseline; margin-bottom:12px;
}
.if-table-caption .formula { font-size:13px; color:var(--text-2); font-variant-numeric:tabular-nums; }

/* ==================== Formula ==================== */
.if-formula {
    background:#EFF4FF; border-radius:var(--r-md); padding:16px 20px; margin-top:16px;
}
.if-formula .h { font-size:13px; font-weight:600; color:var(--p2); margin-bottom:8px; }
.if-formula .grid {
    display:grid; grid-template-columns:1fr 1fr; row-gap:8px; column-gap:24px;
}
.if-formula .grid .k { font-size:13px; font-weight:600; color:var(--p2); display:inline; }
.if-formula .grid .v { font-size:13px; color:var(--text-2); display:inline; }

/* ==================== Tip ==================== */
.if-tip {
    background:var(--warn-bg); color:var(--warn);
    border-radius:var(--r-md); padding:12px 14px; font-size:13px; line-height:1.6;
}

/* ==================== Project card ==================== */
.if-project { background:var(--card); border:1px solid var(--border); border-radius:var(--r-lg); padding:20px; }
.if-project-title { font-size:18px; font-weight:600; color:var(--text); margin-bottom:16px; }
.if-project-meta { display:flex; gap:16px; margin-bottom:8px; font-size:14px; color:var(--text-2); }
.if-project-progress { display:flex; align-items:center; justify-content:space-between; margin-bottom:6px; }
.if-project-progress .label { font-size:14px; color:var(--text-2); }
.if-project-progress .pct { font-size:14px; font-weight:600; color:var(--text); }
.if-progress-track {
    width:100%; height:6px; background:var(--divider);
    border-radius:var(--r-pill); overflow:hidden;
}
.if-progress-fill {
    height:100%; background:var(--dark); border-radius:var(--r-pill);
    transition:width 0.3s ease;
}

/* ==================== Standard list table ==================== */
.if-list-table {
    width:100%; border-collapse:separate; border-spacing:0;
    background:#fff; border:1px solid var(--border);
    border-radius:var(--r-lg); overflow:hidden;
}
.if-list-table thead th {
    background:#fff; color:var(--text-2); font-weight:500;
    font-size:13px; padding:12px 16px; text-align:left;
    border-bottom:1px solid var(--border);
}
.if-list-table tbody td {
    padding:0 16px; height:48px; font-size:14px; color:var(--text);
    border-bottom:1px solid var(--divider);
}
.if-list-table tbody tr:last-child td { border-bottom:none; }
.if-list-table tbody tr {
    cursor:pointer; transition:background 0.15s ease;
}
.if-list-table tbody tr:hover { background:var(--surface-2); }

/* ==================== Page header ==================== */
.main-title {
    font-size:22px; font-weight:600; color:var(--text); margin-bottom:4px;
    animation: fadeIn 0.3s ease;
}
.main-subtitle { font-size:15px; color:var(--text-2); margin-bottom:24px; animation: fadeIn 0.3s ease 0.1s both; }
@keyframes fadeIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }

/* ==================== Section ==================== */
.if-section { margin-bottom:20px; }
.if-section-title {
    font-size:16px; font-weight:600; color:var(--text); margin-bottom:12px;
    padding-left:12px; border-left:3px solid var(--primary);
}

/* ==================== Empty state ==================== */
.if-empty { text-align:center; padding:48px 16px; color:var(--text-3); }
.if-empty-icon { font-size:40px; margin-bottom:12px; }
.if-empty-text { font-size:16px; }

.if-onboarding {
    text-align:center; padding:40px 24px; color:var(--text-2);
    background:linear-gradient(135deg, var(--surface-2) 0%, #F5F3FF 100%);
    border-radius:var(--r-lg); border:1px dashed var(--border-strong);
}
.if-onboarding-icon { font-size:44px; margin-bottom:12px; }
.if-onboarding-title { font-size:18px; font-weight:600; color:var(--text); margin-bottom:20px; }
.if-onboarding-steps { display:flex; flex-direction:column; gap:10px; align-items:center; }
.if-onboarding-steps .step {
    display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-2);
}
.if-onboarding-steps .step .num {
    display:inline-flex; align-items:center; justify-content:center;
    width:22px; height:22px; border-radius:50%;
    background:var(--primary); color:#fff; font-size:12px; font-weight:600;
}

/* ==================== TOC + Report ==================== */
.if-toc { list-style:none; padding:0; margin:0; }
.if-toc li {
    padding:10px 14px; border-radius:var(--r);
    font-size:14px; font-weight:500; color:var(--text-2); cursor:pointer;
}
.if-toc li:hover { background:var(--divider); }
.if-toc li.active { background:var(--dark); color:#fff; }
.if-toc li.active .toc-link { color:#fff; }
.if-toc li.sub { font-size:13px; color:var(--text-3); padding-left:30px; font-weight:400; }
.if-toc li.sub:hover { background:var(--surface-2); color:var(--text-2); }
.if-toc .toc-link {
    display:block; text-decoration:none; color:inherit;
    transition:color 0.15s ease;
}
.if-report-preview h2 {
    scroll-margin-top:20px;
}

.if-finding { background:#EFF4FF; border-radius:var(--r-md); padding:14px 16px; }
.if-finding .row {
    display:flex; gap:8px; align-items:flex-start;
    font-size:14px; font-weight:500; color:var(--p2);
    line-height:1.7; margin-bottom:6px;
}
.if-finding .row::before { content:"✓"; color:#3B82F6; font-weight:700; }

.if-mini-cluster { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.if-mini-cluster .item {
    background:#fff; border:1px solid var(--border);
    border-radius:var(--r-md); padding:12px 14px;
}
.if-mini-cluster .item .t { font-size:14px; font-weight:600; }
.if-mini-cluster .item .m { font-size:12px; color:var(--text-3); margin-top:2px; }

.if-report-layout {
    display:grid;
    grid-template-columns:200px minmax(0, 1fr) 240px;
    gap:20px;
    max-width:1280px;
    margin:0 auto;
}
@media (max-width: 1024px) {
    .if-report-layout {
        grid-template-columns: 1fr;
    }
    .if-export-panel {
        position: static;
    }
}
@media (max-width: 1024px) {
    .if-dashboard-grid [data-testid="column"] {
        width: 50% !important;
        min-width: 50% !important;
        flex: 1 1 50% !important;
    }
}
@media (max-width: 768px) {
    [data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
}
.if-report-preview h1 { font-size:22px; font-weight:700; margin-bottom:16px; }
.if-report-preview h2 { font-size:18px; font-weight:700; margin-top:24px; margin-bottom:12px; }
.if-report-preview h3 { font-size:15px; font-weight:600; margin-top:16px; margin-bottom:8px; }
.if-report-preview p,
.if-report-preview li { font-size:14px; color:var(--text-2); line-height:1.7; }
.if-report-preview p { margin-bottom:12px; }
.if-export-panel { position:sticky; top:20px; }
.if-export-panel .group-title {
    font-size:13px; font-weight:500; color:var(--text-2); margin-bottom:6px; margin-top:16px;
}
.if-export-panel .group-title:first-child { margin-top:0; }

.export-option {
    padding:12px; border-radius:var(--r); border:1px solid var(--border);
    margin-bottom:8px; cursor:pointer; transition:all 0.15s ease;
}
.export-option:hover { border-color:var(--primary); background:#F5F3FF; }
.export-option.active {
    border-color:var(--primary); background:#EEEDFF;
}
.export-option .opt-header {
    display:flex; align-items:center; gap:8px; font-size:14px; font-weight:600;
}
.export-option .opt-icon { font-size:16px; }
.export-option .opt-desc {
    font-size:12px; color:var(--text-3); margin-top:4px; padding-left:24px;
}
.export-option.active .opt-desc { color:var(--text-2); }
.export-status {
    margin-top:16px; padding:10px; border-radius:var(--r);
    font-size:13px; text-align:center; display:none;
}
.if-download-section {
    max-width:1280px; margin:0 auto; padding:20px 0;
    background:var(--surface-2); border-radius:var(--r-lg);
    padding:24px; margin-top:20px;
}

/* ==================== Inputs ==================== */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div,
.stDateInput input {
    border-radius:var(--r-md) !important;
    border:1px solid var(--border) !important;
    background:#fff !important;
}

/* ==================== DataFrame skin ==================== */
.stDataFrame { border:1px solid var(--border); border-radius:var(--r-lg); overflow:hidden; }
.stDataFrame thead tr th {
    background:#fff !important; color:var(--text-2) !important;
    font-weight:500 !important; font-size:13px !important;
    border-bottom:1px solid var(--border) !important;
}
.stDataFrame tbody tr td {
    font-size:14px !important; color:var(--text) !important;
    border-bottom:1px solid var(--divider) !important;
}

/* ==================== Divider ==================== */
hr { border:none !important; border-top:1px solid var(--border) !important; margin:16px 0 !important; }

/* ==================== Hide defaults ==================== */
#MainMenu { visibility:hidden; }
footer { visibility:hidden; }
header[data-testid="stHeader"] {
    background:transparent !important;
    height:0 !important;
    min-height:0 !important;
    overflow:visible !important;
    position:relative !important;
}
.toolbar-container { display:none !important; }

/* ==================== StTable override ==================== */
.stTable { border-radius:var(--r-lg) !important; overflow:hidden; border:1px solid var(--border) !important; }
.stTable thead tr th {
    background:var(--surface-2) !important; color:var(--text-2) !important;
    font-weight:500 !important; font-size:13px !important;
    padding:12px 16px !important; border-bottom:1px solid var(--border) !important;
}
.stTable tbody tr td {
    padding:12px 16px !important; font-size:14px !important;
    border-bottom:1px solid var(--divider) !important; height:48px !important;
}
.stTable tbody tr:last-child td { border-bottom:none !important; }
.stTable tbody tr:hover { background:var(--surface-2) !important; }

.if-cta {
    display:flex; align-items:center; justify-content:space-between;
    background:var(--card); border:1px solid var(--border);
    border-radius:var(--r-lg); padding:16px 20px; margin-top:20px;
}
.if-cta .info { display:flex; flex-direction:column; gap:4px; }
.if-cta .info .title { font-size:15px; font-weight:600; color:var(--text); }
.if-cta .info .desc { font-size:13px; color:var(--text-3); }
.if-cta .arrow { font-size:20px; color:var(--primary); }
.if-cta:hover {
    border-color: var(--border-strong);
    box-shadow: 0 2px 8px rgba(15,23,42,.08);
    transition: all 0.15s ease;
}
</style>
"""


def inject_global_css():
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)


def render_sidebar_logo():
    st.markdown(
        '<div class="sidebar-logo">InsightFlow AI</div>'
        '<hr class="sidebar-divider">',
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str | None = None):
    html = f'<div class="main-title">{title}</div>'
    if subtitle:
        html += f'<div class="main-subtitle">{subtitle}</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_kpi_card(label: str, value, unit: str = "", icon: str = "", color: str = "blue"):
    icon_html = f'<div class="icon {color}">{icon}</div>' if icon else ''
    unit_html = f'<span class="unit">{unit}</span>' if unit else ''
    html = (
        f'<div class="if-card if-metric">'
        f'<div>'
        f'<div class="label">{label}</div>'
        f'<div class="value">{value}{unit_html}</div>'
        f'</div>'
        f'{icon_html}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_project_card(name: str, interview_count: int, insight_count: int, updated: str, progress: int):
    bar_width = max(0, min(100, progress))
    html = (
        f'<div class="if-project">'
        f'<div class="if-project-title">{name}</div>'
        f'<div class="if-project-meta">'
        f'<span>📋 {interview_count} 访谈</span>'
        f'<span>💡 {insight_count} 洞察</span>'
        f'<span>🕐 {updated}</span>'
        f'</div>'
        f'<div class="if-project-progress">'
        f'<span class="label">分析进度</span>'
        f'<span class="pct">{progress}%</span>'
        f'</div>'
        f'<div class="if-progress-track">'
        f'<div class="if-progress-fill" style="width:{bar_width}%"></div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_status_badge(status: str):
    cls = "tag-done" if status == "已完成" else "tag-running"
    return f'<span class="if-tag {cls}">{status}</span>'


def render_section_card(title: str, content: str):
    html = (
        f'<div class="if-section">'
        f'<div class="if-section-title">{title}</div>'
        f'<div style="font-size:14px;color:var(--text-2);line-height:1.6">{content}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_tag(text: str, color: str = "info"):
    cls_map = {"blue": "tag-info", "info": "tag-info", "red": "tag-warn", "warn": "tag-warn",
               "green": "tag-done", "done": "tag-done", "purple": "tag-running", "running": "tag-running"}
    cls = cls_map.get(color, "tag-info")
    return f'<span class="if-tag {cls}">{text}</span>'


def render_quote_block(quote: str, source: str | None = None):
    source_html = f'<br><span style="font-size:12px;color:var(--text-3)">— {source}</span>' if source else ''
    return f'<div class="if-quote">「{quote}」{source_html}</div>'


def render_pain_card(pain: str, evidence: str, severity: int, opportunity: str | None = None):
    dots = ''.join(
        '<span class="dot on"></span>' if i < severity else '<span class="dot"></span>'
        for i in range(5)
    )
    opp_html = ''
    if opportunity:
        opp_html = (
            f'<div class="if-opp-inline">'
            f'<div class="t">产品机会点</div>'
            f'<div class="d">{opportunity}</div>'
            f'</div>'
        )
    html = (
        f'<div class="if-pain">'
        f'<div class="if-pain-head">'
        f'<div class="if-pain-title">{pain}</div>'
        f'<div class="if-severity">严重程度 '
        f'<span class="dots">{dots}</span> '
        f'<span class="score">{severity}/5</span>'
        f'</div>'
        f'</div>'
        f'{render_quote_block(evidence, "用户原话")}'
        f'{opp_html}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_priority_badge(priority: str):
    priority = priority.upper()
    return f'<span class="if-priority {priority.lower()}">{priority}</span>'


def render_empty_state(icon: str, text: str):
    html = (
        f'<div class="if-empty">'
        f'<div class="if-empty-icon">{icon}</div>'
        f'<div class="if-empty-text">{text}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_flow_cta(title: str, desc: str, button_label: str, button_key: str):
    container = st.container()
    with container:
        st.markdown(
            f'<div class="if-cta">'
            f'<div class="info">'
            f'<div class="title">{title}</div>'
            f'<div class="desc">{desc}</div>'
            f'</div>'
            f'<div class="arrow">→</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        clicked = st.button(button_label, key=button_key, type="primary", use_container_width=True)
    return clicked
