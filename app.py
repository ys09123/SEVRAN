# ══════════════════════════════════════════════════════════════
#  ⚡  Smart EV Routing & Availability Network  (SEVRAN)
#  ──────────────────────────────────────────────────────────
#  Hackathon Theme: "Seamless EV Charging Ecosystem"
#  Features: Live Availability · AI Wait Prediction
#            Multi-Network Interop · Unified Payments
# ══════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import folium
from folium.plugins import AntPath
from streamlit.components.v1 import html as st_html
from datetime import datetime
import math
import os
import subprocess

# ─────────────────────────────────────────────────────────
#  PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚡ SEVRAN — Smart EV Network",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
#  CUSTOM CSS  — Dark theme, glassmorphism, animations
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global ────────────────────────────────────── */
.stApp {
    background: linear-gradient(160deg, #05060f 0%, #0b1120 35%, #0f172a 70%, #0a0f1e 100%);
    font-family: 'Inter', -apple-system, sans-serif;
}
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
    color: #cbd5e1;
}

/* ── Sidebar ───────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d1c 0%, #0f1629 60%, #131b36 100%) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.12);
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #94a3b8;
    font-size: 13px;
}

/* ── Headings ──────────────────────────────────── */
h1 {
    background: linear-gradient(135deg, #22d3ee 0%, #6366f1 50%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900 !important;
    letter-spacing: -0.8px;
    font-size: 2.2rem !important;
}
h2 {
    color: #e2e8f0 !important;
    font-weight: 700 !important;
    font-size: 1.3rem !important;
    letter-spacing: -0.3px;
}
h3 {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}

/* ── Metric Cards ──────────────────────────────── */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 18px 22px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(99, 102, 241, 0.35);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.12);
}
div[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-size: 26px !important;
    font-weight: 800 !important;
}
div[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-size: 11px !important;
}

/* ── Buttons ───────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.3px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99, 102, 241, 0.45) !important;
    background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Selectbox / Multiselect ───────────────────── */
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
span[data-testid="stMultiSelectTag"] {
    background: rgba(99, 102, 241, 0.15) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    color: #c7d2fe !important;
    border-radius: 8px !important;
    font-size: 12px !important;
}

/* ── Slider ────────────────────────────────────── */
div[data-testid="stSlider"] label {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── iFrame (folium map) ───────────────────────── */
iframe {
    border-radius: 16px !important;
    border: 1px solid rgba(99, 102, 241, 0.12) !important;
}

/* ── Expander ──────────────────────────────────── */
details[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 14px !important;
}
details summary span {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}

/* ── Alerts ────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    font-size: 14px;
}

/* ── Dividers ──────────────────────────────────── */
hr {
    border-color: rgba(255, 255, 255, 0.05) !important;
}

/* ── Feature cards (custom HTML) ───────────────── */
.feature-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 8px 0 28px 0;
}
.feature-card {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 22px 16px;
    text-align: center;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: default;
}
.feature-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-4px);
    box-shadow: 0 14px 44px rgba(99, 102, 241, 0.12);
}
.feature-icon { font-size: 30px; margin-bottom: 8px; }
.feature-title {
    color: #e2e8f0; font-weight: 700;
    font-size: 13px; margin-bottom: 4px;
}
.feature-desc { color: #64748b; font-size: 11px; line-height: 1.4; }

/* ── Wallet card (custom HTML) ─────────────────── */
.wallet-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.08) 100%);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 20px;
    margin-top: 8px;
}
.wallet-balance {
    font-size: 28px; font-weight: 800;
    color: #e2e8f0; margin: 6px 0;
}
.wallet-label {
    font-size: 11px; text-transform: uppercase;
    letter-spacing: 1px; color: #6366f1; font-weight: 700;
}

/* ── Booking card (custom HTML) ────────────────── */
.booking-card {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 24px;
    margin-top: 8px;
}
.station-badge {
    display: inline-block; padding: 3px 12px;
    border-radius: 20px; font-size: 11px; font-weight: 700;
    letter-spacing: 0.3px;
}
.badge-available  { background: rgba(34,197,94,0.12); color: #4ade80; }
.badge-inuse      { background: rgba(245,158,11,0.12); color: #fbbf24; }
.badge-offline    { background: rgba(239,68,68,0.12); color: #f87171; }

/* ── Peak indicator ────────────────────────────── */
@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 4px rgba(239,68,68,0.5); }
    50% { box-shadow: 0 0 16px rgba(239,68,68,0.8); }
}
.peak-badge {
    display: inline-block;
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    animation: glow-pulse 2s ease-in-out infinite;
}
.offpeak-badge {
    display: inline-block;
    background: rgba(34, 197, 94, 0.12);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.2);
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* ── Legend row ─────────────────────────────────── */
.legend-row {
    display: flex;
    gap: 28px;
    justify-content: center;
    padding: 12px 0 4px 0;
    flex-wrap: wrap;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #94a3b8;
    font-size: 12px;
    font-weight: 500;
}
.legend-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    display: inline-block;
}

/* ── Scrollable table area ─────────────────────── */
.station-table-wrap {
    max-height: 380px;
    overflow-y: auto;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
}

/* ── Hide Streamlit boilerplate ────────────────── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
#  SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────
if "wallet_balance" not in st.session_state:
    st.session_state.wallet_balance = 2500.00

if "bookings" not in st.session_state:
    # Seed with a couple of past transactions for demo realism
    st.session_state.bookings = [
        {
            "id": "BK-260603-001",
            "station": "Ather Grid — Koramangala",
            "provider": "Ather Grid",
            "cost": 245.0,
            "duration": 30,
            "time": "03 Jun, 14:30",
        },
        {
            "id": "BK-260603-002",
            "station": "Tata Power — MG Road",
            "provider": "Tata Power EZ Charge",
            "cost": 187.0,
            "duration": 25,
            "time": "03 Jun, 09:15",
        },
    ]


# ─────────────────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "mock_chargers.csv")
    if not os.path.exists(csv_path):
        gen_path = os.path.join(os.path.dirname(__file__), "generate_mock_data.py")
        subprocess.run(["python", gen_path], check=True)
    return pd.read_csv(csv_path)

df_all = load_data()

# ── Simulated user location (Cubbon Park, Bangalore) ─────
USER_LAT, USER_LON = 12.9763, 77.5929


# ─────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────
def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance between two points in km."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


def predicted_wait(base_wait, hour, status):
    """AI-predicted wait time adjusted for time-of-day peaks."""
    if status == "Offline":
        return None
    if 8 <= hour <= 10:
        mult = 1.8
    elif 17 <= hour <= 20:
        mult = 2.0
    elif 12 <= hour <= 14:
        mult = 1.3
    elif hour >= 22 or hour <= 5:
        mult = 0.5
    else:
        mult = 1.0
    return max(0, int(base_wait * mult))


def is_peak(hour):
    return (8 <= hour <= 10) or (17 <= hour <= 20)


def status_color(status):
    return {"Available": "#22c55e", "In Use": "#f59e0b", "Offline": "#ef4444"}.get(
        status, "#94a3b8"
    )


def status_border(status):
    return {"Available": "#166534", "In Use": "#b45309", "Offline": "#991b1b"}.get(
        status, "#475569"
    )


def badge_class(status):
    return {
        "Available": "badge-available",
        "In Use": "badge-inuse",
        "Offline": "badge-offline",
    }.get(status, "badge-offline")


# ─────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:8px;">
            <span style="font-size:36px;">⚡</span>
            <div style="font-size:20px; font-weight:900; letter-spacing:1.5px;
                        background: linear-gradient(135deg, #22d3ee, #6366f1);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                        background-clip:text; margin-top:2px;">SEVRAN</div>
            <div style="color:#64748b; font-size:11px; letter-spacing:1px;
                        text-transform:uppercase; font-weight:600;">
                Smart EV Routing &amp; Availability Network
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Filters ────────────────────────────────────────
    st.markdown("##### 🔍 Filters")

    all_providers = sorted(df_all["provider"].unique())
    sel_providers = st.multiselect(
        "Provider Network",
        all_providers,
        default=all_providers,
        key="filter_providers",
    )

    all_types = sorted(df_all["charger_type"].unique())
    sel_types = st.multiselect(
        "Charger Type",
        all_types,
        default=all_types,
        key="filter_types",
    )

    all_statuses = ["Available", "In Use", "Offline"]
    sel_statuses = st.multiselect(
        "Status",
        all_statuses,
        default=all_statuses,
        key="filter_statuses",
    )

    st.divider()

    # ── Time Simulator ─────────────────────────────────
    st.markdown("##### 🕐 Time Simulator")
    current_hour = st.slider(
        "Simulated Hour (24h)",
        min_value=0,
        max_value=23,
        value=datetime.now().hour,
        key="sim_hour",
    )
    if is_peak(current_hour):
        st.markdown(
            '<span class="peak-badge">🔴 PEAK HOUR</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="offpeak-badge">🟢 OFF-PEAK</span>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Unified Wallet ─────────────────────────────────
    st.markdown("##### 💳 Unified Wallet")
    st.markdown(
        f"""
        <div class="wallet-card">
            <div class="wallet-label">Available Balance</div>
            <div class="wallet-balance">₹{st.session_state.wallet_balance:,.2f}</div>
            <div style="color:#94a3b8; font-size:11px; margin-top:4px;">
                Works across all {len(all_providers)} provider networks
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")  # spacer
    wcol1, wcol2 = st.columns(2)
    with wcol1:
        if st.button("＋ ₹500", key="add500", use_container_width=True):
            st.session_state.wallet_balance += 500.0
            st.rerun()
    with wcol2:
        if st.button("＋ ₹1,000", key="add1000", use_container_width=True):
            st.session_state.wallet_balance += 1000.0
            st.rerun()

    # ── Recent Transactions ────────────────────────────
    if st.session_state.bookings:
        st.divider()
        st.markdown("##### 📋 Recent Bookings")
        for bk in reversed(st.session_state.bookings[-5:]):
            st.markdown(
                f"""<div style="background:rgba(255,255,255,0.02);
                     border:1px solid rgba(255,255,255,0.05);
                     border-radius:10px; padding:10px 14px; margin-bottom:8px;">
                    <div style="font-size:12px; font-weight:700; color:#e2e8f0;">
                        {bk['station']}</div>
                    <div style="font-size:11px; color:#64748b; margin-top:2px;">
                        {bk['time']} · {bk['duration']} min · 
                        <span style="color:#a78bfa; font-weight:600;">
                            −₹{bk['cost']:.0f}</span>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────────────────────
df = df_all[
    (df_all["provider"].isin(sel_providers))
    & (df_all["charger_type"].isin(sel_types))
    & (df_all["status"].isin(sel_statuses))
].copy()

# Add predicted wait column
df["pred_wait"] = df.apply(
    lambda r: predicted_wait(r["base_wait_min"], current_hour, r["status"]), axis=1
)

# Add distance from user
df["distance_km"] = df.apply(
    lambda r: round(haversine_km(USER_LAT, USER_LON, r["lat"], r["lon"]), 1), axis=1
)


# ─────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────
st.markdown("# ⚡ Smart EV Routing & Availability Network")
st.markdown(
    """<div style="color:#64748b; margin:-12px 0 6px 0; font-size:14px;">
    Real-time charging intelligence for <strong style="color:#a5b4fc;">
    Bangalore</strong> — powered by AI-driven density clustering</div>""",
    unsafe_allow_html=True,
)

# ── Feature Cards ──────────────────────────────────────
st.markdown(
    """
    <div class="feature-row">
        <div class="feature-card">
            <div class="feature-icon">📡</div>
            <div class="feature-title">Live Availability</div>
            <div class="feature-desc">Real-time station status across all networks</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI Wait Prediction</div>
            <div class="feature-desc">ML-powered queue estimates using density clustering</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔗</div>
            <div class="feature-title">Network Interoperability</div>
            <div class="feature-desc">5 providers unified in a single seamless view</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💳</div>
            <div class="feature-title">Unified Payments</div>
            <div class="feature-desc">Book &amp; pay across any network — one wallet</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────
#  KPI METRICS
# ─────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
available_count = len(df[df["status"] == "Available"])
avg_wait = df.loc[df["status"] != "Offline", "pred_wait"].mean()
avg_wait_str = f"~{avg_wait:.0f} min" if pd.notna(avg_wait) else "—"

k1.metric("Total Stations", f"{len(df)}")
k2.metric("Available Now", f"{available_count}", delta=f"{available_count}/{len(df)}")
k3.metric("Avg AI Wait", avg_wait_str)
k4.metric("Networks Linked", f"{df['provider'].nunique()}")

st.markdown("")  # spacer


# ─────────────────────────────────────────────────────────
#  FOLIUM MAP
# ─────────────────────────────────────────────────────────
st.markdown("## 🗺️ Live Charging Map")

# ── Station selector (for route) ──────────────────────
available_df = df[df["status"] == "Available"].sort_values("distance_km")
station_options = ["— None (view all) —"] + [
    f"{r['station_name']}  ·  {r['distance_km']} km  ·  ~{r['pred_wait']} min"
    for _, r in available_df.iterrows()
]
selected_station_label = st.selectbox(
    "📍 Route to station",
    station_options,
    index=0,
    key="route_select",
)

# Resolve selected station
selected_row = None
if selected_station_label != "— None (view all) —":
    sel_name = selected_station_label.split("  ·  ")[0]
    match = df[df["station_name"] == sel_name]
    if not match.empty:
        selected_row = match.iloc[0]

# ── Build Map ─────────────────────────────────────────
map_center = [USER_LAT, USER_LON]
m = folium.Map(
    location=map_center,
    zoom_start=12,
    tiles="CartoDB dark_matter",
    control_scale=True,
)

# User location marker (pulsing blue dot)
folium.Marker(
    location=[USER_LAT, USER_LON],
    icon=folium.DivIcon(html="""
        <div style="position:relative; width:20px; height:20px;">
            <div style="
                position:absolute; top:0; left:0;
                width:20px; height:20px;
                background:rgba(59,130,246,0.25);
                border-radius:50%;
                animation: user-pulse 2s ease-out infinite;
            "></div>
            <div style="
                position:absolute; top:5px; left:5px;
                width:10px; height:10px;
                background:#3b82f6;
                border:2px solid white;
                border-radius:50%;
                box-shadow:0 0 8px rgba(59,130,246,0.6);
            "></div>
        </div>
        <style>
        @keyframes user-pulse {
            0%   { transform:scale(1);   opacity:0.8; }
            100% { transform:scale(2.5); opacity:0; }
        }
        </style>
    """),
    tooltip="📍 Your Location",
).add_to(m)

# Station markers
for _, row in df.iterrows():
    s_color = status_color(row["status"])
    s_border = status_border(row["status"])
    fill_op = 0.4 if row["status"] == "Offline" else 0.8
    radius = 5 if row["status"] == "Offline" else 8

    wait_display = f"~{row['pred_wait']} min" if row["pred_wait"] is not None else "—"

    popup_html = f"""
    <div style="font-family:'Segoe UI','Inter',sans-serif; padding:6px; min-width:250px; max-width:280px;">
        <div style="font-size:14px; font-weight:700; color:#1e293b; margin-bottom:6px; line-height:1.3;">
            {row['station_name']}
        </div>
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; flex-wrap:wrap;">
            <span class="station-badge {badge_class(row['status'])}"
                  style="display:inline-block; padding:3px 10px; border-radius:20px;
                         font-size:11px; font-weight:700;">
                ● {row['status']}
            </span>
            <span style="color:#64748b; font-size:11px;">
                {row['charger_type']} · {row['power_kw']} kW
            </span>
        </div>
        <div style="border-top:1px solid #e2e8f0; padding-top:8px; font-size:12px; color:#475569; line-height:1.7;">
            🏢 <strong>{row['provider']}</strong><br>
            ⏱️ AI Predicted Wait: <strong style="color:#6366f1;">{wait_display}</strong><br>
            💰 ₹{row['price_per_kwh']:.2f}/kWh<br>
            ⭐ {row['rating']} · 📍 {row['distance_km']} km away<br>
            🛠️ {row['amenities']}
        </div>
    </div>
    """

    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=radius,
        color=s_border,
        fill=True,
        fill_color=s_color,
        fill_opacity=fill_op,
        weight=2,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{row['station_name']} — {row['status']}",
    ).add_to(m)

# ── Route Line (if station selected) ──────────────────
if selected_row is not None:
    route_coords = [[USER_LAT, USER_LON], [selected_row["lat"], selected_row["lon"]]]
    try:
        AntPath(
            locations=route_coords,
            color="#6366f1",
            weight=4,
            opacity=0.85,
            dash_array=[12, 24],
            delay=1200,
            pulse_color="#a855f7",
        ).add_to(m)
    except Exception:
        # Fallback to regular dashed line if AntPath unavailable
        folium.PolyLine(
            locations=route_coords,
            color="#6366f1",
            weight=3,
            opacity=0.8,
            dash_array="12 8",
        ).add_to(m)

    # Highlight selected station
    folium.CircleMarker(
        location=[selected_row["lat"], selected_row["lon"]],
        radius=14,
        color="#6366f1",
        fill=False,
        weight=3,
        opacity=0.7,
        dash_array="6 4",
    ).add_to(m)

    # Fit map to show both user and station
    m.fit_bounds(route_coords, padding=[60, 60])

# Render map
map_html = m._repr_html_()
st_html(map_html, height=540)

# ── Map Legend ─────────────────────────────────────────
st.markdown(
    """
    <div class="legend-row">
        <div class="legend-item">
            <span class="legend-dot" style="background:#22c55e;"></span> Available
        </div>
        <div class="legend-item">
            <span class="legend-dot" style="background:#f59e0b;"></span> In Use
        </div>
        <div class="legend-item">
            <span class="legend-dot" style="background:#ef4444;"></span> Offline
        </div>
        <div class="legend-item">
            <span class="legend-dot" style="background:#3b82f6;
                  box-shadow:0 0 6px rgba(59,130,246,0.6);"></span> Your Location
        </div>
        <div class="legend-item">
            <span style="color:#6366f1; font-size:14px;">- - -</span> Route
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")  # spacer


# ─────────────────────────────────────────────────────────
#  STATION DETAILS + BOOKING  (two columns)
# ─────────────────────────────────────────────────────────
col_table, col_booking = st.columns([1.2, 1])

# ── Left Column: Station Table ────────────────────────
with col_table:
    st.markdown("## 📊 Station Directory")

    display_df = df[
        ["station_id", "station_name", "provider", "charger_type",
         "power_kw", "status", "pred_wait", "price_per_kwh",
         "distance_km", "rating"]
    ].rename(columns={
        "station_id": "ID",
        "station_name": "Station",
        "provider": "Provider",
        "charger_type": "Type",
        "power_kw": "kW",
        "status": "Status",
        "pred_wait": "Wait (min)",
        "price_per_kwh": "₹/kWh",
        "distance_km": "Dist (km)",
        "rating": "★",
    }).sort_values("Dist (km)")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={
            "ID": st.column_config.TextColumn(width="small"),
            "Station": st.column_config.TextColumn(width="large"),
            "kW": st.column_config.NumberColumn(format="%d"),
            "Wait (min)": st.column_config.NumberColumn(format="%d"),
            "₹/kWh": st.column_config.NumberColumn(format="₹%.2f"),
            "Dist (km)": st.column_config.NumberColumn(format="%.1f"),
            "★": st.column_config.NumberColumn(format="%.1f"),
        },
    )

# ── Right Column: Booking Flow ────────────────────────
with col_booking:
    st.markdown("## ⚡ Book & Pay")

    if available_df.empty:
        st.warning("No available stations match your filters.")
    else:
        # Station selector for booking
        booking_options = [
            f"{r['station_name']}"
            for _, r in available_df.iterrows()
        ]
        selected_booking = st.selectbox(
            "Select Station to Book",
            booking_options,
            key="booking_select",
        )

        bk_match = df[df["station_name"] == selected_booking]
        if not bk_match.empty:
            bk = bk_match.iloc[0]

            # Station detail card
            wait_str = f"~{bk['pred_wait']} min" if bk["pred_wait"] is not None else "—"
            st.markdown(
                f"""
                <div class="booking-card">
                    <div style="font-size:16px; font-weight:800; color:#e2e8f0;
                                margin-bottom:8px; line-height:1.3;">
                        {bk['station_name']}
                    </div>
                    <div style="margin-bottom:12px;">
                        <span class="station-badge {badge_class(bk['status'])}">
                            ● {bk['status']}</span>
                        <span style="color:#64748b; font-size:12px; margin-left:8px;">
                            {bk['charger_type']} · {bk['power_kw']} kW</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr;
                                gap:8px; font-size:13px; color:#94a3b8;">
                        <div>🏢 {bk['provider']}</div>
                        <div>⏱️ Wait: <span style="color:#a5b4fc; font-weight:600;">
                            {wait_str}</span></div>
                        <div>💰 ₹{bk['price_per_kwh']:.2f}/kWh</div>
                        <div>📍 {bk['distance_km']} km away</div>
                        <div>⭐ {bk['rating']} rating</div>
                        <div>🗺️ {bk['area']}</div>
                    </div>
                    <div style="margin-top:10px; font-size:12px; color:#64748b;">
                        🛠️ {bk['amenities']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("")  # spacer

            # Charge duration slider
            charge_duration = st.slider(
                "Charge Duration (minutes)",
                min_value=15,
                max_value=120,
                value=30,
                step=5,
                key="charge_dur",
            )

            # Cost calculation
            charge_hours = charge_duration / 60
            energy_kwh = charge_hours * bk["power_kw"]
            estimated_cost = round(energy_kwh * bk["price_per_kwh"], 2)

            # ETA calculation
            dist_km = bk["distance_km"]
            eta_min = max(1, int(dist_km / 0.4))  # ~25 km/h avg Bangalore traffic

            st.markdown(
                f"""
                <div style="background:rgba(99,102,241,0.06);
                     border:1px solid rgba(99,102,241,0.15);
                     border-radius:14px; padding:16px; margin:8px 0;">
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                        <div style="font-size:12px; color:#94a3b8;">
                            ⚡ Energy
                            <div style="font-size:18px; font-weight:800; color:#e2e8f0;">
                                {energy_kwh:.1f} kWh</div>
                        </div>
                        <div style="font-size:12px; color:#94a3b8;">
                            💰 Estimated Cost
                            <div style="font-size:18px; font-weight:800; color:#22d3ee;">
                                ₹{estimated_cost:,.0f}</div>
                        </div>
                        <div style="font-size:12px; color:#94a3b8;">
                            🚗 ETA to Station
                            <div style="font-size:18px; font-weight:800; color:#e2e8f0;">
                                ~{eta_min} min</div>
                        </div>
                        <div style="font-size:12px; color:#94a3b8;">
                            🕐 Total Time
                            <div style="font-size:18px; font-weight:800; color:#e2e8f0;">
                                ~{eta_min + charge_duration + (bk['pred_wait'] or 0)} min</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ── Book Button ─────────────────────────────
            st.markdown("")
            if st.button(
                f"⚡  Book & Pay  ·  ₹{estimated_cost:,.0f}",
                key="book_btn",
                use_container_width=True,
            ):
                if st.session_state.wallet_balance >= estimated_cost:
                    st.session_state.wallet_balance -= estimated_cost
                    booking_id = (
                        f"BK-{datetime.now().strftime('%y%m%d')}"
                        f"-{len(st.session_state.bookings) + 1:03d}"
                    )
                    st.session_state.bookings.append({
                        "id": booking_id,
                        "station": bk["station_name"],
                        "provider": bk["provider"],
                        "cost": estimated_cost,
                        "duration": charge_duration,
                        "time": datetime.now().strftime("%d %b, %H:%M"),
                    })
                    st.balloons()
                    st.success(
                        f"**✅ Booking Confirmed!**\n\n"
                        f"**Booking ID:** `{booking_id}`\n\n"
                        f"**Station:** {bk['station_name']}\n\n"
                        f"**Duration:** {charge_duration} min · "
                        f"**Energy:** {energy_kwh:.1f} kWh\n\n"
                        f"**Amount Charged:** ₹{estimated_cost:,.0f} "
                        f"from Unified Wallet\n\n"
                        f"**Remaining Balance:** "
                        f"₹{st.session_state.wallet_balance:,.2f}"
                    )
                else:
                    deficit = estimated_cost - st.session_state.wallet_balance
                    st.error(
                        f"**❌ Insufficient Balance**\n\n"
                        f"Required: ₹{estimated_cost:,.0f} · "
                        f"Balance: ₹{st.session_state.wallet_balance:,.2f}\n\n"
                        f"Please add **₹{deficit:,.0f}** or more to your "
                        f"Unified Wallet (sidebar)."
                    )


# ─────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────
st.divider()
st.markdown(
    """
    <div style="text-align:center; padding:8px 0 20px 0;">
        <div style="font-size:13px; color:#475569;">
            ⚡ <strong style="color:#a5b4fc;">SEVRAN</strong> —
            Smart EV Routing &amp; Availability Network
        </div>
        <div style="font-size:11px; color:#334155; margin-top:4px;">
            Built for Hackathon: Seamless EV Charging Ecosystem ·
            Powered by K-Means density clustering &amp; real-time simulation
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)