import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import hashlib

st.set_page_config(
    page_title="Dashboard Prestasi Akademik",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# CUSTOM CSS - MODERN ACADEMIC ANALYTICS
# ================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

:root {
    --bg: #f5f7fb;
    --surface: #ffffff;
    --surface-2: #f8fafc;
    --ink: #172033;
    --muted: #667085;
    --line: #e6eaf0;
    --navy: #172554;
    --blue: #315efb;
    --blue-soft: #eef2ff;
    --teal: #0f766e;
    --teal-soft: #ecfdf5;
    --amber: #b7791f;
    --amber-soft: #fffbeb;
    --red: #c83b4a;
    --red-soft: #fff1f2;
    --shadow: 0 8px 24px rgba(23, 32, 51, 0.06);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

.stApp {
    background: var(--bg);
}

.main {
    background: var(--bg);
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* ---------- TYPOGRAPHY ---------- */
.masthead {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2.4rem, 4vw, 4rem);
    font-weight: 800;
    line-height: 1.02;
    letter-spacing: -2.5px;
    color: var(--ink);
    margin: 0;
}

.masthead-accent {
    color: var(--blue);
}

.kicker {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--blue);
    margin-bottom: 0.55rem;
}

.kicker-line {
    display: inline-block;
    width: 22px;
    height: 2px;
    background: currentColor;
    vertical-align: middle;
    margin-right: 8px;
    margin-bottom: 3px;
}

.deck {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.65;
    color: var(--muted);
    max-width: 760px;
    margin-top: 0.9rem;
}

.section-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.45rem;
    font-weight: 800;
    color: var(--ink);
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin: 0;
}

.section-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    color: var(--muted);
    letter-spacing: 1.2px;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 3px;
}

/* ---------- DIVIDERS ---------- */
.rule-thick {
    height: 1px;
    background: var(--line);
    margin: 1.35rem 0;
    border: none;
}

.rule-thin {
    height: 1px;
    background: var(--line);
    margin: 1.5rem 0;
    border: none;
}

.rule-red {
    height: 2px;
    background: var(--blue);
    width: 38px;
    margin: 0.7rem 0 1.25rem 0;
    border: none;
}

/* ---------- CARDS ---------- */
.article-card,
.article-card-red,
.article-card-black {
    border-radius: 14px;
    padding: 1.25rem 1.35rem;
    border: 1px solid var(--line);
    box-shadow: var(--shadow);
    position: relative;
}

.article-card {
    background: var(--surface);
    color: var(--ink);
}

.article-card-red {
    background: var(--red-soft);
    color: var(--ink);
    border-color: #fecdd3;
}

.article-card-black {
    background: var(--navy);
    color: #ffffff;
    border-color: var(--navy);
    box-shadow: 0 12px 30px rgba(23, 37, 84, 0.14);
}

.article-card::before,
.article-card-red::before,
.article-card-black::before {
    display: none;
}

/* ---------- STAT CARDS ---------- */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-top: 3px solid var(--blue);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    min-height: 112px;
    box-shadow: 0 4px 14px rgba(23, 32, 51, 0.045);
}

.stat-card-red { border-top-color: var(--red); }
.stat-card-yellow { border-top-color: #d99a27; }
.stat-card-blue { border-top-color: var(--blue); }
.stat-card-green { border-top-color: var(--teal); }

.stat-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.67rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--muted);
    font-weight: 700;
    margin-bottom: 0.45rem;
}

.stat-value {
    font-family: 'Manrope', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.05;
    color: var(--ink);
    letter-spacing: -1px;
}

.stat-unit {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 0.35rem;
}

/* ---------- ALERTS ---------- */
.alert {
    padding: 0.95rem 1.1rem;
    border: 1px solid var(--line);
    border-left: 3px solid var(--blue);
    border-radius: 10px;
    background: var(--surface);
    margin: 0.8rem 0;
    font-size: 0.86rem;
    line-height: 1.55;
}

.alert-info { border-left-color: var(--blue); background: var(--blue-soft); }
.alert-success { border-left-color: var(--teal); background: var(--teal-soft); }
.alert-warning { border-left-color: var(--amber); background: var(--amber-soft); }
.alert-danger { border-left-color: var(--red); background: var(--red-soft); }

.alert-title {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: 0.92rem;
    margin-bottom: 0.25rem;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

[data-testid="stSidebar"] * {
    color: var(--ink);
}

[data-testid="stSidebar"] .kicker {
    color: var(--blue) !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 0.7rem 0.8rem;
    margin: 0.15rem 0;
    border-radius: 9px;
    border-bottom: none;
    transition: all 0.18s ease;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: #f1f5f9;
    color: var(--blue) !important;
}

[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    margin: 0;
}

[data-testid="stSidebar"] hr {
    border-top-color: var(--line) !important;
}

/* ---------- BUTTONS ---------- */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    border-radius: 9px !important;
    border: 1px solid var(--blue) !important;
    background: var(--blue) !important;
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.2px !important;
    padding: 0.55rem 1rem !important;
    min-height: 42px !important;
    box-shadow: none !important;
    transition: all 0.18s ease !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #244bd3 !important;
    border-color: #244bd3 !important;
    transform: translateY(-1px);
    box-shadow: 0 5px 12px rgba(49, 94, 251, 0.16) !important;
}

.stButton > button:active,
.stDownloadButton > button:active {
    transform: translateY(0);
}

.stButton > button[kind="secondary"] {
    background: #ffffff !important;
    color: var(--ink) !important;
    border-color: var(--line) !important;
}

/* ---------- INPUTS ---------- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background: #ffffff !important;
    border: 1px solid #d9dee8 !important;
    border-radius: 9px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--ink) !important;
    min-height: 42px;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(49, 94, 251, 0.10) !important;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stSlider label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    color: var(--ink) !important;
    font-weight: 700 !important;
}

/* ---------- SLIDER ---------- */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--blue) !important;
    border-color: var(--blue) !important;
}

.stSlider [data-baseweb="slider"] > div > div {
    background: #dbe3ff !important;
}

/* ---------- DATAFRAME ---------- */
.stDataFrame {
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ---------- LOGIN ---------- */
.login-hero {
    background: var(--navy);
    color: #ffffff;
    padding: 3rem 2rem 2.8rem;
    text-align: center;
    border: 1px solid #243568;
    border-radius: 18px;
    box-shadow: 0 18px 45px rgba(23, 37, 84, 0.16);
}

.login-hero::before,
.login-hero::after {
    display: none;
}

.login-title-main {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1;
    letter-spacing: -2px;
    margin: 0;
}

.login-title-main em {
    color: #8fa7ff;
    font-style: normal;
}

.login-hero .kicker {
    color: #9fb1ff !important;
}

/* ---------- PROCESS / TAGS ---------- */
.process-box {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 1.1rem;
    margin: 0.7rem 0;
    box-shadow: 0 4px 14px rgba(23, 32, 51, 0.04);
}

.process-box-number {
    font-family: 'Manrope', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--blue);
    line-height: 1;
}

.label-tag {
    display: inline-block;
    padding: 0.28rem 0.65rem;
    background: var(--blue-soft);
    color: var(--navy);
    border: 1px solid #dbe3ff;
    border-radius: 999px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.66rem;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    font-weight: 700;
}

.label-tag-red { background: var(--red-soft); color: var(--red); border-color: #fecdd3; }
.label-tag-yellow { background: var(--amber-soft); color: var(--amber); border-color: #fde68a; }
.label-tag-green { background: var(--teal-soft); color: var(--teal); border-color: #a7f3d0; }
.label-tag-blue { background: var(--blue-soft); color: var(--blue); border-color: #dbe3ff; }

/* ---------- SPACING / CONTAINERS ---------- */
.block-container {
    max-width: 1440px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

div[data-testid="stVerticalBlock"] > div:has(> div.stMarkdown) {
    scroll-margin-top: 20px;
}

/* ---------- MOBILE ---------- */
@media (max-width: 900px) {
    .block-container {
        padding: 1.2rem 1rem 2rem;
    }

    .masthead {
        font-size: 2.45rem;
        letter-spacing: -1.5px;
    }

    .deck {
        font-size: 0.92rem;
    }

    .section-title {
        font-size: 1.25rem;
    }

    .stat-value {
        font-size: 1.7rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ================================================================
# HASH PASSWORD
# ================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    'admin': {'password': hash_password('admin123'), 'nama': 'Administrator'},
    'guru': {'password': hash_password('guru123'), 'nama': 'Guru SMPN 6'},
    'regina': {'password': hash_password('regina2026'), 'nama': 'Regina Ria'},
}

# ================================================================
# SESSION STATE
# ================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_nama' not in st.session_state:
    st.session_state.user_nama = None
if 'database_siswa' not in st.session_state:
    st.session_state.database_siswa = []

# ================================================================
# DATA
# ================================================================

BASELINE_ASPEK = {
    'Self-Efficacy Akademik': 4.63,
    'Keterlibatan Orang Tua': 4.35,
    'Harapan Orang Tua': 3.45,
    'Dukungan Sekolah': 4.60,
    'Motivasi Belajar': 2.52,
    'Kecemasan Akademik': 2.89,
    'Kemalasan Belajar': 1.49,
    'Fasilitas Sekolah': 4.88,
}

BOBOT_PENGARUH = {
    'Self-Efficacy Akademik': 2.0698 * 0.8008,
    'Keterlibatan Orang Tua': 2.2100 * 0.6806,
    'Harapan Orang Tua': -1.5323 * 0.5823,
    'Dukungan Sekolah': -3.8797 * 0.4352,
    'Motivasi Belajar': -0.2850 * 0.3667,
    'Kecemasan Akademik': 0.4522 * 0.1308,
    'Fasilitas Sekolah': 2.4295 * 0.0654,
    'Kemalasan Belajar': -0.0902 * 0.0793,
}

RATA_RATA_NILAI = 83.78

KELAS_LIST = (
    [f"VII-{x}" for x in "ABCDEFGH"] +
    [f"VIII-{x}" for x in "ABCDEFGH"] +
    [f"IX-{x}" for x in "ABCDEFGH"]
)

# ================================================================
# FUNGSI
# ================================================================

def analisis_kausal(nilai_akademik, profil_siswa):
    selisih_nilai = nilai_akademik - RATA_RATA_NILAI
    kontribusi = {}
    for aspek, nilai_input in profil_siswa.items():
        selisih_aspek = nilai_input - BASELINE_ASPEK[aspek]
        kontribusi[aspek] = selisih_aspek * BOBOT_PENGARUH[aspek]
    
    total_kontribusi = sum(kontribusi.values())
    if abs(total_kontribusi) > 0.01:
        skala = selisih_nilai / total_kontribusi
        kontribusi = {k: v * skala for k, v in kontribusi.items()}
    
    return selisih_nilai, kontribusi


def kategori_nilai(nilai):
    if nilai >= 88:
        return "Sangat Baik", "#0f766e", "▲"
    elif nilai >= 84:
        return "Baik", "#315efb", "●"
    elif nilai >= 80:
        return "Cukup", "#d99a27", "◆"
    else:
        return "Perlu Perhatian", "#315efb", "▼"


def editorial_header(kicker, title, subtitle, issue="EDISI 2026 / SMPN 6 SALATIGA"):
    st.markdown(f"""
    <div style="padding: 2rem 0 1rem 0;">
        <div class="kicker"><span class="kicker-line"></span>{kicker}</div>
        <h1 class="masthead">{title}</h1>
        <p class="deck">{subtitle}</p>
        <hr class="rule-thick" style="margin-top: 1.5rem;">
        <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; letter-spacing: 2px; color: #737373; text-transform: uppercase;">
            <span>{issue}</span>
            <span>■ DASHBOARD ANALITIK</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(num, title, subtitle):
    st.markdown(f"""
    <div style="margin: 2.5rem 0 1.5rem 0;">
        <div style="display: flex; align-items: baseline; gap: 1rem;">
            <span style="font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 900; color: #315efb; line-height: 1;">{num}</span>
            <div>
                <h2 class="section-title">{title}</h2>
                <div class="section-sub">{subtitle}</div>
            </div>
        </div>
        <hr class="rule-red">
    </div>
    """, unsafe_allow_html=True)


def stat_card(label, value, unit="", color_class=""):
    unit_html = f'<div class="stat-unit">{unit}</div>' if unit else ''
    st.markdown(f"""
    <div class="stat-card {color_class}">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        {unit_html}
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# LOGIN PAGE
# ================================================================

def halaman_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("""
        <div class="login-hero">
            <div class="kicker" style="color: #315efb; text-align: center; margin-bottom: 1rem;">
                <span class="kicker-line" style="background: #315efb;"></span>SISTEM INFORMASI AKADEMIK
            </div>
            <h1 class="login-title-main">
                Prestasi<br>
                <em>Akademik.</em>
            </h1>
            <p style="font-family: 'Fraunces', serif; font-style: italic; font-size: 1rem; margin-top: 1rem; opacity: 0.85;">
                Analisis Hybrid Causal-Explainable Machine Learning<br>
                SMP Negeri 6 Salatiga
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown('<div class="kicker" style="color: #172033;"><span class="kicker-line" style="background: #172033;"></span>MASUK</div>', unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            submit = st.form_submit_button("MASUK →", use_container_width=True)
            
            if submit:
                if username in USERS and USERS[username]['password'] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.user_nama = USERS[username]['nama']
                    st.rerun()
                else:
                    st.markdown('<div class="alert alert-danger"><b>✕ LOGIN GAGAL</b><br>Username atau password salah.</div>', unsafe_allow_html=True)
        
        with st.expander("🔑 Akun Demo"):
            st.markdown("""
            **Akun yang tersedia:**
            
            | Username | Password |
            |----------|----------|
            | `admin` | `admin123` |
            | `guru` | `guru123` |
            | `regina` | `regina2026` |
            """)

if not st.session_state.logged_in:
    halaman_login()
    st.stop()

# ================================================================
# SIDEBAR
# ================================================================

with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1rem 0;">
        <div class="kicker" style="color: #315efb;"><span class="kicker-line" style="background: #315efb;"></span>DASHBOARD</div>
        <h1 style="font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 900; line-height: 1; letter-spacing: -1px; margin: 0.3rem 0; color: #f5f7fb;">
            Prestasi<br><em style="color: #315efb;">Akademik.</em>
        </h1>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 2px; color: #737373; margin-top: 0.5rem;">SMPN 6 SALATIGA / 2026</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr style="border: none; border-top: 1px solid rgba(250,246,240,0.15); margin: 1rem 0;">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #315efb; padding: 0.8rem; margin-bottom: 1rem;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; color: #f5f7fb; opacity: 0.8;">USER AKTIF</div>
        <div style="font-family: 'Fraunces', serif; font-size: 1.1rem; font-weight: 700; color: #f5f7fb; margin-top: 0.2rem;">{st.session_state.user_nama}</div>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "NAVIGASI",
        [
            "01 · Analisis Sebab-Akibat",
            "02 · Database Siswa",
            "03 · Analisis Kausal",
            "04 · Analisis SHAP",
            "05 · Rekomendasi"
        ],
        label_visibility="visible"
    )
    
    st.markdown('<hr style="border: none; border-top: 1px solid rgba(250,246,240,0.15); margin: 1rem 0;">', unsafe_allow_html=True)
    
    if st.button("← KELUAR", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_nama = None
        st.rerun()
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; color: #737373;">
        ■ HYBRID CAUSAL - XAI
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# MENU 1: ANALISIS SEBAB-AKIBAT
# ================================================================

if menu == "01 · Analisis Sebab-Akibat":
    editorial_header(
        "ANALISIS UTAMA",
        "Sebab & Akibat<br>Nilai <span class='masthead-accent'>Siswa.</span>",
        "Masukkan data siswa untuk melihat faktor-faktor yang secara kausal mempengaruhi nilai akademiknya berdasarkan estimasi ATE dan kontribusi SHAP."
    )
    
    # -------- DATA SISWA --------
    section_header("01", "Data Siswa", "IDENTITAS & NILAI RAPOR")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        nama_siswa = st.text_input("Nama Siswa", placeholder="Nama lengkap")
    with col2:
        kelas_siswa = st.selectbox("Kelas", KELAS_LIST, index=KELAS_LIST.index("IX-A"))
    with col3:
        absen_siswa = st.number_input("No. Absen", min_value=1, max_value=50, value=1)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        nilai_akademik = st.number_input(
            "Nilai Rata-rata Rapor",
            min_value=60.0, max_value=100.0, value=83.78, step=0.01,
            format="%.2f",
            help=f"Rata-rata sekolah: {RATA_RATA_NILAI}"
        )
    with col2:
        selisih_awal = nilai_akademik - RATA_RATA_NILAI
        stat_card(
            "Posisi Nilai",
            f"{selisih_awal:+.2f}",
            "dari rata-rata sekolah",
            "stat-card-red" if selisih_awal < 0 else "stat-card-green"
        )
    
    # -------- PROFIL --------
    section_header("02", "Profil Siswa", "PENILAIAN 8 KONSTRUK / SKALA 1-5")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="label-tag label-tag-red">ASPEK INTERNAL</span>', unsafe_allow_html=True)
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        input_self_efficacy = st.slider("Self-Efficacy Akademik", 1.0, 5.0, 4.63, 0.1)
        input_motivasi = st.slider("Motivasi Belajar", 1.0, 5.0, 2.52, 0.1)
        input_kecemasan = st.slider("Kecemasan Akademik", 1.0, 5.0, 2.89, 0.1)
        input_kemalasan = st.slider("Kemalasan Belajar", 1.0, 5.0, 1.49, 0.1)
    with col2:
        st.markdown('<span class="label-tag label-tag-blue">ASPEK EKSTERNAL</span>', unsafe_allow_html=True)
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        input_keterlibatan = st.slider("Keterlibatan Orang Tua", 1.0, 5.0, 4.35, 0.1)
        input_harapan = st.slider("Harapan Orang Tua", 1.0, 5.0, 3.45, 0.1)
        input_dukungan = st.slider("Dukungan Sekolah", 1.0, 5.0, 4.60, 0.1)
        input_fasilitas = st.slider("Fasilitas Sekolah", 1.0, 5.0, 4.88, 0.1)
    
    profil_siswa = {
        'Self-Efficacy Akademik': input_self_efficacy,
        'Keterlibatan Orang Tua': input_keterlibatan,
        'Harapan Orang Tua': input_harapan,
        'Dukungan Sekolah': input_dukungan,
        'Motivasi Belajar': input_motivasi,
        'Kecemasan Akademik': input_kecemasan,
        'Fasilitas Sekolah': input_fasilitas,
        'Kemalasan Belajar': input_kemalasan,
    }
    
    selisih_nilai, kontribusi = analisis_kausal(nilai_akademik, profil_siswa)
    kategori, warna_kategori, simbol = kategori_nilai(nilai_akademik)
    
    # -------- HASIL --------
    section_header("03", "Hasil Analisis", "ATRIBUSI KAUSAL NILAI SISWA")
    
    if nama_siswa:
        st.markdown(f"""
        <div class="article-card" style="margin-bottom: 1.5rem;">
            <div class="kicker" style="color: #172033;"><span class="kicker-line" style="background: #172033;"></span>SUBJEK ANALISIS</div>
            <div style="font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 700; color: #172033; line-height: 1; margin-top: 0.3rem;">{nama_siswa}</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #737373; margin-top: 0.5rem; letter-spacing: 1px;">
                {kelas_siswa} · ABSEN {absen_siswa:02d}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        stat_card("Nilai Akademik", f"{nilai_akademik:.2f}", "dari rapor siswa", "stat-card-blue")
    with col2:
        stat_card(
            "Selisih Rata-rata",
            f"{selisih_nilai:+.2f}",
            "poin dari baseline",
            "stat-card-green" if selisih_nilai >= 0 else "stat-card-red"
        )
    with col3:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color: {warna_kategori};">
            <div class="stat-label">KATEGORI</div>
            <div class="stat-value" style="color: {warna_kategori}; font-size: 1.6rem;">{kategori}</div>
            <div class="stat-unit">{simbol} posisi nilai</div>
        </div>
        """, unsafe_allow_html=True)
    
    # -------- VISUALISASI POSISI --------
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(14, 2.8))
    fig.patch.set_facecolor('#f5f7fb')
    ax.set_facecolor('#f5f7fb')
    
    nilai_min, nilai_max = 75, 95
    ax.barh(0, RATA_RATA_NILAI - nilai_min, left=nilai_min, 
            color='#fecaca', alpha=0.7, height=0.35, edgecolor='#172033', linewidth=1.5)
    ax.barh(0, nilai_max - RATA_RATA_NILAI, left=RATA_RATA_NILAI,
            color='#bbf7d0', alpha=0.7, height=0.35, edgecolor='#172033', linewidth=1.5)
    
    ax.axvline(RATA_RATA_NILAI, color='#172033', linestyle='--', linewidth=2.5, 
               label=f'Rata-rata: {RATA_RATA_NILAI}')
    
    ax.scatter(nilai_akademik, 0, s=500, color='#315efb', zorder=5, 
               edgecolors='#315efb', linewidth=3, marker='D', label=f'Nilai: {nilai_akademik:.2f}')
    
    ax.set_xlim(nilai_min, nilai_max)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xlabel('NILAI AKADEMIK', fontsize=11, fontweight='bold', fontfamily='JetBrains Mono', labelpad=10)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.35), ncol=2, frameon=False, fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#172033')
    plt.tight_layout()
    st.pyplot(fig)
    
    # -------- FAKTOR PENYEBAB --------
    section_header("04", "Faktor Penyebab", f"NILAI {abs(selisih_nilai):.2f} POIN {'DI ATAS' if selisih_nilai > 0 else 'DI BAWAH'} RATA-RATA")
    
    df_kontribusi = pd.DataFrame([
        {'Aspek': k, 'Kontribusi': v, 'Nilai_Siswa': profil_siswa[k],
         'Baseline': BASELINE_ASPEK[k], 'Selisih': profil_siswa[k] - BASELINE_ASPEK[k]}
        for k, v in kontribusi.items()
    ]).sort_values('Kontribusi', key=abs, ascending=True)
    
    col1, col2 = st.columns([2.2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6.5))
        fig.patch.set_facecolor('#f5f7fb')
        ax.set_facecolor('#f5f7fb')
        
        colors = ['#0f766e' if x > 0 else '#c83b4a' for x in df_kontribusi['Kontribusi']]
        bars = ax.barh(df_kontribusi['Aspek'], df_kontribusi['Kontribusi'], 
                       color=colors, edgecolor='#172033', linewidth=1.5, height=0.65)
        ax.axvline(x=0, color='#172033', linestyle='-', linewidth=2)
        ax.set_xlabel('KONTRIBUSI (POIN NILAI)', fontsize=11, fontweight='bold', fontfamily='JetBrains Mono', labelpad=10)
        ax.set_title('Kontribusi Kausal Setiap Faktor', fontsize=15, fontweight='bold', fontfamily='Fraunces', pad=15, loc='left')
        
        for bar, val in zip(bars, df_kontribusi['Kontribusi']):
            pos = val + 0.05 if val > 0 else val - 0.15
            ha = 'left' if val > 0 else 'right'
            ax.text(pos, bar.get_y() + bar.get_height()/2, f'{val:+.2f}', 
                    va='center', ha=ha, fontsize=10, fontweight='bold', fontfamily='JetBrains Mono', color='#172033')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#172033')
        ax.spines['bottom'].set_color('#172033')
        ax.tick_params(colors='#172033')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class="alert alert-info">
            <div class="alert-title">📖 Cara Membaca</div>
            <div style="font-size: 0.85rem; line-height: 1.6; margin-top: 0.5rem;">
            <b style="color: #0f766e;">▲ HIJAU (Positif)</b><br>
            Meningkatkan nilai siswa<br><br>
            <b style="color: #315efb;">▼ MERAH (Negatif)</b><br>
            Menurunkan nilai siswa<br><br>
            <b>ANGKA</b><br>
            Kontribusi dalam poin nilai
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # -------- TABEL DETAIL --------
    section_header("05", "Detail Perbandingan", "PROFIL SISWA VS BASELINE SEKOLAH")
    
    tabel = df_kontribusi.copy()
    tabel['Status'] = tabel['Selisih'].apply(
        lambda x: '▲ Di atas' if x > 0 else '▼ Di bawah' if x < 0 else '● Sama'
    )
    tabel = tabel[['Aspek', 'Nilai_Siswa', 'Baseline', 'Selisih', 'Kontribusi', 'Status']]
    tabel.columns = ['Aspek', 'Nilai Siswa', 'Baseline', 'Selisih', 'Kontribusi (poin)', 'Status']
    tabel = tabel.sort_values('Kontribusi (poin)', key=abs, ascending=False)
    
    st.dataframe(tabel, use_container_width=True, hide_index=True)
    
    # -------- REKOMENDASI --------
    section_header("06", "Rekomendasi Personal", "TINDAK LANJUT SPESIFIK UNTUK SISWA INI")
    
    faktor_positif = df_kontribusi[df_kontribusi['Kontribusi'] > 0.3].sort_values('Kontribusi', ascending=False)
    faktor_negatif = df_kontribusi[df_kontribusi['Kontribusi'] < -0.3].sort_values('Kontribusi')
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="kicker" style="color: #0f766e;"><span class="kicker-line" style="background: #0f766e;"></span>KEKUATAN</div>', unsafe_allow_html=True)
        if len(faktor_positif) > 0:
            for _, row in faktor_positif.iterrows():
                st.markdown(f"""
                <div class="article-card" style="border-color: #0f766e; margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <b style="font-family: 'Fraunces', serif; font-size: 1.1rem;">{row['Aspek']}</b>
                        <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #0f766e;">{row['Kontribusi']:+.2f}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #404040; margin-top: 0.5rem;">
                        Nilai: <b>{row['Nilai_Siswa']:.2f}</b> · Baseline: {row['Baseline']:.2f}
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; letter-spacing: 1px; margin-top: 0.5rem; color: #0f766e;">▲ PERTAHANKAN</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert alert-info">Belum ada faktor kekuatan dominan.</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="kicker" style="color: #315efb;"><span class="kicker-line" style="background: #315efb;"></span>PERLU DIPERBAIKI</div>', unsafe_allow_html=True)
        if len(faktor_negatif) > 0:
            for _, row in faktor_negatif.iterrows():
                st.markdown(f"""
                <div class="article-card" style="border-color: #c83b4a; margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <b style="font-family: 'Fraunces', serif; font-size: 1.1rem;">{row['Aspek']}</b>
                        <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #315efb;">{row['Kontribusi']:+.2f}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #404040; margin-top: 0.5rem;">
                        Nilai: <b>{row['Nilai_Siswa']:.2f}</b> · Baseline: {row['Baseline']:.2f}
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; letter-spacing: 1px; margin-top: 0.5rem; color: #315efb;">▼ TINGKATKAN</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert alert-success">Tidak ada faktor negatif signifikan.</div>', unsafe_allow_html=True)
    
    # -------- SIMPAN --------
    section_header("07", "Simpan Data", "ARSIPKAN KE DATABASE")
    
    if not nama_siswa:
        st.markdown('<div class="alert alert-warning">⚠️ Isi <b>Nama Siswa</b> terlebih dahulu sebelum menyimpan.</div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1, 3])
        with col1:
            tombol = st.button("SIMPAN →", type="primary", use_container_width=True)
        if tombol:
            duplikat = any(
                s['Nama'] == nama_siswa and s['Kelas'] == kelas_siswa
                for s in st.session_state.database_siswa
            )
            if duplikat:
                st.warning(f"⚠️ Siswa **{nama_siswa}** ({kelas_siswa}) sudah ada.")
            else:
                data_baru = {
                    'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'Nama': nama_siswa,
                    'Kelas': kelas_siswa,
                    'Absen': absen_siswa,
                    'Nilai Akademik': round(nilai_akademik, 2),
                    'Selisih': round(selisih_nilai, 2),
                    'Kategori': kategori,
                    'Self-Efficacy': input_self_efficacy,
                    'Keterlibatan Ortu': input_keterlibatan,
                    'Harapan Ortu': input_harapan,
                    'Dukungan Sekolah': input_dukungan,
                    'Motivasi': input_motivasi,
                    'Kecemasan': input_kecemasan,
                    'Fasilitas': input_fasilitas,
                    'Kemalasan': input_kemalasan,
                    'Dicatat Oleh': st.session_state.user_nama,
                }
                st.session_state.database_siswa.append(data_baru)
                st.success(f"✅ Data **{nama_siswa}** berhasil disimpan!")
                st.balloons()

# ================================================================
# MENU 2: DATABASE
# ================================================================

elif menu == "02 · Database Siswa":
    editorial_header(
        "ARSIP",
        "Database<br><span class='masthead-accent'>Siswa.</span>",
        "Kumpulan seluruh siswa yang telah dianalisis beserta faktor-faktor determinan nilai akademiknya."
    )
    
    if len(st.session_state.database_siswa) == 0:
        st.markdown("""
        <div class="article-card" style="text-align: center; padding: 3rem;">
            <div style="font-family: 'Fraunces', serif; font-size: 3rem; color: #315efb;">◯</div>
            <div style="font-family: 'Fraunces', serif; font-size: 1.5rem; font-weight: 700; margin-top: 1rem;">Belum Ada Data</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #737373; letter-spacing: 2px; margin-top: 0.5rem;">SILAKAN INPUT DI MENU 01</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df_db = pd.DataFrame(st.session_state.database_siswa)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            stat_card("Total Siswa", len(df_db), "siswa terdaftar", "stat-card-blue")
        with col2:
            stat_card("Rata-rata", f"{df_db['Nilai Akademik'].mean():.2f}", "dari seluruh siswa", "stat-card-green")
        with col3:
            stat_card("Tertinggi", f"{df_db['Nilai Akademik'].max():.2f}", "nilai maksimum", "stat-card-yellow")
        with col4:
            stat_card("Terendah", f"{df_db['Nilai Akademik'].min():.2f}", "nilai minimum", "stat-card-red")
        
        section_header("01", "Daftar Siswa", "SELURUH DATA TERARSIP")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            filter_kelas = st.selectbox(
                "Filter Kelas",
                ["Semua"] + sorted(df_db['Kelas'].unique().tolist())
            )
        
        df_tampil = df_db if filter_kelas == "Semua" else df_db[df_db['Kelas'] == filter_kelas]
        
        st.markdown(f'<div class="kicker" style="color: #172033;"><span class="kicker-line" style="background: #172033;"></span>{len(df_tampil)} SISWA DITEMUKAN</div>', unsafe_allow_html=True)
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)
        
        st.markdown('<hr class="rule-thin">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            csv = df_tampil.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="↓ DOWNLOAD CSV",
                data=csv,
                file_name=f"database_siswa_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col2:
            if st.button("✕ HAPUS SEMUA DATA", type="secondary", use_container_width=True):
                st.session_state.database_siswa = []
                st.rerun()

# ================================================================
# MENU 3: KAUSAL
# ================================================================

elif menu == "03 · Analisis Kausal":
    editorial_header(
        "METODE 01",
        "Efek Kausal<br><span class='masthead-accent'>(ATE).</span>",
        "Estimasi Average Treatment Effect dari Structural Causal Model (DoWhy) untuk setiap konstruk terhadap prestasi akademik."
    )
    
    ATE_DATA = {
        'Self-Efficacy Akademik': 2.0698,
        'Keterlibatan Orang Tua': 2.2100,
        'Harapan Orang Tua': -1.5323,
        'Dukungan Sekolah': -3.8797,
        'Motivasi Belajar': -0.2850,
        'Kecemasan Akademik': 0.4522,
        'Kemalasan Belajar': -0.0902,
        'Fasilitas Sekolah': 2.4295,
    }
    
    df_ate = pd.DataFrame([
        {'Konstruk': k, 'ATE': v} for k, v in ATE_DATA.items()
    ]).sort_values('ATE', ascending=True)
    
    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor('#f5f7fb')
    ax.set_facecolor('#f5f7fb')
    colors = ['#0f766e' if x > 0 else '#315efb' for x in df_ate['ATE']]
    bars = ax.barh(df_ate['Konstruk'], df_ate['ATE'], color=colors, edgecolor='#172033', linewidth=1.5, height=0.65)
    ax.axvline(x=0, color='#172033', linestyle='-', linewidth=2)
    ax.set_xlabel('ATE (AVERAGE TREATMENT EFFECT)', fontsize=11, fontweight='bold', fontfamily='JetBrains Mono', labelpad=10)
    ax.set_title('Efek Kausal terhadap Prestasi Akademik', fontsize=16, fontweight='bold', fontfamily='Fraunces', pad=15, loc='left')
    for bar, val in zip(bars, df_ate['ATE']):
        pos = val + 0.05 if val > 0 else val - 0.15
        ha = 'left' if val > 0 else 'right'
        ax.text(pos, bar.get_y() + bar.get_height()/2, f'{val:+.2f}', 
                va='center', ha=ha, fontsize=10, fontweight='bold', fontfamily='JetBrains Mono')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.dataframe(df_ate, use_container_width=True, hide_index=True)

# ================================================================
# MENU 4: SHAP
# ================================================================

elif menu == "04 · Analisis SHAP":
    editorial_header(
        "METODE 02",
        "Analisis<br><span class='masthead-accent'>SHAP.</span>",
        "Kontribusi prediktif setiap fitur terhadap model Random Forest, dihitung menggunakan SHapley Additive exPlanations."
    )
    
    SHAP_DATA = {
        'Self-Efficacy Akademik': 0.8008,
        'Keterlibatan Orang Tua': 0.6806,
        'Harapan Orang Tua': 0.5823,
        'Dukungan Sekolah': 0.4352,
        'Motivasi Belajar': 0.3667,
        'Kecemasan Akademik': 0.1308,
        'Fasilitas Sekolah': 0.0654,
        'Kemalasan Belajar': 0.0793,
    }
    
    df_shap = pd.DataFrame([
        {'Konstruk': k, 'Mean_SHAP': v} for k, v in SHAP_DATA.items()
    ]).sort_values('Mean_SHAP', ascending=True)
    
    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor('#f5f7fb')
    ax.set_facecolor('#f5f7fb')
    bars = ax.barh(df_shap['Konstruk'], df_shap['Mean_SHAP'], 
                   color='#315efb', edgecolor='#172033', linewidth=1.5, height=0.65)
    ax.set_xlabel('MEAN |SHAP VALUE|', fontsize=11, fontweight='bold', fontfamily='JetBrains Mono', labelpad=10)
    ax.set_title('Kontribusi Fitur terhadap Prediksi', fontsize=16, fontweight='bold', fontfamily='Fraunces', pad=15, loc='left')
    for bar, val in zip(bars, df_shap['Mean_SHAP']):
        ax.text(val + 0.02, bar.get_y() + bar.get_height()/2, f'{val:.4f}', 
                va='center', fontsize=10, fontweight='bold', fontfamily='JetBrains Mono')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.dataframe(df_shap, use_container_width=True, hide_index=True)

# ================================================================
# MENU 5: REKOMENDASI
# ================================================================

else:
    editorial_header(
        "TINDAK LANJUT",
        "Rekomendasi<br><span class='masthead-accent'>Intervensi.</span>",
        "Sintesis hasil SCM dan SHAP menjadi rekomendasi kebijakan pendidikan yang actionable."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="article-card" style="border-color: #0f766e;">
            <div class="kicker" style="color: #0f766e;"><span class="kicker-line" style="background: #0f766e;"></span>PRIORITAS TINGGI</div>
            <div style="margin-top: 1rem;">
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">01 · Fasilitas Sekolah</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #0f766e; letter-spacing: 1px;">ATE +2.43 · EFEK TERBESAR</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Tingkatkan kualitas perpustakaan dan laboratorium untuk mendukung pembelajaran optimal.
                </div>
            </div>
            <hr style="border: none; border-top: 1px solid #0f766e; opacity: 0.2; margin: 1rem 0;">
            <div>
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">02 · Keterlibatan Orang Tua</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #0f766e; letter-spacing: 1px;">ATE +2.21 · SHAP 0.68</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Program parenting dan komunikasi rutin sekolah-orang tua untuk pendampingan belajar.
                </div>
            </div>
            <hr style="border: none; border-top: 1px solid #0f766e; opacity: 0.2; margin: 1rem 0;">
            <div>
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">03 · Self-Efficacy</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #0f766e; letter-spacing: 1px;">ATE +2.07 · SHAP 0.80</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Penguatan kepercayaan diri siswa melalui mentoring dan pelatihan motivasi.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="article-card" style="border-color: #315efb;">
            <div class="kicker" style="color: #315efb;"><span class="kicker-line" style="background: #315efb;"></span>PERLU EVALUASI</div>
            <div style="margin-top: 1rem;">
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">01 · Dukungan Sekolah</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #315efb; letter-spacing: 1px;">ATE -3.88 · ANOMALI</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Over-support dari sekolah menurunkan kemandirian. Evaluasi program pendampingan.
                </div>
            </div>
            <hr style="border: none; border-top: 1px solid #315efb; opacity: 0.2; margin: 1rem 0;">
            <div>
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">02 · Harapan Orang Tua</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #315efb; letter-spacing: 1px;">ATE -1.53</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Tekanan berlebihan menimbulkan kecemasan. Edukasi target realistis.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="article-card-black">
        <div class="kicker" style="color: #315efb;"><span class="kicker-line" style="background: #315efb;"></span>KESIMPULAN PENELITIAN</div>
        <div style="font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 700; line-height: 1.2; margin-top: 1rem;">
        Tiga faktor terbukti secara kausal dan prediktif mempengaruhi prestasi akademik siswa SMP Negeri 6 Salatiga.
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #315efb; letter-spacing: 2px; margin-top: 1.5rem;">
        ■ FASILITAS SEKOLAH · ■ KETERLIBATAN ORANG TUA · ■ SELF-EFFICACY
        </div>
    </div>
    """, unsafe_allow_html=True)
