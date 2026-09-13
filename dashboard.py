from pathlib import Path

code = r'''import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import hashlib

st.set_page_config(
    page_title="Prestasi Akademik | SMPN 6 Salatiga",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================================================
# VISUAL SYSTEM — EDUCATIONAL VIBRANT
# ================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

:root{
    --ink:#17233B;
    --muted:#667085;
    --line:#E4EAF2;
    --canvas:#F7F9FC;
    --surface:#FFFFFF;
    --blue:#2563EB;
    --blue-2:#4F7CFF;
    --blue-soft:#EAF1FF;
    --yellow:#F6C945;
    --yellow-soft:#FFF7D6;
    --mint:#18A77A;
    --mint-soft:#E8F8F1;
    --coral:#EF5B67;
    --coral-soft:#FFF0F2;
    --purple:#7C5CFC;
    --purple-soft:#F1EDFF;
    --navy:#13213B;
}

html, body, [class*="css"]{
    font-family:'DM Sans',sans-serif;
    color:var(--ink);
}

.stApp{
    background:
        radial-gradient(circle at 92% 4%, rgba(79,124,255,.08), transparent 22rem),
        radial-gradient(circle at 4% 80%, rgba(246,201,69,.08), transparent 20rem),
        var(--canvas);
}

.main{background:transparent;}
.block-container{
    max-width:1480px;
    padding:1.6rem 2.7rem 4rem 2.7rem;
}

#MainMenu, footer, header{visibility:hidden;}

h1,h2,h3,h4{
    font-family:'Manrope',sans-serif;
}

/* ---------- subtle motion ---------- */
@keyframes riseIn{
    from{opacity:0; transform:translateY(10px);}
    to{opacity:1; transform:translateY(0);}
}
@keyframes growBar{
    from{transform:scaleX(0); transform-origin:left;}
    to{transform:scaleX(1); transform-origin:left;}
}
@keyframes floatDot{
    0%,100%{transform:translateY(0);}
    50%{transform:translateY(-7px);}
}

.motion{
    animation:riseIn .45s ease both;
}

.dashboard-hero{
    position:relative;
    overflow:hidden;
    background:var(--surface);
    border:1px solid var(--line);
    border-radius:28px;
    padding:2.1rem 2.3rem;
    box-shadow:0 16px 45px rgba(30,50,90,.07);
    animation:riseIn .45s ease both;
}
.dashboard-hero:before{
    content:"";
    position:absolute;
    width:180px;height:180px;
    right:-65px;top:-70px;
    border:30px solid rgba(37,99,235,.07);
    border-radius:50%;
}
.dashboard-hero:after{
    content:"";
    position:absolute;
    width:10px;height:10px;
    right:130px;bottom:35px;
    background:var(--yellow);
    border-radius:50%;
    box-shadow:
        42px -22px 0 var(--blue),
        78px 9px 0 var(--mint),
        112px -30px 0 var(--purple);
    animation:floatDot 3s ease-in-out infinite;
}

.eyebrow{
    display:inline-flex;
    align-items:center;
    gap:8px;
    font-size:.68rem;
    font-weight:800;
    letter-spacing:1.5px;
    text-transform:uppercase;
    color:var(--blue);
    margin-bottom:.7rem;
}
.eyebrow-dot{
    width:8px;height:8px;
    background:var(--yellow);
    border-radius:50%;
    display:inline-block;
}

.hero-title{
    font-size:clamp(2.15rem,4vw,3.8rem);
    line-height:1.02;
    letter-spacing:-2.4px;
    margin:0;
    max-width:850px;
}
.hero-title .accent{color:var(--blue);}
.hero-sub{
    color:var(--muted);
    font-size:.98rem;
    line-height:1.65;
    max-width:790px;
    margin:.9rem 0 0;
}
.hero-meta{
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    margin-top:1.25rem;
}
.pill{
    display:inline-flex;
    align-items:center;
    gap:7px;
    padding:.42rem .7rem;
    border-radius:999px;
    font-size:.65rem;
    font-weight:800;
    letter-spacing:.5px;
    border:1px solid var(--line);
    background:#fff;
}
.pill.blue{background:var(--blue-soft);color:var(--blue);border-color:#D4E0FF;}
.pill.yellow{background:var(--yellow-soft);color:#936F00;border-color:#F3DF8D;}
.pill.mint{background:var(--mint-soft);color:#087453;border-color:#BCE8D7;}

.section-wrap{
    margin-top:2rem;
    margin-bottom:1rem;
}
.section-number{
    display:inline-flex;
    width:38px;height:38px;
    align-items:center;justify-content:center;
    border-radius:12px;
    background:var(--blue);
    color:#fff;
    font-size:.78rem;
    font-weight:800;
    box-shadow:0 8px 18px rgba(37,99,235,.2);
}
.section-title{
    font-size:1.45rem;
    letter-spacing:-.7px;
    margin:0;
}
.section-sub{
    color:var(--muted);
    font-size:.72rem;
    text-transform:uppercase;
    letter-spacing:1.1px;
    font-weight:800;
    margin-top:.2rem;
}
.section-line{
    height:1px;
    background:var(--line);
    margin-top:.9rem;
}

/* ---------- cards ---------- */
.card{
    background:var(--surface);
    border:1px solid var(--line);
    border-radius:20px;
    padding:1.25rem 1.35rem;
    box-shadow:0 10px 28px rgba(30,50,90,.045);
    transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease;
    animation:riseIn .45s ease both;
}
.card:hover{
    transform:translateY(-3px);
    box-shadow:0 15px 35px rgba(30,50,90,.08);
    border-color:#CFD9EA;
}
.card-blue{background:linear-gradient(135deg,#fff 0%,#F3F7FF 100%);}
.card-yellow{background:linear-gradient(135deg,#fff 0%,#FFFBEB 100%);}
.card-mint{background:linear-gradient(135deg,#fff 0%,#F1FBF7 100%);}
.card-purple{background:linear-gradient(135deg,#fff 0%,#F7F4FF 100%);}
.card-dark{
    background:var(--navy);
    border-color:var(--navy);
    color:#fff;
}

.card-label{
    font-size:.65rem;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:1px;
    color:var(--muted);
}
.card-value{
    font-family:'Manrope',sans-serif;
    font-size:2rem;
    font-weight:800;
    letter-spacing:-1.2px;
    line-height:1;
    margin-top:.5rem;
}
.card-note{
    color:var(--muted);
    font-size:.74rem;
    margin-top:.45rem;
}

.stat-card{
    min-height:122px;
    position:relative;
    overflow:hidden;
}
.stat-card:after{
    content:"";
    position:absolute;
    width:70px;height:70px;
    border-radius:50%;
    right:-28px;bottom:-28px;
    background:rgba(37,99,235,.06);
}
.stat-card .topline{
    width:34px;height:5px;border-radius:99px;margin-bottom:.85rem;
}
.topline.blue{background:var(--blue);}
.topline.yellow{background:var(--yellow);}
.topline.mint{background:var(--mint);}
.topline.coral{background:var(--coral);}
.topline.purple{background:var(--purple);}

.profile-card{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:1rem;
    padding:1.15rem 1.3rem;
    background:#fff;
    border:1px solid var(--line);
    border-radius:18px;
}
.profile-avatar{
    width:48px;height:48px;
    border-radius:15px;
    display:flex;align-items:center;justify-content:center;
    background:var(--blue-soft);
    color:var(--blue);
    font-weight:800;
    font-size:1rem;
}
.profile-name{
    font-family:'Manrope',sans-serif;
    font-weight:800;
    font-size:1.05rem;
}
.profile-meta{
    color:var(--muted);
    font-size:.72rem;
    margin-top:.2rem;
}

.factor-card{
    border:1px solid var(--line);
    border-radius:18px;
    background:#fff;
    padding:1rem 1.05rem;
    margin:.65rem 0;
    transition:all .2s ease;
}
.factor-card:hover{
    transform:translateX(3px);
    box-shadow:0 8px 22px rgba(30,50,90,.06);
}
.factor-head{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:1rem;
}
.factor-name{font-weight:700;font-size:.86rem;}
.factor-value{
    font-family:'Manrope',sans-serif;
    font-weight:800;
    font-size:1rem;
}
.factor-bar{
    height:7px;
    background:#EEF2F7;
    border-radius:99px;
    overflow:hidden;
    margin-top:.75rem;
}
.factor-fill{
    height:100%;
    border-radius:99px;
    animation:growBar .7s ease both;
}
.fill-blue{background:var(--blue);}
.fill-yellow{background:var(--yellow);}
.fill-mint{background:var(--mint);}
.fill-purple{background:var(--purple);}
.fill-coral{background:var(--coral);}

.info-box{
    border-radius:18px;
    padding:1.1rem 1.2rem;
    border:1px solid var(--line);
    background:#fff;
}
.info-box.blue{background:var(--blue-soft);border-color:#D5E1FF;}
.info-box.yellow{background:var(--yellow-soft);border-color:#F1DF96;}
.info-box.mint{background:var(--mint-soft);border-color:#C5EBDD;}
.info-box.coral{background:var(--coral-soft);border-color:#F4CDD3;}
.info-title{font-weight:800;font-size:.9rem;}
.info-text{font-size:.78rem;line-height:1.6;margin-top:.35rem;color:#475467;}

.rank-row{
    display:grid;
    grid-template-columns:34px 1fr auto;
    align-items:center;
    gap:.8rem;
    padding:.75rem 0;
    border-bottom:1px solid var(--line);
}
.rank-row:last-child{border-bottom:0;}
.rank-num{
    width:30px;height:30px;
    border-radius:10px;
    background:var(--blue-soft);
    color:var(--blue);
    display:flex;align-items:center;justify-content:center;
    font-size:.68rem;font-weight:800;
}
.rank-name{font-weight:700;font-size:.8rem;}
.rank-desc{font-size:.67rem;color:var(--muted);margin-top:.15rem;}
.rank-value{
    font-family:'Manrope',sans-serif;
    font-size:.86rem;
    font-weight:800;
}
.positive{color:var(--mint);}
.negative{color:var(--coral);}

/* ---------- inputs ---------- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox [data-baseweb="select"] > div{
    background:#fff !important;
    border:1px solid #D7DFEA !important;
    border-radius:12px !important;
    min-height:43px;
    color:var(--ink) !important;
}
.stTextInput label,.stNumberInput label,.stSelectbox label{
    font-size:.72rem !important;
    font-weight:800 !important;
    color:#475467 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus{
    border-color:var(--blue) !important;
    box-shadow:0 0 0 3px rgba(37,99,235,.10) !important;
}
.stSlider label{
    font-size:.78rem !important;
    font-weight:700 !important;
    color:var(--ink) !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"]{
    background:var(--blue) !important;
}
.stButton > button,.stDownloadButton > button{
    border-radius:12px !important;
    min-height:43px;
    font-weight:800 !important;
    border:1px solid #D7DFEA !important;
    transition:all .18s ease !important;
}
.stButton > button:hover,.stDownloadButton > button:hover{
    transform:translateY(-2px);
    box-shadow:0 8px 20px rgba(30,50,90,.08);
}
button[kind="primary"]{
    background:var(--blue) !important;
    border-color:var(--blue) !important;
    color:#fff !important;
}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{
    background:var(--navy);
    border-right:0;
}
[data-testid="stSidebar"] > div:first-child{padding:1rem .9rem;}
[data-testid="stSidebar"] *{color:#EEF3FF !important;}

.side-brand{
    padding:.65rem .55rem 1rem;
}
.side-kicker{
    color:#9DBBFF !important;
    font-size:.62rem;
    font-weight:800;
    letter-spacing:1.7px;
    text-transform:uppercase;
}
.side-title{
    font-family:'Manrope',sans-serif;
    color:#fff;
    font-size:1.45rem;
    font-weight:800;
    line-height:1.05;
    margin-top:.35rem;
}
.side-title span{color:#F6C945;}
.side-year{
    color:#9BAAC4 !important;
    font-size:.62rem;
    letter-spacing:1.4px;
    margin-top:.45rem;
}
.side-user{
    background:rgba(255,255,255,.07);
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px;
    padding:.8rem;
    margin:.5rem 0 1rem;
}
.side-user-label{
    color:#9BAAC4 !important;
    font-size:.57rem;
    font-weight:800;
    letter-spacing:1.2px;
}
.side-user-name{
    color:#fff;
    font-weight:800;
    font-size:.88rem;
    margin-top:.25rem;
}

[data-testid="stSidebar"] .stRadio > label{
    font-size:.62rem !important;
    font-weight:800 !important;
    color:#9BAAC4 !important;
    letter-spacing:1.2px;
    text-transform:uppercase;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"]{gap:.35rem;}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label{
    background:transparent;
    border:1px solid transparent;
    border-radius:13px;
    padding:.72rem .72rem !important;
    transition:all .18s ease;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover{
    background:rgba(255,255,255,.07);
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"]{
    background:#2563EB;
    border-color:#4F7CFF;
    box-shadow:0 8px 20px rgba(37,99,235,.25);
}
[data-testid="stSidebar"] .stButton > button{
    background:rgba(255,255,255,.06) !important;
    color:#fff !important;
    border-color:rgba(255,255,255,.12) !important;
}

/* ---------- tables ---------- */
[data-testid="stDataFrame"]{
    border:1px solid var(--line);
    border-radius:16px;
    overflow:hidden;
    box-shadow:0 8px 25px rgba(30,50,90,.04);
}

/* ---------- login ---------- */
.login-shell{
    max-width:930px;
    margin:5vh auto 0;
}
.login-panel{
    display:grid;
    grid-template-columns:1.12fr .88fr;
    overflow:hidden;
    border-radius:30px;
    border:1px solid var(--line);
    box-shadow:0 24px 70px rgba(24,45,82,.12);
    background:#fff;
    animation:riseIn .5s ease both;
}
.login-visual{
    position:relative;
    min-height:500px;
    padding:2.5rem;
    overflow:hidden;
    background:var(--navy);
    color:#fff;
}
.login-visual:before{
    content:"";
    position:absolute;
    width:330px;height:330px;
    border-radius:50%;
    border:50px solid rgba(79,124,255,.12);
    right:-145px;top:-120px;
}
.login-visual:after{
    content:"";
    position:absolute;
    width:9px;height:9px;
    left:42px;bottom:55px;
    border-radius:50%;
    background:var(--yellow);
    box-shadow:35px -22px 0 #4F7CFF, 75px -4px 0 #18A77A, 113px -28px 0 #7C5CFC;
    animation:floatDot 3.2s ease-in-out infinite;
}
.login-kicker{
    font-size:.65rem;
    font-weight:800;
    letter-spacing:1.6px;
    color:#9DBBFF;
}
.login-title{
    font-family:'Manrope',sans-serif;
    font-size:clamp(2.8rem,5vw,4.8rem);
    line-height:.95;
    letter-spacing:-3px;
    margin-top:3.2rem;
}
.login-title span{color:var(--yellow);}
.login-copy{
    color:#C6D1E5;
    line-height:1.65;
    max-width:420px;
    margin-top:1rem;
}
.login-feature{
    position:absolute;
    bottom:34px;
    left:2.5rem;
    right:2.5rem;
    display:flex;
    gap:.6rem;
    flex-wrap:wrap;
}
.login-feature span{
    padding:.45rem .65rem;
    border-radius:999px;
    background:rgba(255,255,255,.08);
    color:#D9E3F5;
    font-size:.62rem;
    font-weight:700;
}
.login-form{
    padding:2.5rem;
    display:flex;
    flex-direction:column;
    justify-content:center;
}
.login-form-title{
    font-family:'Manrope',sans-serif;
    font-size:1.45rem;
    font-weight:800;
}
.login-form-sub{
    color:var(--muted);
    font-size:.78rem;
    margin:.35rem 0 1.4rem;
}
.demo-note{
    margin-top:1rem;
    padding:.75rem .9rem;
    border-radius:13px;
    background:var(--yellow-soft);
    color:#725A00;
    font-size:.7rem;
    line-height:1.5;
}

@media(max-width:850px){
    .block-container{padding:1rem 1rem 3rem;}
    .login-shell{margin:1rem auto 0;}
    .login-panel{grid-template-columns:1fr;}
    .login-visual{min-height:360px;}
    .login-title{margin-top:2.5rem;}
    .login-feature{position:static;margin-top:3rem;}
}
</style>
""", unsafe_allow_html=True)

# ================================================================
# AUTHENTICATION
# ================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    "admin": {"password": hash_password("admin123"), "nama": "Administrator"},
    "guru": {"password": hash_password("guru123"), "nama": "Guru SMPN 6"},
    "regina": {"password": hash_password("regina2026"), "nama": "Regina Ria"},
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_nama" not in st.session_state:
    st.session_state.user_nama = None
if "database_siswa" not in st.session_state:
    st.session_state.database_siswa = []

# ================================================================
# DATA / MODEL OUTPUTS — preserved from original dashboard
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

ATE_DATA = {
    "Self-Efficacy Akademik": 2.0698,
    "Keterlibatan Orang Tua": 2.2100,
    "Harapan Orang Tua": -1.5323,
    "Dukungan Sekolah": -3.8797,
    "Motivasi Belajar": -0.2850,
    "Kecemasan Akademik": 0.4522,
    "Kemalasan Belajar": -0.0902,
    "Fasilitas Sekolah": 2.4295,
}

SHAP_DATA = {
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


def section_header(num, title, subtitle):
    st.markdown(f"""
    <div class="section-wrap motion">
        <div style="display:flex;align-items:center;gap:.85rem;">
            <div class="section-number">{num}</div>
            <div>
                <h2 class="section-title">{title}</h2>
                <div class="section-sub">{subtitle}</div>
            </div>
        </div>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)


def hero_header(eyebrow, title, subtitle, pills=None):
    pills = pills or []
    pills_html = "".join(
        f'<span class="pill {kind}">{text}</span>'
        for text, kind in pills
    )
    st.markdown(f"""
    <div class="dashboard-hero">
        <div class="eyebrow"><span class="eyebrow-dot"></span>{eyebrow}</div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-sub">{subtitle}</p>
        <div class="hero-meta">{pills_html}</div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(label, value, note="", accent="blue", extra_class=""):
    st.markdown(f"""
    <div class="card stat-card {extra_class}">
        <div class="topline {accent}"></div>
        <div class="card-label">{label}</div>
        <div class="card-value">{value}</div>
        <div class="card-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def factor_card(name, value, accent="blue"):
    pct = max(0, min(100, value / 5 * 100))
    st.markdown(f"""
    <div class="factor-card">
        <div class="factor-head">
            <div class="factor-name">{name}</div>
            <div class="factor-value">{value:.2f}</div>
        </div>
        <div class="factor-bar">
            <div class="factor-fill fill-{accent}" style="width:{pct:.1f}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def plot_ate(df):
    df = df.sort_values("ATE", ascending=True)
    fig, ax = plt.subplots(figsize=(11, 6.3))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    vals = df["ATE"].values
    labels = df["Konstruk"].values
    y = np.arange(len(df))

    bars = ax.barh(
        y, vals,
        height=.58,
        color=["#EF5B67" if x < 0 else "#18A77A" for x in vals],
        alpha=.9
    )
    ax.axvline(0, color="#17233B", linewidth=1.3)

    max_abs = max(abs(vals.min()), abs(vals.max()))
    pad = max_abs * .15
    ax.set_xlim(vals.min() - pad, vals.max() + pad)

    for bar, val in zip(bars, vals):
        offset = .07 if val >= 0 else -.07
        ha = "left" if val >= 0 else "right"
        ax.text(
            val + offset,
            bar.get_y() + bar.get_height()/2,
            f"{val:+.2f}",
            va="center",
            ha=ha,
            fontsize=9.5,
            fontweight="bold"
        )

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", labelsize=8, colors="#667085")
    ax.grid(axis="x", alpha=.12, linewidth=.7)
    ax.set_axisbelow(True)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#D8E0EB")

    ax.set_xlabel(
        "Average Treatment Effect (ATE)",
        fontsize=9,
        fontweight="bold",
        color="#667085",
        labelpad=10
    )
    plt.tight_layout()
    return fig


def plot_shap(df):
    df = df.sort_values("Mean_SHAP", ascending=True)
    fig, ax = plt.subplots(figsize=(11, 6.3))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    vals = df["Mean_SHAP"].values
    labels = df["Konstruk"].values
    y = np.arange(len(df))

    bars = ax.barh(y, vals, height=.58, color="#4F7CFF", alpha=.9)
    ax.set_xlim(0, max(vals) * 1.18)

    for bar, val in zip(bars, vals):
        ax.text(
            val + max(vals)*.018,
            bar.get_y() + bar.get_height()/2,
            f"{val:.4f}",
            va="center",
            fontsize=9.5,
            fontweight="bold"
        )

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", labelsize=8, colors="#667085")
    ax.grid(axis="x", alpha=.12, linewidth=.7)
    ax.set_axisbelow(True)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#D8E0EB")

    ax.set_xlabel(
        "Mean |SHAP Value|",
        fontsize=9,
        fontweight="bold",
        color="#667085",
        labelpad=10
    )
    plt.tight_layout()
    return fig


def initial_profile():
    return {
        "Self-Efficacy Akademik": 4.63,
        "Keterlibatan Orang Tua": 4.35,
        "Harapan Orang Tua": 3.45,
        "Dukungan Sekolah": 4.60,
        "Motivasi Belajar": 2.52,
        "Kecemasan Akademik": 2.89,
        "Fasilitas Sekolah": 4.88,
        "Kemalasan Belajar": 1.49,
    }


# ================================================================
# LOGIN
# ================================================================

def halaman_login():
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    st.markdown("""
    <div class="login-panel">
        <div class="login-visual">
            <div class="login-kicker">SISTEM ANALITIK AKADEMIK · 2026</div>
            <div class="login-title">
                Prestasi<br><span>Akademik.</span>
            </div>
            <div class="login-copy">
                Dashboard analitik untuk membaca pola prestasi siswa melalui
                pendekatan kausal dan explainable machine learning.
            </div>
            <div class="login-feature">
                <span>CAUSAL ANALYSIS</span>
                <span>RANDOM FOREST</span>
                <span>SHAP</span>
                <span>SMPN 6 SALATIGA</span>
            </div>
        </div>
        <div class="login-form">
            <div class="login-form-title">Selamat datang 👋</div>
            <div class="login-form-sub">Masuk untuk melanjutkan ke dashboard.</div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Masukkan username")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")
        submit = st.form_submit_button("Masuk ke Dashboard →", type="primary", use_container_width=True)

        if submit:
            if username in USERS and USERS[username]["password"] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.user_nama = USERS[username]["nama"]
                st.rerun()
            else:
                st.error("Username atau password salah.")

    st.markdown("""
            <div class="demo-note">
                <b>Akun demo</b><br>
                admin / admin123 · guru / guru123 · regina / regina2026
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)


if not st.session_state.logged_in:
    halaman_login()
    st.stop()

# ================================================================
# SIDEBAR
# ================================================================

with st.sidebar:
    st.markdown("""
    <div class="side-brand">
        <div class="side-kicker">ACADEMIC INSIGHTS</div>
        <div class="side-title">Prestasi <span>Akademik.</span></div>
        <div class="side-year">SMPN 6 SALATIGA · 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="side-user">
        <div class="side-user-label">PENGGUNA AKTIF</div>
        <div class="side-user-name">{st.session_state.user_nama}</div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "NAVIGASI",
        [
            "01 · Analisis Sebab-Akibat",
            "02 · Database Siswa",
            "03 · Analisis Kausal",
            "04 · Analisis SHAP",
            "05 · Rekomendasi",
        ],
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    if st.button("Keluar dari Dashboard", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_nama = None
        st.rerun()

    st.markdown("""
    <div style="text-align:center;margin-top:1.3rem;color:#7F8DA8;font-size:.58rem;letter-spacing:1.4px;">
        HYBRID CAUSAL · XAI
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# MENU 1 — ANALISIS SEBAB-AKIBAT
# ================================================================

if menu == "01 · Analisis Sebab-Akibat":
    hero_header(
        "ANALISIS UTAMA",
        "Understand the student.<br><span class='accent'>Improve the outcome.</span>",
        "Masukkan profil siswa untuk melihat posisi nilainya, perbandingan terhadap baseline, "
        "serta kontribusi faktor berdasarkan hasil analisis yang digunakan dalam penelitian.",
        [
            ("8 KONSTRUK", "blue"),
            ("ATE", "mint"),
            ("SHAP", "yellow"),
        ],
    )

    section_header("01", "Data Siswa", "IDENTITAS & NILAI RAPOR")

    c1, c2, c3 = st.columns([1.6, .8, .7])
    with c1:
        nama_siswa = st.text_input("Nama Siswa", placeholder="Nama lengkap siswa")
    with c2:
        kelas_siswa = st.selectbox(
            "Kelas", KELAS_LIST,
            index=KELAS_LIST.index("IX-A")
        )
    with c3:
        absen_siswa = st.number_input("No. Absen", 1, 50, 1)

    c1, c2 = st.columns([1.5, 1])
    with c1:
        nilai_akademik = st.number_input(
            "Nilai Rata-rata Rapor",
            min_value=60.0,
            max_value=100.0,
            value=83.78,
            step=.01,
            format="%.2f",
            help=f"Baseline rata-rata sekolah: {RATA_RATA_NILAI:.2f}",
        )
    with c2:
        gap = nilai_akademik - RATA_RATA_NILAI
        gap_label = "di atas baseline" if gap >= 0 else "di bawah baseline"
        gap_accent = "mint" if gap >= 0 else "coral"
        stat_card(
            "Posisi terhadap baseline",
            f"{gap:+.2f}",
            f"poin · {gap_label}",
            gap_accent,
        )

    section_header("02", "Profil Siswa", "8 KONSTRUK · SKALA 1–5")

    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div class="card card-blue">
            <div class="card-label">FAKTOR INTERNAL</div>
            <div style="color:#667085;font-size:.72rem;margin-top:.25rem;">
                Kondisi yang berada pada sisi internal siswa.
            </div>
        </div>
        """, unsafe_allow_html=True)

        input_self_efficacy = st.slider("Self-Efficacy Akademik", 1.0, 5.0, 4.63, .1)
        input_motivasi = st.slider("Motivasi Belajar", 1.0, 5.0, 2.52, .1)
        input_kecemasan = st.slider("Kecemasan Akademik", 1.0, 5.0, 2.89, .1)
        input_kemalasan = st.slider("Kemalasan Belajar", 1.0, 5.0, 1.49, .1)

    with right:
        st.markdown("""
        <div class="card card-yellow">
            <div class="card-label">FAKTOR EKSTERNAL</div>
            <div style="color:#667085;font-size:.72rem;margin-top:.25rem;">
                Lingkungan keluarga dan sekolah yang terkait dengan siswa.
            </div>
        </div>
        """, unsafe_allow_html=True)

        input_keterlibatan = st.slider("Keterlibatan Orang Tua", 1.0, 5.0, 4.35, .1)
        input_harapan = st.slider("Harapan Orang Tua", 1.0, 5.0, 3.45, .1)
        input_dukungan = st.slider("Dukungan Sekolah", 1.0, 5.0, 4.60, .1)
        input_fasilitas = st.slider("Fasilitas Sekolah", 1.0, 5.0, 4.88, .1)

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

    section_header("03", "Academic Snapshot", "RINGKASAN KONDISI SISWA")

    if nama_siswa:
        initials = "".join(x[0] for x in nama_siswa.split()[:2]).upper()
        st.markdown(f"""
        <div class="profile-card">
            <div style="display:flex;align-items:center;gap:.85rem;">
                <div class="profile-avatar">{initials}</div>
                <div>
                    <div class="profile-name">{nama_siswa}</div>
                    <div class="profile-meta">{kelas_siswa} · No. Absen {absen_siswa:02d}</div>
                </div>
            </div>
            <span class="pill blue">SUBJEK ANALISIS</span>
        </div>
        """, unsafe_allow_html=True)

    a,b,c = st.columns(3)
    with a:
        stat_card("Nilai Akademik", f"{nilai_akademik:.2f}", "nilai rata-rata rapor", "blue")
    with b:
        stat_card("Selisih Baseline", f"{selisih_nilai:+.2f}", "poin dari rata-rata sekolah",
                  "mint" if selisih_nilai >= 0 else "coral")
    with c:
        st.markdown(f"""
        <div class="card stat-card">
            <div class="topline {'mint' if kategori=='Sangat Baik' else 'blue' if kategori=='Baik' else 'yellow' if kategori=='Cukup' else 'coral'}"></div>
            <div class="card-label">KATEGORI NILAI</div>
            <div class="card-value" style="font-size:1.55rem;color:{warna_kategori};">{simbol} {kategori}</div>
            <div class="card-note">klasifikasi berdasarkan rentang nilai</div>
        </div>
        """, unsafe_allow_html=True)

    # score band
    st.markdown("<div style='height:.9rem'></div>", unsafe_allow_html=True)
    score_pct = max(0, min(100, (nilai_akademik - 60) / 40 * 100))
    baseline_pct = max(0, min(100, (RATA_RATA_NILAI - 60) / 40 * 100))
    st.markdown(f"""
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div class="card-label">POSISI NILAI</div>
                <div style="font-weight:800;font-size:.88rem;margin-top:.2rem;">
                    Skala 60–100
                </div>
            </div>
            <div style="font-family:'Manrope';font-weight:800;color:#2563EB;">
                {nilai_akademik:.2f}
            </div>
        </div>
        <div style="height:12px;background:#EEF2F7;border-radius:99px;margin-top:1rem;position:relative;overflow:hidden;">
            <div style="width:{score_pct:.1f}%;height:100%;background:#4F7CFF;border-radius:99px;animation:growBar .8s ease both;"></div>
            <div style="position:absolute;left:{baseline_pct:.1f}%;top:-3px;width:3px;height:18px;background:#17233B;border-radius:99px;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:.45rem;color:#667085;font-size:.62rem;">
            <span>60</span><span>Baseline {RATA_RATA_NILAI:.2f}</span><span>100</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section_header("04", "Faktor yang Membentuk Nilai", "KONTRIBUSI TERHADAP SELISIH NILAI")

    df_kontribusi = pd.DataFrame([
        {
            "Aspek": k,
            "Kontribusi": v,
            "Nilai_Siswa": profil_siswa[k],
            "Baseline": BASELINE_ASPEK[k],
            "Selisih": profil_siswa[k] - BASELINE_ASPEK[k],
        }
        for k, v in kontribusi.items()
    ]).sort_values("Kontribusi", key=abs, ascending=False)

    positive = df_kontribusi[df_kontribusi["Kontribusi"] > 0].head(4)
    negative = df_kontribusi[df_kontribusi["Kontribusi"] < 0].sort_values("Kontribusi").head(4)

    c1,c2 = st.columns([1.65,1])

    with c1:
        fig, ax = plt.subplots(figsize=(10.5,6.2))
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        d = df_kontribusi.sort_values("Kontribusi", ascending=True)
        vals = d["Kontribusi"].values
        y = np.arange(len(d))
        bars = ax.barh(
            y, vals, height=.56,
            color=["#EF5B67" if x < 0 else "#18A77A" for x in vals],
            alpha=.9
        )
        ax.axvline(0,color="#17233B",linewidth=1.2)
        max_abs=max(abs(vals.min()),abs(vals.max()))
        ax.set_xlim(vals.min()-max_abs*.2,vals.max()+max_abs*.2)

        for bar,val in zip(bars,vals):
            off=max_abs*.035
            ax.text(
                val+(off if val>=0 else -off),
                bar.get_y()+bar.get_height()/2,
                f"{val:+.2f}",
                va="center",
                ha="left" if val>=0 else "right",
                fontsize=9,
                fontweight="bold"
            )
        ax.set_yticks(y)
        ax.set_yticklabels(d["Aspek"],fontsize=8.5)
        ax.tick_params(axis="y",length=0,pad=7)
        ax.tick_params(axis="x",labelsize=8,colors="#667085")
        ax.grid(axis="x",alpha=.12)
        ax.set_axisbelow(True)
        for spine in ["top","right","left"]:
            ax.spines[spine].set_visible(False)
        ax.spines["bottom"].set_color("#D8E0EB")
        ax.set_xlabel("Kontribusi (poin nilai)",fontsize=9,fontweight="bold",color="#667085")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with c2:
        st.markdown("""
        <div class="card">
            <div class="card-label">TOP POSITIVE INFLUENCES</div>
        """, unsafe_allow_html=True)
        if len(positive):
            for i,(_,row) in enumerate(positive.iterrows(),1):
                st.markdown(f"""
                <div class="rank-row">
                    <div class="rank-num">{i:02d}</div>
                    <div>
                        <div class="rank-name">{row['Aspek']}</div>
                        <div class="rank-desc">Nilai {row['Nilai_Siswa']:.2f} · baseline {row['Baseline']:.2f}</div>
                    </div>
                    <div class="rank-value positive">+{row['Kontribusi']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada kontribusi positif.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-label">TOP NEGATIVE INFLUENCES</div>
        """, unsafe_allow_html=True)
        if len(negative):
            for i,(_,row) in enumerate(negative.iterrows(),1):
                st.markdown(f"""
                <div class="rank-row">
                    <div class="rank-num" style="background:#FFF0F2;color:#EF5B67;">{i:02d}</div>
                    <div>
                        <div class="rank-name">{row['Aspek']}</div>
                        <div class="rank-desc">Nilai {row['Nilai_Siswa']:.2f} · baseline {row['Baseline']:.2f}</div>
                    </div>
                    <div class="rank-value negative">{row['Kontribusi']:+.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Tidak ada kontribusi negatif.")
        st.markdown("</div>", unsafe_allow_html=True)

    section_header("05", "Detail Perbandingan", "PROFIL SISWA VS BASELINE")

    tabel = df_kontribusi.copy()
    tabel["Status"] = tabel["Selisih"].apply(
        lambda x: "▲ Di atas" if x > 0 else "▼ Di bawah" if x < 0 else "● Sama"
    )
    tabel = tabel[["Aspek","Nilai_Siswa","Baseline","Selisih","Kontribusi","Status"]]
    tabel.columns = [
        "Aspek","Nilai Siswa","Baseline","Selisih",
        "Kontribusi (poin)","Status"
    ]
    tabel = tabel.sort_values("Kontribusi (poin)", key=abs, ascending=False)

    st.dataframe(
        tabel,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nilai Siswa": st.column_config.NumberColumn(format="%.2f"),
            "Baseline": st.column_config.NumberColumn(format="%.2f"),
            "Selisih": st.column_config.NumberColumn(format="%+.2f"),
            "Kontribusi (poin)": st.column_config.NumberColumn(format="%+.2f"),
        },
    )

    section_header("06", "Rekomendasi Personal", "TITIK INTERVENSI YANG PERLU DIPERHATIKAN")

    col1,col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-box mint">
            <div class="info-title">✓ Pertahankan kekuatan</div>
            <div class="info-text">
                Fokus pada faktor dengan kontribusi positif agar kondisi yang sudah mendukung
                tetap terjaga.
            </div>
        </div>
        """, unsafe_allow_html=True)

        faktor_positif = df_kontribusi[df_kontribusi["Kontribusi"] > .3].sort_values("Kontribusi",ascending=False)
        for _,row in faktor_positif.iterrows():
            st.markdown(f"""
            <div class="factor-card">
                <div class="factor-head">
                    <div class="factor-name">{row['Aspek']}</div>
                    <div class="factor-value positive">+{row['Kontribusi']:.2f}</div>
                </div>
                <div style="font-size:.72rem;color:#667085;margin-top:.35rem;">
                    Nilai {row['Nilai_Siswa']:.2f} · baseline {row['Baseline']:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box coral">
            <div class="info-title">! Perlu perhatian</div>
            <div class="info-text">
                Identifikasi faktor dengan kontribusi negatif untuk menjadi titik evaluasi
                dan tindak lanjut.
            </div>
        </div>
        """, unsafe_allow_html=True)

        faktor_negatif = df_kontribusi[df_kontribusi["Kontribusi"] < -.3].sort_values("Kontribusi")
        for _,row in faktor_negatif.iterrows():
            st.markdown(f"""
            <div class="factor-card">
                <div class="factor-head">
                    <div class="factor-name">{row['Aspek']}</div>
                    <div class="factor-value negative">{row['Kontribusi']:.2f}</div>
                </div>
                <div style="font-size:.72rem;color:#667085;margin-top:.35rem;">
                    Nilai {row['Nilai_Siswa']:.2f} · baseline {row['Baseline']:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

    section_header("07", "Simpan Data", "ARSIPKAN HASIL ANALISIS")

    if not nama_siswa:
        st.markdown("""
        <div class="info-box yellow">
            <div class="info-title">Data belum siap disimpan</div>
            <div class="info-text">Isi nama siswa terlebih dahulu untuk mengarsipkan hasil analisis.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button("Simpan hasil siswa →", type="primary", use_container_width=True):
            duplikat = any(
                s["Nama"] == nama_siswa and s["Kelas"] == kelas_siswa
                for s in st.session_state.database_siswa
            )

            if duplikat:
                st.warning(f"Siswa {nama_siswa} ({kelas_siswa}) sudah ada di database.")
            else:
                data_baru = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nama": nama_siswa,
                    "Kelas": kelas_siswa,
                    "Absen": absen_siswa,
                    "Nilai Akademik": round(nilai_akademik, 2),
                    "Selisih": round(selisih_nilai, 2),
                    "Kategori": kategori,
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
                st.success(f"Data {nama_siswa} berhasil disimpan.")
                st.balloons()

# ================================================================
# MENU 2 — DATABASE
# ================================================================

elif menu == "02 · Database Siswa":
    hero_header(
        "DATABASE",
        "Student records.<br><span class='accent'>One place.</span>",
        "Arsip siswa yang telah dianalisis beserta nilai dan faktor-faktor yang digunakan dalam dashboard.",
        [("DATA SISWA", "blue"), ("ARSIP", "yellow")],
    )

    if len(st.session_state.database_siswa) == 0:
        st.markdown("""
        <div class="card" style="text-align:center;padding:4rem 2rem;margin-top:1.5rem;">
            <div style="font-size:2.8rem;">◎</div>
            <div style="font-family:'Manrope';font-weight:800;font-size:1.35rem;margin-top:.7rem;">
                Belum ada data
            </div>
            <div style="color:#667085;font-size:.75rem;margin-top:.4rem;">
                Input siswa dari menu Analisis Sebab-Akibat untuk mulai mengisi database.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df_db = pd.DataFrame(st.session_state.database_siswa)

        a,b,c,d = st.columns(4)
        with a: stat_card("Total Siswa", len(df_db), "siswa terarsip", "blue")
        with b: stat_card("Rata-rata", f"{df_db['Nilai Akademik'].mean():.2f}", "nilai seluruh siswa", "mint")
        with c: stat_card("Tertinggi", f"{df_db['Nilai Akademik'].max():.2f}", "nilai maksimum", "yellow")
        with d: stat_card("Terendah", f"{df_db['Nilai Akademik'].min():.2f}", "nilai minimum", "coral")

        section_header("01", "Daftar Siswa", "DATA TERARSIP")

        c1,c2 = st.columns([1,2])
        with c1:
            filter_kelas = st.selectbox(
                "Filter Kelas",
                ["Semua"] + sorted(df_db["Kelas"].unique().tolist())
            )
        with c2:
            search = st.text_input("Cari nama", placeholder="Ketik nama siswa...")

        df_tampil = df_db.copy()
        if filter_kelas != "Semua":
            df_tampil = df_tampil[df_tampil["Kelas"] == filter_kelas]
        if search:
            df_tampil = df_tampil[
                df_tampil["Nama"].str.contains(search, case=False, na=False)
            ]

        st.markdown(
            f'<div class="eyebrow"><span class="eyebrow-dot"></span>{len(df_tampil)} SISWA DITEMUKAN</div>',
            unsafe_allow_html=True
        )
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)

        c1,c2 = st.columns(2)
        with c1:
            csv = df_tampil.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV",
                data=csv,
                file_name=f"database_siswa_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with c2:
            if st.button("Hapus semua data", use_container_width=True):
                st.session_state.database_siswa = []
                st.rerun()

# ================================================================
# MENU 3 — ATE / KAUSAL
# ================================================================

elif menu == "03 · Analisis Kausal":
    hero_header(
        "METODE 01",
        "What changes the outcome?<br><span class='accent'>Causal effects.</span>",
        "Estimasi Average Treatment Effect (ATE) untuk membaca arah dan besar efek setiap konstruk terhadap prestasi akademik.",
        [("SCM", "blue"), ("DOWHY / ATE", "mint"), ("8 KONSTRUK", "yellow")],
    )

    df_ate = pd.DataFrame(
        [{"Konstruk": k, "ATE": v} for k,v in ATE_DATA.items()]
    )

    positive_ate = df_ate[df_ate["ATE"] > 0].sort_values("ATE",ascending=False)
    negative_ate = df_ate[df_ate["ATE"] < 0].sort_values("ATE")

    section_header("01", "Gambaran Efek", "AVERAGE TREATMENT EFFECT")

    a,b,c = st.columns(3)
    with a:
        top_pos = positive_ate.iloc[0]
        stat_card("Efek positif terbesar", f"+{top_pos['ATE']:.2f}", top_pos["Konstruk"], "mint")
    with b:
        top_neg = negative_ate.iloc[0]
        stat_card("Efek negatif terbesar", f"{top_neg['ATE']:.2f}", top_neg["Konstruk"], "coral")
    with c:
        stat_card("Jumlah konstruk", "8", "variabel yang dianalisis", "blue")

    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = plot_ate(df_ate)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("02", "Interpretasi", "ARAH EFEK KAUSAL")

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-box mint">
            <div class="info-title">Efek positif</div>
            <div class="info-text">
                Nilai ATE positif menunjukkan arah efek yang meningkatkan outcome
                pada estimasi yang digunakan.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box coral">
            <div class="info-title">Efek negatif</div>
            <div class="info-text">
                Nilai ATE negatif menunjukkan arah efek yang menurunkan outcome
                pada estimasi yang digunakan.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    st.dataframe(
        df_ate.sort_values("ATE",ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "ATE": st.column_config.NumberColumn("ATE", format="%+.4f")
        }
    )

# ================================================================
# MENU 4 — SHAP
# ================================================================

elif menu == "04 · Analisis SHAP":
    hero_header(
        "METODE 02",
        "Which features matter<br><span class='accent'>to the prediction?</span>",
        "Mean absolute SHAP digunakan untuk menunjukkan seberapa besar kontribusi fitur terhadap prediksi model Random Forest.",
        [("RANDOM FOREST", "blue"), ("SHAP", "yellow"), ("EXPLAINABILITY", "mint")],
    )

    df_shap = pd.DataFrame(
        [{"Konstruk": k, "Mean_SHAP": v} for k,v in SHAP_DATA.items()]
    )

    top = df_shap.sort_values("Mean_SHAP",ascending=False).iloc[0]
    second = df_shap.sort_values("Mean_SHAP",ascending=False).iloc[1]

    section_header("01", "Feature Importance", "MEAN ABSOLUTE SHAP VALUE")

    a,b,c = st.columns(3)
    with a:
        stat_card("Kontributor #1", f"{top['Mean_SHAP']:.4f}", top["Konstruk"], "blue")
    with b:
        stat_card("Kontributor #2", f"{second['Mean_SHAP']:.4f}", second["Konstruk"], "purple")
    with c:
        stat_card("Jumlah fitur", "8", "fitur/konstruk dianalisis", "yellow")

    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = plot_shap(df_shap)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("02", "Ranking Kontribusi", "FAKTOR PALING RELEVAN BAGI MODEL")

    ranked = df_shap.sort_values("Mean_SHAP",ascending=False).reset_index(drop=True)
    for i,row in ranked.iterrows():
        pct = row["Mean_SHAP"] / ranked["Mean_SHAP"].max() * 100
        st.markdown(f"""
        <div class="factor-card">
            <div class="factor-head">
                <div style="display:flex;align-items:center;gap:.7rem;">
                    <div class="rank-num">{i+1:02d}</div>
                    <div class="factor-name">{row['Konstruk']}</div>
                </div>
                <div class="factor-value" style="color:#2563EB;">{row['Mean_SHAP']:.4f}</div>
            </div>
            <div class="factor-bar">
                <div class="factor-fill fill-blue" style="width:{pct:.1f}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.dataframe(
        df_shap.sort_values("Mean_SHAP",ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Mean_SHAP": st.column_config.NumberColumn("Mean |SHAP|", format="%.4f")
        }
    )

# ================================================================
# MENU 5 — REKOMENDASI
# ================================================================

else:
    hero_header(
        "TINDAK LANJUT",
        "From analysis<br><span class='accent'>to action.</span>",
        "Ringkasan faktor yang dapat menjadi prioritas tindak lanjut berdasarkan kombinasi hasil ATE dan SHAP yang tersedia pada dashboard.",
        [("PRIORITAS", "yellow"), ("ATE", "mint"), ("SHAP", "blue")],
    )

    section_header("01", "Prioritas Intervensi", "FAKTOR DENGAN SINYAL PALING KUAT")

    col1,col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card card-mint">
            <div class="card-label">SINYAL POSITIF</div>
            <div style="font-family:'Manrope';font-size:1.25rem;font-weight:800;margin-top:.45rem;">
                Faktor yang layak diperkuat
            </div>
        """, unsafe_allow_html=True)

        positive_priority = [
            ("Fasilitas Sekolah", ATE_DATA["Fasilitas Sekolah"], SHAP_DATA["Fasilitas Sekolah"],
             "Evaluasi dan optimalkan fasilitas belajar yang paling relevan dengan kebutuhan siswa."),
            ("Keterlibatan Orang Tua", ATE_DATA["Keterlibatan Orang Tua"], SHAP_DATA["Keterlibatan Orang Tua"],
             "Perkuat komunikasi dan pendampingan belajar antara sekolah dan keluarga."),
            ("Self-Efficacy Akademik", ATE_DATA["Self-Efficacy Akademik"], SHAP_DATA["Self-Efficacy Akademik"],
             "Dorong kepercayaan diri akademik melalui mentoring dan pengalaman belajar yang bertahap."),
        ]

        for i,(name,ate,shap,desc) in enumerate(positive_priority,1):
            st.markdown(f"""
            <div style="padding:1rem 0;border-bottom:1px solid #CBEBDD;">
                <div style="display:flex;justify-content:space-between;gap:.7rem;">
                    <div style="font-weight:800;font-size:.88rem;">{i:02d} · {name}</div>
                    <div style="font-family:'Manrope';font-weight:800;color:#18A77A;">
                        ATE {ate:+.2f}
                    </div>
                </div>
                <div style="font-size:.69rem;color:#667085;margin-top:.3rem;">
                    SHAP {shap:.4f}
                </div>
                <div style="font-size:.76rem;line-height:1.55;margin-top:.45rem;color:#475467;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card card-yellow">
            <div class="card-label">SINYAL NEGATIF</div>
            <div style="font-family:'Manrope';font-size:1.25rem;font-weight:800;margin-top:.45rem;">
                Faktor yang perlu dievaluasi
            </div>
        """, unsafe_allow_html=True)

        negative_priority = [
            ("Dukungan Sekolah", ATE_DATA["Dukungan Sekolah"], SHAP_DATA["Dukungan Sekolah"],
             "Evaluasi bentuk pendampingan agar dukungan tetap membantu tanpa mengurangi kemandirian siswa."),
            ("Harapan Orang Tua", ATE_DATA["Harapan Orang Tua"], SHAP_DATA["Harapan Orang Tua"],
             "Dorong target akademik yang realistis dan komunikasi yang tidak menambah tekanan belajar."),
            ("Motivasi Belajar", ATE_DATA["Motivasi Belajar"], SHAP_DATA["Motivasi Belajar"],
             "Identifikasi hambatan belajar dan gunakan pendekatan pembelajaran yang lebih relevan bagi siswa."),
        ]

        for i,(name,ate,shap,desc) in enumerate(negative_priority,1):
            st.markdown(f"""
            <div style="padding:1rem 0;border-bottom:1px solid #F1DF96;">
                <div style="display:flex;justify-content:space-between;gap:.7rem;">
                    <div style="font-weight:800;font-size:.88rem;">{i:02d} · {name}</div>
                    <div style="font-family:'Manrope';font-weight:800;color:#EF5B67;">
                        ATE {ate:+.2f}
                    </div>
                </div>
                <div style="font-size:.69rem;color:#667085;margin-top:.3rem;">
                    SHAP {shap:.4f}
                </div>
                <div style="font-size:.76rem;line-height:1.55;margin-top:.45rem;color:#475467;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    section_header("02", "Cara Membaca Dashboard", "CAUSAL + PREDICTIVE + EXPLAINABLE")

    a,b,c = st.columns(3)
    with a:
        st.markdown("""
        <div class="card card-blue">
            <div class="pill blue">01 · ATE</div>
            <h3 style="font-size:1rem;margin:.75rem 0 .35rem;">Efek kausal</h3>
            <div style="font-size:.75rem;line-height:1.6;color:#667085;">
                Menjawab arah dan besarnya efek konstruk dalam estimasi kausal yang digunakan.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.markdown("""
        <div class="card card-purple">
            <div class="pill" style="background:#F1EDFF;color:#7C5CFC;border-color:#DDD5FF;">02 · RANDOM FOREST</div>
            <h3 style="font-size:1rem;margin:.75rem 0 .35rem;">Prediksi</h3>
            <div style="font-size:.75rem;line-height:1.6;color:#667085;">
                Menilai kemampuan fitur dalam mendukung prediksi nilai akademik.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c:
        st.markdown("""
        <div class="card card-yellow">
            <div class="pill yellow">03 · SHAP</div>
            <h3 style="font-size:1rem;margin:.75rem 0 .35rem;">Penjelasan model</h3>
            <div style="font-size:.75rem;line-height:1.6;color:#667085;">
                Menunjukkan kontribusi fitur terhadap prediksi model secara lebih transparan.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card card-dark">
        <div style="font-size:.62rem;font-weight:800;letter-spacing:1.4px;color:#9DBBFF;">
            CATATAN PENELITIAN
        </div>
        <div style="font-family:'Manrope';font-size:1.35rem;line-height:1.25;font-weight:800;margin-top:.7rem;">
            Gunakan hasil kausal untuk menjawab pertanyaan sebab-akibat,
            dan hasil SHAP untuk menjelaskan kontribusi fitur pada model prediktif.
        </div>
        <div style="font-size:.73rem;color:#B9C6DA;line-height:1.6;margin-top:.8rem;max-width:850px;">
            Visual dashboard dibuat sebagai lapisan presentasi; nilai ATE, SHAP,
            baseline, dan konstruk mengikuti data/model yang telah digunakan pada kode penelitian.
        </div>
    </div>
    """, unsafe_allow_html=True)
'''

out = Path("/mnt/data/dashboard_prestasi_akademik_modern.py")
out.write_text(code, encoding="utf-8")
print(f"Created: {out}")
print(f"Lines: {len(code.splitlines())}")
