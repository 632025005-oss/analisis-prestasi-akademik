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
# CUSTOM CSS - EDITORIAL / MAGAZINE STYLE
# ================================================================


st.markdown("""
<style>
/* ============================================================
   MODERN ACADEMIC DASHBOARD
   Clean / premium / restrained — no excessive decoration
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

:root {
    --ink: #172033;
    --muted: #667085;
    --line: #E6EAF0;
    --surface: #FFFFFF;
    --canvas: #F6F8FB;
    --navy: #172554;
    --blue: #315EFB;
    --blue-soft: #EEF3FF;
    --teal: #0F766E;
    --teal-soft: #ECFDF8;
    --red: #C83B4A;
    --red-soft: #FFF1F3;
    --amber: #B7791F;
    --amber-soft: #FFF8E7;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

.stApp {
    background: var(--canvas);
}

.main {
    background: var(--canvas);
}

.block-container {
    max-width: 1440px;
    padding: 2rem 3rem 4rem 3rem;
}

/* Hide Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---------- Typography ---------- */
.masthead {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2.7rem, 5vw, 4.4rem);
    font-weight: 800;
    line-height: .98;
    letter-spacing: -3px;
    color: var(--ink);
    margin: 0;
}

.masthead-accent {
    color: var(--blue);
    font-style: normal;
}

.kicker {
    font-family: 'DM Sans', sans-serif;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: 1.7px;
    text-transform: uppercase;
    color: var(--blue);
    margin-bottom: .65rem;
}

.kicker-line {
    display: inline-block;
    width: 24px;
    height: 2px;
    background: var(--blue);
    vertical-align: middle;
    margin-right: 9px;
    margin-bottom: 2px;
}

.deck {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.65;
    color: var(--muted);
    max-width: 760px;
    margin-top: 1rem;
}

.section-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--ink);
    letter-spacing: -.7px;
    line-height: 1.15;
    margin: 0;
}

.section-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: .68rem;
    color: var(--muted);
    letter-spacing: 1.3px;
    text-transform: uppercase;
    font-weight: 700;
    margin-top: .35rem;
}

.rule-thick {
    height: 1px;
    background: var(--line);
    margin: 1.35rem 0;
    border: none;
}

.rule-thin {
    height: 1px;
    background: var(--line);
    margin: 1.7rem 0;
    border: none;
}

.rule-red {
    height: 3px;
    background: var(--blue);
    width: 42px;
    margin: .8rem 0 1.4rem 0;
    border: none;
    border-radius: 99px;
}

/* ---------- Header ---------- */
[data-testid="stVerticalBlock"] .dashboard-header {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    box-shadow: 0 8px 28px rgba(23,32,51,.045);
}

/* ---------- Cards ---------- */
.article-card,
.article-card-red,
.article-card-black,
.stat-card,
.process-box {
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(23,32,51,.045);
}

.article-card {
    background: var(--surface);
    border: 1px solid var(--line);
    padding: 1.35rem 1.5rem;
    position: relative;
}

.article-card::before {
    display: none;
}

.article-card-red {
    background: var(--red-soft);
    color: var(--ink);
    border: 1px solid #F5CDD2;
    padding: 1.35rem 1.5rem;
}

.article-card-black {
    background: var(--navy);
    color: #fff;
    border: 1px solid var(--navy);
    padding: 1.7rem 1.8rem;
}

.stat-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-top: 3px solid var(--blue);
    padding: 1.15rem 1.25rem;
    min-height: 108px;
    transition: transform .18s ease, box-shadow .18s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(23,32,51,.08);
}

.stat-card-red { border-top-color: var(--red); }
.stat-card-yellow { border-top-color: var(--amber); }
.stat-card-blue { border-top-color: var(--blue); }
.stat-card-green { border-top-color: var(--teal); }

.stat-label {
    font-size: .68rem;
    letter-spacing: 1.15px;
    text-transform: uppercase;
    color: var(--muted);
    font-weight: 700;
    margin-bottom: .55rem;
}

.stat-value {
    font-family: 'Manrope', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    color: var(--ink);
    letter-spacing: -1px;
}

.stat-unit {
    font-size: .78rem;
    color: var(--muted);
    margin-top: .45rem;
}

/* ---------- Alerts ---------- */
.alert {
    padding: .95rem 1.1rem;
    border: 1px solid var(--line);
    border-left: 4px solid var(--blue);
    border-radius: 12px;
    background: var(--surface);
    margin: 1rem 0;
    font-size: .88rem;
    box-shadow: 0 5px 18px rgba(23,32,51,.035);
}

.alert-info { border-left-color: var(--blue); background: var(--blue-soft); }
.alert-success { border-left-color: var(--teal); background: var(--teal-soft); }
.alert-warning { border-left-color: var(--amber); background: var(--amber-soft); }
.alert-danger { border-left-color: var(--red); background: var(--red-soft); }

.alert-title {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: .95rem;
    margin-bottom: .25rem;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--navy);
    border-right: 0;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.25rem 1rem;
}

[data-testid="stSidebar"] * {
    color: #E8ECF7 !important;
}

[data-testid="stSidebar"] .kicker {
    color: #9DB5FF !important;
}

[data-testid="stSidebar"] .kicker-line {
    background: #9DB5FF !important;
}

[data-testid="stSidebar"] .stRadio > label {
    font-size: .67rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #AAB5CB !important;
    margin-bottom: .5rem;
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    gap: .35rem;
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: .72rem .75rem !important;
    transition: all .15s ease;
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: rgba(255,255,255,.07);
    border-color: rgba(255,255,255,.08);
}

[data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"] {
    background: rgba(49,94,251,.22);
    border-color: rgba(157,181,255,.2);
}

[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,.06);
    color: #fff !important;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 10px;
    box-shadow: none;
    text-transform: none;
    letter-spacing: 0;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,.11);
    border-color: rgba(255,255,255,.2);
    transform: none;
    box-shadow: none;
}

/* ---------- Inputs ---------- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background: var(--surface) !important;
    border: 1px solid #D7DDE8 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .9rem !important;
    color: var(--ink) !important;
    min-height: 42px;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(49,94,251,.10) !important;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label {
    font-size: .72rem !important;
    color: #475467 !important;
    font-weight: 700 !important;
    letter-spacing: .2px !important;
}

/* ---------- Sliders ---------- */
.stSlider label {
    font-size: .82rem !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
}

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--blue) !important;
}

/* ---------- Buttons ---------- */
.stButton > button,
.stDownloadButton > button,
button[kind="primary"] {
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: .82rem;
    min-height: 42px;
    box-shadow: none;
    transition: all .15s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px);
}

button[kind="primary"] {
    background: var(--blue) !important;
    border: 1px solid var(--blue) !important;
    color: #fff !important;
}

/* ---------- Tables ---------- */
.stDataFrame {
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(23,32,51,.035);
}

/* ---------- Login ---------- */
.login-hero {
    background: var(--navy);
    color: #fff;
    padding: 3rem 2rem;
    text-align: left;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 20px;
    box-shadow: 0 18px 50px rgba(23,37,84,.16);
    position: relative;
    overflow: hidden;
}

.login-hero::before {
    content: '';
    position: absolute;
    width: 230px;
    height: 230px;
    border-radius: 50%;
    border: 1px solid rgba(157,181,255,.18);
    right: -90px;
    top: -90px;
}

.login-hero::after {
    content: 'ACADEMIC ANALYTICS';
    position: absolute;
    bottom: 18px;
    right: 24px;
    font-size: .58rem;
    letter-spacing: 1.7px;
    color: #9DB5FF;
}

.login-title-main {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4rem);
    font-weight: 800;
    line-height: .98;
    letter-spacing: -2.5px;
    margin: 0;
}

.login-title-main em {
    color: #9DB5FF;
    font-style: normal;
}

/* ---------- Tags ---------- */
.label-tag {
    display: inline-block;
    padding: .35rem .65rem;
    background: var(--blue-soft);
    color: var(--blue);
    border: 1px solid #D8E2FF;
    border-radius: 999px;
    font-size: .62rem;
    letter-spacing: .8px;
    text-transform: uppercase;
    font-weight: 800;
}

.label-tag-red { background: var(--red-soft); color: var(--red); border-color: #F5CDD2; }
.label-tag-yellow { background: var(--amber-soft); color: var(--amber); border-color: #F4DFAB; }
.label-tag-green { background: var(--teal-soft); color: var(--teal); border-color: #BFE8DF; }
.label-tag-blue { background: var(--blue-soft); color: var(--blue); border-color: #D8E2FF; }

/* ---------- Process ---------- */
.process-box {
    background: var(--surface);
    border: 1px solid var(--line);
    padding: 1.2rem;
    margin: .8rem 0;
}

.process-box-number {
    font-family: 'Manrope', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--blue);
    line-height: 1;
}

/* ---------- Responsive ---------- */
@media (max-width: 900px) {
    .block-container {
        padding: 1.25rem 1rem 3rem 1rem;
    }

    .masthead {
        letter-spacing: -2px;
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
        return "Sangat Baik", "#166534", "▲"
    elif nilai >= 84:
        return "Baik", "#1e40af", "●"
    elif nilai >= 80:
        return "Cukup", "#eab308", "◆"
    else:
        return "Perlu Perhatian", "#dc2626", "▼"


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
            <span style="font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 900; color: #dc2626; line-height: 1;">{num}</span>
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
            <div class="kicker" style="color: #dc2626; text-align: center; margin-bottom: 1rem;">
                <span class="kicker-line" style="background: #dc2626;"></span>SISTEM INFORMASI AKADEMIK
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
            st.markdown('<div class="kicker" style="color: #1a1a1a;"><span class="kicker-line" style="background: #1a1a1a;"></span>MASUK</div>', unsafe_allow_html=True)
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
        <div class="kicker" style="color: #dc2626;"><span class="kicker-line" style="background: #dc2626;"></span>DASHBOARD</div>
        <h1 style="font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 900; line-height: 1; letter-spacing: -1px; margin: 0.3rem 0; color: #faf6f0;">
            Prestasi<br><em style="color: #dc2626;">Akademik.</em>
        </h1>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 2px; color: #737373; margin-top: 0.5rem;">SMPN 6 SALATIGA / 2026</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr style="border: none; border-top: 1px solid rgba(250,246,240,0.15); margin: 1rem 0;">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #dc2626; padding: 0.8rem; margin-bottom: 1rem;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; color: #faf6f0; opacity: 0.8;">USER AKTIF</div>
        <div style="font-family: 'Fraunces', serif; font-size: 1.1rem; font-weight: 700; color: #faf6f0; margin-top: 0.2rem;">{st.session_state.user_nama}</div>
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
            <div class="kicker" style="color: #1a1a1a;"><span class="kicker-line" style="background: #1a1a1a;"></span>SUBJEK ANALISIS</div>
            <div style="font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 700; color: #1a1a1a; line-height: 1; margin-top: 0.3rem;">{nama_siswa}</div>
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
    fig.patch.set_facecolor('#F6F8FB')
    ax.set_facecolor('#F6F8FB')
    
    nilai_min, nilai_max = 75, 95
    ax.barh(0, RATA_RATA_NILAI - nilai_min, left=nilai_min, 
            color='#fecaca', alpha=0.7, height=0.35, edgecolor='#1a1a1a', linewidth=1.5)
    ax.barh(0, nilai_max - RATA_RATA_NILAI, left=RATA_RATA_NILAI,
            color='#bbf7d0', alpha=0.7, height=0.35, edgecolor='#1a1a1a', linewidth=1.5)
    
    ax.axvline(RATA_RATA_NILAI, color='#1a1a1a', linestyle='--', linewidth=2.5, 
               label=f'Rata-rata: {RATA_RATA_NILAI}')
    
    ax.scatter(nilai_akademik, 0, s=500, color='#dc2626', zorder=5, 
               edgecolors='#1a1a1a', linewidth=3, marker='D', label=f'Nilai: {nilai_akademik:.2f}')
    
    ax.set_xlim(nilai_min, nilai_max)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xlabel('NILAI AKADEMIK', fontsize=11, fontweight='bold', fontfamily='JetBrains Mono', labelpad=10)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.35), ncol=2, frameon=False, fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#1a1a1a')
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
        fig.patch.set_facecolor('#F6F8FB')
        ax.set_facecolor('#F6F8FB')
        
        colors = ['#166534' if x > 0 else '#dc2626' for x in df_kontribusi['Kontribusi']]
        bars = ax.barh(df_kontribusi['Aspek'], df_kontribusi['Kontribusi'], 
                       color=colors, edgecolor='#1a1a1a', linewidth=1.5, height=0.65)
        ax.axvline(x=0, color='#1a1a1a', linestyle='-', linewidth=2)
        ax.set_xlabel('KONTRIBUSI (POIN NILAI)', fontsize=11, fontweight='bold', fontfamily='JetBrains Mono', labelpad=10)
        ax.set_title('Kontribusi Kausal Setiap Faktor', fontsize=15, fontweight='bold', fontfamily='Fraunces', pad=15, loc='left')
        
        for bar, val in zip(bars, df_kontribusi['Kontribusi']):
            pos = val + 0.05 if val > 0 else val - 0.15
            ha = 'left' if val > 0 else 'right'
            ax.text(pos, bar.get_y() + bar.get_height()/2, f'{val:+.2f}', 
                    va='center', ha=ha, fontsize=10, fontweight='bold', fontfamily='JetBrains Mono', color='#1a1a1a')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#1a1a1a')
        ax.spines['bottom'].set_color('#1a1a1a')
        ax.tick_params(colors='#1a1a1a')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class="alert alert-info">
            <div class="alert-title">📖 Cara Membaca</div>
            <div style="font-size: 0.85rem; line-height: 1.6; margin-top: 0.5rem;">
            <b style="color: #166534;">▲ HIJAU (Positif)</b><br>
            Meningkatkan nilai siswa<br><br>
            <b style="color: #dc2626;">▼ MERAH (Negatif)</b><br>
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
        st.markdown('<div class="kicker" style="color: #166534;"><span class="kicker-line" style="background: #166534;"></span>KEKUATAN</div>', unsafe_allow_html=True)
        if len(faktor_positif) > 0:
            for _, row in faktor_positif.iterrows():
                st.markdown(f"""
                <div class="article-card" style="border-color: #166534; margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <b style="font-family: 'Fraunces', serif; font-size: 1.1rem;">{row['Aspek']}</b>
                        <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #166534;">{row['Kontribusi']:+.2f}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #404040; margin-top: 0.5rem;">
                        Nilai: <b>{row['Nilai_Siswa']:.2f}</b> · Baseline: {row['Baseline']:.2f}
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; letter-spacing: 1px; margin-top: 0.5rem; color: #166534;">▲ PERTAHANKAN</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert alert-info">Belum ada faktor kekuatan dominan.</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="kicker" style="color: #dc2626;"><span class="kicker-line" style="background: #dc2626;"></span>PERLU DIPERBAIKI</div>', unsafe_allow_html=True)
        if len(faktor_negatif) > 0:
            for _, row in faktor_negatif.iterrows():
                st.markdown(f"""
                <div class="article-card" style="border-color: #dc2626; margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <b style="font-family: 'Fraunces', serif; font-size: 1.1rem;">{row['Aspek']}</b>
                        <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #dc2626;">{row['Kontribusi']:+.2f}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #404040; margin-top: 0.5rem;">
                        Nilai: <b>{row['Nilai_Siswa']:.2f}</b> · Baseline: {row['Baseline']:.2f}
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; letter-spacing: 1px; margin-top: 0.5rem; color: #dc2626;">▼ TINGKATKAN</div>
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
            <div style="font-family: 'Fraunces', serif; font-size: 3rem; color: #dc2626;">◯</div>
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
        
        st.markdown(f'<div class="kicker" style="color: #1a1a1a;"><span class="kicker-line" style="background: #1a1a1a;"></span>{len(df_tampil)} SISWA DITEMUKAN</div>', unsafe_allow_html=True)
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
    fig.patch.set_facecolor('#F6F8FB')
    ax.set_facecolor('#F6F8FB')
    colors = ['#166534' if x > 0 else '#dc2626' for x in df_ate['ATE']]
    bars = ax.barh(df_ate['Konstruk'], df_ate['ATE'], color=colors, edgecolor='#1a1a1a', linewidth=1.5, height=0.65)
    ax.axvline(x=0, color='#1a1a1a', linestyle='-', linewidth=2)
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
    fig.patch.set_facecolor('#F6F8FB')
    ax.set_facecolor('#F6F8FB')
    bars = ax.barh(df_shap['Konstruk'], df_shap['Mean_SHAP'], 
                   color='#315EFB', edgecolor='#D7DDE8', linewidth=1.5, height=0.65)
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
        <div class="article-card" style="border-color: #166534;">
            <div class="kicker" style="color: #166534;"><span class="kicker-line" style="background: #166534;"></span>PRIORITAS TINGGI</div>
            <div style="margin-top: 1rem;">
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">01 · Fasilitas Sekolah</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #166534; letter-spacing: 1px;">ATE +2.43 · EFEK TERBESAR</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Tingkatkan kualitas perpustakaan dan laboratorium untuk mendukung pembelajaran optimal.
                </div>
            </div>
            <hr style="border: none; border-top: 1px solid #166534; opacity: 0.2; margin: 1rem 0;">
            <div>
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">02 · Keterlibatan Orang Tua</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #166534; letter-spacing: 1px;">ATE +2.21 · SHAP 0.68</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Program parenting dan komunikasi rutin sekolah-orang tua untuk pendampingan belajar.
                </div>
            </div>
            <hr style="border: none; border-top: 1px solid #166534; opacity: 0.2; margin: 1rem 0;">
            <div>
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">03 · Self-Efficacy</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #166534; letter-spacing: 1px;">ATE +2.07 · SHAP 0.80</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Penguatan kepercayaan diri siswa melalui mentoring dan pelatihan motivasi.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="article-card" style="border-color: #dc2626;">
            <div class="kicker" style="color: #dc2626;"><span class="kicker-line" style="background: #dc2626;"></span>PERLU EVALUASI</div>
            <div style="margin-top: 1rem;">
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">01 · Dukungan Sekolah</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #dc2626; letter-spacing: 1px;">ATE -3.88 · ANOMALI</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Over-support dari sekolah menurunkan kemandirian. Evaluasi program pendampingan.
                </div>
            </div>
            <hr style="border: none; border-top: 1px solid #dc2626; opacity: 0.2; margin: 1rem 0;">
            <div>
                <div style="font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem;">02 · Harapan Orang Tua</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #dc2626; letter-spacing: 1px;">ATE -1.53</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #404040;">
                Tekanan berlebihan menimbulkan kecemasan. Edukasi target realistis.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="article-card-black">
        <div class="kicker" style="color: #dc2626;"><span class="kicker-line" style="background: #dc2626;"></span>KESIMPULAN PENELITIAN</div>
        <div style="font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 700; line-height: 1.2; margin-top: 1rem;">
        Tiga faktor terbukti secara kausal dan prediktif mempengaruhi prestasi akademik siswa SMP Negeri 6 Salatiga.
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #dc2626; letter-spacing: 2px; margin-top: 1.5rem;">
        ■ FASILITAS SEKOLAH · ■ KETERLIBATAN ORANG TUA · ■ SELF-EFFICACY
        </div>
    </div>
    """, unsafe_allow_html=True)
