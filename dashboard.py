import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import hashlib

st.set_page_config(
    page_title="Prestasi Akademik | SMPN 6 Salatiga",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ================================================================
# VISUAL SYSTEM — EDUCATIONAL VIBRANT
# ================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');

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
    --pink:#EC4899;
    --navy:#13213B;
    --navy-2:#1E2F50;
}

html, body, [class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink);}

.stApp{
    background:
        radial-gradient(circle at 92% 4%, rgba(79,124,255,.10), transparent 24rem),
        radial-gradient(circle at 4% 80%, rgba(246,201,69,.10), transparent 22rem),
        radial-gradient(circle at 50% 50%, rgba(124,92,252,.05), transparent 30rem),
        var(--canvas);
}

.main{background:transparent;}
.block-container{max-width:1480px;padding:1.6rem 2.7rem 4rem 2.7rem;}
#MainMenu, footer, header{visibility:hidden;}
h1,h2,h3,h4{font-family:'Manrope',sans-serif;}

@keyframes riseIn{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
@keyframes growBar{from{transform:scaleX(0);transform-origin:left;}to{transform:scaleX(1);transform-origin:left;}}
@keyframes floatDot{0%,100%{transform:translateY(0);}50%{transform:translateY(-7px);}}
@keyframes sparkle{0%,100%{opacity:.3;transform:scale(1);}50%{opacity:1;transform:scale(1.3);}}

.motion{animation:riseIn .5s ease both;}

.dashboard-hero{
    position:relative;overflow:hidden;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 60%,#EFF4FF 100%);
    border:1px solid var(--line);border-radius:28px;padding:2.3rem 2.5rem;
    box-shadow:0 20px 55px rgba(30,50,90,.09);animation:riseIn .5s ease both;
}
.dashboard-hero:before{
    content:"";position:absolute;width:220px;height:220px;
    right:-80px;top:-90px;border:34px solid rgba(37,99,235,.09);border-radius:50%;
}
.dashboard-hero:after{
    content:"";position:absolute;width:10px;height:10px;
    right:140px;bottom:40px;background:var(--yellow);border-radius:50%;
    box-shadow:42px -22px 0 var(--blue),78px 9px 0 var(--mint),112px -30px 0 var(--purple),145px 5px 0 var(--pink);
    animation:floatDot 3s ease-in-out infinite;
}

.eyebrow{display:inline-flex;align-items:center;gap:8px;
    font-size:.68rem;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;
    color:var(--blue);margin-bottom:.7rem;}
.eyebrow-dot{width:8px;height:8px;background:var(--yellow);border-radius:50%;display:inline-block;
    animation:sparkle 2s ease-in-out infinite;}

.hero-title{font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.15rem,4vw,3.8rem);line-height:1.02;letter-spacing:-2.4px;margin:0;max-width:850px;}
.hero-title .accent{background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{color:var(--muted);font-size:.98rem;line-height:1.65;max-width:790px;margin:.9rem 0 0;}
.hero-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:1.25rem;}
.pill{display:inline-flex;align-items:center;gap:7px;padding:.42rem .7rem;border-radius:999px;
    font-size:.65rem;font-weight:800;letter-spacing:.5px;border:1px solid var(--line);background:#fff;}
.pill.blue{background:var(--blue-soft);color:var(--blue);border-color:#D4E0FF;}
.pill.yellow{background:var(--yellow-soft);color:#936F00;border-color:#F3DF8D;}
.pill.mint{background:var(--mint-soft);color:#087453;border-color:#BCE8D7;}
.pill.purple{background:var(--purple-soft);color:#5B3FCC;border-color:#DDD5FF;}

.section-wrap{margin-top:2rem;margin-bottom:1rem;}
.section-number{display:inline-flex;width:38px;height:38px;align-items:center;justify-content:center;
    border-radius:12px;background:linear-gradient(135deg,var(--blue) 0%,var(--purple) 100%);
    color:#fff;font-size:.78rem;font-weight:800;box-shadow:0 8px 18px rgba(37,99,235,.25);}
.section-title{font-size:1.45rem;letter-spacing:-.7px;margin:0;}
.section-sub{color:var(--muted);font-size:.72rem;text-transform:uppercase;
    letter-spacing:1.1px;font-weight:800;margin-top:.2rem;}
.section-line{height:1px;background:var(--line);margin-top:.9rem;}

.card{background:var(--surface);border:1px solid var(--line);border-radius:20px;
    padding:1.25rem 1.35rem;box-shadow:0 10px 28px rgba(30,50,90,.045);
    transition:transform .25s ease, box-shadow .25s ease, border-color .25s ease;
    animation:riseIn .5s ease both;}
.card:hover{transform:translateY(-3px);box-shadow:0 18px 40px rgba(30,50,90,.10);border-color:#CFD9EA;}
.card-blue{background:linear-gradient(135deg,#fff 0%,#F3F7FF 100%);}
.card-yellow{background:linear-gradient(135deg,#fff 0%,#FFFBEB 100%);}
.card-mint{background:linear-gradient(135deg,#fff 0%,#F1FBF7 100%);}
.card-purple{background:linear-gradient(135deg,#fff 0%,#F7F4FF 100%);}
.card-dark{background:var(--navy);border-color:var(--navy);color:#fff;}

.card-label{font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:var(--muted);}
.card-value{font-family:'Manrope',sans-serif;font-size:2rem;font-weight:800;letter-spacing:-1.2px;line-height:1;margin-top:.5rem;}
.card-note{color:var(--muted);font-size:.74rem;margin-top:.45rem;}

.stat-card{min-height:122px;position:relative;overflow:hidden;}
.stat-card:after{content:"";position:absolute;width:70px;height:70px;border-radius:50%;
    right:-28px;bottom:-28px;background:rgba(37,99,235,.06);}
.stat-card .topline{width:34px;height:5px;border-radius:99px;margin-bottom:.85rem;}
.topline.blue{background:var(--blue);}
.topline.yellow{background:var(--yellow);}
.topline.mint{background:var(--mint);}
.topline.coral{background:var(--coral);}
.topline.purple{background:var(--purple);}

.menu-hero{position:relative;overflow:hidden;
    background:linear-gradient(135deg,#17233B 0%,#1E2F50 50%,#2563EB 100%);
    border-radius:32px;padding:3.5rem 3rem;color:#fff;margin-bottom:2.5rem;
    box-shadow:0 30px 70px rgba(23,35,59,.35);animation:riseIn .5s ease both;}
.menu-hero:before{content:"";position:absolute;width:450px;height:450px;border-radius:50%;
    border:70px solid rgba(246,201,69,.08);right:-200px;top:-180px;}
.menu-hero:after{content:"";position:absolute;width:12px;height:12px;
    right:200px;bottom:60px;background:var(--yellow);border-radius:50%;
    box-shadow:48px -28px 0 #4F7CFF,92px 12px 0 #18A77A,135px -35px 0 #7C5CFC,175px 8px 0 #EC4899;
    animation:floatDot 3.5s ease-in-out infinite;}
.menu-hero-kicker{display:inline-flex;align-items:center;gap:8px;
    font-size:.7rem;font-weight:800;letter-spacing:2px;color:#F6C945;
    text-transform:uppercase;margin-bottom:1rem;}
.menu-hero-title{font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.5rem,5vw,4.5rem);line-height:.98;letter-spacing:-3px;font-weight:800;margin:0;max-width:900px;}
.menu-hero-title em{color:#F6C945;font-style:italic;font-family:'Manrope',serif;}
.menu-hero-sub{color:#C6D1E5;font-size:1.05rem;line-height:1.6;max-width:680px;margin:1.2rem 0 0;}
.menu-hero-meta{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.8rem;position:relative;z-index:1;}
.menu-hero-meta span{padding:.55rem .9rem;border-radius:999px;
    background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);
    color:#D9E3F5;font-size:.68rem;font-weight:800;letter-spacing:.7px;}

.menu-card{position:relative;overflow:hidden;background:#fff;border:1px solid var(--line);
    border-radius:24px;padding:1.75rem 1.6rem 1.6rem;text-decoration:none;color:inherit;
    transition:transform .3s cubic-bezier(.2,.7,.3,1), box-shadow .3s ease, border-color .3s ease;
    box-shadow:0 12px 32px rgba(30,50,90,.06);min-height:230px;
    display:flex;flex-direction:column;justify-content:space-between;animation:riseIn .55s ease both;}
.menu-card:hover{transform:translateY(-6px);box-shadow:0 24px 55px rgba(30,50,90,.14);}
.menu-card.mc-blue:hover{border-color:#2563EB;}
.menu-card.mc-yellow:hover{border-color:#F6C945;}
.menu-card.mc-mint:hover{border-color:#18A77A;}
.menu-card.mc-purple:hover{border-color:#7C5CFC;}
.menu-card.mc-pink:hover{border-color:#EC4899;}
.menu-card.mc-teal:hover{border-color:#10B981;}

.menu-card-num{font-family:'Plus Jakarta Sans',sans-serif;font-size:.68rem;font-weight:800;
    letter-spacing:1.6px;color:var(--muted);text-transform:uppercase;}
.menu-card-icon{width:56px;height:56px;border-radius:16px;display:flex;align-items:center;
    justify-content:center;font-size:1.7rem;margin:.9rem 0;}
.menu-card.mc-blue .menu-card-icon{background:var(--blue-soft);color:var(--blue);}
.menu-card.mc-yellow .menu-card-icon{background:var(--yellow-soft);color:#936F00;}
.menu-card.mc-mint .menu-card-icon{background:var(--mint-soft);color:var(--mint);}
.menu-card.mc-purple .menu-card-icon{background:var(--purple-soft);color:var(--purple);}
.menu-card.mc-pink .menu-card-icon{background:#FCE7F3;color:var(--pink);}
.menu-card.mc-teal .menu-card-icon{background:#D1FAE5;color:#10B981;}

.menu-card-title{font-family:'Manrope',sans-serif;font-size:1.15rem;font-weight:800;
    letter-spacing:-.4px;line-height:1.2;margin:0 0 .35rem;}
.menu-card-desc{color:var(--muted);font-size:.78rem;line-height:1.55;margin:0;}
.menu-card-cta{display:inline-flex;align-items:center;gap:.45rem;
    font-size:.72rem;font-weight:800;letter-spacing:.5px;margin-top:1rem;text-transform:uppercase;}
.menu-card.mc-blue .menu-card-cta{color:var(--blue);}
.menu-card.mc-yellow .menu-card-cta{color:#936F00;}
.menu-card.mc-mint .menu-card-cta{color:var(--mint);}
.menu-card.mc-purple .menu-card-cta{color:var(--purple);}
.menu-card.mc-pink .menu-card-cta{color:var(--pink);}
.menu-card.mc-teal .menu-card-cta{color:#10B981;}

.menu-card:before{content:"";position:absolute;width:120px;height:120px;border-radius:50%;
    right:-55px;bottom:-55px;opacity:.06;transition:transform .4s ease;}
.menu-card.mc-blue:before{background:var(--blue);}
.menu-card.mc-yellow:before{background:var(--yellow);}
.menu-card.mc-mint:before{background:var(--mint);}
.menu-card.mc-purple:before{background:var(--purple);}
.menu-card.mc-pink:before{background:var(--pink);}
.menu-card.mc-teal:before{background:#10B981;}
.menu-card:hover:before{transform:scale(1.6);}

.back-btn-wrap{margin-top:2rem;margin-bottom:1rem;padding-top:1.5rem;border-top:1px solid var(--line);}

.info-box{border-radius:18px;padding:1.1rem 1.2rem;border:1px solid var(--line);background:#fff;}
.info-box.blue{background:var(--blue-soft);border-color:#D5E1FF;}
.info-box.yellow{background:var(--yellow-soft);border-color:#F1DF96;}
.info-box.mint{background:var(--mint-soft);border-color:#C5EBDD;}
.info-box.coral{background:var(--coral-soft);border-color:#F4CDD3;}
.info-title{font-weight:800;font-size:.9rem;}
.info-text{font-size:.78rem;line-height:1.6;margin-top:.35rem;color:#475467;}

.profile-card{display:flex;align-items:center;justify-content:space-between;
    gap:1rem;padding:1.15rem 1.3rem;background:#fff;
    border:1px solid var(--line);border-radius:18px;}
.profile-avatar{width:48px;height:48px;border-radius:15px;display:flex;align-items:center;
    justify-content:center;background:linear-gradient(135deg,var(--blue-soft) 0%,var(--purple-soft) 100%);
    color:var(--blue);font-weight:800;font-size:1rem;}
.profile-name{font-family:'Manrope',sans-serif;font-weight:800;font-size:1.05rem;}
.profile-meta{color:var(--muted);font-size:.72rem;margin-top:.2rem;}

.factor-card{border:1px solid var(--line);border-radius:18px;background:#fff;
    padding:1rem 1.05rem;margin:.65rem 0;transition:all .2s ease;}
.factor-card:hover{transform:translateX(3px);box-shadow:0 8px 22px rgba(30,50,90,.06);}
.factor-head{display:flex;justify-content:space-between;align-items:center;gap:1rem;}
.factor-name{font-weight:700;font-size:.86rem;}
.factor-value{font-family:'Manrope',sans-serif;font-weight:800;font-size:1rem;}
.factor-bar{height:7px;background:#EEF2F7;border-radius:99px;overflow:hidden;margin-top:.75rem;}
.factor-fill{height:100%;border-radius:99px;animation:growBar .7s ease both;}
.fill-blue{background:var(--blue);}
.fill-yellow{background:var(--yellow);}
.fill-mint{background:var(--mint);}
.fill-purple{background:var(--purple);}
.fill-coral{background:var(--coral);}

.rank-row{display:grid;grid-template-columns:34px 1fr auto;
    align-items:center;gap:.8rem;padding:.75rem 0;border-bottom:1px solid var(--line);}
.rank-row:last-child{border-bottom:0;}
.rank-num{width:30px;height:30px;border-radius:10px;background:var(--blue-soft);
    color:var(--blue);display:flex;align-items:center;justify-content:center;
    font-size:.68rem;font-weight:800;}
.rank-name{font-weight:700;font-size:.8rem;}
.rank-desc{font-size:.67rem;color:var(--muted);margin-top:.15rem;}
.rank-value{font-family:'Manrope',sans-serif;font-size:.86rem;font-weight:800;}
.positive{color:var(--mint);}
.negative{color:var(--coral);}

/* Radio button styling */
.stRadio > div{gap:.6rem;}
.stRadio [role="radiogroup"]{gap:.5rem;}
.stRadio [role="radiogroup"] label{
    background:#fff;border:1.5px solid var(--line);border-radius:12px;
    padding:.65rem 1rem !important;transition:all .18s ease;font-weight:600 !important;
    cursor:pointer;}
.stRadio [role="radiogroup"] label:hover{
    border-color:var(--blue);background:#F8FAFF;}
.stRadio [role="radiogroup"] label[data-checked="true"]{
    border-color:var(--blue);background:var(--blue-soft);color:var(--blue);}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox [data-baseweb="select"] > div{
    background:#fff !important;border:1px solid #D7DFEA !important;
    border-radius:12px !important;min-height:43px;color:var(--ink) !important;}
.stTextInput label,.stNumberInput label,.stSelectbox label{
    font-size:.72rem !important;font-weight:800 !important;color:#475467 !important;}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus{
    border-color:var(--blue) !important;
    box-shadow:0 0 0 3px rgba(37,99,235,.10) !important;}

.stButton > button,.stDownloadButton > button{
    border-radius:12px !important;min-height:43px;font-weight:800 !important;
    border:1px solid #D7DFEA !important;transition:all .18s ease !important;}
.stButton > button:hover,.stDownloadButton > button:hover{
    transform:translateY(-2px);box-shadow:0 8px 20px rgba(30,50,90,.08);}
button[kind="primary"]{
    background:linear-gradient(135deg,var(--blue) 0%,var(--purple) 100%) !important;
    border-color:var(--blue) !important;color:#fff !important;}

[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:16px;
    overflow:hidden;box-shadow:0 8px 25px rgba(30,50,90,.04);}

.login-shell{max-width:930px;margin:5vh auto 0;}
.login-panel{display:grid;grid-template-columns:1.12fr .88fr;overflow:hidden;
    border-radius:30px;border:1px solid var(--line);
    box-shadow:0 24px 70px rgba(24,45,82,.12);background:#fff;animation:riseIn .5s ease both;}
.login-visual{position:relative;min-height:500px;padding:2.5rem;overflow:hidden;
    background:linear-gradient(135deg,#17233B 0%,#1E2F50 50%,#2563EB 100%);color:#fff;}
.login-visual:before{content:"";position:absolute;width:330px;height:330px;border-radius:50%;
    border:50px solid rgba(79,124,255,.12);right:-145px;top:-120px;}
.login-visual:after{content:"";position:absolute;width:9px;height:9px;left:42px;bottom:55px;
    border-radius:50%;background:var(--yellow);
    box-shadow:35px -22px 0 #4F7CFF,75px -4px 0 #18A77A,113px -28px 0 #7C5CFC;
    animation:floatDot 3.2s ease-in-out infinite;}
.login-kicker{font-size:.65rem;font-weight:800;letter-spacing:1.6px;color:#9DBBFF;}
.login-title{font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.8rem,5vw,4.8rem);line-height:.95;letter-spacing:-3px;margin-top:3.2rem;}
.login-title span{color:var(--yellow);}
.login-copy{color:#C6D1E5;line-height:1.65;max-width:420px;margin-top:1rem;}
.login-feature{position:absolute;bottom:34px;left:2.5rem;right:2.5rem;
    display:flex;gap:.6rem;flex-wrap:wrap;}
.login-feature span{padding:.45rem .65rem;border-radius:999px;
    background:rgba(255,255,255,.08);color:#D9E3F5;font-size:.62rem;font-weight:700;}
.login-form{padding:2.5rem;display:flex;flex-direction:column;justify-content:center;}
.login-form-title{font-family:'Manrope',sans-serif;font-size:1.45rem;font-weight:800;}
.login-form-sub{color:var(--muted);font-size:.78rem;margin:.35rem 0 1.4rem;}
.demo-note{margin-top:1rem;padding:.75rem .9rem;border-radius:13px;
    background:var(--yellow-soft);color:#725A00;font-size:.7rem;line-height:1.5;}

@media(max-width:850px){
    .block-container{padding:1rem 1rem 3rem;}
    .login-shell{margin:1rem auto 0;}
    .login-panel{grid-template-columns:1fr;}
    .login-visual{min-height:360px;}
    .login-title{margin-top:2.5rem;}
    .login-feature{position:static;margin-top:3rem;}
    .menu-hero{padding:2.5rem 1.7rem;}
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
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

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
# SKALA KATEGORI — UNTUK INPUT YANG LEBIH MUDAH
# ================================================================

# Setiap konstruk punya label pilihan 1-5
SKALA_PILIHAN = {
    "Self-Efficacy Akademik": {
        "question": "Seberapa yakin siswa terhadap kemampuan akademiknya?",
        "options": [
            ("1", "Hampir tidak pernah percaya diri"),
            ("2", "Jarang percaya diri"),
            ("3", "Kadang-kadang percaya diri"),
            ("4", "Sering percaya diri"),
            ("5", "Hampir selalu percaya diri"),
        ]
    },
    "Keterlibatan Orang Tua": {
        "question": "Seberapa aktif orang tua mendampingi siswa belajar?",
        "options": [
            ("1", "Hampir tidak pernah mendampingi"),
            ("2", "Jarang mendampingi"),
            ("3", "Kadang-kadang mendampingi"),
            ("4", "Sering mendampingi"),
            ("5", "Hampir selalu mendampingi"),
        ]
    },
    "Harapan Orang Tua": {
        "question": "Seberapa tinggi tuntutan/ekspektasi orang tua terhadap nilai siswa?",
        "options": [
            ("1", "Sangat rendah / tidak menuntut"),
            ("2", "Rendah"),
            ("3", "Sedang / wajar"),
            ("4", "Tinggi"),
            ("5", "Sangat tinggi / menekan"),
        ]
    },
    "Dukungan Sekolah": {
        "question": "Seberapa besar dukungan & perhatian yang diberikan sekolah kepada siswa?",
        "options": [
            ("1", "Sangat kurang / tidak diperhatikan"),
            ("2", "Kurang"),
            ("3", "Cukup"),
            ("4", "Baik"),
            ("5", "Sangat baik / sangat diperhatikan"),
        ]
    },
    "Motivasi Belajar": {
        "question": "Seberapa besar motivasi & semangat belajar siswa?",
        "options": [
            ("1", "Tidak ada motivasi / sangat malas"),
            ("2", "Kurang termotivasi"),
            ("3", "Cukup termotivasi"),
            ("4", "Termotivasi"),
            ("5", "Sangat termotivasi / antusias"),
        ]
    },
    "Kecemasan Akademik": {
        "question": "Seberapa sering siswa merasa cemas / tertekan saat belajar atau ujian?",
        "options": [
            ("1", "Hampir tidak pernah cemas"),
            ("2", "Jarang cemas"),
            ("3", "Kadang-kadang cemas"),
            ("4", "Sering cemas"),
            ("5", "Hampir selalu cemas / sangat tertekan"),
        ]
    },
    "Fasilitas Sekolah": {
        "question": "Seberapa memadai fasilitas belajar yang tersedia di sekolah?",
        "options": [
            ("1", "Sangat kurang memadai"),
            ("2", "Kurang memadai"),
            ("3", "Cukup memadai"),
            ("4", "Memadai"),
            ("5", "Sangat memadai / lengkap"),
        ]
    },
    "Kemalasan Belajar": {
        "question": "Seberapa sering siswa menunjukkan sikap malas belajar?",
        "options": [
            ("1", "Tidak pernah malas"),
            ("2", "Jarang malas"),
            ("3", "Kadang-kadang malas"),
            ("4", "Sering malas"),
            ("5", "Hampir selalu malas"),
        ]
    },
}

# Urutan tampilan di form
FAKTOR_INTERNAL = [
    "Self-Efficacy Akademik",
    "Motivasi Belajar",
    "Kecemasan Akademik",
    "Kemalasan Belajar",
]

FAKTOR_EKSTERNAL = [
    "Keterlibatan Orang Tua",
    "Harapan Orang Tua",
    "Dukungan Sekolah",
    "Fasilitas Sekolah",
]

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
    st.rerun()


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
    pills_html = "".join(f'<span class="pill {k}">{t}</span>' for t, k in pills)
    st.markdown(f"""
    <div class="dashboard-hero">
        <div class="eyebrow"><span class="eyebrow-dot"></span>{eyebrow}</div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-sub">{subtitle}</p>
        <div class="hero-meta">{pills_html}</div>
    </div>
    """, unsafe_allow_html=True)


def stat_card(label, value, note="", accent="blue"):
    st.markdown(f"""
    <div class="card stat-card">
        <div class="topline {accent}"></div>
        <div class="card-label">{label}</div>
        <div class="card-value">{value}</div>
        <div class="card-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def back_to_menu_button(key_suffix=""):
    st.markdown('<div class="back-btn-wrap"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Kembali ke Menu Utama", use_container_width=True, key=f"back_{key_suffix}"):
            goto_page("home")


def plot_ate(df):
    df = df.sort_values("ATE", ascending=True)
    fig, ax = plt.subplots(figsize=(11, 6.3))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    vals = df["ATE"].values
    labels = df["Konstruk"].values
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
    ax.set_xlabel("Average Treatment Effect (ATE)", fontsize=9,
                  fontweight="bold", color="#667085", labelpad=10)
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
    ax.set_xlabel("Mean |SHAP Value|", fontsize=9,
                  fontweight="bold", color="#667085", labelpad=10)
    plt.tight_layout()
    return fig


def input_kategori(key_name, faktor_name):
    """Radio button input dengan label pilihan yang ramah guru"""
    config = SKALA_PILIHAN[faktor_name]
    st.markdown(f"""
    <div style="margin-bottom:.5rem;">
        <div style="font-family:'Manrope';font-weight:800;font-size:.88rem;color:#17233B;">
            {faktor_name}
        </div>
        <div style="font-size:.72rem;color:#667085;margin-top:.15rem;margin-bottom:.6rem;">
            {config['question']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    labels = [opt[1] for opt in config["options"]]
    values = [float(opt[0]) for opt in config["options"]]
    
    # Cari default index berdasarkan baseline
    baseline_val = BASELINE_ASPEK[faktor_name]
    default_idx = 2  # default ke "sedang"
    for i, v in enumerate(values):
        if abs(v - baseline_val) < 0.5:
            default_idx = i
            break
    
    pilihan = st.radio(
        f"{faktor_name}_radio",
        labels,
        index=default_idx,
        key=key_name,
        label_visibility="collapsed",
    )
    
    # Kembalikan nilai numerik
    return values[labels.index(pilihan)]


# ================================================================
# LOGIN PAGE
# ================================================================

def halaman_login():
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    st.markdown("""
    <div class="login-panel">
        <div class="login-visual">
            <div class="login-kicker">SISTEM ANALITIK AKADEMIK · 2026</div>
            <div class="login-title">Prestasi<br><span>Akademik.</span></div>
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
                st.session_state.current_page = "home"
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
# LANDING PAGE
# ================================================================

if st.session_state.current_page == "home":
    st.markdown("""
    <div class="menu-hero">
        <div class="menu-hero-kicker">◆ DASHBOARD ANALITIK AKADEMIK</div>
        <h1 class="menu-hero-title">
            Setiap angka punya cerita.<br>
            <em>Pahami apa yang membentuknya.</em>
        </h1>
        <p class="menu-hero-sub">
            Pilih modul di bawah untuk mulai menganalisis faktor-faktor yang mempengaruhi
            prestasi akademik siswa SMP Negeri 6 Salatiga.
        </p>
        <div class="menu-hero-meta">
            <span>8 KONSTRUK</span>
            <span>ATE</span>
            <span>RANDOM FOREST</span>
            <span>SHAP</span>
            <span>SMPN 6 SALATIGA</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="profile-card" style="margin-bottom:2rem;">
        <div style="display:flex;align-items:center;gap:.85rem;">
            <div class="profile-avatar">{st.session_state.user_nama[0].upper()}</div>
            <div>
                <div class="profile-name">Halo, {st.session_state.user_nama}</div>
                <div class="profile-meta">Sesi aktif · {datetime.now().strftime('%d %B %Y')}</div>
            </div>
        </div>
        <span class="pill mint">● ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-wrap motion">
        <div style="display:flex;align-items:center;gap:.85rem;">
            <div class="section-number">◆</div>
            <div>
                <h2 class="section-title">Modul Dashboard</h2>
                <div class="section-sub">PILIH UNTUK MEMULAI ANALISIS</div>
            </div>
        </div>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    row1 = st.columns(3)
    row2 = st.columns(3)

    with row1[0]:
        st.markdown("""
        <div class="menu-card mc-blue">
            <div class="menu-card-num">MODUL 01</div>
            <div class="menu-card-icon">🔍</div>
            <div class="menu-card-title">Analisis Sebab-Akibat</div>
            <div class="menu-card-desc">
                Analisis personal siswa berdasarkan nilai akademik dan profil 8 konstruk.
            </div>
            <div class="menu-card-cta">MULAI ANALISIS →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Modul 01 →", key="btn_m1", use_container_width=True, type="primary"):
            goto_page("analisis")

    with row1[1]:
        st.markdown("""
        <div class="menu-card mc-yellow">
            <div class="menu-card-num">MODUL 02</div>
            <div class="menu-card-icon">🗄️</div>
            <div class="menu-card-title">Database Siswa</div>
            <div class="menu-card-desc">
                Arsip seluruh siswa yang telah dianalisis, dengan filter dan pencarian.
            </div>
            <div class="menu-card-cta">LIHAT DATABASE →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Modul 02 →", key="btn_m2", use_container_width=True, type="primary"):
            goto_page("database")

    with row1[2]:
        st.markdown("""
        <div class="menu-card mc-mint">
            <div class="menu-card-num">MODUL 03</div>
            <div class="menu-card-icon">📊</div>
            <div class="menu-card-title">Analisis Kausal</div>
            <div class="menu-card-desc">
                Estimasi Average Treatment Effect (ATE) dari Structural Causal Model.
            </div>
            <div class="menu-card-cta">LIHAT EFEK KAUSAL →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Modul 03 →", key="btn_m3", use_container_width=True, type="primary"):
            goto_page("kausal")

    with row2[0]:
        st.markdown("""
        <div class="menu-card mc-purple">
            <div class="menu-card-num">MODUL 04</div>
            <div class="menu-card-icon">📈</div>
            <div class="menu-card-title">Analisis SHAP</div>
            <div class="menu-card-desc">
                Kontribusi prediktif setiap fitur terhadap model Random Forest.
            </div>
            <div class="menu-card-cta">LIHAT SHAP →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Modul 04 →", key="btn_m4", use_container_width=True, type="primary"):
            goto_page("shap")

    with row2[1]:
        st.markdown("""
        <div class="menu-card mc-pink">
            <div class="menu-card-num">MODUL 05</div>
            <div class="menu-card-icon">💡</div>
            <div class="menu-card-title">Rekomendasi Umum</div>
            <div class="menu-card-desc">
                Sintesis hasil ATE dan SHAP menjadi rekomendasi tingkat sekolah.
            </div>
            <div class="menu-card-cta">LIHAT REKOMENDASI →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Modul 05 →", key="btn_m5", use_container_width=True, type="primary"):
            goto_page("rekomendasi")

    with row2[2]:
        st.markdown("""
        <div class="menu-card mc-teal">
            <div class="menu-card-num">MODUL 06</div>
            <div class="menu-card-icon">🎯</div>
            <div class="menu-card-title">Catatan untuk Guru</div>
            <div class="menu-card-desc">
                Kesimpulan sebab-akibat & tindak lanjut personal untuk siswa tertentu.
            </div>
            <div class="menu-card-cta">KONSULTASI SISWA →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Modul 06 →", key="btn_m6", use_container_width=True, type="primary"):
            goto_page("catatan_guru")

    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚪 Keluar dari Dashboard", use_container_width=True, key="logout_home"):
            st.session_state.logged_in = False
            st.session_state.user_nama = None
            st.session_state.current_page = "home"
            st.rerun()

# ================================================================
# MODUL 01 — ANALISIS SEBAB-AKIBAT
# ================================================================

elif st.session_state.current_page == "analisis":
    hero_header(
        "MODUL 01 · ANALISIS UTAMA",
        "Understand the student.<br><span class='accent'>Improve the outcome.</span>",
        "Masukkan profil siswa untuk melihat posisi nilainya, perbandingan terhadap baseline, "
        "serta kontribusi faktor berdasarkan hasil analisis yang digunakan dalam penelitian.",
        [("8 KONSTRUK", "blue"), ("ATE", "mint"), ("SHAP", "yellow")],
    )

    section_header("01", "Data Siswa", "IDENTITAS & NILAI RAPOR")

    c1, c2, c3 = st.columns([1.6, .8, .7])
    with c1:
        nama_siswa = st.text_input("Nama Siswa", placeholder="Nama lengkap siswa")
    with c2:
        kelas_siswa = st.selectbox("Kelas", KELAS_LIST, index=KELAS_LIST.index("IX-A"))
    with c3:
        absen_siswa = st.number_input("No. Absen", 1, 50, 1)

    c1, c2 = st.columns([1.5, 1])
    with c1:
        nilai_akademik = st.number_input(
            "Nilai Rata-rata Rapor",
            min_value=60.0, max_value=100.0, value=83.78,
            step=.01, format="%.2f",
            help=f"Baseline rata-rata sekolah: {RATA_RATA_NILAI:.2f}",
        )
    with c2:
        gap = nilai_akademik - RATA_RATA_NILAI
        gap_label = "di atas baseline" if gap >= 0 else "di bawah baseline"
        gap_accent = "mint" if gap >= 0 else "coral"
        stat_card("Posisi terhadap baseline", f"{gap:+.2f}", f"poin · {gap_label}", gap_accent)

    section_header("02", "Profil Siswa", "PILIH KONDISI SISWA · 8 KONSTRUK")

    st.markdown("""
    <div class="info-box blue" style="margin-bottom:1.5rem;">
        <div class="info-title">💡 Cara Mengisi</div>
        <div class="info-text">
            Klik salah satu pilihan yang paling menggambarkan kondisi siswa. 
            Tidak perlu mengisi angka — cukup pilih deskripsi yang paling sesuai.
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        input_self_efficacy = input_kategori("in_se", "Self-Efficacy Akademik")
        input_motivasi = input_kategori("in_mot", "Motivasi Belajar")
        input_kecemasan = input_kategori("in_cem", "Kecemasan Akademik")
        input_kemalasan = input_kategori("in_mal", "Kemalasan Belajar")

    with right:
        st.markdown("""
        <div class="card card-yellow">
            <div class="card-label">FAKTOR EKSTERNAL</div>
            <div style="color:#667085;font-size:.72rem;margin-top:.25rem;">
                Lingkungan keluarga dan sekolah yang terkait dengan siswa.
            </div>
        </div>
        """, unsafe_allow_html=True)
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

    a, b, c = st.columns(3)
    with a:
        stat_card("Nilai Akademik", f"{nilai_akademik:.2f}", "nilai rata-rata rapor", "blue")
    with b:
        stat_card("Selisih Baseline", f"{selisih_nilai:+.2f}", "poin dari rata-rata sekolah",
                  "mint" if selisih_nilai >= 0 else "coral")
    with c:
        accent_kategori = 'mint' if kategori == 'Sangat Baik' else 'blue' if kategori == 'Baik' else 'yellow' if kategori == 'Cukup' else 'coral'
        st.markdown(f"""
        <div class="card stat-card">
            <div class="topline {accent_kategori}"></div>
            <div class="card-label">KATEGORI NILAI</div>
            <div class="card-value" style="font-size:1.55rem;color:{warna_kategori};">{simbol} {kategori}</div>
            <div class="card-note">klasifikasi berdasarkan rentang nilai</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:.9rem'></div>", unsafe_allow_html=True)
    score_pct = max(0, min(100, (nilai_akademik - 60) / 40 * 100))
    baseline_pct = max(0, min(100, (RATA_RATA_NILAI - 60) / 40 * 100))
    st.markdown(f"""
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div class="card-label">POSISI NILAI</div>
                <div style="font-weight:800;font-size:.88rem;margin-top:.2rem;">Skala 60–100</div>
            </div>
            <div style="font-family:'Manrope';font-weight:800;color:#2563EB;">{nilai_akademik:.2f}</div>
        </div>
        <div style="height:12px;background:#EEF2F7;border-radius:99px;margin-top:1rem;position:relative;overflow:hidden;">
            <div style="width:{score_pct:.1f}%;height:100%;background:linear-gradient(90deg,#4F7CFF,#7C5CFC);border-radius:99px;animation:growBar .8s ease both;"></div>
            <div style="position:absolute;left:{baseline_pct:.1f}%;top:-3px;width:3px;height:18px;background:#17233B;border-radius:99px;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:.45rem;color:#667085;font-size:.62rem;">
            <span>60</span><span>Baseline {RATA_RATA_NILAI:.2f}</span><span>100</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section_header("04", "Faktor yang Membentuk Nilai", "KONTRIBUSI TERHADAP SELISIH NILAI")

    df_kontribusi = pd.DataFrame([
        {"Aspek": k, "Kontribusi": v, "Nilai_Siswa": profil_siswa[k],
         "Baseline": BASELINE_ASPEK[k], "Selisih": profil_siswa[k] - BASELINE_ASPEK[k]}
        for k, v in kontribusi.items()
    ]).sort_values("Kontribusi", key=abs, ascending=False)

    positive = df_kontribusi[df_kontribusi["Kontribusi"] > 0].head(4)
    negative = df_kontribusi[df_kontribusi["Kontribusi"] < 0].sort_values("Kontribusi").head(4)

    c1, c2 = st.columns([1.65, 1])
    with c1:
        fig, ax = plt.subplots(figsize=(10.5, 6.2))
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        d = df_kontribusi.sort_values("Kontribusi", ascending=True)
        vals = d["Kontribusi"].values
        y = np.arange(len(d))
        bars = ax.barh(y, vals, height=.56,
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
        ax.set_yticklabels(d["Aspek"], fontsize=8.5)
        ax.tick_params(axis="y", length=0, pad=7)
        ax.tick_params(axis="x", labelsize=8, colors="#667085")
        ax.grid(axis="x", alpha=.12)
        ax.set_axisbelow(True)
        for s in ["top","right","left"]:
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color("#D8E0EB")
        ax.set_xlabel("Kontribusi (poin nilai)", fontsize=9, fontweight="bold", color="#667085")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with c2:
        st.markdown('<div class="card"><div class="card-label">TOP POSITIVE INFLUENCES</div>', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:.7rem"></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-label">TOP NEGATIVE INFLUENCES</div>', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)

    section_header("05", "Detail Perbandingan", "PROFIL SISWA VS BASELINE")
    tabel = df_kontribusi.copy()
    tabel["Status"] = tabel["Selisih"].apply(lambda x: "▲ Di atas" if x>0 else "▼ Di bawah" if x<0 else "● Sama")
    tabel = tabel[["Aspek","Nilai_Siswa","Baseline","Selisih","Kontribusi","Status"]]
    tabel.columns = ["Aspek","Nilai Siswa","Baseline","Selisih","Kontribusi (poin)","Status"]
    tabel = tabel.sort_values("Kontribusi (poin)", key=abs, ascending=False)
    st.dataframe(tabel, use_container_width=True, hide_index=True,
                 column_config={
                     "Nilai Siswa": st.column_config.NumberColumn(format="%.2f"),
                     "Baseline": st.column_config.NumberColumn(format="%.2f"),
                     "Selisih": st.column_config.NumberColumn(format="%+.2f"),
                     "Kontribusi (poin)": st.column_config.NumberColumn(format="%+.2f"),
                 })

    section_header("06", "Simpan Data", "ARSIPKAN HASIL ANALISIS")
    if not nama_siswa:
        st.markdown("""
        <div class="info-box yellow">
            <div class="info-title">Data belum siap disimpan</div>
            <div class="info-text">Isi nama siswa terlebih dahulu untuk mengarsipkan hasil analisis.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button("Simpan hasil siswa →", type="primary", use_container_width=True):
            duplikat = any(s["Nama"] == nama_siswa and s["Kelas"] == kelas_siswa
                           for s in st.session_state.database_siswa)
            if duplikat:
                st.warning(f"Siswa {nama_siswa} ({kelas_siswa}) sudah ada di database.")
            else:
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
                st.success(f"Data {nama_siswa} berhasil disimpan.")
                st.balloons()

    back_to_menu_button("analisis")

# ================================================================
# MODUL 02 — DATABASE
# ================================================================

elif st.session_state.current_page == "database":
    hero_header(
        "MODUL 02 · DATABASE",
        "Student records.<br><span class='accent'>One place.</span>",
        "Arsip siswa yang telah dianalisis beserta nilai dan faktor-faktor yang digunakan dalam dashboard.",
        [("DATA SISWA", "blue"), ("ARSIP", "yellow")],
    )

    if len(st.session_state.database_siswa) == 0:
        st.markdown("""
        <div class="card" style="text-align:center;padding:4rem 2rem;margin-top:1.5rem;">
            <div style="font-size:2.8rem;">◎</div>
            <div style="font-family:'Manrope';font-weight:800;font-size:1.35rem;margin-top:.7rem;">Belum ada data</div>
            <div style="color:#667085;font-size:.75rem;margin-top:.4rem;">Input siswa dari menu Analisis Sebab-Akibat untuk mulai mengisi database.</div>
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
        c1, c2 = st.columns([1, 2])
        with c1:
            filter_kelas = st.selectbox("Filter Kelas",
                ["Semua"] + sorted(df_db["Kelas"].unique().tolist()))
        with c2:
            search = st.text_input("Cari nama", placeholder="Ketik nama siswa...")

        df_tampil = df_db.copy()
        if filter_kelas != "Semua":
            df_tampil = df_tampil[df_tampil["Kelas"] == filter_kelas]
        if search:
            df_tampil = df_tampil[df_tampil["Nama"].str.contains(search, case=False, na=False)]

        st.markdown(f'<div class="eyebrow"><span class="eyebrow-dot"></span>{len(df_tampil)} SISWA DITEMUKAN</div>',
                    unsafe_allow_html=True)
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2)
        with c1:
            csv = df_tampil.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", data=csv,
                file_name=f"database_siswa_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv", use_container_width=True)
        with c2:
            if st.button("Hapus semua data", use_container_width=True):
                st.session_state.database_siswa = []
                st.rerun()

    back_to_menu_button("database")

# ================================================================
# MODUL 03 — ANALISIS KAUSAL
# ================================================================

elif st.session_state.current_page == "kausal":
    hero_header(
        "MODUL 03 · METODE 01",
        "What changes the outcome?<br><span class='accent'>Causal effects.</span>",
        "Estimasi Average Treatment Effect (ATE) untuk membaca arah dan besar efek setiap konstruk terhadap prestasi akademik.",
        [("SCM", "blue"), ("DOWHY / ATE", "mint"), ("8 KONSTRUK", "yellow")],
    )

    df_ate = pd.DataFrame([{"Konstruk": k, "ATE": v} for k, v in ATE_DATA.items()])
    positive_ate = df_ate[df_ate["ATE"] > 0].sort_values("ATE", ascending=False)
    negative_ate = df_ate[df_ate["ATE"] < 0].sort_values("ATE")

    section_header("01", "Gambaran Efek", "AVERAGE TREATMENT EFFECT")
    a, b, c = st.columns(3)
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
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-box mint">
            <div class="info-title">Efek positif</div>
            <div class="info-text">Nilai ATE positif menunjukkan arah efek yang meningkatkan outcome pada estimasi yang digunakan.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box coral">
            <div class="info-title">Efek negatif</div>
            <div class="info-text">Nilai ATE negatif menunjukkan arah efek yang menurunkan outcome pada estimasi yang digunakan.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    st.dataframe(df_ate.sort_values("ATE", ascending=False),
                 use_container_width=True, hide_index=True,
                 column_config={"ATE": st.column_config.NumberColumn("ATE", format="%+.4f")})

    back_to_menu_button("kausal")

# ================================================================
# MODUL 04 — ANALISIS SHAP
# ================================================================

elif st.session_state.current_page == "shap":
    hero_header(
        "MODUL 04 · METODE 02",
        "Which features matter<br><span class='accent'>to the prediction?</span>",
        "Mean absolute SHAP digunakan untuk menunjukkan seberapa besar kontribusi fitur terhadap prediksi model Random Forest.",
        [("RANDOM FOREST", "blue"), ("SHAP", "yellow"), ("EXPLAINABILITY", "mint")],
    )

    df_shap = pd.DataFrame([{"Konstruk": k, "Mean_SHAP": v} for k, v in SHAP_DATA.items()])
    top = df_shap.sort_values("Mean_SHAP", ascending=False).iloc[0]
    second = df_shap.sort_values("Mean_SHAP", ascending=False).iloc[1]

    section_header("01", "Feature Importance", "MEAN ABSOLUTE SHAP VALUE")
    a, b, c = st.columns(3)
    with a: stat_card("Kontributor #1", f"{top['Mean_SHAP']:.4f}", top["Konstruk"], "blue")
    with b: stat_card("Kontributor #2", f"{second['Mean_SHAP']:.4f}", second["Konstruk"], "purple")
    with c: stat_card("Jumlah fitur", "8", "fitur/konstruk dianalisis", "yellow")

    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = plot_shap(df_shap)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("02", "Ranking Kontribusi", "FAKTOR PALING RELEVAN BAGI MODEL")
    ranked = df_shap.sort_values("Mean_SHAP", ascending=False).reset_index(drop=True)
    for i, row in ranked.iterrows():
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

    st.dataframe(df_shap.sort_values("Mean_SHAP", ascending=False),
                 use_container_width=True, hide_index=True,
                 column_config={"Mean_SHAP": st.column_config.NumberColumn("Mean |SHAP|", format="%.4f")})

    back_to_menu_button("shap")

# ================================================================
# MODUL 05 — REKOMENDASI UMUM
# ================================================================

elif st.session_state.current_page == "rekomendasi":
    hero_header(
        "MODUL 05 · TINDAK LANJUT",
        "From analysis<br><span class='accent'>to action.</span>",
        "Ringkasan faktor yang dapat menjadi prioritas tindak lanjut berdasarkan kombinasi hasil ATE dan SHAP.",
        [("PRIORITAS", "yellow"), ("ATE", "mint"), ("SHAP", "blue")],
    )

    section_header("01", "Prioritas Intervensi", "FAKTOR DENGAN SINYAL PALING KUAT")
    col1, col2 = st.columns(2)

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
        for i, (name, ate, shap, desc) in enumerate(positive_priority, 1):
            st.markdown(f"""
            <div style="padding:1rem 0;border-bottom:1px solid #CBEBDD;">
                <div style="display:flex;justify-content:space-between;gap:.7rem;">
                    <div style="font-weight:800;font-size:.88rem;">{i:02d} · {name}</div>
                    <div style="font-family:'Manrope';font-weight:800;color:#18A77A;">ATE {ate:+.2f}</div>
                </div>
                <div style="font-size:.69rem;color:#667085;margin-top:.3rem;">SHAP {shap:.4f}</div>
                <div style="font-size:.76rem;line-height:1.55;margin-top:.45rem;color:#475467;">{desc}</div>
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
        for i, (name, ate, shap, desc) in enumerate(negative_priority, 1):
            st.markdown(f"""
            <div style="padding:1rem 0;border-bottom:1px solid #F1DF96;">
                <div style="display:flex;justify-content:space-between;gap:.7rem;">
                    <div style="font-weight:800;font-size:.88rem;">{i:02d} · {name}</div>
                    <div style="font-family:'Manrope';font-weight:800;color:#EF5B67;">ATE {ate:+.2f}</div>
                </div>
                <div style="font-size:.69rem;color:#667085;margin-top:.3rem;">SHAP {shap:.4f}</div>
                <div style="font-size:.76rem;line-height:1.55;margin-top:.45rem;color:#475467;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

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
    </div>
    """, unsafe_allow_html=True)

    back_to_menu_button("rekomendasi")

# ================================================================
# MODUL 06 — CATATAN UNTUK GURU
# ================================================================

else:
    hero_header(
        "MODUL 06 · KONSULTASI GURU",
        "From insight<br><span class='accent'>to classroom action.</span>",
        "Kesimpulan sebab-akibat dan tindak lanjut personal yang bisa langsung dilakukan guru "
        "untuk membantu siswa tertentu.",
        [("PERSONAL", "blue"), ("ACTIONABLE", "mint"), ("PER SISWA", "yellow")],
    )

    section_header("01", "Pilih Siswa", "AMBIL DARI DATABASE ATAU INPUT MANUAL")

    opsi_sumber = st.radio(
        "Sumber data siswa",
        ["📁 Ambil dari database", "✍️ Input manual"],
        horizontal=True,
    )

    if opsi_sumber == "📁 Ambil dari database":
        if len(st.session_state.database_siswa) == 0:
            st.warning("⚠️ Database masih kosong. Silakan input siswa terlebih dahulu di Modul 01.")
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
            nama_siswa = st.text_input("Nama Siswa", placeholder="Nama lengkap", key="manual_nama")
        with c2:
            kelas_siswa = st.selectbox("Kelas", KELAS_LIST, key="manual_kelas")
        with c3:
            absen_siswa = st.number_input("No. Absen", 1, 50, 1, key="manual_absen")

        nilai_akademik = st.number_input(
            "Nilai Akademik", min_value=60.0, max_value=100.0, value=83.78,
            step=.01, format="%.2f", key="manual_nilai"
        )

        st.markdown("**Profil 8 Konstruk**")
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

    section_header("02", "Kesimpulan Sebab-Akibat", "RINGKASAN UNTUK GURU")

    posisi = "di atas" if selisih_nilai >= 0 else "di bawah"
    abs_selisih = abs(selisih_nilai)

    if len(faktor_negatif) > 0:
        fn = faktor_negatif.iloc[0]
        narasi_negatif = f"""Faktor yang paling menekan nilai <b>{nama_siswa}</b> adalah <b style="color:#EF5B67;">{fn['Aspek']}</b> (kontribusi <b>{fn['Kontribusi']:.2f} poin</b>). Nilai siswa pada aspek ini adalah <b>{fn['Nilai_Siswa']:.2f}</b>, sedangkan rata-rata sekolah adalah <b>{fn['Baseline']:.2f}</b>."""
    else:
        narasi_negatif = "Tidak ada faktor yang secara signifikan menekan nilai siswa ini."

    if len(faktor_positif) > 0:
        fp = faktor_positif.iloc[0]
        narasi_positif = f"""Sementara itu, kekuatan utama <b>{nama_siswa}</b> terletak pada <b style="color:#18A77A;">{fp['Aspek']}</b> (kontribusi <b>+{fp['Kontribusi']:.2f} poin</b>)."""
    else:
        narasi_positif = "Siswa ini belum memiliki faktor kekuatan dominan yang bisa diandalkan."

    st.markdown(f"""
    <div class="card" style="border-left:5px solid {warna_kategori};">
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem;">
            <div class="profile-avatar" style="width:56px;height:56px;font-size:1.2rem;">
                {"".join(x[0] for x in nama_siswa.split()[:2]).upper()}
            </div>
            <div>
                <div style="font-family:'Manrope';font-weight:800;font-size:1.3rem;">{nama_siswa}</div>
                <div style="color:#667085;font-size:.8rem;">{kelas_siswa} · Absen {absen_siswa:02d} · Nilai {nilai_akademik:.2f}</div>
            </div>
        </div>
        <div style="font-size:.95rem;line-height:1.75;color:#1F2A44;">
            Nilai <b>{nama_siswa}</b> saat ini berada <b>{abs_selisih:.2f} poin {posisi} rata-rata sekolah</b> 
            (baseline {RATA_RATA_NILAI:.2f}). Berdasarkan analisis sebab-akibat:
            <br><br>
            {narasi_negatif}
            <br><br>
            {narasi_positif}
            <br><br>
            <b>Kategori nilai:</b> <span style="color:{warna_kategori};">{simbol} {kategori}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section_header("03", "Prioritas Perbaikan", "FOKUSKAN PADA 3 HAL INI")

    prioritas = faktor_negatif.head(3)

    if len(prioritas) == 0:
        st.markdown("""
        <div class="info-box mint">
            <div class="info-title">✓ Tidak ada prioritas perbaikan mendesak</div>
            <div class="info-text">Semua faktor siswa ini berada dalam kondisi yang baik atau netral. Fokus pada pemeliharaan kondisi saat ini.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(len(prioritas))
        for i, (_, row) in enumerate(prioritas.iterrows()):
            with cols[i]:
                gap_val = row['Selisih']
                level = "🔴 Urgent" if gap_val < -1.0 else "🟡 Perhatian" if gap_val < -0.5 else "🟢 Monitor"
                st.markdown(f"""
                <div class="card" style="border-top:4px solid #EF5B67;min-height:220px;">
                    <div style="font-size:.65rem;font-weight:800;letter-spacing:1.5px;color:#EF5B67;">PRIORITAS {i+1}</div>
                    <div style="font-family:'Manrope';font-weight:800;font-size:1rem;margin:.6rem 0 .3rem;">{row['Aspek']}</div>
                    <div style="font-size:.7rem;color:#667085;margin-bottom:.5rem;">{level}</div>
                    <div style="font-size:.75rem;line-height:1.6;color:#475467;">
                        Nilai siswa: <b>{row['Nilai_Siswa']:.2f}</b><br>
                        Rata-rata: <b>{row['Baseline']:.2f}</b><br>
                        <span style="color:#EF5B67;font-weight:700;">Selisih: {row['Selisih']:+.2f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    section_header("04", "Tindak Lanjut untuk Guru", "CHECKLIST YANG BISA DILAKUKAN MINGGU INI")

    TINDAK_LANJUT = {
        "Self-Efficacy Akademik": {
            "guru": [
                "Berikan tugas bertahap (mudah → sulit) agar siswa merasakan keberhasilan",
                "Berikan pujian spesifik atas usaha, bukan hanya hasil",
                "Ajak siswa merefleksikan pencapaian kecilnya setiap minggu",
                "Dudukkan siswa dengan teman peer-mentor",
            ],
            "siswa": [
                "Buat jurnal harian '1 hal yang berhasil saya lakukan hari ini'",
                "Tetapkan target kecil yang realistis setiap minggu",
            ]
        },
        "Keterlibatan Orang Tua": {
            "guru": [
                "Kirim pesan WhatsApp ke orang tua dengan kabar positif tentang anak",
                "Ajak orang tua ikut 1 sesi belajar bersama di sekolah",
                "Berikan panduan 'cara mendampingi anak belajar 15 menit/hari'",
                "Jadwalkan komunikasi rutin 2 minggu sekali",
            ],
            "siswa": [
                "Ceritakan ke orang tua 1 hal yang dipelajari di sekolah",
                "Minta orang tua memeriksa PR minimal 2x seminggu",
            ]
        },
        "Harapan Orang Tua": {
            "guru": [
                "Pertemuan dengan orang tua untuk membahas ekspektasi realistis",
                "Bantu orang tua memahami tahap perkembangan belajar anak",
                "Sarankan fokus pada usaha anak, bukan hanya nilai",
                "Berikan contoh cara memotivasi tanpa menekan",
            ],
            "siswa": [
                "Belajar menyampaikan perasaan kepada orang tua dengan tenang",
                "Fokus pada usaha yang bisa dikontrol, bukan hasil akhir",
            ]
        },
        "Dukungan Sekolah": {
            "guru": [
                "Refleksi: apakah bantuan justru mengurangi kemandirian?",
                "Kurangi bantuan pada hal yang siswa bisa lakukan sendiri",
                "Berikan kesempatan siswa untuk mencoba dan gagal (safe to fail)",
                "Fokus pada scaffolding, bukan taking over",
            ],
            "siswa": [
                "Coba selesaikan tugas sulit dulu selama 10 menit sebelum bertanya",
                "Catat apa yang sudah dicoba sebelum minta bantuan",
            ]
        },
        "Motivasi Belajar": {
            "guru": [
                "Kaitkan materi dengan kehidupan nyata siswa",
                "Berikan pilihan tugas agar siswa merasa punya kontrol",
                "Apresiasi proses, bukan hanya hasil",
                "Ciptakan suasana kelas yang menyenangkan",
            ],
            "siswa": [
                "Cari 1 hal menarik dari setiap mata pelajaran",
                "Belajar bersama teman untuk menambah semangat",
            ]
        },
        "Kecemasan Akademik": {
            "guru": [
                "Ajarkan teknik relaksasi sederhana sebelum ujian",
                "Ubah suasana ujian jadi lebih santai",
                "Berikan ujian formatif yang tidak menakutkan",
                "Normalisasi bahwa cemas itu wajar",
            ],
            "siswa": [
                "Latihan pernapasan 4-7-8 sebelum ujian",
                "Persiapan lebih awal agar tidak panik",
            ]
        },
        "Fasilitas Sekolah": {
            "guru": [
                "Informasikan fasilitas yang bisa dimanfaatkan siswa",
                "Bantu siswa mengakses perpustakaan/lab di luar jam pelajaran",
                "Cek apakah siswa punya hambatan akses fasilitas",
            ],
            "siswa": [
                "Manfaatkan perpustakaan minimal 1x seminggu",
                "Tanyakan ke guru jika butuh bantuan fasilitas",
            ]
        },
        "Kemalasan Belajar": {
            "guru": [
                "Cari tahu akar kemalasan (bosan? sulit? tidak paham?)",
                "Beri tugas yang lebih menantang jika bosan",
                "Pecah tugas besar jadi langkah kecil",
                "Buat sistem reward sederhana",
            ],
            "siswa": [
                "Mulai dari tugas 5 menit saja",
                "Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat)",
            ]
        }
    }

    if len(prioritas) == 0:
        st.info("Tidak ada tindak lanjut khusus yang diperlukan. Pertahankan kondisi baik siswa ini.")
    else:
        for i, (_, row) in enumerate(prioritas.iterrows()):
            aspek = row["Aspek"]
            tugas = TINDAK_LANJUT.get(aspek, {"guru": [], "siswa": []})

            with st.expander(f"🎯 Prioritas {i+1}: {aspek}", expanded=(i == 0)):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**👨‍🏫 Yang bisa dilakukan GURU:**")
                    for j, t in enumerate(tugas["guru"], 1):
                        st.markdown(f"""
                        <div style="display:flex;gap:.7rem;padding:.6rem 0;border-bottom:1px solid #EEF2F7;">
                            <div style="width:22px;height:22px;border-radius:6px;background:#EAF1FF;color:#2563EB;
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
                        <div style="display:flex;gap:.7rem;padding:.6rem 0;border-bottom:1px solid #EEF2F7;">
                            <div style="width:22px;height:22px;border-radius:6px;background:#E8F8F1;color:#18A77A;
                                        display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:800;flex-shrink:0;">
                                {j}
                            </div>
                            <div style="font-size:.82rem;line-height:1.55;color:#1F2A44;">{s}</div>
                        </div>
                        """, unsafe_allow_html=True)

    section_header("05", "Script Komunikasi", "CARA MENYAMPAIKAN KE SISWA / ORANG TUA")

    st.markdown(f"""
    <div class="card" style="border-left:5px solid #7C5CFC;">
        <div class="card-label">💬 SCRIPT UNTUK BERBICARA DENGAN SISWA</div>
        <div style="font-size:.88rem;line-height:1.8;color:#1F2A44;margin-top:.8rem;font-style:italic;">
            "<b>{nama_siswa}</b>, Ibu/Bapak sudah melihat hasil belajarmu. 
            Ada hal positif yang Ibu/Bapak perhatikan: 
            <b style="color:#18A77A;">{faktor_positif.iloc[0]['Aspek'] if len(faktor_positif) > 0 else 'kamu sudah berusaha'}</b>.
            <br><br>
            Ibu/Bapak ingin bantu kamu untuk hal yang mungkin masih bisa ditingkatkan, 
            khususnya <b style="color:#EF5B67;">{prioritas.iloc[0]['Aspek'] if len(prioritas) > 0 else 'belajar'}</b>.
            Bukan karena kamu kurang, tapi karena Ibu/Bapak yakin kamu bisa lebih baik lagi.
            <br><br>
            Bagaimana kalau kita coba beberapa hal bersama? Ibu/Bapak tidak akan menghakimi, 
            kita cari solusi bersama-sama."
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="border-left:5px solid #F6C945;margin-top:1rem;">
        <div class="card-label">📞 SCRIPT UNTUK KOMUNIKASI DENGAN ORANG TUA</div>
        <div style="font-size:.88rem;line-height:1.8;color:#1F2A44;margin-top:.8rem;font-style:italic;">
            "Selamat siang Bapak/Ibu. Saya ingin berbagi tentang perkembangan 
            <b>{nama_siswa}</b> di sekolah.
            <br><br>
            <b>Pertama, kabar baiknya:</b> {nama_siswa} menunjukkan kekuatan di 
            <b style="color:#18A77A;">{faktor_positif.iloc[0]['Aspek'] if len(faktor_positif) > 0 else 'semangat belajar'}</b>.
            <br><br>
            <b>Yang ingin saya diskusikan:</b> ada beberapa hal yang mungkin bisa kita bantu bersama, 
            terutama di <b style="color:#EF5B67;">{prioritas.iloc[0]['Aspek'] if len(prioritas) > 0 else 'kebiasaan belajar'}</b>.
            Saya ingin dengar juga sudut pandang Bapak/Ibu dari rumah.
            <br><br>
            Kira-kira kapan waktu yang tepat untuk kita bicara lebih lanjut? 
            Saya siap berkolaborasi untuk mendukung {nama_siswa}."
        </div>
    </div>
    """, unsafe_allow_html=True)

    section_header("06", "Indikator Keberhasilan", "KAPAN GURU TAHU PERBAIKAN BERHASIL?")

    st.markdown("""
    <div class="card">
        <div style="font-size:.82rem;line-height:1.7;color:#475467;">
        Evaluasi tindak lanjut dalam <b>2 minggu</b> ke depan dengan indikator berikut:
        </div>
    """, unsafe_allow_html=True)

    indikator = [
        ("2 Minggu", "Siswa menunjukkan perubahan kecil di kelas (lebih aktif bertanya, lebih fokus)", "🟢"),
        ("1 Bulan", "Nilai formatif (kuis, PR, tugas) mulai menunjukkan tren naik", "🟡"),
        ("3 Bulan", "Nilai sumatif (ujian tengah/akhir semester) menunjukkan peningkatan stabil", "🟢"),
        ("6 Bulan", "Perubahan perilaku belajar sudah menjadi kebiasaan siswa", "⭐"),
    ]

    for waktu, indikator_txt, simbol_ind in indikator:
        st.markdown(f"""
        <div style="display:flex;gap:1rem;padding:1rem;border-bottom:1px solid #EEF2F7;align-items:center;">
            <div style="font-size:1.5rem;">{simbol_ind}</div>
            <div style="flex:1;">
                <div style="font-weight:800;font-size:.8rem;color:#2563EB;letter-spacing:1px;">{waktu.upper()}</div>
                <div style="font-size:.85rem;color:#1F2A44;margin-top:.2rem;">{indikator_txt}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    section_header("07", "Export Catatan", "SIMPAN & CETAK UNTUK ARSIP GURU")

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

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Download Catatan (.txt)",
            data=catatan_text.encode("utf-8"),
            file_name=f"catatan_{nama_siswa.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col2:
        st.info("💡 Gunakan Ctrl+P / Cmd+P di browser untuk cetak halaman ini.")

    back_to_menu_button("catatan_guru")
