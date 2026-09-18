import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import hashlib
import json
import os

# ================================================================
# PERSISTENSI DATABASE (opsional — aman kalau file tidak ada)
# ================================================================
DB_FILE = "database_siswa.json"

def load_database():
    """Load database dari file JSON lokal. Return [] kalau belum ada."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_database(data):
    """Simpan database ke file JSON lokal."""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

st.set_page_config(
    page_title="SIA.Prestasi | SMPN 6 Salatiga",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ================================================================
# VISUAL SYSTEM — CLEAN WHITE + ANIMATION
# ================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');

:root{
    --ink:#0F1B33; --muted:#5C6B85; --line:#E4EAF2;
    --canvas:#FFFFFF; --surface:#FFFFFF;
    --blue:#2563EB; --blue-deep:#1E3A8A; --blue-soft:#EAF1FF;
    --violet:#7C5CFC; --violet-soft:#F1EDFF;
    --yellow:#F6C945; --yellow-deep:#B8860B; --yellow-soft:#FFF7D6;
    --mint:#10B981; --mint-soft:#E8F8F1;
    --coral:#EF5B67; --coral-soft:#FFF0F2;
    --pink:#EC4899; --pink-soft:#FCE7F3;
    --cyan:#06B6D4; --cyan-soft:#CFFAFE;
    --purple:#7C5CFC; --purple-soft:#F1EDFF;
    --navy:#0B1730; --navy-2:#16294A;
}

html, body, [class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink);}

/* ===== APP BACKGROUND — PUTIH + GLOW TIPIS ===== */
.stApp{
    background:
        radial-gradient(circle at 100% 0%, rgba(37,99,235,.07), transparent 32rem),
        radial-gradient(circle at 0% 100%, rgba(124,92,252,.06), transparent 32rem),
        radial-gradient(circle at 0% 0%, rgba(236,72,153,.04), transparent 28rem),
        #FFFFFF;
    background-attachment:fixed;
}
.main{background:transparent;}
.block-container{max-width:1480px;padding:1.6rem 2.7rem 4rem 2.7rem;}
#MainMenu, footer, header{visibility:hidden;}
h1,h2,h3,h4{font-family:'Manrope',sans-serif;}

/* ===== KEYFRAMES ===== */
@keyframes riseIn{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeSlideIn{from{opacity:0;transform:translateX(-20px);}to{opacity:1;transform:translateX(0);}}
@keyframes growBar{from{transform:scaleX(0);transform-origin:left;}to{transform:scaleX(1);transform-origin:left;}}
@keyframes floatDot{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
@keyframes softBounce{0%,100%{transform:translateY(0);}50%{transform:translateY(-4px);}}
@keyframes rotateSlow{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
@keyframes sparkle{0%,100%{opacity:.3;transform:scale(1);}50%{opacity:1;transform:scale(1.35);}}
@keyframes glowPulse{0%,100%{box-shadow:0 0 0 0 rgba(124,92,252,.35);}50%{box-shadow:0 0 0 12px rgba(124,92,252,0);}}
@keyframes gradientShift{0%,100%{background-position:0% 50%;}50%{background-position:100% 50%;}}
@keyframes shimmer{0%{background-position:-200% 0;}100%{background-position:200% 0;}}

.motion{animation:riseIn .5s ease both;}
.motion-slide{animation:fadeSlideIn .55s ease both;}
.motion-bounce{animation:softBounce 2.5s ease-in-out infinite;}
.motion-rotate{animation:rotateSlow 30s linear infinite;}
.motion-gradient{background-size:200% 200%;animation:gradientShift 6s ease-in-out infinite;}

/* ============ LOGIN PAGE ============ */
.login-page-header{
    display:flex;justify-content:space-between;align-items:center;
    padding:1rem 2rem;
    background:linear-gradient(135deg,#FFFFFF 0%,#F3F6FF 100%);
    border-bottom:1px solid #DCE4F2;
    margin:-1.6rem -2.7rem 0 -2.7rem;
    box-shadow:0 4px 20px rgba(37,99,235,.06);
}
.login-logo-area{display:flex;align-items:center;gap:.8rem;justify-content:flex-end;width:100%;}
.login-logo-icon{font-size:2.2rem;line-height:1;filter:drop-shadow(0 4px 10px rgba(37,99,235,.3));}
.login-logo-text{text-align:right;line-height:1.15;}
.login-logo-title{
    font-family:'Plus Jakarta Sans',sans-serif;font-size:1.6rem;font-weight:800;
    color:#0F1B33;letter-spacing:-.8px;
}
.login-logo-title .blue-part{
    background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.login-logo-sub{font-size:.72rem;color:#5C6B85;letter-spacing:.3px;margin-top:.15rem;}

.login-content{max-width:1050px;margin:2rem auto;padding:0 2rem;}

.login-date-logout{
    display:flex;justify-content:space-between;align-items:center;
    padding:.9rem 1.1rem;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 100%);
    border:1px solid #DCE4F2;border-left:5px solid #2563EB;
    border-radius:12px;margin-bottom:2rem;
    box-shadow:0 6px 18px rgba(37,99,235,.06);
}
.login-date{font-family:'Manrope',sans-serif;font-weight:800;font-size:.95rem;color:#0F1B33;}
.login-logout-link{font-size:.8rem;color:#2563EB;font-weight:700;padding:.35rem .8rem;border-left:1px solid #E4EAF2;}

.siasat-label{font-family:'DM Sans',sans-serif;font-weight:700;font-size:.9rem;color:#0F1B33;padding-top:.65rem;}
.siasat-label::after{content:" :";color:#5C6B85;font-weight:400;}

.siasat-input .stTextInput > div > div > input,
.siasat-input [data-baseweb="input"] > div,
.siasat-input [data-baseweb="base-input"]{
    border:1.5px solid #A8B5C7 !important;border-radius:8px !important;
    padding:.55rem .85rem !important;font-size:.9rem !important;
    background:linear-gradient(180deg,#FFFFFF 0%,#F9FBFF 100%) !important;
    min-height:42px !important;transition:all .2s ease !important;
    font-family:'DM Sans',sans-serif !important;
}
.siasat-input .stTextInput > div > div > input:focus{
    border-color:#2563EB !important;
    box-shadow:0 0 0 4px rgba(37,99,235,.15) !important;
    outline:none !important;
}
.siasat-input .stTextInput > div > div > input::placeholder{color:#98A2B3 !important;font-style:italic;}
.siasat-input .stTextInput > label{display:none !important;}

.siasat-btn-login button{
    background:linear-gradient(135deg,#4ADE80 0%,#22C55E 50%,#16A34A 100%) !important;
    border:1px solid #16A34A !important;color:#fff !important;
    font-family:'DM Sans',sans-serif !important;font-weight:700 !important;
    font-size:.9rem !important;letter-spacing:.3px !important;
    padding:.55rem 2rem !important;border-radius:8px !important;
    min-height:44px !important;
    box-shadow:0 4px 14px rgba(22,163,74,.35), inset 0 1px 0 rgba(255,255,255,.35) !important;
    transition:all .2s ease !important;text-transform:none !important;
}
.siasat-btn-login button:hover{
    background:linear-gradient(135deg,#22C55E 0%,#16A34A 100%) !important;
    box-shadow:0 6px 20px rgba(22,163,74,.45) !important;
    transform:translateY(-2px) !important;
}

.siasat-btn-lupa button{
    background:linear-gradient(135deg,#F87171 0%,#EF4444 50%,#DC2626 100%) !important;
    border:1px solid #DC2626 !important;color:#fff !important;
    font-family:'DM Sans',sans-serif !important;font-weight:700 !important;
    font-size:.9rem !important;letter-spacing:.3px !important;
    padding:.55rem 2rem !important;border-radius:8px !important;
    min-height:44px !important;
    box-shadow:0 4px 14px rgba(220,38,38,.35), inset 0 1px 0 rgba(255,255,255,.35) !important;
    transition:all .2s ease !important;text-transform:none !important;
}
.siasat-btn-lupa button:hover{
    background:linear-gradient(135deg,#EF4444 0%,#DC2626 100%) !important;
    box-shadow:0 6px 20px rgba(220,38,38,.45) !important;
    transform:translateY(-2px) !important;
}

.siasat-info-box{
    background:linear-gradient(135deg,#FFF9E6 0%,#FFF4CC 100%);
    border:1px solid #F3DF8D;border-left:5px solid #F6C945;
    border-radius:12px;padding:1.2rem 1.4rem;margin-top:2.5rem;
    box-shadow:0 8px 22px rgba(246,201,69,.15);
}
.siasat-info-header{display:flex;align-items:center;gap:.6rem;margin-bottom:.7rem;}
.siasat-info-icon{font-size:1.3rem;line-height:1;}
.siasat-info-title{font-family:'Manrope',sans-serif;font-weight:800;font-size:.9rem;color:#0F1B33;letter-spacing:-.2px;}
.siasat-info-list{font-size:.8rem;color:#475467;line-height:1.85;padding-left:.3rem;}
.siasat-info-list div{display:flex;gap:.5rem;}
.siasat-info-list .num{color:#2563EB;font-weight:800;flex-shrink:0;min-width:18px;}

.siasat-footer{
    text-align:center;padding:2rem 0;margin-top:3rem;
    border-top:1px solid #DCE4F2;font-size:.72rem;color:#5C6B85;
    letter-spacing:.3px;line-height:1.8;
}
.siasat-footer strong{color:#2563EB;font-weight:800;}

.siasat-alert-danger{
    background:linear-gradient(135deg,#FEF2F2 0%,#FEE2E2 100%);
    border:1px solid #FECACA;border-left:5px solid #EF4444;
    border-radius:10px;padding:.85rem 1.1rem;margin-top:1rem;
    animation:riseIn .3s ease both;box-shadow:0 4px 12px rgba(239,68,68,.1);
}
.siasat-alert-danger-title{font-family:'Manrope';font-weight:800;font-size:.82rem;color:#991B1B;}
.siasat-alert-danger-body{font-size:.75rem;color:#7F1D1D;margin-top:.25rem;}

.siasat-alert-info{
    background:linear-gradient(135deg,#EFF6FF 0%,#DBEAFE 100%);
    border:1px solid #BFDBFE;border-left:5px solid #2563EB;
    border-radius:10px;padding:.85rem 1.1rem;margin-top:1rem;
    animation:riseIn .3s ease both;box-shadow:0 4px 12px rgba(37,99,235,.1);
}
.siasat-alert-info-title{font-family:'Manrope';font-weight:800;font-size:.82rem;color:#1E40AF;}
.siasat-alert-info-body{font-size:.75rem;color:#1E3A8A;margin-top:.25rem;}

/* ============ HERO DASHBOARD ============ */
.dashboard-hero{
    position:relative;overflow:hidden;
    background:
        radial-gradient(circle at 90% 10%, rgba(124,92,252,.12), transparent 25rem),
        linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 50%,#EEF3FF 100%);
    border:1px solid #DCE4F2;border-radius:28px;padding:2.3rem 2.5rem;
    box-shadow:0 20px 55px rgba(30,50,90,.10);animation:riseIn .5s ease both;
}
.dashboard-hero:before{
    content:"";position:absolute;width:240px;height:240px;
    right:-90px;top:-100px;border:36px solid rgba(37,99,235,.09);border-radius:50%;
}
.dashboard-hero:after{
    content:"";position:absolute;width:12px;height:12px;
    right:150px;bottom:45px;background:#F6C945;border-radius:50%;
    box-shadow:
        44px -24px 0 #2563EB, 82px 10px 0 #10B981, 118px -32px 0 #7C5CFC,
        152px 6px 0 #EC4899, 186px -20px 0 #06B6D4;
    animation:floatDot 3s ease-in-out infinite;
}

/* ============ MENU HERO ============ */
.menu-hero{
    position:relative;overflow:hidden;
    background:linear-gradient(135deg,#0B1730 0%,#16294A 30%,#1E3A8A 60%,#7C5CFC 100%);
    background-size:200% 200%;
    border-radius:32px;padding:3.5rem 3rem;color:#fff;margin-bottom:2.5rem;
    box-shadow:0 30px 80px rgba(11,23,48,.40), 0 0 0 1px rgba(255,255,255,.06) inset;
    animation:riseIn .5s ease both, gradientShift 10s ease-in-out infinite;
}
.menu-hero:before{
    content:"";position:absolute;width:500px;height:500px;border-radius:50%;
    border:70px solid rgba(246,201,69,.09);right:-220px;top:-200px;
}
.menu-hero:after{
    content:"";position:absolute;width:14px;height:14px;
    right:220px;bottom:70px;background:#F6C945;border-radius:50%;
    box-shadow:
        52px -30px 0 #4F7CFF, 100px 14px 0 #10B981, 148px -38px 0 #7C5CFC,
        190px 10px 0 #EC4899, 232px -22px 0 #06B6D4;
    animation:floatDot 3.5s ease-in-out infinite;
}
.menu-hero-kicker{
    display:inline-flex;align-items:center;gap:8px;
    font-size:.7rem;font-weight:800;letter-spacing:2px;color:#F6C945;
    text-transform:uppercase;margin-bottom:1rem;
}
.menu-hero-title{
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.5rem,5vw,4.5rem);line-height:.98;
    letter-spacing:-3px;font-weight:800;margin:0;max-width:900px;
}
.menu-hero-title em{
    background:linear-gradient(135deg,#F6C945 0%,#FFA94D 50%,#F6C945 100%);
    background-size:200% 200%;
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    font-style:italic;font-family:'Manrope',serif;
    animation:gradientShift 4s ease-in-out infinite;
}
.menu-hero-sub{color:#C6D1E5;font-size:1.05rem;line-height:1.6;max-width:680px;margin:1.2rem 0 0;}
.menu-hero-meta{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.8rem;position:relative;z-index:1;}
.menu-hero-meta span{
    padding:.55rem .9rem;border-radius:999px;
    background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);
    color:#F0F5FF;font-size:.68rem;font-weight:800;letter-spacing:.7px;
    backdrop-filter:blur(10px);transition:all .2s ease;
}
.menu-hero-meta span:hover{
    background:rgba(255,255,255,.22);transform:translateY(-2px);
}

/* ============ MENU CARDS ============ */
.menu-card{
    position:relative;overflow:hidden;
    background:linear-gradient(135deg, #FFFFFF 0%, #FBFDFF 100%);
    border:1px solid #DCE4F2;border-radius:24px;
    padding:1.75rem 1.6rem 1.6rem;text-decoration:none;color:inherit;
    transition:transform .3s cubic-bezier(.2,.7,.3,1), box-shadow .3s ease, border-color .3s ease;
    box-shadow:0 14px 40px rgba(30,50,90,.08);
    min-height:230px;display:flex;flex-direction:column;justify-content:space-between;
    animation:riseIn .55s ease both;
}
.menu-card:hover{
    transform:translateY(-8px);
    box-shadow:0 28px 65px rgba(30,50,90,.18);
    animation:softBounce 1.2s ease-in-out;
}

.menu-card.mc-blue{background:linear-gradient(135deg,#FFFFFF 0%,#EAF1FF 100%);border-color:#D4E0FF;}
.menu-card.mc-blue:hover{border-color:#2563EB;box-shadow:0 28px 65px rgba(37,99,235,.28);}
.menu-card.mc-yellow{background:linear-gradient(135deg,#FFFFFF 0%,#FFF7D6 100%);border-color:#F3DF8D;}
.menu-card.mc-yellow:hover{border-color:#F6C945;box-shadow:0 28px 65px rgba(246,201,69,.32);}
.menu-card.mc-mint{background:linear-gradient(135deg,#FFFFFF 0%,#E8F8F1 100%);border-color:#BCE8D7;}
.menu-card.mc-mint:hover{border-color:#10B981;box-shadow:0 28px 65px rgba(16,185,129,.28);}
.menu-card.mc-purple{background:linear-gradient(135deg,#FFFFFF 0%,#F1EDFF 100%);border-color:#DDD5FF;}
.menu-card.mc-purple:hover{border-color:#7C5CFC;box-shadow:0 28px 65px rgba(124,92,252,.32);}
.menu-card.mc-pink{background:linear-gradient(135deg,#FFFFFF 0%,#FCE7F3 100%);border-color:#F8C7DF;}
.menu-card.mc-pink:hover{border-color:#EC4899;box-shadow:0 28px 65px rgba(236,72,153,.28);}
.menu-card.mc-teal{background:linear-gradient(135deg,#FFFFFF 0%,#CFFAFE 100%);border-color:#A5E8EF;}
.menu-card.mc-teal:hover{border-color:#06B6D4;box-shadow:0 28px 65px rgba(6,182,212,.28);}

.menu-card-num{font-family:'Plus Jakarta Sans',sans-serif;font-size:.68rem;font-weight:800;
    letter-spacing:1.6px;color:var(--muted);text-transform:uppercase;}
.menu-card-icon{
    width:56px;height:56px;border-radius:16px;display:flex;align-items:center;
    justify-content:center;font-size:1.7rem;margin:.9rem 0;
    box-shadow:0 6px 14px rgba(0,0,0,.06);transition:transform .3s ease;
}
.menu-card:hover .menu-card-icon{transform:scale(1.08) rotate(-4deg);}
.menu-card.mc-blue .menu-card-icon{background:linear-gradient(135deg,#DBE7FF 0%,#B8CEFF 100%);color:#2563EB;}
.menu-card.mc-yellow .menu-card-icon{background:linear-gradient(135deg,#FFF1B8 0%,#FFE37A 100%);color:#936F00;}
.menu-card.mc-mint .menu-card-icon{background:linear-gradient(135deg,#C9F2E0 0%,#9BE5C8 100%);color:#087453;}
.menu-card.mc-purple .menu-card-icon{background:linear-gradient(135deg,#E2DBFF 0%,#C9BEFF 100%);color:#5B3FCC;}
.menu-card.mc-pink .menu-card-icon{background:linear-gradient(135deg,#FBD5E8 0%,#F8AFD0 100%);color:#BE185D;}
.menu-card.mc-teal .menu-card-icon{background:linear-gradient(135deg,#B6EFF6 0%,#7FE0EC 100%);color:#0E7490;}

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
.menu-card.mc-teal .menu-card-cta{color:#0E7490;}

.menu-card:before{
    content:"";position:absolute;width:130px;height:130px;border-radius:50%;
    right:-60px;bottom:-60px;opacity:.08;transition:transform .4s ease;
}
.menu-card:hover:before{transform:scale(1.7);opacity:.12;}
.menu-card.mc-blue:before{background:var(--blue);}
.menu-card.mc-yellow:before{background:var(--yellow);}
.menu-card.mc-mint:before{background:var(--mint);}
.menu-card.mc-purple:before{background:var(--purple);}
.menu-card.mc-pink:before{background:var(--pink);}
.menu-card.mc-teal:before{background:#06B6D4;}

/* ============ SECTION HEADER ============ */
.section-wrap{margin-top:2rem;margin-bottom:1rem;}
.section-number{
    display:inline-flex;width:42px;height:42px;align-items:center;justify-content:center;
    border-radius:14px;
    background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 50%,#2563EB 100%);
    background-size:200% 200%;
    color:#fff;font-size:.8rem;font-weight:800;
    box-shadow:0 10px 24px rgba(37,99,235,.35), 0 0 0 4px rgba(124,92,252,.08);
    animation:gradientShift 4s ease-in-out infinite;
}
.section-title{font-size:1.45rem;letter-spacing:-.7px;margin:0;}
.section-sub{color:var(--muted);font-size:.72rem;text-transform:uppercase;
    letter-spacing:1.1px;font-weight:800;margin-top:.2rem;}
.section-line{height:1px;background:linear-gradient(90deg,#DCE4F2 0%,transparent 100%);margin-top:.9rem;}

/* ============ CARDS ============ */
.card{
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    border:1px solid var(--line);border-radius:20px;
    padding:1.25rem 1.35rem;
    box-shadow:0 10px 30px rgba(30,50,90,.06);
    transition:transform .25s ease, box-shadow .25s ease, border-color .25s ease;
    animation:riseIn .5s ease both;
}
.card:hover{transform:translateY(-3px);box-shadow:0 20px 48px rgba(30,50,90,.12);border-color:#CFD9EA;}

.card-blue{background:linear-gradient(135deg,#FFFFFF 0%,#EAF1FF 100%);border-color:#D4E0FF;}
.card-yellow{background:linear-gradient(135deg,#FFFFFF 0%,#FFF7D6 100%);border-color:#F3DF8D;}
.card-mint{background:linear-gradient(135deg,#FFFFFF 0%,#E8F8F1 100%);border-color:#BCE8D7;}
.card-purple{background:linear-gradient(135deg,#FFFFFF 0%,#F1EDFF 100%);border-color:#DDD5FF;}
.card-dark{
    background:
        radial-gradient(circle at 100% 0%, rgba(124,92,252,.35), transparent 20rem),
        linear-gradient(135deg,#0B1730 0%,#16294A 100%);
    border-color:#0B1730;color:#fff;
    box-shadow:0 20px 50px rgba(11,23,48,.35);
}

.card-label{font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:var(--muted);}
.card-dark .card-label{color:#9DBBFF;}
.card-value{font-family:'Manrope',sans-serif;font-size:2rem;font-weight:800;
    letter-spacing:-1.2px;line-height:1;margin-top:.5rem;}
.card-note{color:var(--muted);font-size:.74rem;margin-top:.45rem;}
.card-dark .card-note{color:#9DBBFF;}

.stat-card{min-height:122px;position:relative;overflow:hidden;}
.stat-card:after{
    content:"";position:absolute;width:90px;height:90px;border-radius:50%;
    right:-35px;bottom:-35px;background:radial-gradient(circle,rgba(37,99,235,.15),transparent 70%);
}
.stat-card .topline{width:40px;height:5px;border-radius:99px;margin-bottom:.85rem;background-size:200% 200%;}
.topline.blue{background:linear-gradient(90deg,#2563EB,#7C5CFC,#2563EB);animation:gradientShift 4s ease-in-out infinite;}
.topline.yellow{background:linear-gradient(90deg,#F6C945,#FFA94D,#F6C945);animation:gradientShift 4s ease-in-out infinite;}
.topline.mint{background:linear-gradient(90deg,#10B981,#06B6D4,#10B981);animation:gradientShift 4s ease-in-out infinite;}
.topline.coral{background:linear-gradient(90deg,#EF5B67,#EC4899,#EF5B67);animation:gradientShift 4s ease-in-out infinite;}
.topline.purple{background:linear-gradient(90deg,#7C5CFC,#EC4899,#7C5CFC);animation:gradientShift 4s ease-in-out infinite;}

.eyebrow{display:inline-flex;align-items:center;gap:8px;
    font-size:.68rem;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;
    color:var(--blue);margin-bottom:.7rem;}
.eyebrow-dot{width:8px;height:8px;background:var(--yellow);border-radius:50%;display:inline-block;
    animation:sparkle 2s ease-in-out infinite, rotateSlow 20s linear infinite;}

.hero-title{font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.15rem,4vw,3.8rem);line-height:1.02;letter-spacing:-2.4px;margin:0;max-width:850px;}
.hero-title .accent{
    background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 50%,#EC4899 100%);
    background-size:200% 200%;
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    animation:gradientShift 6s ease-in-out infinite;
}
.hero-sub{color:var(--muted);font-size:.98rem;line-height:1.65;max-width:790px;margin:.9rem 0 0;}
.hero-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:1.25rem;}
.pill{display:inline-flex;align-items:center;gap:7px;padding:.42rem .7rem;border-radius:999px;
    font-size:.65rem;font-weight:800;letter-spacing:.5px;border:1px solid var(--line);background:#fff;}
.pill.blue{background:var(--blue-soft);color:var(--blue);border-color:#D4E0FF;}
.pill.yellow{background:var(--yellow-soft);color:#936F00;border-color:#F3DF8D;}
.pill.mint{background:var(--mint-soft);color:#087453;border-color:#BCE8D7;}
.pill.purple{background:var(--purple-soft);color:#5B3FCC;border-color:#DDD5FF;}

/* ============ PROFILE CARD ============ */
.profile-card{
    display:flex;align-items:center;justify-content:space-between;gap:1rem;
    padding:1.15rem 1.3rem;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 100%);
    border:1px solid #DCE4F2;border-radius:18px;
    box-shadow:0 8px 24px rgba(30,50,90,.05);
}
.profile-avatar{
    width:48px;height:48px;border-radius:15px;display:flex;align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 50%,#EC4899 100%);
    background-size:200% 200%;
    color:#fff;font-weight:800;font-size:1rem;
    box-shadow:0 8px 18px rgba(37,99,235,.3);
    animation:gradientShift 6s ease-in-out infinite;
}
.profile-name{font-family:'Manrope',sans-serif;font-weight:800;font-size:1.05rem;}
.profile-meta{color:var(--muted);font-size:.72rem;margin-top:.2rem;}

/* ============ FACTOR CARD ============ */
.factor-card{
    border:1px solid var(--line);border-radius:18px;
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    padding:1rem 1.05rem;margin:.65rem 0;transition:all .25s ease;
}
.factor-card:hover{transform:translateX(4px);box-shadow:0 10px 26px rgba(30,50,90,.08);border-color:#CFD9EA;}
.factor-head{display:flex;justify-content:space-between;align-items:center;gap:1rem;}
.factor-name{font-weight:700;font-size:.86rem;}
.factor-value{font-family:'Manrope',sans-serif;font-weight:800;font-size:1rem;}
.factor-bar{height:7px;background:#EEF2F7;border-radius:99px;overflow:hidden;margin-top:.75rem;}
.factor-fill{height:100%;border-radius:99px;animation:growBar .7s ease both;}
.fill-blue{background:linear-gradient(90deg,#2563EB,#7C5CFC);}
.fill-yellow{background:linear-gradient(90deg,#F6C945,#FFA94D);}
.fill-mint{background:linear-gradient(90deg,#10B981,#06B6D4);}
.fill-purple{background:linear-gradient(90deg,#7C5CFC,#EC4899);}
.fill-coral{background:linear-gradient(90deg,#EF5B67,#EC4899);}

/* ============ RANK ROW ============ */
.rank-row{display:grid;grid-template-columns:34px 1fr auto;
    align-items:center;gap:.8rem;padding:.75rem 0;border-bottom:1px solid var(--line);}
.rank-row:last-child{border-bottom:0;}
.rank-num{
    width:30px;height:30px;border-radius:10px;
    background:linear-gradient(135deg,#EAF1FF 0%,#F1EDFF 100%);
    color:var(--blue);display:flex;align-items:center;justify-content:center;
    font-size:.68rem;font-weight:800;
}
.rank-name{font-weight:700;font-size:.8rem;}
.rank-desc{font-size:.67rem;color:var(--muted);margin-top:.15rem;}
.rank-value{font-family:'Manrope',sans-serif;font-size:.86rem;font-weight:800;}
.positive{color:var(--mint);}
.negative{color:var(--coral);}

/* ============ INPUT/COMPONENTS OVERRIDE ============ */
.stRadio > div{gap:.6rem;}
.stRadio [role="radiogroup"]{gap:.5rem;}
.stRadio [role="radiogroup"] label{
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    border:1.5px solid var(--line);border-radius:12px;
    padding:.65rem 1rem !important;transition:all .2s ease;
    font-weight:600 !important;cursor:pointer;
}
.stRadio [role="radiogroup"] label:hover{
    border-color:var(--blue);
    background:linear-gradient(135deg,#FFFFFF 0%,#EAF1FF 100%);
    transform:translateY(-1px);
}
.stRadio [role="radiogroup"] label[data-checked="true"]{
    border-color:var(--blue);
    background:linear-gradient(135deg,#EAF1FF 0%,#F1EDFF 100%);
    color:var(--blue);
    box-shadow:0 6px 16px rgba(37,99,235,.15);
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox [data-baseweb="select"] > div{
    background:linear-gradient(180deg,#FFFFFF 0%,#FBFDFF 100%) !important;
    border:1px solid #D7DFEA !important;border-radius:12px !important;
    min-height:43px;color:var(--ink) !important;
    transition:all .2s ease !important;
}
.stTextInput label,.stNumberInput label,.stSelectbox label{
    font-size:.72rem !important;font-weight:800 !important;color:#475467 !important;}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus{
    border-color:var(--blue) !important;
    box-shadow:0 0 0 4px rgba(37,99,235,.12) !important;}

.stButton > button,.stDownloadButton > button{
    border-radius:12px !important;min-height:43px;font-weight:800 !important;
    border:1px solid #D7DFEA !important;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 100%) !important;
    transition:all .2s ease !important;
    color:#17233B !important;
}
.stButton > button:hover,.stDownloadButton > button:hover{
    transform:translateY(-2px);
    box-shadow:0 10px 24px rgba(30,50,90,.12);
    border-color:#2563EB !important;
}
button[kind="primary"]{
    background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 100%) !important;
    background-size:200% 200% !important;
    border-color:#2563EB !important;color:#fff !important;
    box-shadow:0 8px 20px rgba(37,99,235,.3) !important;
    animation:gradientShift 5s ease-in-out infinite;
}
button[kind="primary"]:hover{
    box-shadow:0 12px 30px rgba(37,99,235,.45) !important;
    transform:translateY(-2px);
}
button:disabled{
    opacity:.5 !important;cursor:not-allowed !important;
}

[data-testid="stDataFrame"]{
    border:1px solid var(--line);border-radius:16px;overflow:hidden;
    box-shadow:0 10px 28px rgba(30,50,90,.06);
}

/* ============ TABS ============ */
.stTabs [data-baseweb="tab-list"]{
    gap:.5rem;background:transparent;border-bottom:1px solid var(--line);
}
.stTabs [data-baseweb="tab"]{
    height:44px;border-radius:12px 12px 0 0;
    background:transparent;font-weight:800;font-size:.82rem;
    color:#5C6B85;padding:0 1.2rem;
}
.stTabs [data-baseweb="tab"]:hover{color:#2563EB;background:#F5F8FF;}
.stTabs [aria-selected="true"]{
    background:linear-gradient(135deg,#EAF1FF 0%,#F1EDFF 100%) !important;
    color:#2563EB !important;
    border-bottom:3px solid #2563EB !important;
}

/* ============ INFO BOX ============ */
.info-box{
    border-radius:18px;padding:1.1rem 1.2rem;border:1px solid var(--line);
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
}
.info-box.blue{background:linear-gradient(135deg,#EAF1FF 0%,#DBE7FF 100%);border-color:#D5E1FF;}
.info-box.yellow{background:linear-gradient(135deg,#FFF7D6 0%,#FFF1B8 100%);border-color:#F1DF96;}
.info-box.mint{background:linear-gradient(135deg,#E8F8F1 0%,#C9F2E0 100%);border-color:#C5EBDD;}
.info-box.coral{background:linear-gradient(135deg,#FFF0F2 0%,#FFD9DF 100%);border-color:#F4CDD3;}
.info-title{font-weight:800;font-size:.9rem;}
.info-text{font-size:.78rem;line-height:1.6;margin-top:.35rem;color:#475467;}

/* ============ NOTIFIKASI ============ */
.notif-success{
    background:linear-gradient(135deg,#ECFDF5 0%,#D1FAE5 60%,#A7F3D0 100%);
    border:2px solid #10B981;border-left:6px solid #10B981;
    border-radius:14px;padding:1.2rem 1.4rem;margin:1rem 0;
    animation:riseIn .5s ease both;
    box-shadow:0 10px 30px rgba(16,185,129,.2);
}
.notif-success-title{
    font-family:'Manrope',sans-serif;font-weight:800;
    font-size:1rem;color:#065F46;display:flex;align-items:center;gap:.5rem;
}
.notif-success-body{font-size:.85rem;color:#064E3B;line-height:1.6;margin-top:.4rem;}

/* ============ TOP BAR ============ */
.top-bar{
    display:flex;justify-content:space-between;align-items:center;
    padding:.85rem 1.2rem;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 100%);
    border:1px solid var(--line);border-radius:16px;margin-bottom:1.5rem;
    box-shadow:0 6px 20px rgba(30,50,90,.06);
}

@media(max-width:850px){
    .block-container{padding:1rem 1rem 3rem;}
    .login-page-header{margin:-1rem -1rem 0 -1rem;padding:.8rem 1rem;}
    .login-logo-title{font-size:1.2rem;}
    .login-content{padding:0;}
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
    st.session_state.database_siswa = load_database()
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
        return "Sangat Baik", "#10B981", "▲"
    elif nilai >= 84:
        return "Baik", "#2563EB", "●"
    elif nilai >= 80:
        return "Cukup", "#F0B900", "◆"
    return "Perlu Perhatian", "#EF5B67", "▼"


def terjemah_ate(nilai):
    """Terjemahkan nilai ATE ke bahasa awam untuk guru non-teknis."""
    if nilai > 3:
        return "🔥 Sangat kuat MENINGKATKAN nilai", "#10B981"
    elif nilai > 2:
        return "⬆️ Kuat meningkatkan nilai", "#10B981"
    elif nilai > 1:
        return "↗️ Sedang meningkatkan nilai", "#10B981"
    elif nilai > 0.5:
        return "↑️ Sedikit meningkatkan nilai", "#10B981"
    elif nilai >= -0.5:
        return "➖ Hampir tidak berpengaruh", "#5C6B85"
    elif nilai >= -1:
        return "↓️ Sedikit menurunkan nilai", "#EF5B67"
    elif nilai >= -2:
        return "↘️ Sedang menurunkan nilai", "#EF5B67"
    elif nilai >= -3:
        return "⬇️ Kuat menurunkan nilai", "#EF5B67"
    else:
        return "🚨 Sangat kuat MENURUNKAN nilai", "#EF5B67"


def terjemah_shap(nilai):
    """Terjemahkan nilai SHAP ke bahasa awam."""
    if nilai > 0.7:
        return "⭐⭐⭐ Sangat menentukan prediksi"
    elif nilai > 0.4:
        return "⭐⭐ Cukup menentukan prediksi"
    elif nilai > 0.15:
        return "⭐ Kurang menentukan prediksi"
    else:
        return "◦ Hampir tidak menentukan"


def goto_page(page):
    st.session_state.current_page = page
    st.session_state.last_saved = None
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


def top_bar(page_title, page_sub):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="padding:.5rem 0;">
            <div style="font-family:'Manrope';font-weight:800;font-size:1.1rem;color:#0F1B33;">
                {page_title}
            </div>
            <div style="color:#5C6B85;font-size:.75rem;margin-top:.15rem;">
                {page_sub}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("← Menu Utama", use_container_width=True, key=f"topback_{page_title}"):
            goto_page("home")


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
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    vals = df["Pengaruh"].values
    labels = df["Faktor"].values
    y = np.arange(len(df))
    bars = ax.barh(y, vals, height=.58,
                   color=["#EF5B67" if x < 0 else "#10B981" for x in vals], alpha=.9)
    ax.axvline(0, color="#0F1B33", linewidth=1.3)
    max_abs = max(abs(vals.min()), abs(vals.max()))
    pad = max_abs * .15
    ax.set_xlim(vals.min() - pad, vals.max() + pad)
    for bar, val in zip(bars, vals):
        offset = max_abs * .04 if val >= 0 else -max_abs * .04
        ha = "left" if val >= 0 else "right"
        label = f"{val:+.2f} poin"
        ax.text(val + offset, bar.get_y() + bar.get_height()/2, label,
                va="center", ha=ha, fontsize=9.5, fontweight="bold",
                color="#10B981" if val >= 0 else "#EF5B67")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", labelsize=8, colors="#5C6B85")
    ax.grid(axis="x", alpha=.12, linewidth=.7)
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8E0EB")
    ax.set_xlabel("← MENURUNKAN nilai    |    MENINGKATKAN nilai →",
                  fontsize=10, fontweight="bold", color="#5C6B85", labelpad=12)
    plt.tight_layout()
    return fig


def plot_kepentingan(df):
    df = df.sort_values("Kepentingan", ascending=True)
    fig, ax = plt.subplots(figsize=(11, 6.3))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    vals = df["Kepentingan"].values
    labels = df["Faktor"].values
    y = np.arange(len(df))
    bars = ax.barh(y, vals, height=.58, color="#7C5CFC", alpha=.9)
    ax.set_xlim(0, max(vals) * 1.18)
    for bar, val in zip(bars, vals):
        ax.text(val + max(vals)*.018, bar.get_y() + bar.get_height()/2,
                f"{val:.4f}", va="center", fontsize=9.5, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", labelsize=8, colors="#5C6B85")
    ax.grid(axis="x", alpha=.12, linewidth=.7)
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8E0EB")
    ax.set_xlabel("Semakin panjang → semakin penting untuk prediksi",
                  fontsize=10, fontweight="bold", color="#5C6B85", labelpad=12)
    plt.tight_layout()
    return fig


def input_kategori(key_name, faktor_name):
    config = SKALA_PILIHAN[faktor_name]
    st.markdown(f"""
    <div style="margin-bottom:.5rem;">
        <div style="font-family:'Manrope';font-weight:800;font-size:.88rem;color:#0F1B33;">
            {faktor_name}
        </div>
        <div style="font-size:.72rem;color:#5C6B85;margin-top:.15rem;margin-bottom:.6rem;">
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
            username = st.text_input(
                "username_siasat",
                placeholder="Masukkan nama pengguna",
                label_visibility="collapsed",
                key="login_username_siasat"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        col_label2, col_input2 = st.columns([1, 3])
        with col_label2:
            st.markdown('<div class="siasat-label" style="padding-top:.65rem;padding-left:.3rem;">Kata Sandi</div>', unsafe_allow_html=True)
        with col_input2:
            st.markdown('<div class="siasat-input">', unsafe_allow_html=True)
            password = st.text_input(
                "password_siasat",
                type="password",
                placeholder="Masukkan kata sandi",
                label_visibility="collapsed",
                key="login_password_siasat"
            )
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
                st.session_state.current_page = "home"
                st.rerun()
            else:
                st.markdown("""
                <div class="siasat-alert-danger">
                    <div class="siasat-alert-danger-title">❌ Login Gagal</div>
                    <div class="siasat-alert-danger-body">
                        Nama pengguna atau kata sandi salah. Silakan coba lagi.
                    </div>
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

    # Tampilkan akun demo HANYA saat mode development
    if os.environ.get("SHOW_DEMO_ACCOUNTS", "true").lower() == "true":
        with st.expander("🔑 Lihat Akun Demo (mode development)"):
            st.markdown("""
            | Nama Pengguna | Kata Sandi | Peran |
            |---------------|------------|-------|
            | `admin` | `admin123` | Administrator |
            | `guru` | `guru123` | Guru |
            | `regina` | `regina2026` | Peneliti |
            """)

    st.markdown("""
    <div class="siasat-footer">
        <strong>SIA.Prestasi</strong> · Sistem Informasi Analisis Prestasi Siswa<br>
        Dikembangkan oleh Program Studi Magister Sains Data<br>
        Universitas Kristen Satya Wacana · © 2026
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if not st.session_state.logged_in:
    halaman_login()
    st.stop()

# ================================================================
# LANDING PAGE
# ================================================================

if st.session_state.current_page == "home":
    st.markdown("""
    <div class="menu-hero">
        <div class="menu-hero-kicker">◆ ANALISIS PRESTASI SISWA</div>
        <h1 class="menu-hero-title">
            Setiap angka punya cerita.<br>
            <em>Pahami apa yang membentuknya.</em>
        </h1>
        <p class="menu-hero-sub">
            Pilih modul di bawah untuk mulai menganalisis faktor-faktor yang mempengaruhi
            prestasi akademik siswa SMP Negeri 6 Salatiga.
        </p>
        <div class="menu-hero-meta">
            <span>8 FAKTOR</span>
            <span>SEBAB-AKIBAT</span>
            <span>PREDIKSI</span>
            <span>PENJELASAN</span>
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
                <div class="section-sub">PILIH UNTUK MEMULAI</div>
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
            <div class="menu-card-title">Analisis Siswa</div>
            <div class="menu-card-desc">
                Analisis personal siswa berdasarkan nilai akademik dan profil 8 faktor.
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
            <div class="menu-card-title">Faktor Penyebab</div>
            <div class="menu-card-desc">
                Faktor apa yang benar-benar membuat nilai siswa naik atau turun?
            </div>
            <div class="menu-card-cta">LIHAT FAKTOR →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Modul 03 →", key="btn_m3", use_container_width=True, type="primary"):
            goto_page("kausal")

    with row2[0]:
        st.markdown("""
        <div class="menu-card mc-purple">
            <div class="menu-card-num">MODUL 04</div>
            <div class="menu-card-icon">📈</div>
            <div class="menu-card-title">Tingkat Kepentingan</div>
            <div class="menu-card-desc">
                Faktor mana yang paling menentukan prediksi nilai siswa?
            </div>
            <div class="menu-card-cta">LIHAT KEPENTINGAN →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Modul 04 →", key="btn_m4", use_container_width=True, type="primary"):
            goto_page("kepentingan")

    with row2[1]:
        st.markdown("""
        <div class="menu-card mc-pink">
            <div class="menu-card-num">MODUL 05</div>
            <div class="menu-card-icon">💡</div>
            <div class="menu-card-title">Rekomendasi Umum</div>
            <div class="menu-card-desc">
                Saran tindak lanjut untuk sekolah berdasarkan hasil analisis.
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
                Kesimpulan & tindak lanjut personal untuk siswa tertentu.
            </div>
            <div class="menu-card-cta">KONSULTASI SISWA →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Modul 06 →", key="btn_m6", use_container_width=True, type="primary"):
            goto_page("catatan_guru")

    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🚪 Logout", use_container_width=True, key="logout_home"):
            st.session_state.logged_in = False
            st.session_state.user_nama = None
            st.session_state.current_page = "home"
            st.rerun()

# ================================================================
# MODUL 01 — ANALISIS SISWA
# ================================================================

elif st.session_state.current_page == "analisis":
    top_bar("🔍 Analisis Siswa", "Modul 01 · Analisis personal per siswa")

    hero_header(
        "MODUL 01 · ANALISIS UTAMA",
        "Pahami siswa.<br><span class='accent'>Tingkatkan hasilnya.</span>",
        "Masukkan profil siswa untuk melihat posisi nilainya, perbandingan terhadap rata-rata sekolah, "
        "serta faktor yang paling berpengaruh.",
        [("8 FAKTOR", "blue"), ("SEBAB-AKIBAT", "mint"), ("PER SISWA", "yellow")],
    )

    # ============================================================
    # JIKA BARU SELESAI SIMPAN → TAMPILKAN NOTIF SAJA, STOP FORM
    # ============================================================
    if st.session_state.last_saved:
        notifikasi_simpan(
            st.session_state.last_saved["nama"],
            st.session_state.last_saved["kelas"]
        )
        st.stop()

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
            help=f"Rata-rata sekolah: {RATA_RATA_NILAI:.2f}",
        )
    with c2:
        gap = nilai_akademik - RATA_RATA_NILAI
        gap_label = "di atas rata-rata" if gap >= 0 else "di bawah rata-rata"
        gap_accent = "mint" if gap >= 0 else "coral"
        stat_card("Posisi Nilai", f"{gap:+.2f}", f"poin · {gap_label}", gap_accent)

    section_header("02", "Profil Siswa", "PILIH KONDISI SISWA · 8 FAKTOR")

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
            <div style="color:#5C6B85;font-size:.72rem;margin-top:.25rem;">
                Kondisi yang berasal dari dalam diri siswa.
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
            <div style="color:#5C6B85;font-size:.72rem;margin-top:.25rem;">
                Lingkungan keluarga dan sekolah yang mempengaruhi siswa.
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

    section_header("03", "Ringkasan Siswa", "KONDISI SAAT INI")

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
        stat_card("Selisih Rata-rata", f"{selisih_nilai:+.2f}", "poin dari rata-rata sekolah",
                  "mint" if selisih_nilai >= 0 else "coral")
    with c:
        accent_kategori = 'mint' if kategori == 'Sangat Baik' else 'blue' if kategori == 'Baik' else 'yellow' if kategori == 'Cukup' else 'coral'
        st.markdown(f"""
        <div class="card stat-card">
            <div class="topline {accent_kategori}"></div>
            <div class="card-label">KATEGORI</div>
            <div class="card-value" style="font-size:1.55rem;color:{warna_kategori};">{simbol} {kategori}</div>
            <div class="card-note">berdasarkan rentang nilai</div>
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
            <div style="width:{score_pct:.1f}%;height:100%;background:linear-gradient(90deg,#2563EB,#7C5CFC,#EC4899);border-radius:99px;animation:growBar .8s ease both;"></div>
            <div style="position:absolute;left:{baseline_pct:.1f}%;top:-3px;width:3px;height:18px;background:#0F1B33;border-radius:99px;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:.45rem;color:#5C6B85;font-size:.62rem;">
            <span>60</span><span>Rata-rata {RATA_RATA_NILAI:.2f}</span><span>100</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section_header("04", "Faktor yang Mempengaruhi Nilai", "FAKTOR POSITIF & NEGATIF")

    st.markdown("""
    <div class="info-box blue" style="margin-bottom:1rem;">
        <div class="info-title">ℹ️ Tentang estimasi ini</div>
        <div class="info-text">
            Estimasi pengaruh di bawah ini dihitung dari <b>selisih profil siswa terhadap rata-rata sekolah</b>,
            dikalikan dengan <b>bobot sebab-akibat (ATE)</b> dan <b>bobot kepentingan (SHAP)</b>
            yang telah dihitung dari data seluruh siswa. Ini adalah <b>estimasi berbasis bobot</b>,
            bukan prediksi langsung dari model.
        </div>
    </div>
    """, unsafe_allow_html=True)

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
                       color=["#EF5B67" if x < 0 else "#10B981" for x in vals], alpha=.9)
        ax.axvline(0, color="#0F1B33", linewidth=1.2)
        max_abs = max(abs(vals.min()), abs(vals.max()))
        ax.set_xlim(vals.min() - max_abs*.2, vals.max() + max_abs*.2)
        for bar, val in zip(bars, vals):
            off = max_abs*.035
            ax.text(val + (off if val >= 0 else -off),
                    bar.get_y()+bar.get_height()/2, f"{val:+.2f}",
                    va="center", ha="left" if val>=0 else "right",
                    fontsize=9, fontweight="bold",
                    color="#10B981" if val >= 0 else "#EF5B67")
        ax.set_yticks(y)
        ax.set_yticklabels(d["Aspek"], fontsize=8.5)
        ax.tick_params(axis="y", length=0, pad=7)
        ax.tick_params(axis="x", labelsize=8, colors="#5C6B85")
        ax.grid(axis="x", alpha=.12)
        ax.set_axisbelow(True)
        for s in ["top","right","left"]:
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color("#D8E0EB")
        ax.set_xlabel("← MENURUNKAN nilai    |    MENINGKATKAN nilai →",
                      fontsize=10, fontweight="bold", color="#5C6B85", labelpad=10)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with c2:
        st.markdown('<div class="card"><div class="card-label">🟢 FAKTOR YANG MENINGKATKAN NILAI</div>', unsafe_allow_html=True)
        if len(positive):
            for i,(_,row) in enumerate(positive.iterrows(),1):
                st.markdown(f"""
                <div class="rank-row">
                    <div class="rank-num">{i:02d}</div>
                    <div>
                        <div class="rank-name">{row['Aspek']}</div>
                        <div class="rank-desc">Nilai siswa {row['Nilai_Siswa']:.2f} · rata-rata {row['Baseline']:.2f}</div>
                    </div>
                    <div class="rank-value positive">+{row['Kontribusi']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada faktor positif signifikan.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:.7rem"></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-label">🔴 FAKTOR YANG MENURUNKAN NILAI</div>', unsafe_allow_html=True)
        if len(negative):
            for i,(_,row) in enumerate(negative.iterrows(),1):
                st.markdown(f"""
                <div class="rank-row">
                    <div class="rank-num" style="background:#FFF0F2;color:#EF5B67;">{i:02d}</div>
                    <div>
                        <div class="rank-name">{row['Aspek']}</div>
                        <div class="rank-desc">Nilai siswa {row['Nilai_Siswa']:.2f} · rata-rata {row['Baseline']:.2f}</div>
                    </div>
                    <div class="rank-value negative">{row['Kontribusi']:+.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Tidak ada faktor negatif signifikan.")
        st.markdown('</div>', unsafe_allow_html=True)

    section_header("05", "Detail Perbandingan", "PROFIL SISWA VS RATA-RATA SEKOLAH")
    tabel = df_kontribusi.copy()
    tabel["Status"] = tabel["Selisih"].apply(lambda x: "▲ Di atas" if x>0 else "▼ Di bawah" if x<0 else "● Sama")
    tabel = tabel[["Aspek","Nilai_Siswa","Baseline","Selisih","Kontribusi","Status"]]
    tabel.columns = ["Faktor","Nilai Siswa","Rata-rata","Selisih","Pengaruh (poin)","Status"]
    tabel = tabel.sort_values("Pengaruh (poin)", key=abs, ascending=False)
    st.dataframe(tabel, use_container_width=True, hide_index=True,
                 column_config={
                     "Nilai Siswa": st.column_config.NumberColumn(format="%.2f"),
                     "Rata-rata": st.column_config.NumberColumn(format="%.2f"),
                     "Selisih": st.column_config.NumberColumn(format="%+.2f"),
                     "Pengaruh (poin)": st.column_config.NumberColumn(format="%+.2f"),
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
        # ============ VALIDASI DUPLIKAT 2 TINGKAT ============
        # 1) Nama + Kelas + Absen sama persis → peringatan duplikat
        # 2) Kelas + Absen sama (nama beda) → peringatan absen bentrok
        duplikat_persis = False
        duplikat_absen = None

        for s in st.session_state.database_siswa:
            nama_sama = s["Nama"].strip().lower() == nama_siswa.strip().lower()
            kelas_sama = s["Kelas"] == kelas_siswa
            absen_sama = int(s["Absen"]) == int(absen_siswa)

            if nama_sama and kelas_sama and absen_sama:
                duplikat_persis = True
                break
            elif kelas_sama and absen_sama and not nama_sama:
                duplikat_absen = s["Nama"]

        if duplikat_persis:
            st.markdown(f"""
            <div class="info-box coral">
                <div class="info-title">⚠️ Data sudah ada</div>
                <div class="info-text">
                    Siswa <b>{nama_siswa}</b> kelas <b>{kelas_siswa}</b>
                    dengan nomor absen <b>{absen_siswa:02d}</b> sudah tersimpan di database.
                    <br><br>
                    Jika ingin memperbarui, hapus dulu data lama di menu <b>Database Siswa</b>.
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif duplikat_absen:
            st.markdown(f"""
            <div class="info-box coral">
                <div class="info-title">⚠️ Nomor absen sudah dipakai</div>
                <div class="info-text">
                    Di kelas <b>{kelas_siswa}</b>, nomor absen <b>{absen_siswa:02d}</b>
                    sudah dipakai oleh siswa <b>{duplikat_absen}</b>.
                    <br><br>
                    <b>Solusi:</b> gunakan nomor absen yang berbeda, atau cek kembali data siswa tersebut di <b>Database Siswa</b>.
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            if st.button("💾 Simpan Hasil Siswa", type="primary", use_container_width=True):
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
                save_database(st.session_state.database_siswa)
                st.session_state.last_saved = {
                    "nama": nama_siswa,
                    "kelas": kelas_siswa,
                    "absen": absen_siswa
                }
                st.rerun()

# ================================================================
# MODUL 02 — DATABASE
# ================================================================

elif st.session_state.current_page == "database":
    top_bar("🗄️ Database Siswa", "Modul 02 · Arsip seluruh siswa")

    hero_header(
        "MODUL 02 · DATABASE",
        "Catatan siswa.<br><span class='accent'>Di satu tempat.</span>",
        "Arsip siswa yang telah dianalisis beserta nilai dan faktor-faktor yang digunakan dalam dashboard.",
        [("DATA SISWA", "blue"), ("ARSIP", "yellow")],
    )

    if len(st.session_state.database_siswa) == 0:
        st.markdown("""
        <div class="card" style="text-align:center;padding:4rem 2rem;margin-top:1.5rem;">
            <div style="font-size:2.8rem;">◎</div>
            <div style="font-family:'Manrope';font-weight:800;font-size:1.35rem;margin-top:.7rem;">Belum ada data</div>
            <div style="color:#5C6B85;font-size:.75rem;margin-top:.4rem;">Input siswa dari menu Analisis Siswa untuk mulai mengisi database.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df_db = pd.DataFrame(st.session_state.database_siswa)
        a,b,c,d = st.columns(4)
        with a: stat_card("Total Siswa", len(df_db), "siswa terarsip", "blue")
        with b: stat_card("Rata-rata", f"{df_db['Nilai Akademik'].mean():.2f}", "nilai seluruh siswa", "mint")
        with c: stat_card("Tertinggi", f"{df_db['Nilai Akademik'].max():.2f}", "nilai maksimum", "yellow")
        with d: stat_card("Terendah", f"{df_db['Nilai Akademik'].min():.2f}", "nilai minimum", "coral")

        # ============ DAFTAR SISWA ============
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
            st.download_button("📥 Download CSV", data=csv,
                file_name=f"database_siswa_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv", use_container_width=True)

        # ============ KELOLA DATA ============
        section_header("02", "Kelola Data Siswa", "HAPUS SATU-PER-SATU ATAU SEMUA")

        tab_hapus1, tab_hapus_all = st.tabs(["🗑️ Hapus Satu Siswa", "⚠️ Hapus Semua Data"])

        # ---------- TAB 1: HAPUS SATU-PER-SATU ----------
        with tab_hapus1:
            st.markdown("""
            <div class="info-box blue" style="margin-bottom:1rem;">
                <div class="info-title">💡 Cara Hapus Satu Siswa</div>
                <div class="info-text">
                    Pilih siswa yang ingin dihapus dari daftar di bawah,
                    lalu klik tombol <b>Hapus Siswa Ini</b>. Data yang dihapus tidak bisa dikembalikan.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if len(df_db) == 0:
                st.warning("Database kosong.")
            else:
                df_db_reset = df_db.reset_index(drop=True)
                opsi_label = df_db_reset.apply(
                    lambda x: f"{x['Nama']} — {x['Kelas']} (Absen {x['Absen']}) · Nilai {x['Nilai Akademik']:.2f}",
                    axis=1
                ).tolist()

                siswa_dipilih = st.selectbox(
                    "Pilih siswa yang ingin dihapus",
                    opsi_label,
                    key="pilih_hapus_satu"
                )

                idx_preview = opsi_label.index(siswa_dipilih)
                row_preview = df_db_reset.iloc[idx_preview]
                st.markdown(f"""
                <div class="card" style="border-left:5px solid #EF5B67;margin-top:.8rem;">
                    <div class="card-label">⚠️ SISWA YANG AKAN DIHAPUS</div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:.7rem;">
                        <div>
                            <div style="font-family:'Manrope';font-weight:800;font-size:1.05rem;">
                                {row_preview['Nama']}
                            </div>
                            <div style="font-size:.75rem;color:#5C6B85;margin-top:.2rem;">
                                {row_preview['Kelas']} · Absen {int(row_preview['Absen']):02d}
                                · Nilai {row_preview['Nilai Akademik']:.2f}
                                · {row_preview['Kategori']}
                            </div>
                        </div>
                        <span class="pill" style="background:#FFF0F2;color:#EF5B67;border-color:#F4CDD3;">
                            AKAN DIHAPUS
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
                if st.button("🗑️ Hapus Siswa Ini", use_container_width=True, key="btn_hapus_satu", type="primary"):
                    idx_hapus = opsi_label.index(siswa_dipilih)
                    nama_hapus = st.session_state.database_siswa[idx_hapus]["Nama"]
                    st.session_state.database_siswa.pop(idx_hapus)
                    save_database(st.session_state.database_siswa)
                    st.success(f"✅ Data siswa **{nama_hapus}** berhasil dihapus.")
                    st.rerun()

        # ---------- TAB 2: HAPUS SEMUA ----------
        with tab_hapus_all:
            st.markdown(f"""
            <div class="info-box coral" style="margin-bottom:1rem;">
                <div class="info-title">⚠️ Peringatan Keras</div>
                <div class="info-text">
                    Tombol ini akan <b>menghapus SEMUA data siswa ({len(df_db)} siswa)</b> dari database.
                    Tindakan ini <b>tidak bisa dibatalkan</b>. Pastikan Anda sudah download CSV
                    sebagai backup sebelum melanjutkan.
                </div>
            </div>
            """, unsafe_allow_html=True)

            konfirmasi = st.checkbox(
                f"Saya mengerti, saya ingin menghapus SEMUA {len(df_db)} data siswa",
                key="konfirmasi_hapus_semua"
            )

            col_a, col_b = st.columns([1, 1])
            with col_a:
                csv_all = df_db.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "💾 Download Backup Dulu",
                    data=csv_all,
                    file_name=f"backup_database_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="dl_backup_all"
                )
            with col_b:
                if st.button(
                    "🗑️ Hapus SEMUA Data",
                    use_container_width=True,
                    type="primary",
                    disabled=not konfirmasi,
                    key="btn_hapus_semua"
                ):
                    jumlah = len(st.session_state.database_siswa)
                    st.session_state.database_siswa = []
                    save_database(st.session_state.database_siswa)
                    st.success(f"✅ {jumlah} data siswa berhasil dihapus semua.")
                    st.rerun()

            if not konfirmasi:
                st.caption("🔒 Centang kotak di atas untuk mengaktifkan tombol hapus.")

# ================================================================
# MODUL 03 — FAKTOR PENYEBAB
# ================================================================

elif st.session_state.current_page == "kausal":
    top_bar("📊 Faktor Penyebab", "Modul 03 · Apa yang membuat nilai naik atau turun?")

    hero_header(
        "MODUL 03 · FAKTOR PENYEBAB",
        "Apa yang membuat nilai naik<br><span class='accent'>atau turun?</span>",
        "Faktor-faktor yang secara sebab-akibat mempengaruhi prestasi akademik siswa, "
        "berdasarkan analisis data seluruh siswa di sekolah.",
        [("SEBAB-AKIBAT", "blue"), ("8 FAKTOR", "mint"), ("TINGKAT SEKOLAH", "yellow")],
    )

    df_ate = pd.DataFrame([{"Faktor": k, "Pengaruh": v} for k, v in PENGARUH_DATA.items()])
    positive_ate = df_ate[df_ate["Pengaruh"] > 0].sort_values("Pengaruh", ascending=False)
    negative_ate = df_ate[df_ate["Pengaruh"] < 0].sort_values("Pengaruh")

    section_header("01", "Gambaran Umum", "FAKTOR YANG PALING BERPENGARUH")

    a, b, c = st.columns(3)
    with a:
        top_pos = positive_ate.iloc[0]
        stat_card("Paling MENINGKATKAN nilai", top_pos["Faktor"],
                  f"⬆️ Kuat mendorong prestasi (skor: +{top_pos['Pengaruh']:.2f})", "mint")
    with b:
        top_neg = negative_ate.iloc[0]
        stat_card("Paling MENURUNKAN nilai", top_neg["Faktor"],
                  f"⬇️ Kuat menekan prestasi (skor: {top_neg['Pengaruh']:.2f})", "coral")
    with c:
        stat_card("Jumlah faktor", "8", "variabel yang dianalisis", "blue")

    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = plot_pengaruh(df_ate)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("02", "Cara Membaca", "PENJELASAN SEDERHANA")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-box mint">
            <div class="info-title">🟢 Faktor Pendorong Nilai</div>
            <div class="info-text">
                Faktor-faktor ini <b>membantu menaikkan nilai siswa</b>.
                Semakin hijau & semakin panjang batangnya di grafik, semakin besar bantuannya.
                <br><br>
                💡 <b>Contoh:</b> Fasilitas Sekolah yang bagus cenderung <b>menaikkan</b> nilai siswa.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box coral">
            <div class="info-title">🔴 Faktor Penghambat Nilai</div>
            <div class="info-text">
                Faktor-faktor ini <b>menekan / menghambat nilai siswa</b>.
                Semakin merah & semakin panjang batangnya, semakin besar hambatannya.
                <br><br>
                💡 <b>Contoh:</b> Dukungan sekolah yang <b>terlalu berlebihan</b> justru bisa membuat
                siswa kurang mandiri, sehingga nilainya tidak berkembang.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    tabel_ate = df_ate.copy()
    tabel_ate["Penjelasan"] = tabel_ate["Pengaruh"].apply(lambda x: terjemah_ate(x)[0])
    tabel_ate["Arah"] = tabel_ate["Pengaruh"].apply(
        lambda x: "🟢 MENINGKATKAN" if x > 0 else "🔴 MENURUNKAN" if x < 0 else "➖ NETRAL"
    )
    tabel_ate = tabel_ate.sort_values("Pengaruh", ascending=False)
    tabel_ate = tabel_ate[["Faktor", "Penjelasan", "Arah", "Pengaruh"]]
    tabel_ate.columns = ["Faktor", "Artinya untuk Nilai Siswa", "Arah", "Skor Teknis (ATE)"]
    st.dataframe(tabel_ate, use_container_width=True, hide_index=True,
                 column_config={"Skor Teknis (ATE)": st.column_config.NumberColumn(format="%+.4f")})

    with st.expander("📌 Catatan Teknis (untuk peneliti / guru yang penasaran)"):
        st.markdown("""
        **Apa itu skor yang ditampilkan?**

        Skor di atas dihitung menggunakan metode **Average Treatment Effect (ATE)**
        dari **Structural Causal Model (SCM)** — sebuah teknik statistik untuk mengukur
        sebab-akibat, bukan sekadar korelasi.

        **Cara membaca angka:**
        - **Angka positif (+)**: faktor tersebut **menaikkan** nilai siswa. Contoh: `+2.43`
          artinya rata-rata menaikkan nilai sebesar **2,43 poin**.
        - **Angka negatif (−)**: faktor tersebut justru **menurunkan** nilai siswa.
          Contoh: `−3.88` artinya rata-rata **menurunkan** nilai sebesar **3,88 poin**.
        - **Mendekati 0**: faktor tersebut hampir tidak berpengaruh.

        **Untuk guru:** cukup lihat label **"Artinya untuk Nilai Siswa"** di tabel —
        itu versi bahasa sederhananya.
        """)

# ================================================================
# MODUL 04 — TINGKAT KEPENTINGAN
# ================================================================

elif st.session_state.current_page == "kepentingan":
    top_bar("📈 Tingkat Kepentingan Faktor", "Modul 04 · Faktor mana yang paling menentukan prediksi?")

    hero_header(
        "MODUL 04 · TINGKAT KEPENTINGAN",
        "Faktor mana yang paling<br><span class='accent'>menentukan prediksi?</span>",
        "Faktor-faktor yang paling sering muncul dalam keputusan model saat memprediksi nilai siswa. "
        "Semakin tinggi, semakin penting faktor tersebut.",
        [("PREDIKSI", "blue"), ("8 FAKTOR", "yellow"), ("MODEL", "mint")],
    )

    df_shap = pd.DataFrame([{"Faktor": k, "Kepentingan": v} for k, v in KEPENTINGAN_DATA.items()])
    top = df_shap.sort_values("Kepentingan", ascending=False).iloc[0]
    second = df_shap.sort_values("Kepentingan", ascending=False).iloc[1]

    section_header("01", "Faktor Paling Penting", "HASIL ANALISIS MODEL")

    a, b, c = st.columns(3)
    with a: stat_card("Faktor #1", top["Faktor"], "⭐⭐⭐ Sangat menentukan prediksi", "blue")
    with b: stat_card("Faktor #2", second["Faktor"], "⭐⭐ Cukup menentukan prediksi", "purple")
    with c: stat_card("Jumlah faktor", "8", "faktor dianalisis", "yellow")

    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig = plot_kepentingan(df_shap)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("02", "Ranking Lengkap", "URUTAN DARI YANG PALING PENTING")

    ranked = df_shap.sort_values("Kepentingan", ascending=False).reset_index(drop=True)
    for i, row in ranked.iterrows():
        pct = row["Kepentingan"] / ranked["Kepentingan"].max() * 100
        label_awam = terjemah_shap(row["Kepentingan"])
        st.markdown(f"""
        <div class="factor-card">
            <div class="factor-head">
                <div style="display:flex;align-items:center;gap:.7rem;">
                    <div class="rank-num">{i+1:02d}</div>
                    <div>
                        <div class="factor-name">{row['Faktor']}</div>
                        <div style="font-size:.7rem;color:#5C6B85;margin-top:.2rem;">{label_awam}</div>
                    </div>
                </div>
                <div class="factor-value" style="color:#2563EB;">{row['Kepentingan']:.4f}</div>
            </div>
            <div class="factor-bar">
                <div class="factor-fill fill-blue" style="width:{pct:.1f}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📌 Catatan Teknis (untuk peneliti / guru yang penasaran)"):
        st.markdown("""
        **Apa arti tingkat kepentingan?**

        Skor ini dihitung menggunakan metode **Mean |SHAP Value|** — sebuah cara
        untuk mengukur **seberapa sering faktor tertentu dipakai model** untuk
        memprediksi nilai siswa.

        **Cara membaca:**
        - ⭐⭐⭐ **Sangat menentukan** — faktor ini paling sering jadi penentu prediksi
        - ⭐⭐ **Cukup menentukan** — berpengaruh tapi bukan yang utama
        - ⭐ **Kurang menentukan** — kontribusinya kecil
        - ◦ **Hampir tidak menentukan** — model jarang pakai faktor ini

        **Untuk guru:** lihat label bintang di tiap kartu — itu versi bahasa sederhananya.

        **Beda dengan Modul 03?**
        - **Modul 03** → menjawab *"faktor apa yang MENYEBABKAN nilai naik/turun?"*
        - **Modul 04** → menjawab *"faktor apa yang paling DIPAKAI untuk memprediksi?"*
        """)

# ================================================================
# MODUL 05 — REKOMENDASI UMUM
# ================================================================

elif st.session_state.current_page == "rekomendasi":
    top_bar("💡 Rekomendasi Umum", "Modul 05 · Saran untuk tingkat sekolah")

    hero_header(
        "MODUL 05 · REKOMENDASI",
        "Dari analisis<br><span class='accent'>menjadi tindakan.</span>",
        "Ringkasan faktor yang dapat menjadi prioritas tindak lanjut untuk tingkat sekolah.",
        [("PRIORITAS", "yellow"), ("SEKOLAH", "mint"), ("TINDAK LANJUT", "blue")],
    )

    section_header("01", "Prioritas Intervensi", "FAKTOR DENGAN PENGARUH TERKUAT")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card card-mint">
            <div class="card-label">🟢 FAKTOR YANG PERLU DIPERKUAT</div>
            <div style="font-family:'Manrope';font-size:1.25rem;font-weight:800;margin-top:.45rem;">
                Faktor pendorong prestasi
            </div>
        """, unsafe_allow_html=True)
        positive_priority = [
            ("Fasilitas Sekolah", PENGARUH_DATA["Fasilitas Sekolah"], KEPENTINGAN_DATA["Fasilitas Sekolah"],
             "Evaluasi dan optimalkan fasilitas belajar yang paling relevan dengan kebutuhan siswa."),
            ("Keterlibatan Orang Tua", PENGARUH_DATA["Keterlibatan Orang Tua"], KEPENTINGAN_DATA["Keterlibatan Orang Tua"],
             "Perkuat komunikasi dan pendampingan belajar antara sekolah dan keluarga."),
            ("Self-Efficacy Akademik", PENGARUH_DATA["Self-Efficacy Akademik"], KEPENTINGAN_DATA["Self-Efficacy Akademik"],
             "Dorong kepercayaan diri akademik melalui mentoring dan pengalaman belajar bertahap."),
        ]
        for i, (name, ate, shap, desc) in enumerate(positive_priority, 1):
            label, _ = terjemah_ate(ate)
            st.markdown(f"""
            <div style="padding:1rem 0;border-bottom:1px solid #CBEBDD;">
                <div style="display:flex;justify-content:space-between;gap:.7rem;align-items:center;">
                    <div style="font-weight:800;font-size:.88rem;">{i:02d} · {name}</div>
                    <div style="font-weight:800;color:#10B981;font-size:.78rem;">{label}</div>
                </div>
                <div style="font-size:.69rem;color:#5C6B85;margin-top:.35rem;">{terjemah_shap(shap)}</div>
                <div style="font-size:.76rem;line-height:1.55;margin-top:.45rem;color:#475467;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card card-yellow">
            <div class="card-label">🔴 FAKTOR YANG PERLU DIEVALUASI</div>
            <div style="font-family:'Manrope';font-size:1.25rem;font-weight:800;margin-top:.45rem;">
                Faktor penghambat prestasi
            </div>
        """, unsafe_allow_html=True)
        negative_priority = [
            ("Dukungan Sekolah", PENGARUH_DATA["Dukungan Sekolah"], KEPENTINGAN_DATA["Dukungan Sekolah"],
             "Evaluasi bentuk pendampingan agar dukungan tetap membantu tanpa mengurangi kemandirian siswa."),
            ("Harapan Orang Tua", PENGARUH_DATA["Harapan Orang Tua"], KEPENTINGAN_DATA["Harapan Orang Tua"],
             "Dorong target akademik yang realistis dan komunikasi yang tidak menambah tekanan belajar."),
            ("Motivasi Belajar", PENGARUH_DATA["Motivasi Belajar"], KEPENTINGAN_DATA["Motivasi Belajar"],
             "Identifikasi hambatan belajar dan gunakan pendekatan pembelajaran yang lebih relevan."),
        ]
        for i, (name, ate, shap, desc) in enumerate(negative_priority, 1):
            label, _ = terjemah_ate(ate)
            st.markdown(f"""
            <div style="padding:1rem 0;border-bottom:1px solid #F1DF96;">
                <div style="display:flex;justify-content:space-between;gap:.7rem;align-items:center;">
                    <div style="font-weight:800;font-size:.88rem;">{i:02d} · {name}</div>
                    <div style="font-weight:800;color:#EF5B67;font-size:.78rem;">{label}</div>
                </div>
                <div style="font-size:.69rem;color:#5C6B85;margin-top:.35rem;">{terjemah_shap(shap)}</div>
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
            Gunakan hasil analisis sebab-akibat untuk memahami apa yang perlu diubah,
            dan hasil analisis kepentingan faktor untuk memahami apa yang paling menentukan.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# MODUL 06 — CATATAN UNTUK GURU
# ================================================================

else:
    top_bar("🎯 Catatan untuk Guru", "Modul 06 · Konsultasi personal per siswa")

    hero_header(
        "MODUL 06 · CATATAN UNTUK GURU",
        "Dari pemahaman<br><span class='accent'>menjadi tindakan kelas.</span>",
        "Kesimpulan sebab-akibat dan tindak lanjut personal yang bisa langsung dilakukan guru "
        "untuk membantu siswa tertentu.",
        [("PERSONAL", "blue"), ("PRAKTIS", "mint"), ("PER SISWA", "yellow")],
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

    section_header("02", "Kesimpulan Sebab-Akibat", "RINGKASAN UNTUK GURU")

    posisi = "di atas" if selisih_nilai >= 0 else "di bawah"
    abs_selisih = abs(selisih_nilai)

    if len(faktor_negatif) > 0:
        fn = faktor_negatif.iloc[0]
        narasi_negatif = f"""Faktor yang paling menekan nilai <b>{nama_siswa}</b> adalah <b style="color:#EF5B67;">{fn['Aspek']}</b> (kontribusi <b>{fn['Kontribusi']:.2f} poin</b>). Nilai siswa pada faktor ini adalah <b>{fn['Nilai_Siswa']:.2f}</b>, sedangkan rata-rata sekolah adalah <b>{fn['Baseline']:.2f}</b>."""
    else:
        narasi_negatif = "Tidak ada faktor yang secara signifikan menekan nilai siswa ini."

    if len(faktor_positif) > 0:
        fp = faktor_positif.iloc[0]
        narasi_positif = f"""Sementara itu, kekuatan utama <b>{nama_siswa}</b> terletak pada <b style="color:#10B981;">{fp['Aspek']}</b> (kontribusi <b>+{fp['Kontribusi']:.2f} poin</b>)."""
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
                <div style="color:#5C6B85;font-size:.8rem;">{kelas_siswa} · Absen {absen_siswa:02d} · Nilai {nilai_akademik:.2f}</div>
            </div>
        </div>
        <div style="font-size:.95rem;line-height:1.75;color:#1F2A44;">
            Nilai <b>{nama_siswa}</b> saat ini berada <b>{abs_selisih:.2f} poin {posisi} rata-rata sekolah</b>
            (rata-rata {RATA_RATA_NILAI:.2f}). Berdasarkan analisis sebab-akibat:
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
                    <div style="font-size:.7rem;color:#5C6B85;margin-bottom:.5rem;">{level}</div>
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
                            <div style="width:22px;height:22px;border-radius:6px;background:linear-gradient(135deg,#EAF1FF,#F1EDFF);color:#2563EB;
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
                            <div style="width:22px;height:22px;border-radius:6px;background:linear-gradient(135deg,#E8F8F1,#C9F2E0);color:#10B981;
                                        display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:800;flex-shrink:0;">
                                {j}
                            </div>
                            <div style="font-size:.82rem;line-height:1.55;color:#1F2A44;">{s}</div>
                        </div>
                        """, unsafe_allow_html=True)

    section_header("05", "Script Komunikasi", "CARA MENYAMPAIKAN KE SISWA / ORANG TUA")

    st.markdown(f"""
    <div class="card" style="border-left:5px solid #7C5CFC;">
        <div class="card-label">💬 UNTUK BERBICARA DENGAN SISWA</div>
        <div style="font-size:.88rem;line-height:1.8;color:#1F2A44;margin-top:.8rem;font-style:italic;">
            "<b>{nama_siswa}</b>, Ibu/Bapak sudah melihat hasil belajarmu.
            Ada hal positif yang Ibu/Bapak perhatikan:
            <b style="color:#10B981;">{faktor_positif.iloc[0]['Aspek'] if len(faktor_positif) > 0 else 'kamu sudah berusaha'}</b>.
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
    <div class="card" style="border-left:5px solid #F6C945;margin-top:1rem;">
        <div class="card-label">📞 UNTUK KOMUNIKASI DENGAN ORANG TUA</div>
        <div style="font-size:.88rem;line-height:1.8;color:#1F2A44;margin-top:.8rem;font-style:italic;">
            "Selamat siang Bapak/Ibu. Saya ingin berbagi tentang perkembangan
            <b>{nama_siswa}</b> di sekolah.
            <br><br>
            <b>Kabar baiknya:</b> {nama_siswa} menunjukkan kekuatan di
            <b style="color:#10B981;">{faktor_positif.iloc[0]['Aspek'] if len(faktor_positif) > 0 else 'semangat belajar'}</b>.
            <br><br>
            <b>Yang ingin saya diskusikan:</b> ada beberapa hal yang mungkin bisa kita bantu bersama,
            terutama di <b style="color:#EF5B67;">{prioritas.iloc[0]['Aspek'] if len(prioritas) > 0 else 'kebiasaan belajar'}</b>.
            <br><br>
            Kira-kira kapan waktu yang tepat untuk kita bicara lebih lanjut?"
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

    section_header("07", "Download Catatan", "SIMPAN UNTUK ARSIP GURU")

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
