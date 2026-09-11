import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import hashlib

st.set_page_config(
    page_title="Dashboard Prestasi Akademik - SMPN 6 Salatiga",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# CUSTOM CSS - TEMA PENDIDIKAN
# ================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f0f9ff 0%, #ecfdf5 50%, #fef3c7 100%);
        background-attachment: fixed;
    }
    
    /* HERO BANNER */
    .hero-banner {
        background: linear-gradient(135deg, #2563eb 0%, #10b981 100%);
        padding: 2.5rem 2rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        animation: pulse 12s infinite;
    }
    
    .hero-banner::after {
        content: '🎓📚✏️🎯';
        position: absolute;
        top: 15px;
        right: 25px;
        font-size: 1.5rem;
        opacity: 0.3;
        letter-spacing: 8px;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.15); opacity: 0.8; }
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        font-weight: 400;
        opacity: 0.95;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* METRIC CARDS */
    .metric-card {
        background: white;
        padding: 1.4rem;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.1);
        border-left: 6px solid #2563eb;
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 80px;
        height: 80px;
        background: radial-gradient(circle, rgba(37,99,235,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.2);
    }
    
    .metric-icon { font-size: 1.8rem; margin-bottom: 0.3rem; }
    .metric-label {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0.2rem 0;
        letter-spacing: -0.5px;
    }
    .metric-delta { font-size: 0.8rem; font-weight: 600; }
    
    /* SECTION HEADER */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem 0 0.5rem 1rem;
        border-left: 5px solid #10b981;
        background: linear-gradient(90deg, rgba(16,185,129,0.08) 0%, transparent 100%);
        border-radius: 0 10px 10px 0;
    }
    
    /* INFO BOXES */
    .info-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        padding: 1.2rem;
        border-radius: 14px;
        border-left: 5px solid #2563eb;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(37,99,235,0.08);
    }
    .success-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 1.2rem;
        border-radius: 14px;
        border-left: 5px solid #10b981;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(16,185,129,0.08);
    }
    .warning-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        padding: 1.2rem;
        border-radius: 14px;
        border-left: 5px solid #f59e0b;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(245,158,11,0.08);
    }
    .danger-box {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        padding: 1.2rem;
        border-radius: 14px;
        border-left: 5px solid #ef4444;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(239,68,68,0.08);
    }
    .purple-box {
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        padding: 1.2rem;
        border-radius: 14px;
        border-left: 5px solid #8b5cf6;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(139,92,246,0.08);
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #064e3b 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-weight: 500;
        padding: 0.5rem 0;
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #10b981 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
        font-family: 'Poppins', sans-serif;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(37, 99, 235, 0.4);
    }
    
    /* INPUTS */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        font-family: 'Poppins', sans-serif;
        padding: 0.5rem 0.8rem;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }
    .stSelectbox > div > div > div {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    /* SLIDER */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #2563eb 0%, #10b981 100%);
    }
    
    /* DATAFRAME */
    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(37,99,235,0.08);
    }
    
    /* LOGIN PAGE */
    .login-container {
        max-width: 420px;
        margin: 3rem auto;
        padding: 2.5rem 2rem;
        background: white;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(37, 99, 235, 0.2);
        border-top: 6px solid #2563eb;
    }
    .login-logo {
        text-align: center;
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }
    .login-title {
        text-align: center;
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.3rem;
    }
    .login-subtitle {
        text-align: center;
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    
    /* Hide branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* DIVIDER */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #2563eb, #10b981, transparent);
        margin: 2rem 0;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ================================================================
# DATABASE USER (GURU)
# ================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Akun default (bisa ditambah)
USERS = {
    'admin': {
        'password': hash_password('admin123'),
        'nama': 'Administrator',
        'role': 'admin'
    },
    'guru': {
        'password': hash_password('guru123'),
        'nama': 'Guru SMPN 6',
        'role': 'guru'
    },
    'regina': {
        'password': hash_password('regina2026'),
        'nama': 'Regina Ria Aurellia',
        'role': 'peneliti'
    },
}

# ================================================================
# SESSION STATE
# ================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_nama' not in st.session_state:
    st.session_state.user_nama = None
if 'database_siswa' not in st.session_state:
    st.session_state.database_siswa = []

# ================================================================
# DATA BASELINE & BOBOT
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
        return "🌟 Sangat Baik", "#10b981"
    elif nilai >= 84:
        return "✅ Baik", "#2563eb"
    elif nilai >= 80:
        return "⚠️ Cukup", "#f59e0b"
    else:
        return "❗ Perlu Perhatian", "#ef4444"


def render_hero(title, subtitle, icon="🎓"):
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">{icon} {title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_metric(icon, label, value, delta=None, color="#2563eb"):
    delta_html = f'<div class="metric-delta" style="color: {color};">{delta}</div>' if delta else ''
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {color};">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

# ================================================================
# HALAMAN LOGIN
# ================================================================

def halaman_login():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-logo">🎓</div>
            <div class="login-title">Dashboard Prestasi Akademik</div>
            <div class="login-subtitle">SMP Negeri 6 Salatiga</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Masukkan username")
            password = st.text_input("🔒 Password", type="password", placeholder="Masukkan password")
            
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit:
                if username in USERS and USERS[username]['password'] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_nama = USERS[username]['nama']
                    st.success(f"✅ Selamat datang, {USERS[username]['nama']}!")
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
        
        with st.expander("🔑 Info Akun Demo"):
            st.markdown("""
            **Akun Demo:**
            - 👤 `admin` / 🔒 `admin123`
            - 👤 `guru` / 🔒 `guru123`
            - 👤 `regina` / 🔒 `regina2026`
            """)

# ================================================================
# CEK LOGIN
# ================================================================

if not st.session_state.logged_in:
    halaman_login()
    st.stop()

# ================================================================
# SIDEBAR (SETELAH LOGIN)
# ================================================================

with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem;">🎓</div>
        <h3 style="color: white; margin: 0.3rem 0; font-weight: 700;">Dashboard</h3>
        <p style="color: #cbd5e1; font-size: 0.85rem;">Analisis Prestasi Akademik</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #10b981 0%, #2563eb 100%); 
                padding: 0.8rem; border-radius: 12px; margin: 1rem 0; text-align: center;">
        <p style="color: white; font-size: 0.75rem; margin: 0; opacity: 0.9;">LOGIN SEBAGAI</p>
        <p style="color: white; font-size: 0.95rem; margin: 0.2rem 0; font-weight: 700;">
            👤 {st.session_state.user_nama}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "📌 MENU",
        [
            "🔍 Analisis Sebab-Akibat",
            "🗄️ Database Siswa",
            "📊 Analisis Kausal",
            "📈 Analisis SHAP",
            "💡 Rekomendasi"
        ]
    )
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_nama = None
        st.rerun()
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 10px; 
                margin-top: 1rem; text-align: center;">
        <p style="color: #cbd5e1; font-size: 0.8rem; margin: 0;">
        📍 <b>SMP Negeri 6 Salatiga</b><br>
        <span style="font-size: 0.7rem;">© 2026</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# MENU 1: ANALISIS SEBAB-AKIBAT
# ================================================================

if menu == "🔍 Analisis Sebab-Akibat":
    render_hero(
        "Analisis Sebab-Akibat Nilai Siswa",
        "Masukkan data siswa untuk menganalisis faktor penyebab nilai akademiknya",
        "🔍"
    )
    
    render_section("👤 Data Siswa")
    col1, col2, col3 = st.columns(3)
    with col1:
        nama_siswa = st.text_input("Nama Siswa", placeholder="Contoh: Ahmad Rizki")
    with col2:
        kelas_siswa = st.selectbox("Kelas", KELAS_LIST, index=KELAS_LIST.index("IX-A"))
    with col3:
        absen_siswa = st.number_input("No. Absen", min_value=1, max_value=50, value=1)
    
    render_section("📊 Nilai Akademik")
    col1, col2 = st.columns([2, 1])
    with col1:
        nilai_akademik = st.number_input(
            "Nilai Rata-rata Rapor",
            min_value=60.0, max_value=100.0, value=83.78, step=0.01,
            format="%.2f"
        )
    with col2:
        selisih_awal = nilai_akademik - RATA_RATA_NILAI
        color_delta = "#10b981" if selisih_awal >= 0 else "#ef4444"
        render_metric("📍", "Posisi Nilai", f"{selisih_awal:+.2f}", "dari rata-rata", color_delta)
    
    render_section("📝 Profil Siswa")
    st.caption("Skala 1-5 (1=Sangat Rendah, 5=Sangat Tinggi)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 🧠 Aspek Internal")
        input_self_efficacy = st.slider("Self-Efficacy Akademik", 1.0, 5.0, 4.63, 0.1)
        input_motivasi = st.slider("Motivasi Belajar", 1.0, 5.0, 2.52, 0.1)
        input_kecemasan = st.slider("Kecemasan Akademik", 1.0, 5.0, 2.89, 0.1)
        input_kemalasan = st.slider("Kemalasan Belajar", 1.0, 5.0, 1.49, 0.1)
    with col2:
        st.markdown("##### 🌍 Aspek Eksternal")
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
    kategori, warna_kategori = kategori_nilai(nilai_akademik)
    
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    render_section("🎯 Hasil Analisis")
    
    if nama_siswa:
        st.markdown(f"""
        <div class="info-box">
            <b>👤 {nama_siswa}</b> &nbsp;|&nbsp; 
            <b>🏫 {kelas_siswa}</b> &nbsp;|&nbsp; 
            <b>📌 No. {absen_siswa}</b>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric("📊", "Nilai Akademik", f"{nilai_akademik:.2f}", color="#2563eb")
    with col2:
        delta_color = "#10b981" if selisih_nilai >= 0 else "#ef4444"
        render_metric("📈", "Posisi", f"{selisih_nilai:+.2f}", "dari rata-rata", delta_color)
    with col3:
        render_metric("🏆", "Kategori", kategori, color=warna_kategori)
    
    render_section("📍 Posisi Nilai Siswa")
    
    fig, ax = plt.subplots(figsize=(12, 2.5))
    fig.patch.set_facecolor('#f0f9ff')
    ax.set_facecolor('#f0f9ff')
    
    nilai_min, nilai_max = 75, 95
    ax.barh(0, RATA_RATA_NILAI - nilai_min, left=nilai_min, color='#fecaca', alpha=0.6, height=0.4)
    ax.barh(0, nilai_max - RATA_RATA_NILAI, left=RATA_RATA_NILAI, color='#bbf7d0', alpha=0.6, height=0.4)
    ax.axvline(RATA_RATA_NILAI, color='#ef4444', linestyle='--', linewidth=2, 
               label=f'Rata-rata: {RATA_RATA_NILAI}')
    ax.scatter(nilai_akademik, 0, s=400, color='#2563eb', zorder=5, 
               edgecolors='white', linewidth=3, label=f'Nilai: {nilai_akademik:.2f}')
    
    ax.set_xlim(nilai_min, nilai_max)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xlabel('Nilai Akademik', fontsize=12, fontweight='bold')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.5), ncol=2, frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    
    render_section("🔍 Faktor Penyebab Nilai")
    st.caption(f"Nilai siswa berada **{abs(selisih_nilai):.2f} poin** {'di atas' if selisih_nilai > 0 else 'di bawah'} rata-rata sekolah.")
    
    df_kontribusi = pd.DataFrame([
        {'Aspek': k, 'Kontribusi': v, 'Nilai_Siswa': profil_siswa[k],
         'Baseline': BASELINE_ASPEK[k], 'Selisih': profil_siswa[k] - BASELINE_ASPEK[k]}
        for k, v in kontribusi.items()
    ]).sort_values('Kontribusi', key=abs, ascending=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#f0f9ff')
        ax.set_facecolor('#f0f9ff')
        
        colors = ['#10b981' if x > 0 else '#ef4444' for x in df_kontribusi['Kontribusi']]
        bars = ax.barh(df_kontribusi['Aspek'], df_kontribusi['Kontribusi'], 
                       color=colors, alpha=0.85, edgecolor='white', linewidth=2)
        ax.axvline(x=0, color='#0f172a', linestyle='-', alpha=0.5)
        ax.set_xlabel('Kontribusi (poin nilai)', fontsize=12, fontweight='bold')
        ax.set_title('Kontribusi Setiap Faktor', fontsize=14, fontweight='bold', pad=20)
        
        for bar, val in zip(bars, df_kontribusi['Kontribusi']):
            pos = val + 0.05 if val > 0 else val - 0.15
            ax.text(pos, bar.get_y() + bar.get_height()/2, f'{val:+.2f}', 
                    va='center', fontsize=10, fontweight='bold')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <b>📖 Cara Membaca</b><br><br>
        <b style="color: #10b981;">🟢 Hijau (Positif)</b><br>
        Meningkatkan nilai siswa<br><br>
        <b style="color: #ef4444;">🔴 Merah (Negatif)</b><br>
        Menurunkan nilai siswa<br><br>
        <b>Angka</b><br>
        Kontribusi dalam <b>poin nilai</b>
        </div>
        """, unsafe_allow_html=True)
    
    render_section("📋 Detail Perbandingan")
    tabel = df_kontribusi.copy()
    tabel['Status'] = tabel['Selisih'].apply(
        lambda x: '⬆️ Di atas' if x > 0 else '⬇️ Di bawah' if x < 0 else '➡️ Sama'
    )
    tabel = tabel[['Aspek', 'Nilai_Siswa', 'Baseline', 'Selisih', 'Kontribusi', 'Status']]
    tabel.columns = ['Aspek', 'Nilai Siswa', 'Rata-rata', 'Selisih', 'Kontribusi (poin)', 'Status']
    tabel = tabel.sort_values('Kontribusi (poin)', key=abs, ascending=False)
    st.dataframe(tabel, use_container_width=True, hide_index=True)
    
    render_section("💡 Rekomendasi Personal")
    faktor_positif = df_kontribusi[df_kontribusi['Kontribusi'] > 0.3].sort_values('Kontribusi', ascending=False)
    faktor_negatif = df_kontribusi[df_kontribusi['Kontribusi'] < -0.3].sort_values('Kontribusi')
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: #065f46;">✅ KEKUATAN SISWA</h4>', unsafe_allow_html=True)
        if len(faktor_positif) > 0:
            for _, row in faktor_positif.iterrows():
                st.markdown(f"""
                <div class="success-box">
                <b>{row['Aspek']}</b><br>
                Kontribusi: <b style="color: #10b981;">{row['Kontribusi']:+.2f} poin</b><br>
                Nilai: {row['Nilai_Siswa']:.2f} (rata-rata: {row['Baseline']:.2f})<br>
                <em>📌 Pertahankan!</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada faktor kekuatan dominan")
    
    with col2:
        st.markdown('<h4 style="color: #991b1b;">⚠️ PERLU DIPERBAIKI</h4>', unsafe_allow_html=True)
        if len(faktor_negatif) > 0:
            for _, row in faktor_negatif.iterrows():
                st.markdown(f"""
                <div class="danger-box">
                <b>{row['Aspek']}</b><br>
                Kontribusi: <b style="color: #ef4444;">{row['Kontribusi']:+.2f} poin</b><br>
                Nilai: {row['Nilai_Siswa']:.2f} (rata-rata: {row['Baseline']:.2f})<br>
                <em>📌 Perlu ditingkatkan!</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Tidak ada faktor negatif signifikan")
    
    render_section("💾 Simpan ke Database")
    if not nama_siswa:
        st.markdown('<div class="warning-box">⚠️ Isi <b>Nama Siswa</b> terlebih dahulu sebelum menyimpan.</div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1, 3])
        with col1:
            tombol = st.button("💾 Simpan Data", type="primary", use_container_width=True)
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
# MENU 2: DATABASE SISWA
# ================================================================

elif menu == "🗄️ Database Siswa":
    render_hero("Database Siswa", "Daftar semua siswa yang sudah dianalisis", "🗄️")
    
    if len(st.session_state.database_siswa) == 0:
        st.markdown('<div class="info-box">📭 Belum ada data siswa. Silakan input di menu <b>🔍 Analisis Sebab-Akibat</b>.</div>', unsafe_allow_html=True)
    else:
        df_db = pd.DataFrame(st.session_state.database_siswa)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric("👥", "Total Siswa", len(df_db), color="#2563eb")
        with col2:
            render_metric("📊", "Rata-rata", f"{df_db['Nilai Akademik'].mean():.2f}", color="#10b981")
        with col3:
            render_metric("🏆", "Tertinggi", f"{df_db['Nilai Akademik'].max():.2f}", color="#f59e0b")
        with col4:
            render_metric("📉", "Terendah", f"{df_db['Nilai Akademik'].min():.2f}", color="#ef4444")
        
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            filter_kelas = st.selectbox(
                "Filter Kelas",
                ["Semua"] + sorted(df_db['Kelas'].unique().tolist())
            )
        
        df_tampil = df_db if filter_kelas == "Semua" else df_db[df_db['Kelas'] == filter_kelas]
        
        render_section(f"📋 Daftar Siswa ({len(df_tampil)} siswa)")
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)
        
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            csv = df_tampil.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"database_siswa_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col2:
            if st.button("🗑️ Hapus Semua Data", type="secondary", use_container_width=True):
                st.session_state.database_siswa = []
                st.rerun()

# ================================================================
# MENU 3: ANALISIS KAUSAL
# ================================================================

elif menu == "📊 Analisis Kausal":
    render_hero("Analisis Kausal Global", "Efek kausal setiap faktor terhadap prestasi akademik", "📊")
    
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
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#f0f9ff')
    ax.set_facecolor('#f0f9ff')
    colors = ['#10b981' if x > 0 else '#ef4444' for x in df_ate['ATE']]
    bars = ax.barh(df_ate['Konstruk'], df_ate['ATE'], color=colors, alpha=0.85, edgecolor='white', linewidth=2)
    ax.axvline(x=0, color='#0f172a', linestyle='-', alpha=0.5)
    ax.set_xlabel('ATE (Average Treatment Effect)', fontsize=12, fontweight='bold')
    ax.set_title('Efek Kausal terhadap Prestasi Akademik', fontsize=14, fontweight='bold', pad=20)
    for bar, val in zip(bars, df_ate['ATE']):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2, f'{val:+.2f}', 
                va='center', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    st.dataframe(df_ate, use_container_width=True, hide_index=True)

# ================================================================
# MENU 4: ANALISIS SHAP
# ================================================================

elif menu == "📈 Analisis SHAP":
    render_hero("Analisis SHAP", "Kontribusi prediktif setiap faktor", "📈")
    
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
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#f0f9ff')
    ax.set_facecolor('#f0f9ff')
    bars = ax.barh(df_shap['Konstruk'], df_shap['Mean_SHAP'], 
                   color='#2563eb', alpha=0.85, edgecolor='white', linewidth=2)
    ax.set_xlabel('Mean |SHAP Value|', fontsize=12, fontweight='bold')
    ax.set_title('Kontribusi Fitur terhadap Prediksi', fontsize=14, fontweight='bold', pad=20)
    for bar, val in zip(bars, df_shap['Mean_SHAP']):
        ax.text(val + 0.02, bar.get_y() + bar.get_height()/2, f'{val:.4f}', 
                va='center', fontsize=10, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    st.dataframe(df_shap, use_container_width=True, hide_index=True)

# ================================================================
# MENU 5: REKOMENDASI
# ================================================================

else:
    render_hero("Rekomendasi Intervensi", "Berdasarkan hasil analisis keseluruhan", "💡")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="success-box">
        <h3 style="color: #065f46; margin-top: 0;">✅ PRIORITAS TINGGI</h3>
        <hr>
        <b>1. Fasilitas Sekolah</b> (ATE: +2.43)<br>
        → Tingkatkan kualitas perpustakaan<br>
        → Optimalkan laboratorium<br><br>
        <b>2. Keterlibatan Orang Tua</b> (ATE: +2.21)<br>
        → Program parenting<br>
        → Komunikasi rutin sekolah-orang tua<br><br>
        <b>3. Self-Efficacy Akademik</b> (ATE: +2.07)<br>
        → Penguatan kepercayaan diri<br>
        → Pelatihan motivasi belajar
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <h3 style="color: #92400e; margin-top: 0;">⚠️ PERLU EVALUASI</h3>
        <hr>
        <b>1. Dukungan Sekolah</b> (ATE: -3.88)<br>
        → Evaluasi program pendampingan<br>
        → Kurangi intervensi berlebihan<br><br>
        <b>2. Harapan Orang Tua</b> (ATE: -1.53)<br>
        → Edukasi orang tua<br>
        → Target realistis
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h3 style="color: #1e40af; margin-top: 0;">📌 KESIMPULAN</h3>
    <b>Faktor Penentu Keberhasilan:</b><br>
    1. ✅ Fasilitas Sekolah yang memadai<br>
    2. ✅ Kepercayaan diri siswa (Self-Efficacy)<br>
    3. ✅ Keterlibatan aktif orang tua<br><br>
    <b>Faktor yang Perlu Dikelola:</b><br>
    1. ⚠️ Over-support dari sekolah<br>
    2. ⚠️ Tekanan harapan orang tua berlebihan
    </div>
    """, unsafe_allow_html=True)
