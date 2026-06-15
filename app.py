import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import time
import random

# ══════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════
st.set_page_config(
    page_title="KRYPTERIS XDR",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛡️"
)

# ══════════════════════════════════════════════════
# GLOBAL CSS — Dark theme matching your HTML UI
# ══════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #080c12 !important;
    color: #e8edf5 !important;
}
.stApp { background-color: #080c12 !important; }
section[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
section[data-testid="stSidebar"] * { color: #a0aab8 !important; }
.block-container { padding: 1.5rem 2rem !important; }

/* Hide default decoration bar but KEEP sidebar collapse button visible */
div[data-testid="stDecoration"] { visibility: hidden; height: 0px; }
iframe[title="streamlitApp"] { margin-top: 0px; }

/* Metric cards */
.krypt-metric {
    background: #111820;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.krypt-metric::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 8px 8px 0 0;
}
.krypt-metric.cyan::before  { background: #00d4ff; }
.krypt-metric.red::before   { background: #ff3b3b; }
.krypt-metric.green::before { background: #00d68f; }
.krypt-metric.amber::before { background: #ffb547; }
.km-label { font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; color: #5a6478; margin-bottom: 8px; }
.km-value { font-size: 28px; font-weight: 300; color: #e8edf5; line-height: 1; margin-bottom: 6px; }
.km-delta { font-size: 11px; font-weight: 600; }
.km-delta.up   { color: #00d68f; }
.km-delta.down { color: #ff3b3b; }
.km-delta.warn { color: #ffb547; }

/* Panel */
.krypt-panel {
    background: #111820;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 16px;
}
.krypt-panel-hdr {
    padding: 12px 18px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.krypt-panel-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #a0aab8;
}
.krypt-panel-body { padding: 16px 18px; }

/* Badges */
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; letter-spacing: 0.05em; }
.badge-red    { background: rgba(255,59,59,.12);  color: #ff3b3b; }
.badge-green  { background: rgba(0,214,143,.1);   color: #00d68f; }
.badge-cyan   { background: rgba(0,212,255,.08);  color: #00d4ff; }
.badge-amber  { background: rgba(255,181,71,.1);  color: #ffb547; }
.badge-purple { background: rgba(155,109,255,.1); color: #9b6dff; }

/* Severity badges */
.sev-critical { background: rgba(255,59,59,.15);  color: #ff3b3b;  padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 700; }
.sev-high     { background: rgba(255,122,61,.12); color: #ff7a3d;  padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 700; }
.sev-medium   { background: rgba(255,181,71,.1);  color: #ffb547;  padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 700; }
.sev-low      { background: rgba(0,214,143,.1);   color: #00d68f;  padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 700; }

/* Alert banners */
.alert-critical { background: rgba(255,59,59,.06); border: 1px solid rgba(255,59,59,.25); border-radius: 6px; padding: 12px 16px; margin-bottom: 14px; font-size: 12px; color: #e8edf5; }
.alert-warning  { background: rgba(255,181,71,.05); border: 1px solid rgba(255,181,71,.2); border-radius: 6px; padding: 12px 16px; margin-bottom: 14px; font-size: 12px; color: #e8edf5; }
.alert-info     { background: rgba(0,212,255,.06); border: 1px solid rgba(0,212,255,.2); border-radius: 6px; padding: 12px 16px; margin-bottom: 14px; font-size: 12px; color: #e8edf5; }

/* Tables */
.krypt-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.krypt-table th { font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; color: #5a6478; padding: 6px 10px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.07); }
.krypt-table td { padding: 9px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #a0aab8; }
.krypt-table tr:last-child td { border-bottom: none; }

/* Code blocks */
.krypt-code { background: #05080d; border: 1px solid rgba(255,255,255,0.07); border-radius: 6px; padding: 16px; font-family: 'SF Mono', 'Fira Code', monospace; font-size: 12px; line-height: 1.7; color: #abb2bf; overflow-x: auto; white-space: pre; }

/* Access deny */
.access-deny { background: rgba(255,59,59,.05); border: 1px solid rgba(255,59,59,.2); border-radius: 8px; padding: 40px; text-align: center; }

/* User rows */
.user-row { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.user-row:last-child { border-bottom: none; }
.u-avatar { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }
.u-name  { font-size: 13px; color: #e8edf5; font-weight: 500; }
.u-email { font-size: 11px; color: #5a6478; }

/* Streamlit widget overrides */
div[data-testid="stSelectbox"] > div { background: #161d28 !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 6px !important; color: #e8edf5 !important; }
div[data-testid="stTextInput"] > div > div { background: #161d28 !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 6px !important; }
div[data-testid="stTextInput"] input { color: #e8edf5 !important; }
.stButton > button { background: #00d4ff !important; color: #000 !important; font-weight: 700 !important; border: none !important; border-radius: 6px !important; font-size: 13px !important; padding: 8px 18px !important; letter-spacing: 0.04em !important; }
.stButton > button:hover { opacity: 0.9 !important; }
div[data-testid="stFileUploader"] { background: #161d28 !important; border: 1px dashed rgba(255,255,255,0.15) !important; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ══════════════════════════════════════════════════
if 'logged_in'     not in st.session_state: st.session_state.logged_in     = False
if 'user_name'     not in st.session_state: st.session_state.user_name     = None
if 'user_role'     not in st.session_state: st.session_state.user_role     = None
if 'user_init'     not in st.session_state: st.session_state.user_init     = None
if 'active_tenant' not in st.session_state: st.session_state.active_tenant = "Acme Corp — Global"
if 'tenants'       not in st.session_state: st.session_state.tenants       = ["Acme Corp — Global","Acme Corp — Azure Cloud","Acme Corp — Endpoint Security","Acme Corp — Dev Environment"]
if 'sim_done'      not in st.session_state: st.session_state.sim_done      = False
if 'prod_done'     not in st.session_state: st.session_state.prod_done     = False

# FIXED: Global state variable backup array prevents structural attribute assignment crashes across panels
if 'sim_df' not in st.session_state:
    cves_base = ["CVE-2026-ZERO", "CVE-2024-3094", "CVE-2023-38545", "None"]
    init_records = []
    for i in range(1250):
        cve_pick = random.choice(cves_base)
        init_records.append({
            "Asset ID": f"TCS-NODE-{10000 + i}",
            "Vulnerability Profile": cve_pick,
            "CVSS Impact": 9.8 if cve_pick == "CVE-2026-ZERO" else (10.0 if cve_pick == "CVE-2024-3094" else 0.0),
            "Calculated Severity": "Critical" if cve_pick == "CVE-2026-ZERO" else "Clear",
        })
    st.session_state.sim_df = pd.DataFrame(init_records)

USERS = {
    "admin":   {"name": "System Admin",    "role": "Administrator", "init": "SA"},
    "analyst": {"name": "SOC Analyst L2",  "role": "Analyst",       "init": "AL"},
    "viewer":  {"name": "Executive Board", "role": "Read-Only",     "init": "EB"},
}

# ══════════════════════════════════════════════════
# LOGIN SCREEN
# ══════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
        <style>
        html, body { margin: 0 !important; padding: 0 !important; background: #080c12 !important; }
        header[data-testid="stHeader"], [data-testid="stToolbar"],
        [data-testid="stDecoration"], footer, #MainMenu { display: none !important; }
        [data-testid="stAppViewContainer"], [data-testid="stMain"],
        [data-testid="stMainBlockContainer"], .block-container {
            background: transparent !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        iframe {
            position: fixed !important;
            top: 0 !important; left: 0 !important;
            width: 100vw !important; height: 100vh !important;
            border: none !important;
            z-index: 0 !important;
            pointer-events: none !important;
        }
        section[data-testid="stMain"] > div {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            min-height: 100vh !important;
        }
        div[data-testid="stVerticalBlock"] {
            position: relative !important;
            z-index: 999 !important;
        }
        div[data-testid="stTextInput"] input {
            background: #161d28 !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 6px !important;
            color: #e8edf5 !important;
            font-size: 13px !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #00d4ff !important;
            box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
        }
        div[data-testid="stTextInput"] label {
            color: #a0aab8 !important;
            font-size: 11px !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
        }
        div[data-testid="stButton"] button {
            background: #00d4ff !important;
            color: #000 !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            letter-spacing: 0.06em !important;
            border: none !important;
            border-radius: 6px !important;
        }
        div[data-testid="stButton"] button:hover { opacity: 0.88 !important; }
        </style>
    """, unsafe_allow_html=True)

    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body, html { background: #080c12; overflow: hidden; width: 100%; height: 100%; }
    canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; }
    </style>
    </head>
    <body>
    <canvas id="matrix"></canvas>
    <script>
    const canvas = document.getElementById("matrix");
    const ctx = canvas.getContext("2d");
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener("resize", resize);
    const letters = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    const fontSize = 13;
    let drops = [];
    function initDrops() {
        drops = Array(Math.floor(canvas.width / fontSize)).fill(0).map(() => Math.floor(Math.random() * -50));
    }
    initDrops();
    window.addEventListener("resize", initDrops);
    function draw() {
        ctx.fillStyle = "rgba(8, 12, 18, 0.055)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.font = fontSize + "px monospace";
        for (let i = 0; i < drops.length; i++) {
            const ch = letters[Math.floor(Math.random() * letters.length)];
            ctx.fillStyle = Math.random() > 0.97 ? "#ffffff" : "rgba(0, 212, 255, 0.7)";
            ctx.fillText(ch, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975)
                drops[i] = Math.floor(Math.random() * -20);
            drops[i]++;
        }
    }
    setInterval(draw, 33);
    </script>
    </body>
    </html>
    """, height=0)

    st.markdown("""
        <div style="text-align:center; margin-bottom:20px; position:relative; z-index:999;">
            <div style="font-size:26px; font-weight:800; letter-spacing:0.14em; color:#e8edf5; font-family:Inter,sans-serif; text-transform:uppercase;">
                KRYPTERIS <span style="color:#00d4ff;">XDR</span>
            </div>
            <div style="font-size:10px; letter-spacing:0.14em; color:#5a6478; text-transform:uppercase; margin-top:6px; font-family:Inter,sans-serif;">
                Autonomous Security Platform · Enterprise Authentication
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        username = st.text_input("Corporate ID", placeholder="username")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        if st.button("Authenticate Securely", use_container_width=True):
            u = username.strip().lower()
            if u in USERS and password == u:
                st.session_state.logged_in = True
                st.session_state.user_name = USERS[u]["name"]
                st.session_state.user_role = USERS[u]["role"]
                st.session_state.user_init = USERS[u]["init"]
                st.rerun()
            else:
                st.error("Invalid credentials. Try: admin/admin · analyst/analyst · viewer/viewer")
        st.markdown('<div style="text-align:center;font-size:11px;color:#5a6478;margin-top:10px">Demo: <code>admin</code> / <code>admin</code></div>', unsafe_allow_html=True)

    st.stop()
    

# ══════════════════════════════════════════════════
# TOP BAR
# ══════════════════════════════════════════════════
components.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
body {{ margin: 0; background-color: #080c12; }}
.topbar {{
    background: #0d1117;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    padding: 0 24px;
    height: 75px;
    display: flex;
    align-items: center;
    gap: 20px;
    font-family: 'Inter', sans-serif;
}}
.tb-logo {{ font-size: 15px; font-weight: 800; letter-spacing: 0.1em; color: #e8edf5; white-space: nowrap; }}
.tb-logo span {{ color: #00d4ff; }}
.tb-div {{ width: 1px; height: 24px; background: rgba(255,255,255,0.07); }}
.tb-spacer {{ flex: 1; }}
.tb-status {{ display: flex; align-items: center; gap: 6px; font-size: 11px; color: #a0aab8; }}
.tb-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #00d68f; animation: pulse 2s ease-in-out infinite; }}
@keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:.4}} }}
.tb-user {{ display: flex; align-items: center; gap: 8px; font-size: 12px; color: #a0aab8; }}
.tb-avatar {{ width: 28px; height: 28px; border-radius: 50%; background: rgba(0,212,255,.12); border: 1px solid #00a8cc; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #00d4ff; }}
.tb-name {{ font-size: 12px; color: #e8edf5; font-weight: 600; text-align: right; }}
.tb-role {{ font-size: 10px; color: #5a6478; text-align: right; }}
</style>
<div class="topbar">
  <div class="tb-logo">KRYPTERIS <span>XDR</span></div>
  <div class="tb-div"></div>
  <div class="tb-status"><div class="tb-dot"></div> Platform Online · All Systems Nominal</div>
  <div class="tb-spacer"></div>
  <div class="tb-user">
    <div>
      <div class="tb-name">{st.session_state.user_name}</div>
      <div class="tb-role">{st.session_state.user_role}</div>
    </div>
    <div class="tb-avatar">{st.session_state.user_init}</div>
  </div>
</div>
""", height=54)

# ══════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 8px;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:#5a6478">Overview</div>
    """, unsafe_allow_html=True)

    nav = st.radio("Navigation", [
        "⬡  Dashboard",
        "⚡  Zero-Day Intel",
        "◉  MITRE ATT&CK",
        "◈  Simulation Hub",
        "◈  Sandbox Twin",
        "⬟  Production Enforce",
        "⬟  Live Enforcement Room",
        "⊞  Integration Gateway",
        "⚙  Platform Settings"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px;color:#5a6478;margin-bottom:8px">
        Active Tenant
    </div>
    """, unsafe_allow_html=True)
    tenant = st.selectbox("Tenant", st.session_state.tenants, label_visibility="collapsed",
                          index=st.session_state.tenants.index(st.session_state.active_tenant))
    if tenant != st.session_state.active_tenant:
        st.session_state.active_tenant = tenant
        st.rerun()

    st.markdown("---")
    if st.button("🚪 Log Out", use_container_width=True):
        for key in ['logged_in','user_name','user_role','user_init','sim_done','prod_done']:
            st.session_state[key] = False if key == 'logged_in' else None
        st.rerun()

    st.markdown("""
    <div style="font-size:10px;color:#5a6478;text-align:center;margin-top:16px">
        Build 2.7.1 · AMD-Accelerated<br>KRYPTERIS XDR Platform
    </div>
    """, unsafe_allow_html=True)

is_admin   = st.session_state.user_role == "Administrator"
is_analyst = st.session_state.user_role in ["Administrator", "Analyst"]

# ══════════════════════════════════════════════════
# HELPER — PLOTLY DARK THEME BASE
# ══════════════════════════════════════════════════
PLOT_LAYOUT = dict(
    paper_bgcolor='#111820', plot_bgcolor='#111820',
    font=dict(color='#a0aab8', family='Inter, sans-serif', size=11),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(showgrid=False, zeroline=False, color='#5a6478'),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', zeroline=False, color='#5a6478'),
)

# ══════════════════════════════════════════════════
# ██████ VIEW: DASHBOARD ██████
# ══════════════════════════════════════════════════
if nav == "⬡  Dashboard":
    st.markdown(f"""
    <div class="krypt-panel-hdr" style="background:#111820;border-radius:8px 8px 0 0;margin-bottom:0;padding:16px 20px 12px">
        <div style="font-size:18px;font-weight:600;color:#e8edf5">Security Operations Center</div>
        <div style="font-size:12px;color:#5a6478;margin-top:2px">Real-time threat intelligence across {st.session_state.active_tenant}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # — Metric Cards —
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="krypt-metric cyan"><div class="km-label">Security Score</div><div class="km-value">92<span style="font-size:18px;color:#5a6478">/100</span></div><div class="km-delta up">↑ 4 pts — Last 7 Days</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="krypt-metric red"><div class="km-label">New Detections</div><div class="km-value">61,102</div><div class="km-delta down">⬤ Action Required</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="krypt-metric green"><div class="km-label">Threats Neutralised</div><div class="km-value">1,158</div><div class="km-delta up">↑ Autonomous Response</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="krypt-metric amber"><div class="km-label">Assets Monitored</div><div class="km-value">8,340</div><div class="km-delta warn">3 Unpatched Critical</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1.6])

    with col_left:
        st.markdown("""
        <div class="krypt-panel">
          <div class="krypt-panel-hdr">
            <span class="krypt-panel-title">🚨 Global Threat Intel</span>
            <span class="badge badge-red">LIVE</span>
          </div>
          <div class="krypt-panel-body">
            <div class="news-item">
              <div><span class="news-cve">CVE-2026-ZERO</span> — Actively exploited. Nginx RCE. No vendor patch.</div>
              <div class="news-meta">CRITICAL · 47 mins ago · Gateway-01, Gateway-02</div>
            </div>
            <div class="news-item">
              <div><span style="color:#ffb547;font-weight:600">CVE-2024-3094</span> — XZ Utils backdoor in 3 containers.</div>
              <div class="news-meta">HIGH · 2 hours ago · Database-EU</div>
            </div>
            <div class="news-item">
              <div><span style="color:#00d4ff;font-weight:600">Intel Feed</span> — Lazarus Group targeting financial sector. T1059.001.</div>
              <div class="news-meta">INFO · 4 hours ago · Nation-State: DPRK</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="krypt-panel">
          <div class="krypt-panel-hdr"><span class="krypt-panel-title">Asset Risk Table</span></div>
          <div class="krypt-panel-body" style="padding:8px 0">
          <table class="krypt-table">
            <thead><tr><th>Asset</th><th>Severity</th><th>CVE</th><th>Status</th></tr></thead>
            <tbody>
              <tr><td>Gateway-01</td><td><span class="sev-critical">CRITICAL</span></td><td>CVE-2026-ZERO</td><td style="color:#ff3b3b">● Unpatched</td></tr>
              <tr><td>Database-EU</td><td><span class="sev-high">HIGH</span></td><td>CVE-2024-3094</td><td style="color:#ffb547">● Mitigated</td></tr>
              <tr><td>HR-Portal</td><td><span class="sev-medium">MEDIUM</span></td><td>CVE-2023-38545</td><td style="color:#00d68f">● Patched</td></tr>
              <tr><td>Auth-Svc</td><td><span class="sev-low">LOW</span></td><td>CVE-2023-1729</td><td style="color:#00d68f">● Patched</td></tr>
            </tbody>
          </table>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="krypt-panel">
          <div class="krypt-panel-hdr"><span class="krypt-panel-title">Incident Timeline</span><span class="badge badge-red">Active</span></div>
          <div class="krypt-panel-body">
            <div class="tl-item"><div class="tl-dot" style="background:#ff3b3b"></div><div class="tl-time">14:22</div><div><div class="tl-title">RCE attempt detected</div><div class="tl-desc">Gateway-01 — CVE-2026-ZERO exploit chain</div></div></div>
            <div class="tl-item"><div class="tl-dot" style="background:#ffb547"></div><div class="tl-time">14:19</div><div><div class="tl-title">Lateral movement blocked</div><div class="tl-desc">Subnet A → Auth Server pivot attempt</div></div></div>
            <div class="tl-item"><div class="tl-dot" style="background:#00d4ff"></div><div class="tl-time">13:58</div><div><div class="tl-title">Honeypot triggered</div><div class="tl-desc">Deception container — 847 requests drained</div></div></div>
            <div class="tl-item"><div class="tl-dot" style="background:#00d68f"></div><div class="tl-time">13:41</div><div><div class="tl-title">Virtual patch deployed</div><div class="tl-desc">Autonomous remediation on Database-EU</div></div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        # — XM Cyber Attack Graph —
        st.markdown("""
        <div class="krypt-panel">
          <div class="krypt-panel-hdr">
            <span class="krypt-panel-title">Cross-Environment Attack Graph</span>
            <span class="badge badge-cyan">Cyber Mode</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        node_x = [0.5, 0.75, 0.90, 0.60, 0.25, 0.10, 0.05, 0.50, 0.95, 0.50]
        node_y = [0.90, 0.70, 0.45, 0.45, 0.55, 0.65, 0.35, 0.20, 0.75, 0.10]
        labels = ["Gateway","Proxy","Database","Auth Svc","Subnet A","Subnet B","Endpoint 1","Endpoint 2","Endpoint 3","Cloud WAN"]
        colors = ["#ff3b3b","#ff7a3d","#ff3b3b","#ffb547","#ffb547","#00d68f","#00d68f","#00d68f","#00d68f","#00d4ff"]

        edges_critical = [(9,0),(0,1),(1,2)]
        edges_normal   = [(0,4),(1,3),(4,5),(4,7),(3,8),(0,6)]

        fig_g = go.Figure()
        for s,t in edges_critical:
            fig_g.add_trace(go.Scatter(x=[node_x[s],node_x[t],None], y=[node_y[s],node_y[t],None],
                mode='lines', line=dict(width=1.5, color='rgba(255,59,59,0.4)'), hoverinfo='none', showlegend=False))
        for s,t in edges_normal:
            fig_g.add_trace(go.Scatter(x=[node_x[s],node_x[t],None], y=[node_y[s],node_y[t],None],
                mode='lines', line=dict(width=1, color='rgba(0,212,255,0.2)'), hoverinfo='none', showlegend=False))
        fig_g.add_trace(go.Scatter(
            x=node_x, y=node_y, mode='markers+text',
            marker=dict(size=14, color=colors, line=dict(width=1.5, color='rgba(255,255,255,0.3)')),
            text=labels, textposition='top center',
            textfont=dict(size=9, color='#5a6478'),
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
        
        GRAPH_LAYOUT = PLOT_LAYOUT.copy()
        GRAPH_LAYOUT.update(dict(
            height=300,
            title=dict(text='Live Threat Path Analysis', font=dict(color='#5a6478', size=11)),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05,1.05]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05,1.05])
        ))
        fig_g.update_layout(**GRAPH_LAYOUT)
        st.plotly_chart(fig_g, use_container_width=True, config={'displayModeBar': False})

        # — Security Score Trend —
        st.markdown("""
        <div class="krypt-panel">
          <div class="krypt-panel-hdr">
            <span class="krypt-panel-title">Security Score — 30 Day Trend</span>
            <span class="badge badge-green">↑ Improving</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        days  = list(range(1, 31))
        score = [74,75,74,76,78,77,80,81,83,81,85,86,84,87,88,87,89,88,88,90,91,89,90,91,92,91,92,91,92,92]
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(x=days, y=score, mode='lines',
            line=dict(color='#00d68f', width=1.5),
            fill='tozeroy', fillcolor='rgba(0,214,143,0.05)'))
            
        TREND_LAYOUT = PLOT_LAYOUT.copy()
        TREND_LAYOUT.update(dict(
            height=160,
            xaxis=dict(showgrid=False, zeroline=False, color='#5a6478', title=''),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', zeroline=False, range=[60,100])
        ))
        fig_t.update_layout(**TREND_LAYOUT)
        st.plotly_chart(fig_t, use_container_width=True, config={'displayModeBar': False})

# ══════════════════════════════════════════════════
# ██████ VIEW: ZERO-DAY INTEL ██████
# ══════════════════════════════════════════════════
elif nav == "⚡  Zero-Day Intel":
    st.markdown('<div style="font-size:18px;font-weight:600;color:#e8edf5;margin-bottom:4px">Zero-Day Intelligence & Autonomous Remediation</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#5a6478;margin-bottom:20px">AI-synthesised mitigation strategies for unpatched vulnerabilities</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-critical">
      <strong>⚠ CRITICAL — No vendor patch available.</strong>
      <span style="color:#ff3b3b;font-weight:700"> CVE-2026-ZERO</span> is actively being exploited in the wild targeting Nginx.
      KRYPTERIS has autonomously generated a virtual patch. Review below and deploy via Production Enforcement.
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="krypt-panel">
          <div class="krypt-panel-hdr"><span class="krypt-panel-title">Autonomous Remediation Path</span><span class="badge badge-cyan">AI-Generated</span></div>
          <div class="krypt-panel-body">
            <div style="display:flex;gap:10px;align-items:flex-start;padding:10px;background:#161d28;border-radius:6px;border:1px solid rgba(255,255,255,0.05);margin-bottom:10px">
              <div style="width:24px;height:24px;border-radius:50%;background:rgba(255,59,59,.12);border:1px solid #ff3b3b;display:flex;align-items:center;justify-content:center;font-size:11px;color:#ff3b3b;font-weight:700;flex-shrink:0">1</div>
              <div><div style="font-size:12px;font-weight:600;color:#e8edf5">Isolate</div><div style="font-size:11px;color:#5a6478;margin-top:2px">Disconnect affected Nginx nodes from WAN load balancer. Quarantine traffic to Gateway-01, Gateway-02.</div></div>
            </div>
            <div style="display:flex;gap:10px;align-items:flex-start;padding:10px;background:#161d28;border-radius:6px;border:1px solid rgba(255,255,255,0.05);margin-bottom:10px">
              <div style="width:24px;height:24px;border-radius:50%;background:rgba(155,109,255,.12);border:1px solid #9b6dff;display:flex;align-items:center;justify-content:center;font-size:11px;color:#9b6dff;font-weight:700;flex-shrink:0">2</div>
              <div><div style="font-size:12px;font-weight:600;color:#e8edf5">Synthesise</div><div style="font-size:11px;color:#5a6478;margin-top:2px">KRYPTERIS Engine generates a custom regex traffic filter using AMD Instinct MI300X hardware-accelerated reasoning.</div></div>
            </div>
            <div style="display:flex;gap:10px;align-items:flex-start;padding:10px;background:#161d28;border-radius:6px;border:1px solid rgba(255,255,255,0.05)">
              <div style="width:24px;height:24px;border-radius:50%;background:rgba(0,214,143,.1);border:1px solid #00d68f;display:flex;align-items:center;justify-content:center;font-size:11px;color:#00d68f;font-weight:700;flex-shrink:0">3</div>
              <div><div style="font-size:12px;font-weight:600;color:#e8edf5">Deploy</div><div style="font-size:11px;color:#5a6478;margin-top:2px">Push virtual patch to production edge. Full audit trail, RBAC enforcement, and automatic rollback on failure.</div></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="krypt-panel" style="margin-top:16px">
          <div class="krypt-panel-hdr"><span class="krypt-panel-title">CVE Intelligence Feed</span></div>
          <div class="krypt-panel-body" style="padding:8px 0">
          <table class="krypt-table">
            <thead><tr><th>CVE</th><th>CVSS</th><th>Affected</th><th>Status</th><th>MITRE</th></tr></thead>
            <tbody>
              <tr><td><span class="news-cve">CVE-2026-ZERO</span></td><td>9.8</td><td>Nginx &lt;1.25.3</td><td><span class="sev-critical">UNPATCHED</span></td><td>T1190</td></tr>
              <tr><td>CVE-2024-3094</td><td>10.0</td><td>XZ Utils</td><td><span class="sev-high">MITIGATED</span></td><td>T1554</td></tr>
              <tr><td>CVE-2023-38545</td><td>7.5</td><td>cURL &lt;8.4</td><td><span class="sev-medium">PATCHED</span></td><td>T1071</td></tr>
            </tbody>
          </table>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="krypt-panel">
          <div class="krypt-panel-hdr"><span class="krypt-panel-title">AI-Generated Virtual Patch</span><span class="badge badge-amber">Nginx Config</span></div>
          <div class="krypt-panel-body">
        """, unsafe_allow_html=True)
        st.code("""# ─────────────────────────────────────────────────
# KRYPTERIS XDR — Autonomous Virtual Patch
# CVE-2026-ZERO | Generated: 2026-06-14 14:22 UTC
# AMD Instinct MI300X | Confidence: 98.4%
# ─────────────────────────────────────────────────

server {
    listen 80;
    server_name gateway.internal;

    # KRYPTERIS: Block known exploit path patterns
    location ~* /(exploit_path|admin_bypass|\\.env|config\\.bak) {
        deny all;
        return 403;
        error_log /var/log/nginx/krypteris_block.log crit;
    }

    # KRYPTERIS: Block path traversal in headers
    if ($http_x_forwarded_for ~* "(\\.\\./|%2e%2e)") {
        return 444;
    }

    # KRYPTERIS: Rate-limit anomalous source IPs
    limit_req_zone $binary_remote_addr zone=krypt_rl:10m rate=5r/s;
    limit_req zone=krypt_rl burst=10 nodelay;
}""", language="nginx")
        st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# ██████ VIEW: MITRE ATT&CK ██████
# ══════════════════════════════════════════════════
elif nav == "◉  MITRE ATT&CK":
    st.markdown('<div style="font-size:18px;font-weight:600;color:#e8edf5;margin-bottom:4px">MITRE ATT&CK Coverage Matrix</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:12px;color:#5a6478;margin-bottom:20px">Active detections mapped to ATT&CK framework — {st.session_state.active_tenant}</div>', unsafe_allow_html=True)

    tactics = ['Recon','Resource Dev','Initial Access','Execution','Persistence',
               'Priv Esc','Defense Evasion','Cred Access','Discovery','Lateral Move','Exfiltration']
    techniques = [
        ['T1595','T1583','T1190','T1059','T1543','T1548','T1562','T1110','T1082','T1021','T1041'],
        ['T1592','T1587','T1566','T1203','T1078','T1134','T1070','T1003','T1083','T1550','T1048'],
        ['T1589','T1586','T1133','T1106','T1053','T1055','T1027','T1056','T1087','T1080','T1052'],
        ['T1590','T1584','T1199','T1129','T1505','T1484','T1036','T1558','T1069','T1072','T1030'],
    ]
    hits    = {'T1190','T1059','T1021'}
    mitigated = {'T1566','T1082','T1003'}
    covered = {'T1078','T1548','T1562'}

    # Re-engineered using explicit inline styles to guarantee horizontal matrix compilation bounds
    hdr_html = ''.join(f'<div style="background:#161d28; padding:8px 4px; text-align:center; color:#5a6478; font-weight:700; font-size:9px; text-transform:uppercase; letter-spacing:0.04em; border-radius:3px; overflow:hidden; white-space:nowrap;">{t}</div>' for t in tactics)
    
    rows_html = ''
    for row in techniques:
        for code in row:
            # Inline conditional coloring rules to bypass internal CSS block compression overrides
            cell_style = "background:#161d28; padding:8px 2px; border-radius:3px; text-align:center; font-size:10px; font-weight:500; font-family:monospace; border:1px solid transparent; color:#5a6478;"
            if code in hits:
                cell_style = "background:rgba(255,59,59,0.15); border:1px solid rgba(255,59,59,0.4); color:#ff3b3b; padding:8px 2px; border-radius:3px; text-align:center; font-size:10px; font-weight:700; font-family:monospace;"
            elif code in mitigated:
                cell_style = "background:rgba(255,181,71,0.12); border:1px solid rgba(255,181,71,0.3); color:#ffb547; padding:8px 2px; border-radius:3px; text-align:center; font-size:10px; font-weight:700; font-family:monospace;"
            elif code in covered:
                cell_style = "background:rgba(0,212,255,0.1); border:1px solid rgba(0,212,255,0.3); color:#00d4ff; padding:8px 2px; border-radius:3px; text-align:center; font-size:10px; font-weight:700; font-family:monospace;"
                
            rows_html += f'<div style="{cell_style}">{code}</div>'

    st.markdown(f"""
    <div class="krypt-panel">
      <div class="krypt-panel-hdr">
        <span class="krypt-panel-title">ATT&CK Technique Heatmap</span>
        <span class="badge badge-red">3 Active Detections</span>
      </div>
      <div class="krypt-panel-body" style="overflow-x: auto; padding: 20px;">
        <div style="display: grid; grid-template-columns: repeat(11, 1fr); gap: 6px; min-width: 900px;">
            {hdr_html}
            {rows_html}
        </div>
        <div style="margin-top:20px; display:flex; gap:24px; font-size:11px; color:#5a6478; font-weight:500;">
          <span><span style="display:inline-block; width:12px; height:12px; background:rgba(255,59,59,0.15); border:1px solid #ff3b3b; border-radius:2px; margin-right:6px; vertical-align:middle;"></span>Active Detection (Exploited)</span>
          <span><span style="display:inline-block; width:12px; height:12px; background:rgba(255,181,71,0.12); border:1px solid #ffb547; border-radius:2px; margin-right:6px; vertical-align:middle;"></span>Mitigated via Shield Rules</span>
          <span><span style="display:inline-block; width:12px; height:12px; background:rgba(0,212,255,0.1); border:1px solid #00d4ff; border-radius:2px; margin-right:6px; vertical-align:middle;"></span>Monitored Policy Coverage</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# ██████ VIEW: SIMULATION HUB ██████
# ══════════════════════════════════════════════════
elif nav == "◈  Simulation Hub":
    st.markdown('<div style="font-size:18px;font-weight:600;color:#e8edf5;margin-bottom:4px">Simulation Hub — Sandbox Engine</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#5a6478;margin-bottom:20px">Upload telemetry datasets and execute simulated virtual patching models. Zero production impact.</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="krypt-panel"><div class="krypt-panel-hdr"><span class="krypt-panel-title">Simulation Configuration</span></div><div class="krypt-panel-body">', unsafe_allow_html=True)
        
        uploaded_telemetry = st.file_uploader("Upload Telemetry (CSV / XLSX / JSON)", type=['csv','xlsx','json'])
        
        if uploaded_telemetry is not None:
            try:
                if uploaded_telemetry.name.endswith('.csv'):
                    raw_inbound = pd.read_csv(uploaded_telemetry)
                elif uploaded_telemetry.name.endswith('.xlsx'):
                    raw_inbound = pd.read_excel(uploaded_telemetry)
                else:
                    raw_inbound = pd.read_json(uploaded_telemetry)
                
                rename_map = {}
                for col in raw_inbound.columns:
                    if "Asset" in col: rename_map[col] = "Asset ID"
                    if "Vulnerability" in col or "Profile" in col: rename_map[col] = "Vulnerability Profile"
                    if "CVSS" in col: rename_map[col] = "CVSS Impact"
                    if "Severity" in col: rename_map[col] = "Calculated Severity"
                
                st.session_state.sim_df = raw_inbound.rename(columns=rename_map)
                st.success(f"Telemetry synchronized seamlessly. {len(st.session_state.sim_df)} nodes ingested.")
            except Exception as e:
                st.error(f"Ingest parse variance: {e}")
                
        sim_mode = st.selectbox("Simulation Mode", [
            "Full Attack Surface Simulation",
            "Patch Generation Only",
            "Lateral Movement Analysis",
            "APT Attribution Mode"
        ])
        sim_target = st.selectbox("Target Asset Group", [
            "All Assets","Critical Infrastructure Only","Cloud Workloads","Endpoints"
        ])
        run_sim = st.button("⬟  Initialise Sandbox Simulation", use_container_width=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div class="krypt-panel">
          <div class="krypt-panel-hdr">
             <span class="krypt-panel-title">Ingested Ingress Asset Inventory Sheet</span>
             <span class="badge badge-cyan">Scrollable Data Matrix</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="max-height: 280px; overflow-y: auto; border: 1px solid rgba(255,255,255,0.07); border-radius: 6px; padding: 1px;">', unsafe_allow_html=True)
        
        display_df = st.session_state.sim_df[["Asset ID", "Vulnerability Profile", "CVSS Impact", "Calculated Severity"]].copy()
        display_df.columns = ["Asset ID", "Vulnerability Profile", "CVSS Impact", "Severity Index"]
        
        st.dataframe(
            display_df, 
            use_container_width=True, 
            hide_index=True,
            height=276
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if run_sim:
            st.session_state.sim_done = True
            st.toast("⚡ Simulation loop initiated! Access Sandbox Twin side menu to review dynamic data matrices.", icon="⚙️")

# ══════════════════════════════════════════════════
# ██████ VIEW: SANDBOX TWIN ██████
# ══════════════════════════════════════════════════
elif nav == "◈  Sandbox Twin":
    st.markdown('<div style="font-size:18px;font-weight:600;color:#e8edf5;margin-bottom:4px">Sandbox Twin — Backend Evidence Lab</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#5a6478;margin-bottom:20px">Live tracking engine metrics modeling autonomous patch lifecycle states across environment models.</div>', unsafe_allow_html=True)

    if not st.session_state.sim_done:
        st.markdown("""
        <div class="access-deny" style="padding:60px 40px;">
          <div style="font-size:42px;margin-bottom:16px">🧪</div>
          <div style="color:#ffb547;font-size:15px;font-weight:600;margin-bottom:8px">Lab Telemetry Idle</div>
          <div style="color:#5a6478;font-size:12px">No active data pipelines are currently processing.<br>Go to the <strong>Simulation Hub</strong> tab and trigger the initialization button.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        total_assets = len(st.session_state.sim_df)
        critical_count = len(st.session_state.sim_df[st.session_state.sim_df["Calculated Severity"] == "Critical"])
        
        st.markdown("#### Live Progress Mitigation Orchestration Tracker")
        
        p1, p2, p3, p4 = st.columns(4)
        m_affected = p1.empty()
        m_process = p2.empty()
        m_remediated = p3.empty()
        m_pending = p4.empty()
        
        st.markdown("<br><b>Detailed Security Orchestration Loop Evidence Trail:</b>", unsafe_allow_html=True)
        evidence_placeholder = st.empty()
        
        running_evidence_log = ""
        current_time = time.strftime("%H:%M:%S")
        
        steps = [
            f"[{current_time}] [STAGE 1] [INITIALIZATION] Ingesting {total_assets} network architecture nodes into isolated virtual sandbox environment container...",
            f"[{current_time}] [STAGE 1] [TELEMETRY] Mapping operational topology; identifying active asset clusters and lateral exposure corridors.",
            f"[{current_time}] [STAGE 2] [RISK METRICS] Scanning framework vulnerabilities. Found {critical_count} unpatched critical exposures mapping to T1190 exploits.",
            f"[{current_time}] [STAGE 2] [GRAPH ANALYSIS] XM Cyber intelligence vector mapping initiated. Scanning perimeter choke points for active risk mitigation paths...",
            f"[{current_time}] [STAGE 3] [REASONING] Activating local Krypteris Contextual Reasoning Core powered by dedicated AMD Instinct acceleration layer...",
            f"[{current_time}] [STAGE 3] [AI SYNTHESIS] Generating defensive scripts. Local context compiled down to targeted hardware register instructions successfully.",
            f"[{current_time}] [STAGE 4] [PATCH VERIFICATION] Simulating automated deployment of custom virtual regex configuration rule blocks across digital twin gateway proxies...",
            f"[{current_time}] [STAGE 4] [COLLATERAL CHECK] Validating payload stability metrics: 0% disruption detected. Network baseline performance parameters nominal.",
            f"[{current_time}] [STAGE 5] [COMPLIANCE] Closing feedback mitigation loop. Generating detailed cryptographic remediation event trail log entries..."
        ]
        
        for tick in range(1, 10):
            progress_ratio = tick / 9.0
            processed_assets = int(progress_ratio * total_assets)
            remediated_assets = int(progress_ratio * critical_count) if critical_count > 0 else processed_assets
            pending_assets = total_assets - processed_assets
            in_process = int(total_assets * 0.12) if tick < 9 else 0
            
            m_affected.markdown(f'<div class="krypt-metric red"><div class="km-label">Total Node Assets</div><div class="km-value">{total_assets}</div><div class="km-delta down">⬤ Inbound Data Matrix</div></div>', unsafe_allow_html=True)
            m_process.markdown(f'<div class="krypt-metric amber"><div class="km-label">In-Process Remediating</div><div class="km-value">{in_process}</div><div class="km-delta warn">⏳ Calibrating Signatures</div></div>', unsafe_allow_html=True)
            m_remediated.markdown(f'<div class="krypt-metric green"><div class="km-label">Remediated Successfully</div><div class="km-value">{remediated_assets}</div><div class="km-delta up">↑ Hardened Target States</div></div>', unsafe_allow_html=True)
            m_pending.markdown(f'<div class="krypt-metric cyan"><div class="km-label">Pending Pipeline Queue</div><div class="km-value">{pending_assets}</div><div class="km-delta up">↓ In Processing Sequence</div></div>', unsafe_allow_html=True)
            
            running_evidence_log += f'<span style="color:#00d4ff">{steps[tick-1]}</span><br>'
            if tick == 9:
                running_evidence_log += f'<span style="color:#00d68f; font-weight:600;"><br>✔ SUCCESS: [Krypteris Autonomous Remediation Engine] validated all {total_assets} records. 100% security baseline posture compliance map complete.</span><br>'
                
            evidence_placeholder.markdown(f'<div class="krypt-code" style="height:280px; overflow-y:auto; font-size:11px; line-height:1.6;">{running_evidence_log}</div>', unsafe_allow_html=True)
            time.sleep(0.5)

# ══════════════════════════════════════════════════
# ██████ VIEW: PRODUCTION ENFORCEMENT ██████
# ══════════════════════════════════════════════════
elif nav == "⬟  Production Enforce":
    st.markdown('<div style="font-size:18px;font-weight:600;color:#e8edf5;margin-bottom:4px">Production Enforcement</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#5a6478;margin-bottom:20px">Live autonomous remediation deployment. Administrator access required.</div>', unsafe_allow_html=True)

    if not is_admin:
        st.markdown(f"""
        <div class="access-deny">
          <div style="font-size:32px;margin-bottom:12px">🔒</div>
          <div style="color:#ff3b3b;font-size:16px;font-weight:600;margin-bottom:8px">Access Restricted</div>
          <div style="color:#5a6478;font-size:12px">You are logged in as <strong style="color:#a0aab8">{st.session_state.user_role}</strong>.<br>Only Administrators can deploy live infrastructure changes.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-warning">
          <strong>⚠ LIVE PRODUCTION MODE.</strong> Actions here modify active routing tables, firewall rules, and configurations in real time.
          Always validate in Simulation Hub before deploying.
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="krypt-panel"><div class="krypt-panel-hdr"><span class="krypt-panel-title">Deployment Package</span></div><div class="krypt-panel-body">', unsafe_allow_html=True)
            st.file_uploader("Upload Approved Deployment Matrix (CSV / XLSX)", type=['csv','xlsx'], key="prod_uploader")
            st.selectbox("Target Environment", ["Production — All Gateways","Production — Gateway-01 Only","Staging — Pre-validation"])
            st.selectbox("Rollback Policy", ["Auto-rollback on failure (Recommended)","Manual rollback only"])
            confirm = st.checkbox("I confirm this deployment has been validated in Simulation Hub")
            run_prod = st.button("⬟  Execute Autonomous Remediation", use_container_width=True, disabled=not confirm)
            st.markdown("</div></div>", unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            <div class="krypt-panel">
              <div class="krypt-panel-hdr">
                 <span class="krypt-panel-title">Active Production Target Inventory Scope</span>
                 <span class="badge badge-amber">Enforcement Scope</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div style="max-height: 280px; overflow-y: auto; border: 1px solid rgba(255,255,255,0.07); border-radius: 6px; padding: 1px;">', unsafe_allow_html=True)
            
            display_prod_df = st.session_state.sim_df[["Asset ID", "Vulnerability Profile", "CVSS Impact", "Calculated Severity"]].copy()
            display_prod_df.columns = ["Asset ID", "Target Profile", "CVSS Impact", "Risk Severity"]
            
            st.dataframe(
                display_prod_df, 
                use_container_width=True, 
                hide_index=True,
                height=276
            )
            st.markdown('</div>', unsafe_allow_html=True)

            if run_prod:
                st.session_state.prod_done = True
                st.toast("🚀 Live Infrastructure Enforcement Action Sent! Access the Live Enforcement Room menu immediately.", icon="🛡️")

# ══════════════════════════════════════════════════
# ██████ VIEW: LIVE ENFORCEMENT ROOM ██████
# ══════════════════════════════════════════════════
elif nav == "⬟  Live Enforcement Room":
    st.markdown('<div style="font-size:18px;font-weight:600;color:#e8edf5;margin-bottom:4px">Live Enforcement Room — Infrastructure Control Loop</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#5a6478;margin-bottom:20px">Real-time infrastructure hardening logs and deployment verification statuses.</div>', unsafe_allow_html=True)

    if not st.session_state.prod_done:
        st.markdown("""
        <div class="access-deny" style="padding:60px 40px; border-color: rgba(255,59,59,0.15)">
          <div style="font-size:42px;margin-bottom:16px">📡</div>
          <div style="color:#ff3b3b;font-size:15px;font-weight:600;margin-bottom:8px">Enforcement Pipeline Standby</div>
          <div style="color:#5a6478;font-size:12px">No production deployment packages have been executed yet.<br>Go to the <strong>Production Enforce</strong> tab and trigger the execution command.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        total_prod_assets = len(st.session_state.sim_df)
        critical_prod_count = len(st.session_state.sim_df[st.session_state.sim_df["Calculated Severity"] == "Critical"])
        
        st.markdown("#### Live Production Fleet Deployment Posture")
        
        e1, e2, e3, e4 = st.columns(4)
        p_total = e1.empty()
        p_active = e2.empty()
        p_secured = e3.empty()
        p_compliance = e4.empty()
        
        st.markdown("<br><b>Cryptographically Audited Live Deployment Event Trail:</b>", unsafe_allow_html=True)
        prod_log_placeholder = st.empty()
        
        running_prod_log = ""
        current_time = time.strftime("%H:%M:%S")
        
        prod_steps = [
            f"[{current_time}] [CONNECT] Opening TLS 1.3 cryptographic session tunnels to live environment clusters...",
            f"[{current_time}] [AUDIT] Registered hardware-backed administrator deployment token signature...",
            f"[{current_time}] [PRE-FLIGHT] Verifying structural checksums for candidate virtual configuration filters...",
            f"[{current_time}] [ENFORCE] Deploying dynamic rulesets to edge proxies. Hardening {critical_prod_count} exposed cluster endpoints...",
            f"[{current_time}] [HOT-RELOAD] Executing zero-downtime hot config reloads on active server clusters safely...",
            f"[{current_time}] [INTEGRITY CHECK] Verification pipeline routing safe trial traffic packets through updated nodes...",
            f"[{current_time}] [SUCCESS] 0% variance anomaly scores returned. Live traffic routes confirmed nominal."
        ]
        
        for tick in range(1, 8):
            ratio = tick / 7.0
            p_secured_val = int(ratio * total_prod_assets)
            p_pending_val = total_prod_assets - p_secured_val
            p_active_val = int(total_prod_assets * 0.08) if tick < 7 else 0
            compliance_percentage = int(ratio * 100)
            
            p_total.markdown(f'<div class="krypt-metric cyan"><div class="km-label">Active Prod Scope</div><div class="km-value">{total_prod_assets}</div><div class="km-delta up">● Network Targets Online</div></div>', unsafe_allow_html=True)
            p_active.markdown(f'<div class="krypt-metric amber"><div class="km-label">Active Hot Deployments</div><div class="km-value">{p_active_val}</div><div class="km-delta warn">⚡ Injecting Rules</div></div>', unsafe_allow_html=True)
            p_secured.markdown(f'<div class="krypt-metric green"><div class="km-label">Nodes Fully Hardened</div><div class="km-value">{p_secured_val}</div><div class="km-delta up">✔ Verification Integrity Safe</div></div>', unsafe_allow_html=True)
            p_compliance.markdown(f'<div class="krypt-metric cyan"><div class="km-label">Fleet Compliance Level</div><div class="km-value">{compliance_percentage}%</div><div class="km-delta up">↑ Standard Baseline Attained</div></div>', unsafe_allow_html=True)
            
            running_prod_log += f'<span style="color:#00d4ff">{prod_steps[tick-1]}</span><br>'
            if tick == 7:
                running_prod_log += f'<span style="color:#00d68f; font-weight:600;"><br>✔ PLATFORM INFRASTRUCTURE STATUS RESOLVED: Krypteris Core has updated production architecture. Audit log successfully committed.</span><br>'
                
            prod_log_placeholder.markdown(f'<div class="krypt-code" style="height:280px; overflow-y:auto; font-size:11px; line-height:1.6;">{running_prod_log}</div>', unsafe_allow_html=True)
            time.sleep(0.4)

# ══════════════════════════════════════════════════
# ██████ VIEW: INTEGRATION GATEWAY ██████
# ══════════════════════════════════════════════════
elif nav == "⊞  Integration Gateway":
    st.markdown('<div style="font-size:18px;font-weight:600;color:#e8edf5;margin-bottom:4px">Integration Gateway</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:12px;color:#5a6478;margin-bottom:20px">Connect external EDR, SIEM, and VA tools to pipe data into {st.session_state.active_tenant}.</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="krypt-panel">
          <div class="krypt-panel-hdr"><span class="krypt-panel-title">Connected Platforms</span></div>
          <div class="krypt-panel-body">
            <div class="int-card"><div class="int-logo" style="background:rgba(255,0,0,.08)">🦅</div><div style="flex:1"><div class="int-name">CrowdStrike Falcon</div><div class="int-desc">EDR Telemetry — Active · 12K events/sec</div></div><span class="badge badge-green">LIVE</span></div>
            <div class="int-card"><div class="int-logo" style="background:rgba(0,120,255,.08)">🔍</div><div style="flex:1"><div class="int-name">Qualys VMDR</div><div class="int-desc">Vulnerability Scanning — Active</div></div><span class="badge badge-green">LIVE</span></div>
            <div class="int-card"><div class="int-logo" style="background:rgba(255,150,0,.08)">🌐</div><div style="flex:1"><div class="int-name">Splunk SIEM</div><div class="int-desc">Log Ingestion — 14K eps</div></div><span class="badge badge-cyan">ACTIVE</span></div>
            <div class="int-card"><div class="int-logo" style="background:rgba(100,255,100,.08)">📡</div><div style="flex:1"><div class="int-name">Palo Alto Cortex XDR</div><div class="int-desc">Setup pending — API key required</div></div><span class="badge badge-amber">SETUP</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="krypt-panel"><div class="krypt-panel-hdr"><span class="krypt-panel-title">Webhook Endpoint</span></div><div class="krypt-panel-body">', unsafe_allow_html=True)
        st.code(f"""POST https://api.krypteris.io/v1/ingress
X-Tenant-ID: acme-corp-global
X-Auth-Token: Bearer KRYPT_[REDACTED]
Content-Type: application/json""", language="http")
        st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown('<div class="krypt-panel" style="margin-top:14px"><div class="krypt-panel-hdr"><span class="krypt-panel-title">Python Forwarder SDK</span></div><div class="krypt-panel-body">', unsafe_allow_html=True)
        st.code("""import requests

def forward_telemetry(payload: dict) -> int:
    endpoint = "https://api.krypteris.io/v1/ingress"
    headers = {
        "Authorization": "Bearer KRYPT_TOKEN",
        "X-Tenant-ID":   "acme-corp-global",
        "X-Source":      "crowdstrike-falcon"
    }
    r = requests.post(endpoint, json=payload, headers=headers)
    return r.status_code""", language="python")
        st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# ██████ VIEW: PLATFORM SETTINGS ██████
# ══════════════════════════════════════════════════
elif nav == "⚙  Platform Settings":
    st.markdown('<div style="font-size:18px;font-weight:600;color:#e8edf5;margin-bottom:4px">Platform Administration</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#5a6478;margin-bottom:20px">Multi-tenant configuration and user management.</div>', unsafe_allow_html=True)

    if not is_admin:
        st.markdown(f"""
        <div class="access-deny">
          <div style="font-size:32px;margin-bottom:12px">🔒</div>
          <div style="color:#ff3b3b;font-size:16px;font-weight:600;margin-bottom:8px">Access Restricted</div>
          <div style="color:#5a6478;font-size:12px">You are logged in as <strong style="color:#a0aab8">{st.session_state.user_role}</strong>.<br>Only Administrators can manage platform settings.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="krypt-panel"><div class="krypt-panel-hdr"><span class="krypt-panel-title">Multi-Tenant Management</span></div><div class="krypt-panel-body">', unsafe_allow_html=True)
            pills = ''.join(f'<span class="t-pill">{t}</span>' for t in st.session_state.tenants)
            st.markdown(f'<div style="margin-bottom:14px">{pills}</div>', unsafe_allow_html=True)
            new_tenant = st.text_input("New Tenant Name", placeholder="e.g. Acme Corp — APAC")
            if st.button("+ Create Tenant"):
                if new_tenant and new_tenant not in st.session_state.tenants:
                    st.session_state.tenants.append(new_tenant)
                    st.success(f"Tenant '{new_tenant}' created successfully.")
                    st.rerun()
                elif new_tenant:
                    st.warning("Tenant already exists.")
            st.markdown("</div></div>", unsafe_allow_html=True)

        with col_b:
            st.markdown("""
            <div class="krypt-panel">
              <div class="krypt-panel-hdr"><span class="krypt-panel-title">User Management</span></div>
              <div class="krypt-panel-body">
                <div class="user-row">
                  <div class="u-avatar" style="background:rgba(155,109,255,.15);color:#9b6dff">SA</div>
                  <div style="flex:1"><div class="u-name">System Admin</div><div class="u-email">admin@krypteris.io</div></div>
                  <span class="badge badge-purple">ADMIN</span>
                </div>
                <div class="user-row">
                  <div class="u-avatar" style="background:rgba(0,212,255,.1);color:#00d4ff">AL</div>
                  <div style="flex:1"><div class="u-name">SOC Analyst L2</div><div class="u-email">analyst@krypteris.io</div></div>
                  <span class="badge badge-cyan">ANALYST</span>
                </div>
                <div class="user-row">
                  <div class="u-avatar" style="background:rgba(0,214,143,.1);color:#00d68f">EB</div>
                  <div style="flex:1"><div class="u-name">Executive Board</div><div class="u-email">viewer@krypteris.io</div></div>
                  <span class="badge badge-green">READ-ONLY</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="krypt-panel" style="margin-top:14px"><div class="krypt-panel-hdr"><span class="krypt-panel-title">Provision New User</span></div><div class="krypt-panel-body">', unsafe_allow_html=True)
            st.text_input("Employee Email", placeholder="user@company.com")
            st.selectbox("Assign Role", ["Analyst","Administrator","Read-Only"])
            if st.button("+ Add User"):
                st.success("User provisioned. Activation email sent.")
            st.markdown("</div></div>", unsafe_allow_html=True)
