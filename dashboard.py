import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import hashlib

st.set_page_config(
    page_title="SIA.Prestasi | SMPN 6 Salatiga",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================================================
# CSS — SIASAT STYLE
# ================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');

:root{
    --ink:#17233B; --muted:#667085; --line:#E4EAF2;
    --canvas:#FFFFFF; --surface:#FFFFFF;
    --blue:#2563EB; --blue-soft:#EAF1FF;
    --yellow:#F6C945; --yellow-soft:#FFF7D6;
    --mint:#18A77A; --mint-soft:#E8F8F1;
    --coral:#EF5B67; --coral-soft:#FFF0F2;
    --purple:#7C5CFC; --purple-soft:#F1EDFF;
    --pink:#EC4899; --navy:#13213B; --navy-2:#1E2F50;
    --cream:#FFF9E6; --cream-2:#FFF3D0; --cream-border:#D4B896;
}

html, body, [class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink);}
.stApp{background:#FFFFFF;}
.main{background:#FFFFFF;}
.block-container{max-width:100%;padding:0 !important;}
#MainMenu, footer, header{visibility:hidden;}
h1,h2,h3,h4{font-family:'Manrope',sans-serif;}

@keyframes riseIn{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
@keyframes growBar{from{transform:scaleX(0);transform-origin:left;}to{transform:scaleX(1);transform-origin:left;}}

.motion{animation:riseIn .5s ease both;}

/* ============ LOGIN PAGE — SIASAT ============ */
.login-page-header{
    display:flex;justify-content:space-between;align-items:center;
    padding:1rem 2rem;background:#fff;
    border-bottom:1px solid #E4EAF2;
}
.login-logo-area{
    display:flex;align-items:center;gap:.8rem;
    justify-content:flex-end;width:100%;
}
.login-logo-icon{font-size:2.2rem;line-height:1;}
.login-logo-text{text-align:right;line-height:1.15;}
.login-logo-title{
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:1.6rem;font-weight:800;
    color:#17233B;letter-spacing:-.8px;
}
.login-logo-title .blue-part{color:#2563EB;}
.login-logo-sub{font-size:.72rem;color:#667085;letter-spacing:.3px;margin-top:.15rem;}

.login-content{max-width:1050px;margin:2rem auto;padding:0 2rem;}

.login-date-logout{
    display:flex;justify-content:space-between;align-items:center;
    padding:.9rem 0;border-bottom:2px solid #17233B;margin-bottom:2rem;
}
.login-date{font-family:'Manrope',sans-serif;font-weight:800;font-size:.95rem;color:#17233B;}
.login-logout-link{font-size:.8rem;color:#2563EB;font-weight:700;padding:.35rem .8rem;border-left:1px solid #E4EAF2;}

.siasat-label{font-family:'DM Sans',sans-serif;font-weight:700;font-size:.9rem;color:#17233B;padding-top:.65rem;}
.siasat-label::after{content:" :";color:#667085;font-weight:400;}

.siasat-input .stTextInput > div > div > input{
    border:1.5px solid #A8B5C7 !important;border-radius:4px !important;
    padding:.55rem .85rem !important;font-size:.9rem !important;
    background:#fff !important;min-height:42px !important;
    font-family:'DM Sans',sans-serif !important;
}
.siasat-input .stTextInput > div > div > input:focus{
    border-color:#2563EB !important;
    box-shadow:0 0 0 3px rgba(37,99,235,.12) !important;
}
.siasat-input .stTextInput > label{display:none !important;}

.siasat-btn-login button{
    background:linear-gradient(180deg,#4ADE80 0%,#22C55E 100%) !important;
    border:1px solid #16A34A !important;color:#fff !important;
    font-weight:700 !important;font-size:.9rem !important;
    padding:.55rem 2rem !important;border-radius:5px !important;
    min-height:44px !important;text-transform:none !important;
}
.siasat-btn-login button:hover{
    background:linear-gradient(180deg,#22C55E 0%,#16A34A 100%) !important;
}
.siasat-btn-lupa button{
    background:linear-gradient(180deg,#F87171 0%,#EF4444 100%) !important;
    border:1px solid #DC2626 !important;color:#fff !important;
    font-weight:700 !important;font-size:.9rem !important;
    padding:.55rem 2rem !important;border-radius:5px !important;
    min-height:44px !important;text-transform:none !important;
}
.siasat-btn-lupa button:hover{
    background:linear-gradient(180deg,#EF4444 0%,#DC2626 100%) !important;
}

.siasat-info-box{
    background:#F7F9FC;border:1px solid #E4EAF2;
    border-left:4px solid #F6C945;border-radius:6px;
    padding:1.2rem 1.4rem;margin-top:2.5rem;
}
.siasat-info-header{display:flex;align-items:center;gap:.6rem;margin-bottom:.7rem;}
.siasat-info-icon{font-size:1.3rem;}
.siasat-info-title{font-family:'Manrope';font-weight:800;font-size:.9rem;color:#17233B;}
.siasat-info-list{font-size:.8rem;color:#475467;line-height:1.85;padding-left:.3rem;}
.siasat-info-list div{display:flex;gap:.5rem;}
.siasat-info-list .num{color:#2563EB;font-weight:800;flex-shrink:0;min-width:18px;}

.siasat-footer{
    text-align:center;padding:2rem 0;margin-top:3rem;
    border-top:1px solid #E4EAF2;font-size:.72rem;color:#98A2B3;line-height:1.8;
}
.siasat-footer strong{color:#475467;font-weight:700;}

.siasat-alert-danger{
    background:#FEF2F2;border:1px solid #FECACA;border-left:4px solid #EF4444;
    border-radius:6px;padding:.85rem 1.1rem;margin-top:1rem;
}
.siasat-alert-danger-title{font-family:'Manrope';font-weight:800;font-size:.82rem;color:#991B1B;}
.siasat-alert-danger-body{font-size:.75rem;color:#7F1D1D;margin-top:.25rem;}

.siasat-alert-info{
    background:#EFF6FF;border:1px solid #BFDBFE;border-left:4px solid #2563EB;
    border-radius:6px;padding:.85rem 1.1rem;margin-top:1rem;
}
.siasat-alert-info-title{font-family:'Manrope';font-weight:800;font-size:.82rem;color:#1E40AF;}
.siasat-alert-info-body{font-size:.75rem;color:#1E3A8A;margin-top:.25rem;}

/* ============ SIASAT INTERNAL LAYOUT ============ */
.siasat-topbar{
    display:flex;justify-content:space-between;align-items:center;
    padding:.6rem 1.5rem;background:#fff;
    border-bottom:1px solid #CCC;
    font-family:'Arial',sans-serif;font-size:.78rem;font-weight:700;color:#000;
}
.siasat-topbar .logout-link{
    color:#0645AD;text-decoration:none;font-weight:700;
    padding-left:1rem;border-left:1px solid #CCC;
}

.siasat-user-header{
    background:#000;color:#fff;
    padding:.7rem 1.5rem;
    font-family:'Courier New',monospace;
    font-size:.78rem;line-height:1.75;
    border-bottom:1px solid #333;
}
.siasat-user-header .row{display:flex;gap:.8rem;}
.siasat-user-header .label{color:#fff;min-width:14px;font-weight:700;}
.siasat-user-header .value{color:#fff;}

/* Content area */
.siasat-content{
    background:#fff;
    padding:1.5rem 2rem 3rem 2rem;
    min-height:80vh;
}

.siasat-breadcrumb{
    display:flex;align-items:center;gap:.6rem;
    margin-bottom:1.5rem;padding-bottom:.8rem;
    border-bottom:2px solid #E0E0E0;
}
.siasat-breadcrumb-icon{font-size:2rem;line-height:1;}
.siasat-breadcrumb-title{
    font-family:'Arial',sans-serif;
    font-size:1.5rem;font-weight:700;color:#000;letter-spacing:.3px;
}

.siasat-section-title{
    font-family:'Arial',sans-serif;
    font-size:.95rem;font-weight:700;color:#000;
    margin:1.5rem 0 .8rem 0;padding-bottom:.3rem;
}

.siasat-table{
    width:100%;border-collapse:collapse;
    font-family:'Arial',sans-serif;font-size:.82rem;margin:.5rem 0;
}
.siasat-table th{
    background:#F0F0F0;border:1px solid #999;
    padding:.6rem .8rem;text-align:left;font-weight:700;
}
.siasat-table td{
    border:1px solid #CCC;padding:.6rem .8rem;vertical-align:top;
}

.siasat-notice{
    background:#E8F5E9;border:1px solid #66BB6A;
    border-left:5px solid #2E7D32;padding:1rem 1.2rem;
    font-family:'Arial',sans-serif;font-size:.85rem;
    color:#1B5E20;margin:1rem 0;line-height:1.75;
}
.siasat-notice strong{color:#1B5E20;}

.siasat-warning{
    background:#FFF3E0;border:1px solid #FFB74D;
    border-left:5px solid #F57C00;padding:1rem 1.2rem;
    font-family:'Arial',sans-serif;font-size:.85rem;
    color:#E65100;margin:1rem 0;line-height:1.75;
}

/* ============ STREAMLIT SIDEBAR — STYLE SIASAT CREAM ============ */
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#FFF9E6 0%,#FFF3D0 100%) !important;
    border-right:1px solid #D4B896 !important;
    padding-top:0 !important;
}
[data-testid="stSidebar"] > div:first-child{padding:1rem .5rem;}
[data-testid="stSidebar"] *{
    color:#000 !important;
    font-family:'Arial',sans-serif !important;
}
[data-testid="stSidebar"] .stRadio > label{
    font-size:.68rem !important;font-weight:800 !important;
    color:#8B7355 !important;text-transform:uppercase;
    letter-spacing:1.5px;padding:0 .8rem;margin-bottom:.5rem;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"]{gap:.1rem;}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label{
    background:transparent;border:0;border-radius:0;
    padding:.6rem .8rem !important;font-weight:400 !important;
    font-size:.85rem !important;transition:background .15s ease;
    cursor:pointer;margin:0;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover{
    background:rgba(255,200,100,.3);
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"]{
    background:rgba(255,200,100,.55);
    font-weight:700 !important;
    border-left:3px solid #B8860B;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"] p{
    font-weight:700 !important;
}
[data-testid="stSidebar"] .stButton > button{
    background:#8B4513 !important;color:#fff !important;
    border:1px solid #6B3410 !important;border-radius:3px !important;
    font-weight:700 !important;font-size:.8rem !important;
    min-height:38px !important;
}
[data-testid="stSidebar"] .stButton > button:hover{
    background:#6B3410 !important;
}
[data-testid="stSidebar"] hr{
    margin:.8rem .8rem;border-color:#D4B896 !important;
}

/* ============ STREAMLIT CONTENT STYLE ============ */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox [data-baseweb="select"] > div{
    background:#fff !important;border:1px solid #D7DFEA !important;
    border-radius:6px !important;min-height:42px;
    color:var(--ink) !important;font-family:'Arial',sans-serif !important;
}
.stTextInput label,.stNumberInput label,.stSelectbox label{
    font-size:.82rem !important;font-weight:700 !important;
    color:#17233B !important;font-family:'Arial',sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus{
    border-color:var(--blue) !important;
    box-shadow:0 0 0 3px rgba(37,99,235,.10) !important;
}
.stButton > button,.stDownloadButton > button{
    border-radius:6px !important;min-height:42px;
    font-weight:700 !important;
    border:1px solid #D7DFEA !important;
    font-family:'Arial',sans-serif !important;
    transition:all .18s ease !important;
}
.stButton > button:hover,.stDownloadButton > button:hover{
    transform:translateY(-1px);
}
button[kind="primary"]{
    background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 100%) !important;
    border-color:#2563EB !important;color:#fff !important;
}

.stRadio > div{gap:.5rem;}
.stRadio [role="radiogroup"]{gap:.5rem;}
.stRadio [role="radiogroup"] label{
    background:#fff;border:1.5px solid #E4EAF2;border-radius:8px;
    padding:.6rem 1rem !important;transition:all .18s ease;
    font-weight:500 !important;cursor:pointer;
    font-family:'Arial',sans-serif !important;
}
.stRadio [role="radiogroup"] label:hover{
    border-color:#2563EB;background:#F8FAFF;
}
.stRadio [role="radiogroup"] label[data-checked="true"]{
    border-color:#2563EB;background:#EAF1FF;
}
.stRadio [role="radiogroup"] label[data-checked="true"] p{
    color:#2563EB !important;font-weight:700 !important;
}

[data-testid="stDataFrame"]{
    border:1px solid #E4EAF2;border-radius:8px;overflow:hidden;
}

/* Info boxes */
.info-box{border-radius:8px;padding:1rem 1.2rem;border:1px solid var(--line);background:#fff;}
.info-box.blue{background:#EAF1FF;border-color:#D5E1FF;}
.info-box.yellow{background:#FFF7D6;border-color:#F1DF96;}
.info-box.mint{background:#E8F8F1;border-color:#C5EBDD;}
.info-box.coral{background:#FFF0F2;border-color:#F4CDD3;}
.info-title{font-weight:800;font-size:.88rem;}
.info-text{font-size:.78rem;line-height:1.6;margin-top:.35rem;color:#475467;}

/* Notifikasi simpan */
.notif-success{
    background:linear-gradient(135deg,#ECFDF5 0%,#D1FAE5 100%);
    border:2px solid #10B981;border-left:6px solid #10B981;
    border-radius:8px;padding:1.2rem 1.4rem;margin:1rem 0;
}
.notif-success-title{
    font-family:'Manrope';font-weight:800;font-size:1rem;color:#065F46;
}
.notif-success-body{font-size:.85rem;color:#064E3B;line-height:1.6;margin-top:.4rem;}

/* Stat card */
.stat-box{
    background:#fff;border:1px solid #E4EAF2;border-radius:8px;
    padding:1rem 1.2rem;margin-bottom:1rem;
}
.stat-box .topline{width:34px;height:4px;border-radius:99px;margin-bottom:.6rem;}
.stat-box .topline.blue{background:#2563EB;}
.stat-box .topline.mint{background:#18A77A;}
.stat-box .topline.yellow{background:#F6C945;}
.stat-box .topline.coral{background:#EF5B67;}
.stat-box .topline.purple{background:#7C5CFC;}
.stat-box .label{font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#667085;}
.stat-box .value{font-family:'Manrope';font-size:1.8rem;font-weight:800;color:#17233B;margin-top:.4rem;line-height:1;}
.stat-box .note{color:#667085;font-size:.72rem;margin-top:.35rem;}

/* ============ LOGIN untuk view utama ============ */
.login-shell{max-width:1000px;margin:0 auto;padding:0 2rem;}
@media(max-width:850px){
    .block-container{padding:0 !important;}
    .siasat-content{padding:1rem;}
    .siasat-breadcrumb-title{font-size:1.2rem;}
}
</style>
""", unsafe_allow_html=True)

# ================================================================
# AUTH
# ================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    "admin": {"password": hash_password("admin123"), "nama": "Administrator"},
    "guru": {"password": hash_password("guru123"), "nama": "Guru SMPN 6"},
    "regina": {"password": hash_password("regina2026"), "nama": "Regina Ria Aurellia"},
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_nama" not in st.session_state:
    st.session_state.user_nama = None
if "username" not in st.session_state:
    st.session_state.username = None
if "database_siswa" not in st.session_state:
    st.session_state.database_siswa = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "last_saved" not in st.session_state:
    st.session_state.last_saved = None

# ================================================================
# DATA
# ================================================================

BASELINE_ASPEK = {
    "Self-Efficacy Akademik": 4.63,
    "Keterlibatan Orang Tua": 4.35,
    "Harapan Orang Tua": 3.45,
    "Dukungan Sekolah": 4.60,
    "Motivasi Belajar": 2.52,
    "Kecemasan Akademik": 2.89,
    "Kemalasan Belajar": 1.49,
    "Fasilitas Sekolah": 4.88,
}

PENGARUH_DATA = {
    "Self-Efficacy Akademik": 2.0698,
    "Keterlibatan Orang Tua": 2.2100,
    "Harapan Orang Tua": -1.5323,
    "Dukungan Sekolah": -3.8797,
    "Motivasi Belajar": -0.2850,
    "Kecemasan Akademik": 0.4522,
    "Kemalasan Belajar": -0.0902,
    "Fasilitas Sekolah": 2.4295,
}

KEPENTINGAN_DATA = {
    "Self-Efficacy Akademik": 0.8008,
    "Keterlibatan Orang Tua": 0.6806,
    "Harapan Orang Tua": 0.5823,
    "Dukungan Sekolah": 0.4352,
    "Motivasi Belajar": 0.3667,
    "Kecemasan Akademik": 0.1308,
    "Fasilitas Sekolah": 0.0654,
    "Kemalasan Belajar": 0.0793,
}

BOBOT_PENGARUH = {
    "Self-Efficacy Akademik": 2.0698 * 0.8008,
    "Keterlibatan Orang Tua": 2.2100 * 0.6806,
    "Harapan Orang Tua": -1.5323 * 0.5823,
    "Dukungan Sekolah": -3.8797 * 0.4352,
    "Motivasi Belajar": -0.2850 * 0.3667,
    "Kecemasan Akademik": 0.4522 * 0.1308,
    "Fasilitas Sekolah": 2.4295 * 0.0654,
    "Kemalasan Belajar": -0.0902 * 0.0793,
}

RATA_RATA_NILAI = 83.78

KELAS_LIST = (
    [f"VII-{x}" for x in "ABCDEFGH"]
    + [f"VIII-{x}" for x in "ABCDEFGH"]
    + [f"IX-{x}" for x in "ABCDEFGH"]
)

SKALA_PILIHAN = {
    "Self-Efficacy Akademik": {"question":"Seberapa yakin siswa terhadap kemampuan akademiknya?","options":[("1","Hampir tidak pernah percaya diri"),("2","Jarang percaya diri"),("3","Kadang-kadang percaya diri"),("4","Sering percaya diri"),("5","Hampir selalu percaya diri")]},
    "Keterlibatan Orang Tua": {"question":"Seberapa aktif orang tua mendampingi siswa belajar?","options":[("1","Hampir tidak pernah mendampingi"),("2","Jarang mendampingi"),("3","Kadang-kadang mendampingi"),("4","Sering mendampingi"),("5","Hampir selalu mendampingi")]},
    "Harapan Orang Tua": {"question":"Seberapa tinggi tuntutan/ekspektasi orang tua terhadap nilai siswa?","options":[("1","Sangat rendah / tidak menuntut"),("2","Rendah"),("3","Sedang / wajar"),("4","Tinggi"),("5","Sangat tinggi / menekan")]},
    "Dukungan Sekolah": {"question":"Seberapa besar dukungan & perhatian yang diberikan sekolah kepada siswa?","options":[("1","Sangat kurang / tidak diperhatikan"),("2","Kurang"),("3","Cukup"),("4","Baik"),("5","Sangat baik / sangat diperhatikan")]},
    "Motivasi Belajar": {"question":"Seberapa besar motivasi & semangat belajar siswa?","options":[("1","Tidak ada motivasi / sangat malas"),("2","Kurang termotivasi"),("3","Cukup termotivasi"),("4","Termotivasi"),("5","Sangat termotivasi / antusias")]},
    "Kecemasan Akademik": {"question":"Seberapa sering siswa merasa cemas / tertekan saat belajar atau ujian?","options":[("1","Hampir tidak pernah cemas"),("2","Jarang cemas"),("3","Kadang-kadang cemas"),("4","Sering cemas"),("5","Hampir selalu cemas / sangat tertekan")]},
    "Fasilitas Sekolah": {"question":"Seberapa memadai fasilitas belajar yang tersedia di sekolah?","options":[("1","Sangat kurang memadai"),("2","Kurang memadai"),("3","Cukup memadai"),("4","Memadai"),("5","Sangat memadai / lengkap")]},
    "Kemalasan Belajar": {"question":"Seberapa sering siswa menunjukkan sikap malas belajar?","options":[("1","Tidak pernah malas"),("2","Jarang malas"),("3","Kadang-kadang malas"),("4","Sering malas"),("5","Hampir selalu malas")]},
}

# ================================================================
# FUNCTIONS
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
        return "Sangat Baik", "#18A77A", "▲"
    elif nilai >= 84:
        return "Baik", "#2563EB", "●"
    elif nilai >= 80:
        return "Cukup", "#F0B900", "◆"
    return "Perlu Perhatian", "#EF5B67", "▼"


def goto_page(page):
    st.session_state.current_page = page
    st.session_state.last_saved = None
    st.rerun()


def siasat_breadcrumb(icon, title):
    st.markdown(f"""
    <div class="siasat-breadcrumb">
        <span class="siasat-breadcrumb-icon">{icon}</span>
        <span class="siasat-breadcrumb-title">{title}</span>
    </div>
    """, unsafe_allow_html=True)


def siasat_section(title):
    st.markdown(f'<div class="siasat-section-title">{title}</div>', unsafe_allow_html=True)


def stat_box(label, value, note="", color="blue"):
    st.markdown(f"""
    <div class="stat-box">
        <div class="topline {color}"></div>
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        <div class="note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def notifikasi_simpan(nama, kelas):
    st.markdown(f"""
    <div class="notif-success">
        <div class="notif-success-title">✅ Data Berhasil Disimpan</div>
        <div class="notif-success-body">
            Data siswa <b>{nama}</b> kelas <b>{kelas}</b> telah tersimpan di database.<br>
            Anda dapat melihat atau mengelola data ini di menu <b>Database Siswa</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📁 Buka Database", use_container_width=True, key="go_db"):
            goto_page("database")
    with col2:
        if st.button("✓ Lanjut Input Siswa Lain", use_container_width=True, key="reset_form"):
            st.session_state.last_saved = None
            st.rerun()


def plot_pengaruh(df):
    df = df.sort_values("Pengaruh", ascending=True)
    fig, ax = plt.subplots(figsize=(11, 6.3))
    fig.patch.set_facecolor('#fff')
    ax.set_facecolor('#fff')
    vals = df["Pengaruh"].values
    labels = df["Faktor"].values
    y = np.arange(len(df))
    bars = ax.barh(y, vals, height=.58,
                   color=["#EF5B67" if x < 0 else "#18A77A" for x in vals], alpha=.9)
    ax.axvline(0, color="#17233B", linewidth=1.3)
    max_abs = max(abs(vals.min()), abs(vals.max()))
    pad = max_abs * .15
    ax.set_xlim(vals.min() - pad, vals.max() + pad)
    for bar, val in zip(bars, vals):
        offset = .07 if val >= 0 else -.07
        ha = "left" if val >= 0 else "right"
        ax.text(val + offset, bar.get_y() + bar.get_height()/2, f"{val:+.2f}",
                va="center", ha=ha, fontsize=9.5, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", labelsize=8, colors="#667085")
    ax.grid(axis="x", alpha=.12, linewidth=.7)
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8E0EB")
    ax.set_xlabel("Kekuatan Pengaruh (poin nilai)", fontsize=9,
                  fontweight="bold", color="#667085", labelpad=10)
    plt.tight_layout()
    return fig


def plot_kepentingan(df):
    df = df.sort_values("Kepentingan", ascending=True)
    fig, ax = plt.subplots(figsize=(11, 6.3))
    fig.patch.set_facecolor('#fff')
    ax.set_facecolor('#fff')
    vals = df["Kepentingan"].values
    labels = df["Faktor"].values
    y = np.arange(len(df))
    bars = ax.barh(y, vals, height=.58, color="#4F7CFF", alpha=.9)
    ax.set_xlim(0, max(vals) * 1.18)
    for bar, val in zip(bars, vals):
        ax.text(val + max(vals)*.018, bar.get_y() + bar.get_height()/2,
                f"{val:.4f}", va="center", fontsize=9.5, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", labelsize=8, colors="#667085")
    ax.grid(axis="x", alpha=.12, linewidth=.7)
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8E0EB")
    ax.set_xlabel("Tingkat Kepentingan Faktor", fontsize=9,
                  fontweight="bold", color="#667085", labelpad=10)
    plt.tight_layout()
    return fig


def input_kategori(key_name, faktor_name):
    config = SKALA_PILIHAN[faktor_name]
    st.markdown(f"""
    <div style="margin-bottom:.5rem;">
        <div style="font-family:'Arial';font-weight:700;font-size:.88rem;color:#17233B;">
            {faktor_name}
        </div>
        <div style="font-size:.72rem;color:#667085;margin-top:.15rem;margin-bottom:.6rem;">
            {config['question']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    labels = [opt[1] for opt in config["options"]]
    values = [float(opt[0]) for opt in config["options"]]
    baseline_val = BASELINE_ASPEK[faktor_name]
    default_idx = 2
    for i, v in enumerate(values):
        if abs(v - baseline_val) < 0.5:
            default_idx = i
            break
    pilihan = st.radio(f"{faktor_name}_radio", labels, index=default_idx,
                       key=key_name, label_visibility="collapsed")
    return values[labels.index(pilihan)]


# ================================================================
# LOGIN PAGE
# ================================================================

def halaman_login():
    st.markdown("""
    <div class="login-page-header">
        <div></div>
        <div class="login-logo-area">
            <div class="login-logo-icon">🎓</div>
            <div class="login-logo-text">
                <div class="login-logo-title">
                    SIA.<span class="blue-part">Prestasi</span>
                </div>
                <div class="login-logo-sub">smpn6salatiga.sch.id</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-content">', unsafe_allow_html=True)

    hari_ini = datetime.now()
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][hari_ini.weekday()]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
             "Juli", "Agustus", "September", "Oktober", "November", "Desember"][hari_ini.month - 1]
    tanggal_str = f"{hari}, {hari_ini.day} {bulan} {hari_ini.year}"

    st.markdown(f"""
    <div class="login-date-logout">
        <div class="login-date">{tanggal_str}</div>
        <div class="login-logout-link">| Logout</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form_siasat", clear_on_submit=False):
        col_label1, col_input1 = st.columns([1, 3])
        with col_label1:
            st.markdown('<div class="siasat-label" style="padding-top:.65rem;padding-left:.3rem;">Nama Pengguna</div>', unsafe_allow_html=True)
        with col_input1:
            st.markdown('<div class="siasat-input">', unsafe_allow_html=True)
            username = st.text_input("username_siasat", placeholder="Masukkan nama pengguna",
                                     label_visibility="collapsed", key="login_username_siasat")
            st.markdown('</div>', unsafe_allow_html=True)

        col_label2, col_input2 = st.columns([1, 3])
        with col_label2:
            st.markdown('<div class="siasat-label" style="padding-top:.65rem;padding-left:.3rem;">Kata Sandi</div>', unsafe_allow_html=True)
        with col_input2:
            st.markdown('<div class="siasat-input">', unsafe_allow_html=True)
            password = st.text_input("password_siasat", type="password", placeholder="Masukkan kata sandi",
                                     label_visibility="collapsed", key="login_password_siasat")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:.5rem;"></div>', unsafe_allow_html=True)

        col_empty, col_btn1, col_btn2, col_rest = st.columns([1, 1, 1, 2])
        with col_btn1:
            st.markdown('<div class="siasat-btn-login">', unsafe_allow_html=True)
            submit = st.form_submit_button("Login", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_btn2:
            st.markdown('<div class="siasat-btn-lupa">', unsafe_allow_html=True)
            lupa = st.form_submit_button("Lupa Password", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if submit:
            if username in USERS and USERS[username]["password"] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.user_nama = USERS[username]["nama"]
                st.session_state.username = username
                st.session_state.current_page = "home"
                st.rerun()
            else:
                st.markdown("""
                <div class="siasat-alert-danger">
                    <div class="siasat-alert-danger-title">❌ Login Gagal</div>
                    <div class="siasat-alert-danger-body">Nama pengguna atau kata sandi salah. Silakan coba lagi.</div>
                </div>
                """, unsafe_allow_html=True)

        if lupa:
            st.markdown("""
            <div class="siasat-alert-info">
                <div class="siasat-alert-info-title">ℹ️ Lupa Password</div>
                <div class="siasat-alert-info-body">
                    Silakan hubungi Administrator sekolah untuk melakukan reset password.
                    Hubungi: admin@smpn6salatiga.sch.id
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="siasat-info-box">
        <div class="siasat-info-header">
            <div class="siasat-info-icon">💡</div>
            <div class="siasat-info-title">Informasi Login</div>
        </div>
        <div class="siasat-info-list">
            <div><span class="num">1.</span><span>Gunakan akun resmi yang diberikan oleh sekolah.</span></div>
            <div><span class="num">2.</span><span>Hubungi Administrator jika lupa password.</span></div>
            <div><span class="num">3.</span><span>Jangan bagikan akun kepada orang lain.</span></div>
            <div><span class="num">4.</span><span>Logout setelah selesai menggunakan dashboard.</span></div>
            <div><span class="num">5.</span><span>Hindari login menggunakan perangkat bersama.</span></div>
            <div><span class="num">6.</span><span>Perhatikan keamanan data siswa saat menggunakan sistem.</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔑 Lihat Akun Demo"):
        st.markdown("""
        | Nama Pengguna | Kata Sandi | Peran |
        |---------------|------------|-------|
        | `admin` | `admin123` | Administrator |
        | `guru` | `guru123` | Guru |
        | `regina` | `regina2026` | Peneliti |
        """)

    st.markdown("""
    <div class="siasat-footer">
        <strong>SIA.Prestasi</strong> · Sistem Informasi Akademik<br>
        Dikembangkan oleh Program Studi Magister Sains Data<br>
        Universitas Kristen Satya Wacana · © 2026
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if not st.session_state.logged_in:
    halaman_login()
    st.stop()

# ================================================================
# SIDEBAR SIASAT — CREAM STYLE
# ================================================================

# Header kecil di sidebar
st.sidebar.markdown("""
<div style="text-align:center;padding:.5rem 0 1rem 0;border-bottom:1px solid #D4B896;margin-bottom:.5rem;">
    <div style="font-size:2rem;line-height:1;">🎓</div>
    <div style="font-family:'Plus Jakarta Sans';font-size:1.1rem;font-weight:800;color:#17233B;letter-spacing:-.5px;margin-top:.3rem;">
        SIA.<span style="color:#2563EB;">Prestasi</span>
    </div>
    <div style="font-size:.68rem;color:#8B7355;letter-spacing:.5px;margin-top:.15rem;">
        SMPN 6 SALATIGA
    </div>
</div>
""", unsafe_allow_html=True)

# Menu via radio (di-style cream)
menu_choice = st.sidebar.radio(
    "NAVIGASI",
    [
        "🏠  HOME",
        "🔍  Analisis Siswa",
        "🗄️  Database Siswa",
        "📊  Faktor Penyebab",
        "📈  Tingkat Kepentingan",
        "💡  Rekomendasi Umum",
        "🎯  Catatan untuk Guru",
    ],
    key="siasat_menu",
    label_visibility="visible"
)

# Info user di bawah menu
st.sidebar.markdown("""
<div style="padding:.8rem;margin:1rem .3rem .5rem .3rem;border-top:1px solid #D4B896;">
    <div style="font-size:.6rem;font-weight:800;color:#8B7355;letter-spacing:1.2px;text-transform:uppercase;">
        Pengguna Aktif
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div style="padding:0 .8rem .8rem .8rem;">
    <div style="font-weight:800;font-size:.85rem;color:#17233B;">
        {st.session_state.user_nama}
    </div>
    <div style="font-size:.7rem;color:#8B7355;margin-top:.15rem;">
        {st.session_state.username}
    </div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
    st.session_state.logged_in = False
    st.session_state.user_nama = None
    st.session_state.username = None
    st.session_state.current_page = "home"
    st.rerun()

# Mapping menu ke page
menu_map = {
    "🏠  HOME": "home",
    "🔍  Analisis Siswa": "analisis",
    "🗄️  Database Siswa": "database",
    "📊  Faktor Penyebab": "kausal",
    "📈  Tingkat Kepentingan": "kepentingan",
    "💡  Rekomendasi Umum": "rekomendasi",
    "🎯  Catatan untuk Guru": "catatan_guru",
}

new_page = menu_map.get(menu_choice, "home")
if new_page != st.session_state.current_page:
    st.session_state.current_page = new_page
    st.session_state.last_saved = None

# ================================================================
# HEADER HITAM + TOPBAR
# ================================================================

hari_ini = datetime.now()
hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][hari_ini.weekday()]
bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
         "Juli", "Agustus", "September", "Oktober", "November", "Desember"][hari_ini.month - 1]
tanggal_str = f"{hari}, {hari_ini.day} {bulan} {hari_ini.year}"

st.markdown(f"""
<div class="siasat-topbar">
    <div>{tanggal_str}</div>
    <a class="logout-link">| Logout</a>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="siasat-user-header">
    <div class="row">
        <span class="label">:</span>
        <span class="value"><b>{st.session_state.username or 'user'}</b> - {st.session_state.user_nama}</span>
    </div>
    <div class="row">
        <span class="label">:</span>
        <span class="value">SISTEM INFORMASI AKADEMIK · SMP NEGERI 6 SALATIGA</span>
    </div>
    <div class="row">
        <span class="label">:</span>
        <span class="value">HYBRID CAUSAL-EXPLAINABLE MACHINE LEARNING · 2026</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================================================================
# KONTEN SETIAP HALAMAN
# ================================================================

st.markdown('<div class="siasat-content">', unsafe_allow_html=True)

# ================================================================
# HOME
# ================================================================

if st.session_state.current_page == "home":
    siasat_breadcrumb("🏠", "HOME")

    st.markdown("""
    <div style="font-family:'Arial';font-size:.9rem;color:#000;line-height:1.9;">
        <b>SELAMAT DATANG DI SISTEM INFORMASI AKADEMIK</b><br>
        <b>SMP NEGERI 6 SALATIGA</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="siasat-notice">
        <strong>ℹ️ INFORMASI SISTEM</strong><br>
        Dashboard ini merupakan hasil penelitian <b>Hybrid Causal-Explainable Machine Learning</b> 
        untuk menganalisis determinan prestasi akademik siswa SMP Negeri 6 Salatiga.
        <br><br>
        Silakan pilih menu di sidebar kiri untuk memulai analisis.
    </div>
    """, unsafe_allow_html=True)

    siasat_section("📋 RINGKASAN MODUL TERSEDIA")

    st.markdown("""
    <table class="siasat-table">
        <thead>
            <tr>
                <th style="width:50px;">No</th>
                <th style="width:250px;">Modul</th>
                <th>Deskripsi</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>1</td><td><b>Analisis Siswa</b></td><td>Analisis personal siswa berdasarkan nilai akademik dan profil 8 faktor.</td></tr>
            <tr><td>2</td><td><b>Database Siswa</b></td><td>Arsip seluruh siswa yang telah dianalisis dengan filter dan pencarian.</td></tr>
            <tr><td>3</td><td><b>Faktor Penyebab</b></td><td>Faktor yang secara sebab-akibat mempengaruhi prestasi akademik.</td></tr>
            <tr><td>4</td><td><b>Tingkat Kepentingan</b></td><td>Faktor yang paling menentukan prediksi nilai siswa.</td></tr>
            <tr><td>5</td><td><b>Rekomendasi Umum</b></td><td>Saran tindak lanjut untuk tingkat sekolah.</td></tr>
            <tr><td>6</td><td><b>Catatan untuk Guru</b></td><td>Kesimpulan & tindak lanjut personal per siswa.</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    siasat_section("📊 STATISTIK DATABASE")

    jumlah_data = len(st.session_state.database_siswa)

    st.markdown(f"""
    <table class="siasat-table">
        <tr><td style="width:300px;"><b>Total Siswa Terarsip</b></td><td>{jumlah_data} siswa</td></tr>
        <tr><td><b>Pengguna Aktif</b></td><td>{st.session_state.user_nama}</td></tr>
        <tr><td><b>Tanggal Akses</b></td><td>{datetime.now().strftime('%d %B %Y, %H:%M')}</td></tr>
    </table>
    """, unsafe_allow_html=True)

# ================================================================
# ANALISIS SISWA
# ================================================================

elif st.session_state.current_page == "analisis":
    siasat_breadcrumb("🔍", "ANALISIS SISWA")

    siasat_section("📝 DATA SISWA")

    c1, c2, c3 = st.columns([1.6, .8, .7])
    with c1:
        nama_siswa = st.text_input("Nama Siswa", placeholder="Nama lengkap siswa", key="a_nama")
    with c2:
        kelas_siswa = st.selectbox("Kelas", KELAS_LIST, index=KELAS_LIST.index("IX-A"), key="a_kelas")
    with c3:
        absen_siswa = st.number_input("No. Absen", 1, 50, 1, key="a_absen")

    c1, c2 = st.columns([1.5, 1])
    with c1:
        nilai_akademik = st.number_input(
            "Nilai Rata-rata Rapor",
            min_value=60.0, max_value=100.0, value=83.78,
            step=.01, format="%.2f",
            help=f"Rata-rata sekolah: {RATA_RATA_NILAI:.2f}",
            key="a_nilai"
        )
    with c2:
        gap = nilai_akademik - RATA_RATA_NILAI
        gap_label = "di atas rata-rata" if gap >= 0 else "di bawah rata-rata"
        color = "mint" if gap >= 0 else "coral"
        st.markdown(f"""
        <div class="stat-box">
            <div class="topline {color}"></div>
            <div class="label">Posisi Nilai</div>
            <div class="value">{gap:+.2f}</div>
            <div class="note">poin · {gap_label}</div>
        </div>
        """, unsafe_allow_html=True)

    siasat_section("📊 PROFIL SISWA · 8 FAKTOR")

    st.markdown("""
    <div class="info-box blue" style="margin-bottom:1rem;">
        <div class="info-title">💡 Cara Mengisi</div>
        <div class="info-text">Klik salah satu pilihan yang paling menggambarkan kondisi siswa.</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.markdown("**🧠 FAKTOR INTERNAL**")
        input_self_efficacy = input_kategori("in_se", "Self-Efficacy Akademik")
        input_motivasi = input_kategori("in_mot", "Motivasi Belajar")
        input_kecemasan = input_kategori("in_cem", "Kecemasan Akademik")
        input_kemalasan = input_kategori("in_mal", "Kemalasan Belajar")

    with right:
        st.markdown("**🌍 FAKTOR EKSTERNAL**")
        input_keterlibatan = input_kategori("ex_ket", "Keterlibatan Orang Tua")
        input_harapan = input_kategori("ex_har", "Harapan Orang Tua")
        input_dukungan = input_kategori("ex_duk", "Dukungan Sekolah")
        input_fasilitas = input_kategori("ex_fas", "Fasilitas Sekolah")

    profil_siswa = {
        "Self-Efficacy Akademik": input_self_efficacy,
        "Keterlibatan Orang Tua": input_keterlibatan,
        "Harapan Orang Tua": input_harapan,
        "Dukungan Sekolah": input_dukungan,
        "Motivasi Belajar": input_motivasi,
        "Kecemasan Akademik": input_kecemasan,
        "Fasilitas Sekolah": input_fasilitas,
        "Kemalasan Belajar": input_kemalasan,
    }

    selisih_nilai, kontribusi = analisis_kausal(nilai_akademik, profil_siswa)
    kategori, warna_kategori, simbol = kategori_nilai(nilai_akademik)

    siasat_section("🎯 HASIL ANALISIS")

    if nama_siswa:
        st.markdown(f"""
        <div class="siasat-notice">
            <strong>SUBJEK ANALISIS</strong><br>
            <b>{nama_siswa}</b> · {kelas_siswa} · No. Absen {absen_siswa:02d}
        </div>
        """, unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with a:
        stat_box("Nilai Akademik", f"{nilai_akademik:.2f}", "nilai rata-rata rapor", "blue")
    with b:
        stat_box("Selisih Rata-rata", f"{selisih_nilai:+.2f}", "poin dari rata-rata",
                 "mint" if selisih_nilai >= 0 else "coral")
    with c:
        color_kategori = 'mint' if kategori == 'Sangat Baik' else 'blue' if kategori == 'Baik' else 'yellow' if kategori == 'Cukup' else 'coral'
        st.markdown(f"""
        <div class="stat-box">
            <div class="topline {color_kategori}"></div>
            <div class="label">Kategori</div>
            <div class="value" style="font-size:1.4rem;color:{warna_kategori};">{simbol} {kategori}</div>
            <div class="note">berdasarkan rentang nilai</div>
        </div>
        """, unsafe_allow_html=True)

    siasat_section("📈 FAKTOR YANG MEMPENGARUHI NILAI")

    df_kontribusi = pd.DataFrame([
        {"Faktor": k, "Pengaruh": v, "Nilai": profil_siswa[k], "Rata": BASELINE_ASPEK[k]}
        for k, v in kontribusi.items()
    ]).sort_values("Pengaruh", key=abs, ascending=False)

    c1, c2 = st.columns([1.6, 1])
    with c1:
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#fff')
        ax.set_facecolor('#fff')
        d = df_kontribusi.sort_values("Pengaruh", ascending=True)
        vals = d["Pengaruh"].values
        y = np.arange(len(d))
        bars = ax.barh(y, vals, height=.58,
                       color=["#EF5B67" if x < 0 else "#18A77A" for x in vals], alpha=.9)
        ax.axvline(0, color="#17233B", linewidth=1.2)
        max_abs = max(abs(vals.min()), abs(vals.max()))
        ax.set_xlim(vals.min() - max_abs*.2, vals.max() + max_abs*.2)
        for bar, val in zip(bars, vals):
            off = max_abs*.035
            ax.text(val + (off if val >= 0 else -off),
                    bar.get_y()+bar.get_height()/2, f"{val:+.2f}",
                    va="center", ha="left" if val>=0 else "right",
                    fontsize=9, fontweight="bold")
        ax.set_yticks(y)
        ax.set_yticklabels(d["Faktor"], fontsize=9)
        ax.tick_params(axis="y", length=0, pad=7)
        ax.tick_params(axis="x", labelsize=8, colors="#667085")
        ax.grid(axis="x", alpha=.12)
        ax.set_axisbelow(True)
        for s in ["top","right","left"]:
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color("#D8E0EB")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with c2:
        positive = df_kontribusi[df_kontribusi["Pengaruh"] > 0].head(4)
        negative = df_kontribusi[df_kontribusi["Pengaruh"] < 0].sort_values("Pengaruh").head(4)

        st.markdown("**🟢 FAKTOR MENINGKATKAN NILAI**")
        if len(positive):
            for _, row in positive.iterrows():
                st.markdown(f"""
                <div style="padding:.6rem 0;border-bottom:1px solid #EEF2F7;font-size:.82rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span><b>{row['Faktor']}</b></span>
                        <span style="color:#18A77A;font-weight:800;">+{row['Pengaruh']:.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Belum ada faktor positif.")

        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        st.markdown("**🔴 FAKTOR MENURUNKAN NILAI**")
        if len(negative):
            for _, row in negative.iterrows():
                st.markdown(f"""
                <div style="padding:.6rem 0;border-bottom:1px solid #EEF2F7;font-size:.82rem;">
                    <div style="display:flex;justify-content:space-between;">
                        <span><b>{row['Faktor']}</b></span>
                        <span style="color:#EF5B67;font-weight:800;">{row['Pengaruh']:+.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Tidak ada faktor negatif.")

    siasat_section("📋 DETAIL PERBANDINGAN")

    tabel = df_kontribusi.copy()
    tabel["Selisih"] = tabel["Nilai"] - tabel["Rata"]
    tabel = tabel[["Faktor", "Nilai", "Rata", "Selisih", "Pengaruh"]]
    tabel.columns = ["Faktor", "Nilai Siswa", "Rata-rata", "Selisih", "Pengaruh (poin)"]
    tabel = tabel.sort_values("Pengaruh (poin)", key=abs, ascending=False)
    st.dataframe(tabel, use_container_width=True, hide_index=True)

    siasat_section("💾 SIMPAN DATA")

    if not nama_siswa:
        st.markdown("""
        <div class="siasat-warning">
            ⚠️ Isi <b>Nama Siswa</b> terlebih dahulu sebelum menyimpan.
        </div>
        """, unsafe_allow_html=True)
    else:
        duplikat = any(s["Nama"] == nama_siswa and s["Kelas"] == kelas_siswa
                       for s in st.session_state.database_siswa)
        if duplikat:
            st.markdown(f"""
            <div class="siasat-warning">
                ⚠️ Data siswa <b>{nama_siswa}</b> kelas <b>{kelas_siswa}</b> sudah tersimpan.
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button("💾 Simpan Hasil Siswa", type="primary", use_container_width=True, key="save_a"):
                data_baru = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nama": nama_siswa, "Kelas": kelas_siswa, "Absen": absen_siswa,
                    "Nilai Akademik": round(nilai_akademik,2),
                    "Selisih": round(selisih_nilai,2), "Kategori": kategori,
                    "Self-Efficacy": input_self_efficacy,
                    "Keterlibatan Ortu": input_keterlibatan,
                    "Harapan Ortu": input_harapan,
                    "Dukungan Sekolah": input_dukungan,
                    "Motivasi": input_motivasi,
                    "Kecemasan": input_kecemasan,
                    "Fasilitas": input_fasilitas,
                    "Kemalasan": input_kemalasan,
                    "Dicatat Oleh": st.session_state.user_nama,
                }
                st.session_state.database_siswa.append(data_baru)
                st.session_state.last_saved = {"nama": nama_siswa, "kelas": kelas_siswa}
                st.rerun()

        if st.session_state.last_saved:
            notifikasi_simpan(
                st.session_state.last_saved["nama"],
                st.session_state.last_saved["kelas"]
            )

# ================================================================
# DATABASE
# ================================================================

elif st.session_state.current_page == "database":
    siasat_breadcrumb("🗄️", "DATABASE SISWA")

    if len(st.session_state.database_siswa) == 0:
        st.markdown("""
        <div class="siasat-warning">
            📭 Belum ada data siswa. Silakan input siswa terlebih dahulu di menu <b>Analisis Siswa</b>.
        </div>
        """, unsafe_allow_html=True)
    else:
        df_db = pd.DataFrame(st.session_state.database_siswa)

        a, b, c, d = st.columns(4)
        with a: stat_box("Total Siswa", len(df_db), "siswa terarsip", "blue")
        with b: stat_box("Rata-rata", f"{df_db['Nilai Akademik'].mean():.2f}", "nilai seluruh siswa", "mint")
        with c: stat_box("Tertinggi", f"{df_db['Nilai Akademik'].max():.2f}", "nilai maksimum", "yellow")
        with d: stat_box("Terendah", f"{df_db['Nilai Akademik'].min():.2f}", "nilai minimum", "coral")

        siasat_section("📋 DAFTAR SISWA")

        c1, c2 = st.columns([1, 2])
        with c1:
            filter_kelas = st.selectbox("Filter Kelas",
                ["Semua"] + sorted(df_db["Kelas"].unique().tolist()), key="f_kelas")
        with c2:
            search = st.text_input("Cari nama", placeholder="Ketik nama siswa...", key="f_search")

        df_tampil = df_db.copy()
        if filter_kelas != "Semua":
            df_tampil = df_tampil[df_tampil["Kelas"] == filter_kelas]
        if search:
            df_tampil = df_tampil[df_tampil["Nama"].str.contains(search, case=False, na=False)]

        st.caption(f"**{len(df_tampil)} siswa ditemukan**")
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2)
        with c1:
            csv = df_tampil.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", data=csv,
                file_name=f"database_siswa_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv", use_container_width=True)
        with c2:
            if st.button("🗑️ Hapus semua data", use_container_width=True, key="del_all"):
                st.session_state.database_siswa = []
                st.rerun()

# ================================================================
# FAKTOR PENYEBAB
# ================================================================

elif st.session_state.current_page == "kausal":
    siasat_breadcrumb("📊", "FAKTOR PENYEBAB")

    st.markdown("""
    <div class="siasat-notice">
        <b>Faktor-faktor yang secara sebab-akibat mempengaruhi prestasi akademik siswa</b>, 
        berdasarkan analisis data seluruh siswa di sekolah.
    </div>
    """, unsafe_allow_html=True)

    df_ate = pd.DataFrame([{"Faktor": k, "Pengaruh": v} for k, v in PENGARUH_DATA.items()])
    positive_ate = df_ate[df_ate["Pengaruh"] > 0].sort_values("Pengaruh", ascending=False)
    negative_ate = df_ate[df_ate["Pengaruh"] < 0].sort_values("Pengaruh")

    a, b, c = st.columns(3)
    with a:
        top_pos = positive_ate.iloc[0]
        stat_box("Pendorong terbesar", f"+{top_pos['Pengaruh']:.2f}", top_pos["Faktor"], "mint")
    with b:
        top_neg = negative_ate.iloc[0]
        stat_box("Penghambat terbesar", f"{top_neg['Pengaruh']:.2f}", top_neg["Faktor"], "coral")
    with c:
        stat_box("Jumlah faktor", "8", "variabel dianalisis", "blue")

    siasat_section("📈 GRAFIK KEKUATAN PENGARUH")

    fig = plot_pengaruh(df_ate)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    siasat_section("📋 DAFTAR FAKTOR")

    tabel_ate = df_ate.copy()
    tabel_ate["Arah"] = tabel_ate["Pengaruh"].apply(lambda x: "🟢 Meningkatkan" if x>0 else "🔴 Menurunkan")
    tabel_ate = tabel_ate.sort_values("Pengaruh", ascending=False)
    tabel_ate.columns = ["Faktor", "Kekuatan Pengaruh", "Arah"]
    st.dataframe(tabel_ate, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="siasat-notice">
        <b>📌 Catatan Teknis:</b> Nilai ditampilkan dalam skala <b>Average Treatment Effect (ATE)</b> 
        dari analisis Structural Causal Model.
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# TINGKAT KEPENTINGAN
# ================================================================

elif st.session_state.current_page == "kepentingan":
    siasat_breadcrumb("📈", "TINGKAT KEPENTINGAN FAKTOR")

    st.markdown("""
    <div class="siasat-notice">
        <b>Faktor-faktor yang paling sering muncul dalam keputusan model</b> saat memprediksi nilai siswa.
        Semakin tinggi, semakin penting faktor tersebut.
    </div>
    """, unsafe_allow_html=True)

    df_shap = pd.DataFrame([{"Faktor": k, "Kepentingan": v} for k, v in KEPENTINGAN_DATA.items()])
    top = df_shap.sort_values("Kepentingan", ascending=False).iloc[0]
    second = df_shap.sort_values("Kepentingan", ascending=False).iloc[1]

    a, b, c = st.columns(3)
    with a: stat_box("Faktor #1", top["Faktor"], f"skor {top['Kepentingan']:.4f}", "blue")
    with b: stat_box("Faktor #2", second["Faktor"], f"skor {second['Kepentingan']:.4f}", "purple")
    with c: stat_box("Jumlah faktor", "8", "faktor dianalisis", "yellow")

    siasat_section("📊 GRAFIK TINGKAT KEPENTINGAN")

    fig = plot_kepentingan(df_shap)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    siasat_section("📋 RANKING LENGKAP")

    ranked = df_shap.sort_values("Kepentingan", ascending=False).reset_index(drop=True)
    for i, row in ranked.iterrows():
        pct = row["Kepentingan"] / ranked["Kepentingan"].max() * 100
        st.markdown(f"""
        <div style="padding:.6rem 0;border-bottom:1px solid #EEF2F7;font-size:.85rem;">
            <div style="display:flex;justify-content:space-between;margin-bottom:.3rem;">
                <span><b>{i+1:02d}. {row['Faktor']}</b></span>
                <span style="color:#2563EB;font-weight:800;">{row['Kepentingan']:.4f}</span>
            </div>
            <div style="height:6px;background:#EEF2F7;border-radius:99px;overflow:hidden;">
                <div style="width:{pct:.1f}%;height:100%;background:#4F7CFF;border-radius:99px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="siasat-notice">
        <b>📌 Catatan Teknis:</b> Nilai ditampilkan dalam skala <b>Mean |SHAP Value|</b>.
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# REKOMENDASI UMUM
# ================================================================

elif st.session_state.current_page == "rekomendasi":
    siasat_breadcrumb("💡", "REKOMENDASI UMUM")

    st.markdown("""
    <div class="siasat-notice">
        <b>Ringkasan faktor yang dapat menjadi prioritas tindak lanjut untuk tingkat sekolah.</b>
    </div>
    """, unsafe_allow_html=True)

    siasat_section("🟢 FAKTOR YANG PERLU DIPERKUAT")

    positive_priority = [
        ("Fasilitas Sekolah", PENGARUH_DATA["Fasilitas Sekolah"], KEPENTINGAN_DATA["Fasilitas Sekolah"],
         "Evaluasi dan optimalkan fasilitas belajar yang paling relevan dengan kebutuhan siswa."),
        ("Keterlibatan Orang Tua", PENGARUH_DATA["Keterlibatan Orang Tua"], KEPENTINGAN_DATA["Keterlibatan Orang Tua"],
         "Perkuat komunikasi dan pendampingan belajar antara sekolah dan keluarga."),
        ("Self-Efficacy Akademik", PENGARUH_DATA["Self-Efficacy Akademik"], KEPENTINGAN_DATA["Self-Efficacy Akademik"],
         "Dorong kepercayaan diri akademik melalui mentoring dan pengalaman belajar bertahap."),
    ]

    st.markdown("""
    <table class="siasat-table">
        <thead>
            <tr>
                <th style="width:40px;">No</th>
                <th style="width:220px;">Faktor</th>
                <th style="width:100px;">Pengaruh</th>
                <th style="width:100px;">Kepentingan</th>
                <th>Rekomendasi</th>
            </tr>
        </thead>
        <tbody>
    """ + "".join([f"""
        <tr>
            <td>{i:02d}</td>
            <td><b>{name}</b></td>
            <td style="color:#18A77A;font-weight:700;">+{ate:.2f}</td>
            <td>{shap:.4f}</td>
            <td>{desc}</td>
        </tr>
    """ for i, (name, ate, shap, desc) in enumerate(positive_priority, 1)]) + """
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    siasat_section("🔴 FAKTOR YANG PERLU DIEVALUASI")

    negative_priority = [
        ("Dukungan Sekolah", PENGARUH_DATA["Dukungan Sekolah"], KEPENTINGAN_DATA["Dukungan Sekolah"],
         "Evaluasi bentuk pendampingan agar dukungan tetap membantu tanpa mengurangi kemandirian siswa."),
        ("Harapan Orang Tua", PENGARUH_DATA["Harapan Orang Tua"], KEPENTINGAN_DATA["Harapan Orang Tua"],
         "Dorong target akademik yang realistis dan komunikasi yang tidak menambah tekanan belajar."),
        ("Motivasi Belajar", PENGARUH_DATA["Motivasi Belajar"], KEPENTINGAN_DATA["Motivasi Belajar"],
         "Identifikasi hambatan belajar dan gunakan pendekatan pembelajaran yang lebih relevan."),
    ]

    st.markdown("""
    <table class="siasat-table">
        <thead>
            <tr>
                <th style="width:40px;">No</th>
                <th style="width:220px;">Faktor</th>
                <th style="width:100px;">Pengaruh</th>
                <th style="width:100px;">Kepentingan</th>
                <th>Rekomendasi</th>
            </tr>
        </thead>
        <tbody>
    """ + "".join([f"""
        <tr>
            <td>{i:02d}</td>
            <td><b>{name}</b></td>
            <td style="color:#EF5B67;font-weight:700;">{ate:+.2f}</td>
            <td>{shap:.4f}</td>
            <td>{desc}</td>
        </tr>
    """ for i, (name, ate, shap, desc) in enumerate(negative_priority, 1)]) + """
        </tbody>
    </table>
    """, unsafe_allow_html=True)

# ================================================================
# CATATAN UNTUK GURU
# ================================================================

else:
    siasat_breadcrumb("🎯", "CATATAN UNTUK GURU")

    st.markdown("""
    <div class="siasat-notice">
        <b>Kesimpulan sebab-akibat dan tindak lanjut personal</b> yang bisa langsung dilakukan guru untuk siswa tertentu.
    </div>
    """, unsafe_allow_html=True)

    siasat_section("1️⃣ PILIH SISWA")

    opsi_sumber = st.radio(
        "Sumber data siswa",
        ["📁 Ambil dari database", "✍️ Input manual"],
        horizontal=True, key="g_sumber"
    )

    if opsi_sumber == "📁 Ambil dari database":
        if len(st.session_state.database_siswa) == 0:
            st.warning("⚠️ Database masih kosong. Silakan input siswa terlebih dahulu di menu Analisis Siswa.")
            st.stop()

        df_db = pd.DataFrame(st.session_state.database_siswa)
        opsi_siswa = df_db.apply(lambda x: f"{x['Nama']} — {x['Kelas']} (Absen {x['Absen']})", axis=1).tolist()
        pilihan = st.selectbox("Pilih Siswa", opsi_siswa, key="pilih_siswa_db")

        idx = opsi_siswa.index(pilihan)
        baris = df_db.iloc[idx]

        nama_siswa = baris["Nama"]
        kelas_siswa = baris["Kelas"]
        absen_siswa = int(baris["Absen"])
        nilai_akademik = float(baris["Nilai Akademik"])

        profil_siswa = {
            "Self-Efficacy Akademik": float(baris["Self-Efficacy"]),
            "Keterlibatan Orang Tua": float(baris["Keterlibatan Ortu"]),
            "Harapan Orang Tua": float(baris["Harapan Ortu"]),
            "Dukungan Sekolah": float(baris["Dukungan Sekolah"]),
            "Motivasi Belajar": float(baris["Motivasi"]),
            "Kecemasan Akademik": float(baris["Kecemasan"]),
            "Fasilitas Sekolah": float(baris["Fasilitas"]),
            "Kemalasan Belajar": float(baris["Kemalasan"]),
        }
    else:
        c1, c2, c3 = st.columns([1.6, .8, .7])
        with c1:
            nama_siswa = st.text_input("Nama Siswa", placeholder="Nama lengkap", key="g_nama")
        with c2:
            kelas_siswa = st.selectbox("Kelas", KELAS_LIST, key="g_kelas")
        with c3:
            absen_siswa = st.number_input("No. Absen", 1, 50, 1, key="g_absen")

        nilai_akademik = st.number_input(
            "Nilai Akademik", min_value=60.0, max_value=100.0, value=83.78,
            step=.01, format="%.2f", key="g_nilai"
        )

        st.markdown("**Profil 8 Faktor**")
        col1, col2 = st.columns(2)
        with col1:
            input_self_efficacy = input_kategori("g_se", "Self-Efficacy Akademik")
            input_motivasi = input_kategori("g_mot", "Motivasi Belajar")
            input_kecemasan = input_kategori("g_cem", "Kecemasan Akademik")
            input_kemalasan = input_kategori("g_mal", "Kemalasan Belajar")
        with col2:
            input_keterlibatan = input_kategori("g_ket", "Keterlibatan Orang Tua")
            input_harapan = input_kategori("g_har", "Harapan Orang Tua")
            input_dukungan = input_kategori("g_duk", "Dukungan Sekolah")
            input_fasilitas = input_kategori("g_fas", "Fasilitas Sekolah")

        profil_siswa = {
            "Self-Efficacy Akademik": input_self_efficacy,
            "Keterlibatan Orang Tua": input_keterlibatan,
            "Harapan Orang Tua": input_harapan,
            "Dukungan Sekolah": input_dukungan,
            "Motivasi Belajar": input_motivasi,
            "Kecemasan Akademik": input_kecemasan,
            "Fasilitas Sekolah": input_fasilitas,
            "Kemalasan Belajar": input_kemalasan,
        }

    selisih_nilai, kontribusi = analisis_kausal(nilai_akademik, profil_siswa)
    kategori, warna_kategori, simbol = kategori_nilai(nilai_akademik)

    df_kontribusi = pd.DataFrame([
        {"Aspek": k, "Kontribusi": v, "Nilai_Siswa": profil_siswa[k],
         "Baseline": BASELINE_ASPEK[k], "Selisih": profil_siswa[k] - BASELINE_ASPEK[k]}
        for k, v in kontribusi.items()
    ]).sort_values("Kontribusi")

    faktor_negatif = df_kontribusi[df_kontribusi["Kontribusi"] < -0.2].sort_values("Kontribusi")
    faktor_positif = df_kontribusi[df_kontribusi["Kontribusi"] > 0.2].sort_values("Kontribusi", ascending=False)

    siasat_section("2️⃣ KESIMPULAN SEBAB-AKIBAT")

    posisi = "di atas" if selisih_nilai >= 0 else "di bawah"
    abs_selisih = abs(selisih_nilai)

    if len(faktor_negatif) > 0:
        fn = faktor_negatif.iloc[0]
        narasi_negatif = f"Faktor yang paling menekan nilai <b>{nama_siswa}</b> adalah <b style='color:#EF5B67;'>{fn['Aspek']}</b> (kontribusi <b>{fn['Kontribusi']:.2f} poin</b>). Nilai siswa pada faktor ini adalah <b>{fn['Nilai_Siswa']:.2f}</b>, sedangkan rata-rata sekolah <b>{fn['Baseline']:.2f}</b>."
    else:
        narasi_negatif = "Tidak ada faktor yang secara signifikan menekan nilai siswa ini."

    if len(faktor_positif) > 0:
        fp = faktor_positif.iloc[0]
        narasi_positif = f"Kekuatan utama <b>{nama_siswa}</b> terletak pada <b style='color:#18A77A;'>{fp['Aspek']}</b> (kontribusi <b>+{fp['Kontribusi']:.2f} poin</b>)."
    else:
        narasi_positif = "Siswa ini belum memiliki faktor kekuatan dominan."

    st.markdown(f"""
    <div style="background:#F7F9FC;border:1px solid #E4EAF2;border-left:5px solid {warna_kategori};padding:1.2rem 1.5rem;border-radius:6px;margin:1rem 0;">
        <div style="font-family:'Manrope';font-size:1.2rem;font-weight:800;color:#17233B;margin-bottom:.8rem;">
            {nama_siswa}
        </div>
        <div style="font-family:'Arial';font-size:.85rem;color:#667085;margin-bottom:1rem;">
            {kelas_siswa} · Absen {absen_siswa:02d} · Nilai {nilai_akademik:.2f} · Kategori {simbol} {kategori}
        </div>
        <div style="font-size:.9rem;line-height:1.75;color:#1F2A44;">
            Nilai siswa berada <b>{abs_selisih:.2f} poin {posisi} rata-rata sekolah</b> (rata-rata {RATA_RATA_NILAI:.2f}).
            <br><br>
            {narasi_negatif}
            <br><br>
            {narasi_positif}
        </div>
    </div>
    """, unsafe_allow_html=True)

    siasat_section("3️⃣ PRIORITAS PERBAIKAN")

    prioritas = faktor_negatif.head(3)

    if len(prioritas) == 0:
        st.markdown("""
        <div class="siasat-notice">
            ✓ Tidak ada prioritas perbaikan mendesak. Semua faktor siswa ini dalam kondisi baik.
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, (_, row) in enumerate(prioritas.iterrows(), 1):
            st.markdown(f"""
            <div class="siasat-warning" style="margin:.8rem 0;">
                <b>PRIORITAS {i}: {row['Aspek']}</b><br>
                Nilai siswa: <b>{row['Nilai_Siswa']:.2f}</b> · Rata-rata: <b>{row['Baseline']:.2f}</b> · 
                Selisih: <b style="color:#EF5B67;">{row['Selisih']:+.2f}</b>
            </div>
            """, unsafe_allow_html=True)

    siasat_section("4️⃣ TINDAK LANJUT UNTUK GURU")

    TINDAK_LANJUT = {
        "Self-Efficacy Akademik": {
            "guru": ["Berikan tugas bertahap (mudah → sulit) agar siswa merasakan keberhasilan",
                     "Berikan pujian spesifik atas usaha, bukan hanya hasil",
                     "Ajak siswa merefleksikan pencapaian kecilnya setiap minggu",
                     "Dudukkan siswa dengan teman peer-mentor"],
            "siswa": ["Buat jurnal harian '1 hal yang berhasil saya lakukan hari ini'",
                      "Tetapkan target kecil yang realistis setiap minggu"]
        },
        "Keterlibatan Orang Tua": {
            "guru": ["Kirim pesan WhatsApp ke orang tua dengan kabar positif tentang anak",
                     "Ajak orang tua ikut 1 sesi belajar bersama di sekolah",
                     "Berikan panduan 'cara mendampingi anak belajar 15 menit/hari'",
                     "Jadwalkan komunikasi rutin 2 minggu sekali"],
            "siswa": ["Ceritakan ke orang tua 1 hal yang dipelajari di sekolah",
                      "Minta orang tua memeriksa PR minimal 2x seminggu"]
        },
        "Harapan Orang Tua": {
            "guru": ["Pertemuan dengan orang tua untuk membahas ekspektasi realistis",
                     "Bantu orang tua memahami tahap perkembangan belajar anak",
                     "Sarankan fokus pada usaha anak, bukan hanya nilai",
                     "Berikan contoh cara memotivasi tanpa menekan"],
            "siswa": ["Belajar menyampaikan perasaan kepada orang tua dengan tenang",
                      "Fokus pada usaha yang bisa dikontrol, bukan hasil akhir"]
        },
        "Dukungan Sekolah": {
            "guru": ["Refleksi: apakah bantuan justru mengurangi kemandirian?",
                     "Kurangi bantuan pada hal yang siswa bisa lakukan sendiri",
                     "Berikan kesempatan siswa untuk mencoba dan gagal (safe to fail)",
                     "Fokus pada scaffolding, bukan taking over"],
            "siswa": ["Coba selesaikan tugas sulit dulu selama 10 menit sebelum bertanya",
                      "Catat apa yang sudah dicoba sebelum minta bantuan"]
        },
        "Motivasi Belajar": {
            "guru": ["Kaitkan materi dengan kehidupan nyata siswa",
                     "Berikan pilihan tugas agar siswa merasa punya kontrol",
                     "Apresiasi proses, bukan hanya hasil",
                     "Ciptakan suasana kelas yang menyenangkan"],
            "siswa": ["Cari 1 hal menarik dari setiap mata pelajaran",
                      "Belajar bersama teman untuk menambah semangat"]
        },
        "Kecemasan Akademik": {
            "guru": ["Ajarkan teknik relaksasi sederhana sebelum ujian",
                     "Ubah suasana ujian jadi lebih santai",
                     "Berikan ujian formatif yang tidak menakutkan",
                     "Normalisasi bahwa cemas itu wajar"],
            "siswa": ["Latihan pernapasan 4-7-8 sebelum ujian",
                      "Persiapan lebih awal agar tidak panik"]
        },
        "Fasilitas Sekolah": {
            "guru": ["Informasikan fasilitas yang bisa dimanfaatkan siswa",
                     "Bantu siswa mengakses perpustakaan/lab di luar jam pelajaran",
                     "Cek apakah siswa punya hambatan akses fasilitas"],
            "siswa": ["Manfaatkan perpustakaan minimal 1x seminggu",
                      "Tanyakan ke guru jika butuh bantuan fasilitas"]
        },
        "Kemalasan Belajar": {
            "guru": ["Cari tahu akar kemalasan (bosan? sulit? tidak paham?)",
                     "Beri tugas yang lebih menantang jika bosan",
                     "Pecah tugas besar jadi langkah kecil",
                     "Buat sistem reward sederhana"],
            "siswa": ["Mulai dari tugas 5 menit saja",
                      "Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat)"]
        }
    }

    if len(prioritas) == 0:
        st.info("Tidak ada tindak lanjut khusus yang diperlukan.")
    else:
        for i, (_, row) in enumerate(prioritas.iterrows(), 1):
            aspek = row["Aspek"]
            tugas = TINDAK_LANJUT.get(aspek, {"guru": [], "siswa": []})

            with st.expander(f"🎯 Prioritas {i}: {aspek}", expanded=(i == 1)):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**👨‍🏫 Yang bisa dilakukan GURU:**")
                    for j, t in enumerate(tugas["guru"], 1):
                        st.markdown(f"""
                        <div style="display:flex;gap:.7rem;padding:.5rem 0;border-bottom:1px solid #EEF2F7;">
                            <div style="width:22px;height:22px;border-radius:4px;background:#EAF1FF;color:#2563EB;
                                        display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:800;flex-shrink:0;">
                                {j}
                            </div>
                            <div style="font-size:.82rem;line-height:1.55;color:#1F2A44;">{t}</div>
                        </div>
                        """, unsafe_allow_html=True)
                with col2:
                    st.markdown("**🎓 Yang bisa dilakukan SISWA:**")
                    for j, s in enumerate(tugas["siswa"], 1):
                        st.markdown(f"""
                        <div style="display:flex;gap:.7rem;padding:.5rem 0;border-bottom:1px solid #EEF2F7;">
                            <div style="width:22px;height:22px;border-radius:4px;background:#E8F8F1;color:#18A77A;
                                        display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:800;flex-shrink:0;">
                                {j}
                            </div>
                            <div style="font-size:.82rem;line-height:1.55;color:#1F2A44;">{s}</div>
                        </div>
                        """, unsafe_allow_html=True)

    siasat_section("5️⃣ SCRIPT KOMUNIKASI")

    st.markdown(f"""
    <div style="background:#F7F9FC;border-left:5px solid #7C5CFC;padding:1.2rem 1.5rem;border-radius:6px;margin:1rem 0;">
        <div style="font-family:'Manrope';font-weight:800;font-size:.9rem;color:#17233B;margin-bottom:.6rem;">
            💬 UNTUK BERBICARA DENGAN SISWA
        </div>
        <div style="font-size:.85rem;line-height:1.8;color:#1F2A44;font-style:italic;">
            "{nama_siswa}, Ibu/Bapak sudah melihat hasil belajarmu. 
            Ada hal positif yang Ibu/Bapak perhatikan: 
            <b style="color:#18A77A;">{faktor_positif.iloc[0]['Aspek'] if len(faktor_positif) > 0 else 'kamu sudah berusaha'}</b>.
            <br><br>
            Ibu/Bapak ingin bantu kamu untuk hal yang mungkin masih bisa ditingkatkan, 
            khususnya <b style="color:#EF5B67;">{prioritas.iloc[0]['Aspek'] if len(prioritas) > 0 else 'belajar'}</b>.
            Bukan karena kamu kurang, tapi karena Ibu/Bapak yakin kamu bisa lebih baik lagi.
            <br><br>
            Bagaimana kalau kita coba beberapa hal bersama?"
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#FFFBEB;border-left:5px solid #F6C945;padding:1.2rem 1.5rem;border-radius:6px;margin:1rem 0;">
        <div style="font-family:'Manrope';font-weight:800;font-size:.9rem;color:#17233B;margin-bottom:.6rem;">
            📞 UNTUK KOMUNIKASI DENGAN ORANG TUA
        </div>
        <div style="font-size:.85rem;line-height:1.8;color:#1F2A44;font-style:italic;">
            "Selamat siang Bapak/Ibu. Saya ingin berbagi tentang perkembangan 
            <b>{nama_siswa}</b> di sekolah.
            <br><br>
            <b>Kabar baiknya:</b> {nama_siswa} menunjukkan kekuatan di 
            <b style="color:#18A77A;">{faktor_positif.iloc[0]['Aspek'] if len(faktor_positif) > 0 else 'semangat belajar'}</b>.
            <br><br>
            <b>Yang ingin saya diskusikan:</b> ada beberapa hal yang mungkin bisa kita bantu bersama, 
            terutama di <b style="color:#EF5B67;">{prioritas.iloc[0]['Aspek'] if len(prioritas) > 0 else 'kebiasaan belajar'}</b>.
            <br><br>
            Kira-kira kapan waktu yang tepat untuk kita bicara lebih lanjut?"
        </div>
    </div>
    """, unsafe_allow_html=True)

    siasat_section("6️⃣ INDIKATOR KEBERHASILAN")

    indikator = [
        ("2 Minggu", "Siswa menunjukkan perubahan kecil di kelas (lebih aktif bertanya, lebih fokus)"),
        ("1 Bulan", "Nilai formatif (kuis, PR, tugas) mulai menunjukkan tren naik"),
        ("3 Bulan", "Nilai sumatif (ujian tengah/akhir semester) menunjukkan peningkatan stabil"),
        ("6 Bulan", "Perubahan perilaku belajar sudah menjadi kebiasaan siswa"),
    ]

    st.markdown("""
    <table class="siasat-table">
        <thead>
            <tr><th style="width:120px;">Waktu</th><th>Indikator</th></tr>
        </thead>
        <tbody>
    """ + "".join([f"<tr><td><b>{w}</b></td><td>{i}</td></tr>" for w, i in indikator]) + """
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    siasat_section("7️⃣ DOWNLOAD CATATAN")

    catatan_text = f"""CATATAN KONSULTASI GURU
=======================
Nama Siswa  : {nama_siswa}
Kelas       : {kelas_siswa}
Absen       : {absen_siswa}
Nilai       : {nilai_akademik:.2f}
Kategori    : {kategori}

KESIMPULAN
----------
Nilai siswa berada {abs(selisih_nilai):.2f} poin {"di atas" if selisih_nilai >= 0 else "di bawah"} rata-rata sekolah.

Faktor yang paling menekan: {prioritas.iloc[0]['Aspek'] if len(prioritas) > 0 else "-"}
Faktor kekuatan: {faktor_positif.iloc[0]['Aspek'] if len(faktor_positif) > 0 else "-"}

PRIORITAS PERBAIKAN
-------------------
"""
    for i, (_, row) in enumerate(prioritas.iterrows(), 1):
        catatan_text += f"{i}. {row['Aspek']} (selisih {row['Selisih']:+.2f})\n"

    catatan_text += f"""
Dibuat oleh: {st.session_state.user_nama}
Tanggal    : {datetime.now().strftime('%d %B %Y, %H:%M')}
"""

    st.download_button(
        "📥 Download Catatan (.txt)",
        data=catatan_text.encode("utf-8"),
        file_name=f"catatan_{nama_siswa.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.markdown('</div>', unsafe_allow_html=True)
