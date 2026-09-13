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
# VISUAL SYSTEM v2 — EYE-CATCHING + LANDING PAGE
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

html, body, [class*="css"]{
    font-family:'DM Sans',sans-serif;
    color:var(--ink);
}

.stApp{
    background:
        radial-gradient(circle at 92% 4%, rgba(79,124,255,.10), transparent 24rem),
        radial-gradient(circle at 4% 80%, rgba(246,201,69,.10), transparent 22rem),
        radial-gradient(circle at 50% 50%, rgba(124,92,252,.05), transparent 30rem),
        var(--canvas);
}

.main{background:transparent;}
.block-container{
    max-width:1480px;
    padding:1.6rem 2.7rem 4rem 2.7rem;
}

#MainMenu, footer, header{visibility:hidden;}

h1,h2,h3,h4{font-family:'Manrope',sans-serif;}

/* ============ ANIMATIONS ============ */
@keyframes riseIn{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
@keyframes growBar{from{transform:scaleX(0);transform-origin:left;}to{transform:scaleX(1);transform-origin:left;}}
@keyframes floatDot{0%,100%{transform:translateY(0);}50%{transform:translateY(-7px);}}
@keyframes glow{0%,100%{box-shadow:0 0 0 0 rgba(79,124,255,.35);}50%{box-shadow:0 0 0 18px rgba(79,124,255,0);}}
@keyframes gradientShift{0%,100%{background-position:0% 50%;}50%{background-position:100% 50%;}}
@keyframes sparkle{0%,100%{opacity:.3;transform:scale(1);}50%{opacity:1;transform:scale(1.3);}}

.motion{animation:riseIn .5s ease both;}

/* ============ HERO ============ */
.dashboard-hero{
    position:relative;overflow:hidden;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 60%,#EFF4FF 100%);
    border:1px solid var(--line);
    border-radius:28px;
    padding:2.3rem 2.5rem;
    box-shadow:0 20px 55px rgba(30,50,90,.09);
    animation:riseIn .5s ease both;
}
.dashboard-hero:before{
    content:"";position:absolute;
    width:220px;height:220px;
    right:-80px;top:-90px;
    border:34px solid rgba(37,99,235,.09);
    border-radius:50%;
}
.dashboard-hero:after{
    content:"";position:absolute;
    width:10px;height:10px;
    right:140px;bottom:40px;
    background:var(--yellow);
    border-radius:50%;
    box-shadow:
        42px -22px 0 var(--blue),
        78px 9px 0 var(--mint),
        112px -30px 0 var(--purple),
        145px 5px 0 var(--pink);
    animation:floatDot 3s ease-in-out infinite;
}

.eyebrow{
    display:inline-flex;align-items:center;gap:8px;
    font-size:.68rem;font-weight:800;letter-spacing:1.5px;
    text-transform:uppercase;color:var(--blue);
    margin-bottom:.7rem;
}
.eyebrow-dot{
    width:8px;height:8px;background:var(--yellow);
    border-radius:50%;display:inline-block;
    animation:sparkle 2s ease-in-out infinite;
}

.hero-title{
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.15rem,4vw,3.8rem);
    line-height:1.02;letter-spacing:-2.4px;
    margin:0;max-width:850px;
}
.hero-title .accent{
    background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;
}
.hero-sub{
    color:var(--muted);font-size:.98rem;line-height:1.65;
    max-width:790px;margin:.9rem 0 0;
}
.hero-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:1.25rem;}
.pill{
    display:inline-flex;align-items:center;gap:7px;
    padding:.42rem .7rem;border-radius:999px;
    font-size:.65rem;font-weight:800;letter-spacing:.5px;
    border:1px solid var(--line);background:#fff;
}
.pill.blue{background:var(--blue-soft);color:var(--blue);border-color:#D4E0FF;}
.pill.yellow{background:var(--yellow-soft);color:#936F00;border-color:#F3DF8D;}
.pill.mint{background:var(--mint-soft);color:#087453;border-color:#BCE8D7;}
.pill.purple{background:var(--purple-soft);color:#5B3FCC;border-color:#DDD5FF;}

/* ============ SECTIONS ============ */
.section-wrap{margin-top:2rem;margin-bottom:1rem;}
.section-number{
    display:inline-flex;width:38px;height:38px;
    align-items:center;justify-content:center;border-radius:12px;
    background:linear-gradient(135deg,var(--blue) 0%,var(--purple) 100%);
    color:#fff;font-size:.78rem;font-weight:800;
    box-shadow:0 8px 18px rgba(37,99,235,.25);
}
.section-title{font-size:1.45rem;letter-spacing:-.7px;margin:0;}
.section-sub{
    color:var(--muted);font-size:.72rem;text-transform:uppercase;
    letter-spacing:1.1px;font-weight:800;margin-top:.2rem;
}
.section-line{height:1px;background:var(--line);margin-top:.9rem;}

/* ============ CARDS ============ */
.card{
    background:var(--surface);border:1px solid var(--line);
    border-radius:20px;padding:1.25rem 1.35rem;
    box-shadow:0 10px 28px rgba(30,50,90,.045);
    transition:transform .25s ease, box-shadow .25s ease, border-color .25s ease;
    animation:riseIn .5s ease both;
}
.card:hover{
    transform:translateY(-3px);
    box-shadow:0 18px 40px rgba(30,50,90,.10);
    border-color:#CFD9EA;
}
.card-blue{background:linear-gradient(135deg,#fff 0%,#F3F7FF 100%);}
.card-yellow{background:linear-gradient(135deg,#fff 0%,#FFFBEB 100%);}
.card-mint{background:linear-gradient(135deg,#fff 0%,#F1FBF7 100%);}
.card-purple{background:linear-gradient(135deg,#fff 0%,#F7F4FF 100%);}
.card-dark{background:var(--navy);border-color:var(--navy);color:#fff;}

.card-label{
    font-size:.65rem;font-weight:800;text-transform:uppercase;
    letter-spacing:1px;color:var(--muted);
}
.card-value{
    font-family:'Manrope',sans-serif;font-size:2rem;font-weight:800;
    letter-spacing:-1.2px;line-height:1;margin-top:.5rem;
}
.card-note{color:var(--muted);font-size:.74rem;margin-top:.45rem;}

.stat-card{min-height:122px;position:relative;overflow:hidden;}
.stat-card:after{
    content:"";position:absolute;width:70px;height:70px;
    border-radius:50%;right:-28px;bottom:-28px;
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

/* ============ LANDING PAGE - MENU CARDS ============ */
.menu-hero{
    position:relative;overflow:hidden;
    background:linear-gradient(135deg,#17233B 0%,#1E2F50 50%,#2563EB 100%);
    border-radius:32px;
    padding:3.5rem 3rem;
    color:#fff;
    margin-bottom:2.5rem;
    box-shadow:0 30px 70px rgba(23,35,59,.35);
    animation:riseIn .5s ease both;
}
.menu-hero:before{
    content:"";position:absolute;
    width:450px;height:450px;
    border-radius:50%;
    border:70px solid rgba(246,201,69,.08);
    right:-200px;top:-180px;
}
.menu-hero:after{
    content:"";position:absolute;
    width:12px;height:12px;
    right:200px;bottom:60px;
    background:var(--yellow);border-radius:50%;
    box-shadow:
        48px -28px 0 #4F7CFF,
        92px 12px 0 #18A77A,
        135px -35px 0 #7C5CFC,
        175px 8px 0 #EC4899;
    animation:floatDot 3.5s ease-in-out infinite;
}
.menu-hero-kicker{
    display:inline-flex;align-items:center;gap:8px;
    font-size:.7rem;font-weight:800;letter-spacing:2px;
    color:#F6C945;text-transform:uppercase;
    margin-bottom:1rem;
}
.menu-hero-title{
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.5rem,5vw,4.5rem);
    line-height:.98;letter-spacing:-3px;
    font-weight:800;margin:0;
    max-width:900px;
}
.menu-hero-title em{
    color:#F6C945;font-style:italic;
    font-family:'Manrope',serif;
}
.menu-hero-sub{
    color:#C6D1E5;
    font-size:1.05rem;line-height:1.6;
    max-width:680px;margin:1.2rem 0 0;
}
.menu-hero-meta{
    display:flex;gap:.7rem;flex-wrap:wrap;
    margin-top:1.8rem;
    position:relative;z-index:1;
}
.menu-hero-meta span{
    padding:.55rem .9rem;
    border-radius:999px;
    background:rgba(255,255,255,.1);
    border:1px solid rgba(255,255,255,.15);
    color:#D9E3F5;
    font-size:.68rem;font-weight:800;letter-spacing:.7px;
}

/* Menu card grid */
.menu-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));
    gap:1.3rem;
    margin-bottom:2rem;
}

.menu-card{
    position:relative;
    overflow:hidden;
    background:#fff;
    border:1px solid var(--line);
    border-radius:24px;
    padding:1.75rem 1.6rem 1.6rem;
    text-decoration:none;
    color:inherit;
    transition:transform .3s cubic-bezier(.2,.7,.3,1), box-shadow .3s ease, border-color .3s ease;
    box-shadow:0 12px 32px rgba(30,50,90,.06);
    min-height:230px;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    animation:riseIn .55s ease both;
}
.menu-card:hover{
    transform:translateY(-6px);
    box-shadow:0 24px 55px rgba(30,50,90,.14);
}
.menu-card.mc-blue:hover{border-color:#2563EB;}
.menu-card.mc-yellow:hover{border-color:#F6C945;}
.menu-card.mc-mint:hover{border-color:#18A77A;}
.menu-card.mc-purple:hover{border-color:#7C5CFC;}
.menu-card.mc-pink:hover{border-color:#EC4899;}

.menu-card-num{
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:.68rem;font-weight:800;letter-spacing:1.6px;
    color:var(--muted);text-transform:uppercase;
}
.menu-card-icon{
    width:56px;height:56px;border-radius:16px;
    display:flex;align-items:center;justify-content:center;
    font-size:1.7rem;
    margin:.9rem 0;
}
.menu-card.mc-blue .menu-card-icon{background:var(--blue-soft);color:var(--blue);}
.menu-card.mc-yellow .menu-card-icon{background:var(--yellow-soft);color:#936F00;}
.menu-card.mc-mint .menu-card-icon{background:var(--mint-soft);color:var(--mint);}
.menu-card.mc-purple .menu-card-icon{background:var(--purple-soft);color:var(--purple);}
.menu-card.mc-pink .menu-card-icon{background:#FCE7F3;color:var(--pink);}

.menu-card-title{
    font-family:'Manrope',sans-serif;
    font-size:1.15rem;font-weight:800;
    letter-spacing:-.4px;line-height:1.2;
    margin:0 0 .35rem;
}
.menu-card-desc{
    color:var(--muted);font-size:.78rem;line-height:1.55;
    margin:0;
}
.menu-card-cta{
    display:inline-flex;align-items:center;gap:.45rem;
    font-size:.72rem;font-weight:800;letter-spacing:.5px;
    margin-top:1rem;
    text-transform:uppercase;
}
.menu-card.mc-blue .menu-card-cta{color:var(--blue);}
.menu-card.mc-yellow .menu-card-cta{color:#936F00;}
.menu-card.mc-mint .menu-card-cta{color:var(--mint);}
.menu-card.mc-purple .menu-card-cta{color:var(--purple);}
.menu-card.mc-pink .menu-card-cta{color:var(--pink);}

.menu-card:before{
    content:"";position:absolute;
    width:120px;height:120px;border-radius:50%;
    right:-55px;bottom:-55px;
    opacity:.06;
    transition:transform .4s ease;
}
.menu-card.mc-blue:before{background:var(--blue);}
.menu-card.mc-yellow:before{background:var(--yellow);}
.menu-card.mc-mint:before{background:var(--mint);}
.menu-card.mc-purple:before{background:var(--purple);}
.menu-card.mc-pink:before{background:var(--pink);}
.menu-card:hover:before{transform:scale(1.6);}

/* ============ BACK BUTTON ============ */
.back-btn-wrap{
    margin-top:2rem;margin-bottom:1rem;
    padding-top:1.5rem;
    border-top:1px solid var(--line);
}

/* ============ ALERTS ============ */
.info-box{
    border-radius:18px;padding:1.1rem 1.2rem;
    border:1px solid var(--line);background:#fff;
}
.info-box.blue{background:var(--blue-soft);border-color:#D5E1FF;}
.info-box.yellow{background:var(--yellow-soft);border-color:#F1DF96;}
.info-box.mint{background:var(--mint-soft);border-color:#C5EBDD;}
.info-box.coral{background:var(--coral-soft);border-color:#F4CDD3;}
.info-title{font-weight:800;font-size:.9rem;}
.info-text{font-size:.78rem;line-height:1.6;margin-top:.35rem;color:#475467;}

/* ============ PROFILE ============ */
.profile-card{
    display:flex;align-items:center;justify-content:space-between;
    gap:1rem;padding:1.15rem 1.3rem;
    background:#fff;border:1px solid var(--line);border-radius:18px;
}
.profile-avatar{
    width:48px;height:48px;border-radius:15px;
    display:flex;align-items:center;justify-content:center;
    background:linear-gradient(135deg,var(--blue-soft) 0%,var(--purple-soft) 100%);
    color:var(--blue);font-weight:800;font-size:1rem;
}
.profile-name{font-family:'Manrope',sans-serif;font-weight:800;font-size:1.05rem;}
.profile-meta{color:var(--muted);font-size:.72rem;margin-top:.2rem;}

/* ============ FACTOR CARDS ============ */
.factor-card{
    border:1px solid var(--line);border-radius:18px;
    background:#fff;padding:1rem 1.05rem;margin:.65rem 0;
    transition:all .2s ease;
}
.factor-card:hover{transform:translateX(3px);box-shadow:0 8px 22px rgba(30,50,90,.06);}
.factor-head{display:flex;justify-content:space-between;align-items:center;gap:1rem;}
.factor-name{font-weight:700;font-size:.86rem;}
.factor-value{font-family:'Manrope',sans-serif;font-weight:800;font-size:1rem;}
.factor-bar{
    height:7px;background:#EEF2F7;border-radius:99px;
    overflow:hidden;margin-top:.75rem;
}
.factor-fill{height:100%;border-radius:99px;animation:growBar .7s ease both;}
.fill-blue{background:var(--blue);}
.fill-yellow{background:var(--yellow);}
.fill-mint{background:var(--mint);}
.fill-purple{background:var(--purple);}
.fill-coral{background:var(--coral);}

.rank-row{
    display:grid;grid-template-columns:34px 1fr auto;
    align-items:center;gap:.8rem;
    padding:.75rem 0;border-bottom:1px solid var(--line);
}
.rank-row:last-child{border-bottom:0;}
.rank-num{
    width:30px;height:30px;border-radius:10px;
    background:var(--blue-soft);color:var(--blue);
    display:flex;align-items:center;justify-content:center;
    font-size:.68rem;font-weight:800;
}
.rank-name{font-weight:700;font-size:.8rem;}
.rank-desc{font-size:.67rem;color:var(--muted);margin-top:.15rem;}
.rank-value{font-family:'Manrope',sans-serif;font-size:.86rem;font-weight:800;}
.positive{color:var(--mint);}
.negative{color:var(--coral);}

/* ============ INPUTS ============ */
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
    font-size:.72rem !important;font-weight:800 !important;
    color:#475467 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus{
    border-color:var(--blue) !important;
    box-shadow:0 0 0 3px rgba(37,99,235,.10) !important;
}
.stSlider label{
    font-size:.78rem !important;font-weight:700 !important;
    color:var(--ink) !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"]{
    background:var(--blue) !important;
}
.stButton > button,.stDownloadButton > button{
    border-radius:12px !important;min-height:43px;
    font-weight:800 !important;
    border:1px solid #D7DFEA !important;
    transition:all .18s ease !important;
}
.stButton > button:hover,.stDownloadButton > button:hover{
    transform:translateY(-2px);
    box-shadow:0 8px 20px rgba(30,50,90,.08);
}
button[kind="primary"]{
    background:linear-gradient(135deg,var(--blue) 0%,var(--purple) 100%) !important;
    border-color:var(--blue) !important;
    color:#fff !important;
}

/* ============ SIDEBAR ============ */
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,var(--navy) 0%,var(--navy-2) 100%);
    border-right:0;
}
[data-testid="stSidebar"] > div:first-child{padding:1rem .9rem;}
[data-testid="stSidebar"] *{color:#EEF3FF !important;}

.side-brand{padding:.65rem .55rem 1rem;}
.side-kicker{
    color:#9DBBFF !important;font-size:.62rem;font-weight:800;
    letter-spacing:1.7px;text-transform:uppercase;
}
.side-title{
    font-family:'Manrope',sans-serif;color:#fff;
    font-size:1.45rem;font-weight:800;line-height:1.05;margin-top:.35rem;
}
.side-title span{color:#F6C945;}
.side-year{
    color:#9BAAC4 !important;font-size:.62rem;
    letter-spacing:1.4px;margin-top:.45rem;
}
.side-user{
    background:rgba(255,255,255,.07);
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px;padding:.8rem;margin:.5rem 0 1rem;
}
.side-user-label{
    color:#9BAAC4 !important;font-size:.57rem;
    font-weight:800;letter-spacing:1.2px;
}
.side-user-name{
    color:#fff;font-weight:800;font-size:.88rem;margin-top:.25rem;
}

[data-testid="stSidebar"] .stButton > button{
    background:rgba(255,255,255,.06) !important;
    color:#fff !important;
    border-color:rgba(255,255,255,.12) !important;
}

/* ============ TABLE ============ */
[data-testid="stDataFrame"]{
    border:1px solid var(--line);
    border-radius:16px;overflow:hidden;
    box-shadow:0 8px 25px rgba(30,50,90,.04);
}

/* ============ LOGIN ============ */
.login-shell{max-width:930px;margin:5vh auto 0;}
.login-panel{
    display:grid;grid-template-columns:1.12fr .88fr;
    overflow:hidden;border-radius:30px;
    border:1px solid var(--line);
    box-shadow:0 24px 70px rgba(24,45,82,.12);
    background:#fff;animation:riseIn .5s ease both;
}
.login-visual{
    position:relative;min-height:500px;padding:2.5rem;
    overflow:hidden;
    background:linear-gradient(135deg,#17233B 0%,#1E2F50 50%,#2563EB 100%);
    color:#fff;
}
.login-visual:before{
    content:"";position:absolute;
    width:330px;height:330px;border-radius:50%;
    border:50px solid rgba(79,124,255,.12);
    right:-145px;top:-120px;
}
.login-visual:after{
    content:"";position:absolute;
    width:9px;height:9px;left:42px;bottom:55px;
    border-radius:50%;background:var(--yellow);
    box-shadow:35px -22px 0 #4F7CFF,75px -4px 0 #18A77A,113px -28px 0 #7C5CFC;
    animation:floatDot 3.2s ease-in-out infinite;
}
.login-kicker{
    font-size:.65rem;font-weight:800;
    letter-spacing:1.6px;color:#9DBBFF;
}
.login-title{
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.8rem,5vw,4.8rem);
    line-height:.95;letter-spacing:-3px;margin-top:3.2rem;
}
.login-title span{color:var(--yellow);}
.login-copy{
    color:#C6D1E5;line-height:1.65;
    max-width:420px;margin-top:1rem;
}
.login-feature{
    position:absolute;bottom:34px;left:2.5rem;right:2.5rem;
    display:flex;gap:.6rem;flex-wrap:wrap;
}
.login-feature span{
    padding:.45rem .65rem;border-radius:999px;
    background:rgba(255,255,255,.08);color:#D9E3F5;
    font-size:.62rem;font-weight:700;
}
.login-form{padding:2.5rem;display:flex;flex-direction:column;justify-content:center;}
.login-form-title{font-family:'Manrope',sans-serif;font-size:1.45rem;font-weight:800;}
.login-form-sub{color:var(--muted);font-size:.78rem;margin:.35rem 0 1.4rem;}
.demo-note{
    margin-top:1rem;padding:.75rem .9rem;
    border-radius:13px;background:var(--yellow-soft);
    color:#725A00;font-size:.7rem;line-height:1.5;
}

@media(max-width:850px){
    .block-container{padding:1rem 1rem 3rem;}
    .login-shell{margin:1rem auto 0;}
    .login-panel{grid-template-columns:1fr;}
    .login-visual{min-height:360px;}
    .login-title{margin-top:2.5rem;}
    .login-feature{position:static;margin-top:3rem;}
    .menu-hero{padding:2.5rem 1.7rem;}
    .menu-grid{grid-template-columns:1fr;}
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
    st.session_state.current_page = "home"  # home / analisis / database / kausal / shap / rekomendasi

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
        <div style="display:flex;align-items:center
