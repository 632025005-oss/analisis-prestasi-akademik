# -*- coding: utf-8 -*-
# ================================================================
# SMART ACADEMIC ANALYTICS (SAA)
# Sub-brand: SIA.Prestasi - Magister Sains Data UKSW
# Hilirisasi penelitian Hybrid Causal-Explainable Machine Learning
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import hashlib
import json
import os

# ================================================================
# KONFIGURASI FILE
# ================================================================
DB_FILE     = "database_siswa.json"
CONFIG_FILE = "config_school.json"
LOG_FILE    = "log_aktivitas.json"

def _load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def _save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def load_database(): return _load_json(DB_FILE, [])
def save_database(d): _save_json(DB_FILE, d)
def load_config(): return _load_json(CONFIG_FILE, {
    "nama_sekolah": "SMP Negeri 6 Salatiga",
    "tahun_ajaran": "2025/2026",
    "semester": "Genap",
    "kepala_sekolah": "Kepala SMPN 6 Salatiga",
})
def save_config(c): _save_json(CONFIG_FILE, c)
def load_log(): return _load_json(LOG_FILE, [])
def save_log(l): _save_json(LOG_FILE, l)

st.set_page_config(
    page_title="SAA - Smart Academic Analytics | SMPN 6 Salatiga",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ================================================================
# VISUAL SYSTEM
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
    --navy:#0B1730;
}
html, body, [class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink);}
.stApp{
    background:
        radial-gradient(circle at 100% 0%, rgba(37,99,235,.07), transparent 32rem),
        radial-gradient(circle at 0% 100%, rgba(124,92,252,.06), transparent 32rem),
        #FFFFFF;
    background-attachment:fixed;
}
.main{background:transparent;}
.block-container{max-width:1480px;padding:1.6rem 2.7rem 4rem 2.7rem;}
#MainMenu, footer, header{visibility:hidden;}
h1,h2,h3,h4{font-family:'Manrope',sans-serif;}

@keyframes riseIn{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
@keyframes growBar{from{transform:scaleX(0);transform-origin:left;}to{transform:scaleX(1);transform-origin:left;}}
@keyframes floatDot{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
@keyframes softBounce{0%,100%{transform:translateY(0);}50%{transform:translateY(-4px);}}
@keyframes sparkle{0%,100%{opacity:.3;transform:scale(1);}50%{opacity:1;transform:scale(1.35);}}
@keyframes gradientShift{0%,100%{background-position:0% 50%;}50%{background-position:100% 50%;}}
.motion{animation:riseIn .5s ease both;}

/* ==== LOGIN ==== */
.login-page-header{display:flex;justify-content:space-between;align-items:center;padding:1rem 2rem;
    background:linear-gradient(135deg,#FFFFFF 0%,#F3F6FF 100%);border-bottom:1px solid #DCE4F2;
    margin:-1.6rem -2.7rem 0 -2.7rem;box-shadow:0 4px 20px rgba(37,99,235,.06);}
.login-logo-area{display:flex;align-items:center;gap:.8rem;justify-content:flex-end;width:100%;}
.login-logo-icon{font-size:2.2rem;line-height:1;filter:drop-shadow(0 4px 10px rgba(37,99,235,.3));}
.login-logo-text{text-align:right;line-height:1.15;}
.login-logo-title{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.6rem;font-weight:800;
    color:#0F1B33;letter-spacing:-.8px;}
.login-logo-title .blue-part{background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.login-logo-sub{font-size:.72rem;color:#5C6B85;letter-spacing:.3px;margin-top:.15rem;}
.login-content{max-width:1050px;margin:2rem auto;padding:0 2rem;}
.login-date-logout{display:flex;justify-content:space-between;align-items:center;padding:.9rem 1.1rem;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 100%);border:1px solid #DCE4F2;
    border-left:5px solid #2563EB;border-radius:12px;margin-bottom:2rem;
    box-shadow:0 6px 18px rgba(37,99,235,.06);}
.login-date{font-family:'Manrope',sans-serif;font-weight:800;font-size:.95rem;color:#0F1B33;}
.login-logout-link{font-size:.8rem;color:#2563EB;font-weight:700;padding:.35rem .8rem;border-left:1px solid #E4EAF2;}
.siasat-label{font-family:'DM Sans',sans-serif;font-weight:700;font-size:.9rem;color:#0F1B33;padding-top:.65rem;}
.siasat-input .stTextInput > div > div > input,
.siasat-input [data-baseweb="input"] > div,
.siasat-input [data-baseweb="base-input"]{
    border:1.5px solid #A8B5C7 !important;border-radius:8px !important;
    padding:.55rem .85rem !important;font-size:.9rem !important;
    background:linear-gradient(180deg,#FFFFFF 0%,#F9FBFF 100%) !important;
    min-height:42px !important;transition:all .2s ease !important;}
.siasat-input .stTextInput > div > div > input:focus{
    border-color:#2563EB !important;box-shadow:0 0 0 4px rgba(37,99,235,.15) !important;outline:none !important;}
.siasat-input .stTextInput > div > div > input::placeholder{color:#98A2B3 !important;font-style:italic;}
.siasat-input .stTextInput > label{display:none !important;}
.siasat-btn-login button{background:linear-gradient(135deg,#4ADE80 0%,#22C55E 50%,#16A34A 100%) !important;
    border:1px solid #16A34A !important;color:#fff !important;font-weight:700 !important;
    font-size:.9rem !important;padding:.55rem 2rem !important;border-radius:8px !important;
    min-height:44px !important;box-shadow:0 4px 14px rgba(22,163,74,.35) !important;
    transition:all .2s ease !important;text-transform:none !important;}
.siasat-btn-login button:hover{transform:translateY(-2px) !important;}
.siasat-btn-lupa button{background:linear-gradient(135deg,#F87171 0%,#EF4444 50%,#DC2626 100%) !important;
    border:1px solid #DC2626 !important;color:#fff !important;font-weight:700 !important;
    font-size:.9rem !important;padding:.55rem 2rem !important;border-radius:8px !important;
    min-height:44px !important;box-shadow:0 4px 14px rgba(220,38,38,.35) !important;
    transition:all .2s ease !important;text-transform:none !important;}
.siasat-btn-lupa button:hover{transform:translateY(-2px) !important;}
.siasat-info-box{background:linear-gradient(135deg,#FFF9E6 0%,#FFF4CC 100%);
    border:1px solid #F3DF8D;border-left:5px solid #F6C945;
    border-radius:12px;padding:1.2rem 1.4rem;margin-top:2.5rem;
    box-shadow:0 8px 22px rgba(246,201,69,.15);}
.siasat-info-header{display:flex;align-items:center;gap:.6rem;margin-bottom:.7rem;}
.siasat-info-icon{font-size:1.3rem;}
.siasat-info-title{font-family:'Manrope',sans-serif;font-weight:800;font-size:.9rem;color:#0F1B33;}
.siasat-info-list{font-size:.8rem;color:#475467;line-height:1.85;padding-left:.3rem;}
.siasat-info-list div{display:flex;gap:.5rem;}
.siasat-info-list .num{color:#2563EB;font-weight:800;flex-shrink:0;min-width:18px;}
.siasat-footer{text-align:center;padding:2rem 0;margin-top:3rem;
    border-top:1px solid #DCE4F2;font-size:.72rem;color:#5C6B85;line-height:1.8;}
.siasat-footer strong{color:#2563EB;font-weight:800;}
.siasat-alert-danger{background:linear-gradient(135deg,#FEF2F2 0%,#FEE2E2 100%);
    border:1px solid #FECACA;border-left:5px solid #EF4444;
    border-radius:10px;padding:.85rem 1.1rem;margin-top:1rem;animation:riseIn .3s ease both;}
.siasat-alert-danger-title{font-weight:800;font-size:.82rem;color:#991B1B;}
.siasat-alert-danger-body{font-size:.75rem;color:#7F1D1D;margin-top:.25rem;}
.siasat-alert-info{background:linear-gradient(135deg,#EFF6FF 0%,#DBEAFE 100%);
    border:1px solid #BFDBFE;border-left:5px solid #2563EB;
    border-radius:10px;padding:.85rem 1.1rem;margin-top:1rem;animation:riseIn .3s ease both;}
.siasat-alert-info-title{font-weight:800;font-size:.82rem;color:#1E40AF;}
.siasat-alert-info-body{font-size:.75rem;color:#1E3A8A;margin-top:.25rem;}

/* ==== HERO ==== */
.dashboard-hero{position:relative;overflow:hidden;
    background:radial-gradient(circle at 90% 10%, rgba(124,92,252,.12), transparent 25rem),
    linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 50%,#EEF3FF 100%);
    border:1px solid #DCE4F2;border-radius:28px;padding:2.3rem 2.5rem;
    box-shadow:0 20px 55px rgba(30,50,90,.10);animation:riseIn .5s ease both;}
.dashboard-hero:before{content:"";position:absolute;width:240px;height:240px;right:-90px;top:-100px;
    border:36px solid rgba(37,99,235,.09);border-radius:50%;}
.dashboard-hero:after{content:"";position:absolute;width:12px;height:12px;right:150px;bottom:45px;
    background:#F6C945;border-radius:50%;
    box-shadow:44px -24px 0 #2563EB,82px 10px 0 #10B981,118px -32px 0 #7C5CFC,
    152px 6px 0 #EC4899,186px -20px 0 #06B6D4;animation:floatDot 3s ease-in-out infinite;}

.menu-hero{position:relative;overflow:hidden;
    background:linear-gradient(135deg,#0B1730 0%,#16294A 30%,#1E3A8A 60%,#7C5CFC 100%);
    background-size:200% 200%;border-radius:32px;padding:3.5rem 3rem;color:#fff;margin-bottom:2.5rem;
    box-shadow:0 30px 80px rgba(11,23,48,.40),0 0 0 1px rgba(255,255,255,.06) inset;
    animation:riseIn .5s ease both, gradientShift 10s ease-in-out infinite;}
.menu-hero:before{content:"";position:absolute;width:500px;height:500px;border-radius:50%;
    border:70px solid rgba(246,201,69,.09);right:-220px;top:-200px;}
.menu-hero:after{content:"";position:absolute;width:14px;height:14px;right:220px;bottom:70px;
    background:#F6C945;border-radius:50%;
    box-shadow:52px -30px 0 #4F7CFF,100px 14px 0 #10B981,148px -38px 0 #7C5CFC,
    190px 10px 0 #EC4899,232px -22px 0 #06B6D4;animation:floatDot 3.5s ease-in-out infinite;}
.menu-hero-kicker{display:inline-flex;align-items:center;gap:8px;font-size:.7rem;font-weight:800;
    letter-spacing:2px;color:#F6C945;text-transform:uppercase;margin-bottom:1rem;}
.menu-hero-title{font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.5rem,5vw,4.5rem);line-height:.98;letter-spacing:-3px;font-weight:800;margin:0;max-width:900px;}
.menu-hero-title em{background:linear-gradient(135deg,#F6C945 0%,#FFA94D 50%,#F6C945 100%);
    background-size:200% 200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;font-style:italic;font-family:'Manrope',serif;
    animation:gradientShift 4s ease-in-out infinite;}
.menu-hero-sub{color:#C6D1E5;font-size:1.05rem;line-height:1.6;max-width:680px;margin:1.2rem 0 0;}
.menu-hero-meta{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.8rem;position:relative;z-index:1;}
.menu-hero-meta span{padding:.55rem .9rem;border-radius:999px;
    background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);
    color:#F0F5FF;font-size:.68rem;font-weight:800;letter-spacing:.7px;backdrop-filter:blur(10px);
    transition:all .2s ease;}
.menu-hero-meta span:hover{background:rgba(255,255,255,.22);transform:translateY(-2px);}

/* ==== MENU CARDS ==== */
.menu-card{position:relative;overflow:hidden;
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    border:1px solid #DCE4F2;border-radius:24px;padding:1.75rem 1.6rem 1.6rem;
    text-decoration:none;color:inherit;
    transition:transform .3s cubic-bezier(.2,.7,.3,1),box-shadow .3s ease,border-color .3s ease;
    box-shadow:0 14px 40px rgba(30,50,90,.08);min-height:230px;
    display:flex;flex-direction:column;justify-content:space-between;animation:riseIn .55s ease both;}
.menu-card:hover{transform:translateY(-8px);box-shadow:0 28px 65px rgba(30,50,90,.18);}
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
.menu-card-icon{width:56px;height:56px;border-radius:16px;display:flex;align-items:center;
    justify-content:center;font-size:1.7rem;margin:.9rem 0;box-shadow:0 6px 14px rgba(0,0,0,.06);
    transition:transform .3s ease;}
.menu-card:hover .menu-card-icon{transform:scale(1.08) rotate(-4deg);}
.menu-card.mc-blue .menu-card-icon{background:linear-gradient(135deg,#DBE7FF,#B8CEFF);color:#2563EB;}
.menu-card.mc-yellow .menu-card-icon{background:linear-gradient(135deg,#FFF1B8,#FFE37A);color:#936F00;}
.menu-card.mc-mint .menu-card-icon{background:linear-gradient(135deg,#C9F2E0,#9BE5C8);color:#087453;}
.menu-card.mc-purple .menu-card-icon{background:linear-gradient(135deg,#E2DBFF,#C9BEFF);color:#5B3FCC;}
.menu-card.mc-pink .menu-card-icon{background:linear-gradient(135deg,#FBD5E8,#F8AFD0);color:#BE185D;}
.menu-card.mc-teal .menu-card-icon{background:linear-gradient(135deg,#B6EFF6,#7FE0EC);color:#0E7490;}
.menu-card-title{font-family:'Manrope',sans-serif;font-size:1.15rem;font-weight:800;
    letter-spacing:-.4px;line-height:1.2;margin:0 0 .35rem;}
.menu-card-desc{color:var(--muted);font-size:.78rem;line-height:1.55;margin:0;}
.menu-card-cta{display:inline-flex;align-items:center;gap:.45rem;
    font-size:.72rem;font-weight:800;letter-spacing:.5px;margin-top:1rem;text-transform:uppercase;}
.menu-card.mc-blue .menu-card-cta{color:var(--blue);}
.menu-card.mc-yellow .menu-card-cta{color:#936F00;}
.menu-card.mc-mint .menu-card-cta{color:var(--mint);}
.menu-card.mc-purple .menu-card-cta{color:var(--violet);}
.menu-card.mc-pink .menu-card-cta{color:var(--pink);}
.menu-card.mc-teal .menu-card-cta{color:#0E7490;}

/* ==== SECTIONS ==== */
.section-wrap{margin-top:2rem;margin-bottom:1rem;}
.section-number{display:inline-flex;width:42px;height:42px;align-items:center;justify-content:center;
    border-radius:14px;background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 50%,#2563EB 100%);
    background-size:200% 200%;color:#fff;font-size:.8rem;font-weight:800;
    box-shadow:0 10px 24px rgba(37,99,235,.35);animation:gradientShift 4s ease-in-out infinite;}
.section-title{font-size:1.45rem;letter-spacing:-.7px;margin:0;}
.section-sub{color:var(--muted);font-size:.72rem;text-transform:uppercase;
    letter-spacing:1.1px;font-weight:800;margin-top:.2rem;}
.section-line{height:1px;background:linear-gradient(90deg,#DCE4F2 0%,transparent 100%);margin-top:.9rem;}

/* ==== CARDS ==== */
.card{background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    border:1px solid var(--line);border-radius:20px;padding:1.25rem 1.35rem;
    box-shadow:0 10px 30px rgba(30,50,90,.06);transition:transform .25s ease, box-shadow .25s ease;
    animation:riseIn .5s ease both;}
.card:hover{transform:translateY(-3px);box-shadow:0 20px 48px rgba(30,50,90,.12);border-color:#CFD9EA;}
.card-blue{background:linear-gradient(135deg,#FFFFFF 0%,#EAF1FF 100%);border-color:#D4E0FF;}
.card-yellow{background:linear-gradient(135deg,#FFFFFF 0%,#FFF7D6 100%);border-color:#F3DF8D;}
.card-mint{background:linear-gradient(135deg,#FFFFFF 0%,#E8F8F1 100%);border-color:#BCE8D7;}
.card-purple{background:linear-gradient(135deg,#FFFFFF 0%,#F1EDFF 100%);border-color:#DDD5FF;}
.card-dark{background:radial-gradient(circle at 100% 0%, rgba(124,92,252,.35), transparent 20rem),
    linear-gradient(135deg,#0B1730 0%,#16294A 100%);border-color:#0B1730;color:#fff;
    box-shadow:0 20px 50px rgba(11,23,48,.35);}
.card-label{font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:var(--muted);}
.card-dark .card-label{color:#9DBBFF;}
.card-value{font-family:'Manrope',sans-serif;font-size:2rem;font-weight:800;
    letter-spacing:-1.2px;line-height:1;margin-top:.5rem;}
.card-note{color:var(--muted);font-size:.74rem;margin-top:.45rem;}
.card-dark .card-note{color:#9DBBFF;}

.stat-card{min-height:122px;position:relative;overflow:hidden;}
.stat-card:after{content:"";position:absolute;width:90px;height:90px;border-radius:50%;
    right:-35px;bottom:-35px;background:radial-gradient(circle,rgba(37,99,235,.15),transparent 70%);}
.stat-card .topline{width:40px;height:5px;border-radius:99px;margin-bottom:.85rem;background-size:200% 200%;}
.topline.blue{background:linear-gradient(90deg,#2563EB,#7C5CFC,#2563EB);animation:gradientShift 4s ease-in-out infinite;}
.topline.yellow{background:linear-gradient(90deg,#F6C945,#FFA94D,#F6C945);animation:gradientShift 4s ease-in-out infinite;}
.topline.mint{background:linear-gradient(90deg,#10B981,#06B6D4,#10B981);animation:gradientShift 4s ease-in-out infinite;}
.topline.coral{background:linear-gradient(90deg,#EF5B67,#EC4899,#EF5B67);animation:gradientShift 4s ease-in-out infinite;}
.topline.purple{background:linear-gradient(90deg,#7C5CFC,#EC4899,#7C5CFC);animation:gradientShift 4s ease-in-out infinite;}

.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:.68rem;font-weight:800;
    letter-spacing:1.5px;text-transform:uppercase;color:var(--blue);margin-bottom:.7rem;}
.eyebrow-dot{width:8px;height:8px;background:var(--yellow);border-radius:50%;display:inline-block;
    animation:sparkle 2s ease-in-out infinite;}

.hero-title{font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.15rem,4vw,3.8rem);line-height:1.02;letter-spacing:-2.4px;margin:0;max-width:850px;}
.hero-title .accent{background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 50%,#EC4899 100%);
    background-size:200% 200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;animation:gradientShift 6s ease-in-out infinite;}
.hero-sub{color:var(--muted);font-size:.98rem;line-height:1.65;max-width:790px;margin:.9rem 0 0;}
.hero-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:1.25rem;}
.pill{display:inline-flex;align-items:center;gap:7px;padding:.42rem .7rem;border-radius:999px;
    font-size:.65rem;font-weight:800;letter-spacing:.5px;border:1px solid var(--line);background:#fff;}
.pill.blue{background:var(--blue-soft);color:var(--blue);border-color:#D4E0FF;}
.pill.yellow{background:var(--yellow-soft);color:#936F00;border-color:#F3DF8D;}
.pill.mint{background:var(--mint-soft);color:#087453;border-color:#BCE8D7;}
.pill.purple{background:var(--violet-soft);color:#5B3FCC;border-color:#DDD5FF;}
.pill.coral{background:var(--coral-soft);color:#B91C1C;border-color:#F4CDD3;}

.profile-card{display:flex;align-items:center;justify-content:space-between;gap:1rem;
    padding:1.15rem 1.3rem;background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 100%);
    border:1px solid #DCE4F2;border-radius:18px;box-shadow:0 8px 24px rgba(30,50,90,.05);}
.profile-avatar{width:48px;height:48px;border-radius:15px;display:flex;align-items:center;
    justify-content:center;background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 50%,#EC4899 100%);
    background-size:200% 200%;color:#fff;font-weight:800;font-size:1rem;
    box-shadow:0 8px 18px rgba(37,99,235,.3);animation:gradientShift 6s ease-in-out infinite;}
.profile-name{font-family:'Manrope',sans-serif;font-weight:800;font-size:1.05rem;}
.profile-meta{color:var(--muted);font-size:.72rem;margin-top:.2rem;}

.factor-card{border:1px solid var(--line);border-radius:18px;
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    padding:1rem 1.05rem;margin:.65rem 0;transition:all .25s ease;}
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

.rank-row{display:grid;grid-template-columns:34px 1fr auto;
    align-items:center;gap:.8rem;padding:.75rem 0;border-bottom:1px solid var(--line);}
.rank-row:last-child{border-bottom:0;}
.rank-num{width:30px;height:30px;border-radius:10px;
    background:linear-gradient(135deg,#EAF1FF 0%,#F1EDFF 100%);
    color:var(--blue);display:flex;align-items:center;justify-content:center;
    font-size:.68rem;font-weight:800;}
.rank-name{font-weight:700;font-size:.8rem;}
.rank-desc{font-size:.67rem;color:var(--muted);margin-top:.15rem;}
.rank-value{font-family:'Manrope',sans-serif;font-size:.86rem;font-weight:800;}
.positive{color:var(--mint);}
.negative{color:var(--coral);}

.stRadio > div{gap:.6rem;}
.stRadio [role="radiogroup"]{gap:.5rem;}
.stRadio [role="radiogroup"] label{background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    border:1.5px solid var(--line);border-radius:12px;padding:.65rem 1rem !important;
    transition:all .2s ease;font-weight:600 !important;cursor:pointer;}
.stRadio [role="radiogroup"] label:hover{border-color:var(--blue);
    background:linear-gradient(135deg,#FFFFFF 0%,#EAF1FF 100%);transform:translateY(-1px);}
.stRadio [role="radiogroup"] label[data-checked="true"]{border-color:var(--blue);
    background:linear-gradient(135deg,#EAF1FF 0%,#F1EDFF 100%);color:var(--blue);
    box-shadow:0 6px 16px rgba(37,99,235,.15);}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox [data-baseweb="select"] > div{
    background:linear-gradient(180deg,#FFFFFF 0%,#FBFDFF 100%) !important;
    border:1px solid #D7DFEA !important;border-radius:12px !important;
    min-height:43px;color:var(--ink) !important;transition:all .2s ease !important;}
.stTextInput label,.stNumberInput label,.stSelectbox label{
    font-size:.72rem !important;font-weight:800 !important;color:#475467 !important;}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus{
    border-color:var(--blue) !important;box-shadow:0 0 0 4px rgba(37,99,235,.12) !important;}

.stButton > button,.stDownloadButton > button{
    border-radius:12px !important;min-height:43px;font-weight:800 !important;
    border:1px solid #D7DFEA !important;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 100%) !important;
    transition:all .2s ease !important;color:#17233B !important;}
.stButton > button:hover,.stDownloadButton > button:hover{
    transform:translateY(-2px);box-shadow:0 10px 24px rgba(30,50,90,.12);
    border-color:#2563EB !important;}
button[kind="primary"]{background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 100%) !important;
    background-size:200% 200% !important;border-color:#2563EB !important;color:#fff !important;
    box-shadow:0 8px 20px rgba(37,99,235,.3) !important;
    animation:gradientShift 5s ease-in-out infinite;}
button[kind="primary"]:hover{box-shadow:0 12px 30px rgba(37,99,235,.45) !important;transform:translateY(-2px);}
button:disabled{opacity:.5 !important;cursor:not-allowed !important;}

[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:16px;overflow:hidden;
    box-shadow:0 10px 28px rgba(30,50,90,.06);}

.stTabs [data-baseweb="tab-list"]{gap:.5rem;background:transparent;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{height:44px;border-radius:12px 12px 0 0;
    background:transparent;font-weight:800;font-size:.82rem;color:#5C6B85;padding:0 1.2rem;}
.stTabs [data-baseweb="tab"]:hover{color:#2563EB;background:#F5F8FF;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#EAF1FF 0%,#F1EDFF 100%) !important;
    color:#2563EB !important;border-bottom:3px solid #2563EB !important;}

.info-box{border-radius:18px;padding:1.1rem 1.2rem;border:1px solid var(--line);
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);}
.info-box.blue{background:linear-gradient(135deg,#EAF1FF 0%,#DBE7FF 100%);border-color:#D5E1FF;}
.info-box.yellow{background:linear-gradient(135deg,#FFF7D6 0%,#FFF1B8 100%);border-color:#F1DF96;}
.info-box.mint{background:linear-gradient(135deg,#E8F8F1 0%,#C9F2E0 100%);border-color:#C5EBDD;}
.info-box.coral{background:linear-gradient(135deg,#FFF0F2 0%,#FFD9DF 100%);border-color:#F4CDD3;}
.info-title{font-weight:800;font-size:.9rem;}
.info-text{font-size:.78rem;line-height:1.6;margin-top:.35rem;color:#475467;}

.notif-success{background:linear-gradient(135deg,#ECFDF5 0%,#D1FAE5 60%,#A7F3D0 100%);
    border:2px solid #10B981;border-left:6px solid #10B981;
    border-radius:14px;padding:1.2rem 1.4rem;margin:1rem 0;animation:riseIn .5s ease both;
    box-shadow:0 10px 30px rgba(16,185,129,.2);}
.notif-success-title{font-family:'Manrope',sans-serif;font-weight:800;
    font-size:1rem;color:#065F46;display:flex;align-items:center;gap:.5rem;}
.notif-success-body{font-size:.85rem;color:#064E3B;line-height:1.6;margin-top:.4rem;}

.role-badge{display:inline-flex;align-items:center;gap:6px;padding:.35rem .75rem;
    border-radius:999px;font-size:.65rem;font-weight:800;letter-spacing:.5px;
    background:linear-gradient(135deg,#EAF1FF,#F1EDFF);color:#2563EB;border:1px solid #D4E0FF;}
.role-badge.admin{background:linear-gradient(135deg,#FCE7F3,#FBCFE8);color:#BE185D;border-color:#F8C7DF;}
.role-badge.kepala_sekolah{background:linear-gradient(135deg,#FEF3C7,#FDE68A);color:#92400E;border-color:#FCD34D;}
.role-badge.wali_kelas{background:linear-gradient(135deg,#D1FAE5,#A7F3D0);color:#065F46;border-color:#6EE7B7;}
.role-badge.guru{background:linear-gradient(135deg,#DBEAFE,#BFDBFE);color:#1E40AF;border-color:#93C5FD;}

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
# AUTHENTICATION & ROLES
# ================================================================
def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()

USERS = {
    "admin":  {"password": hash_password("admin123"),  "nama": "Administrator",       "role": "admin",          "kelas_ampu": None},
    "kepsek": {"password": hash_password("kepsek123"), "nama": "Kepala Sekolah",      "role": "kepala_sekolah", "kelas_ampu": None},
    "guru":   {"password": hash_password("guru123"),   "nama": "Guru SMPN 6",         "role": "guru",           "kelas_ampu": None},
    "wali":   {"password": hash_password("wali123"),   "nama": "Wali Kelas IX-A",     "role": "wali_kelas",     "kelas_ampu": ["IX-A"]},
    "regina": {"password": hash_password("regina2026"),"nama": "Regina Ria Aurellia", "role": "admin",          "kelas_ampu": None},
}

ROLE_LABEL = {
    "admin": "Administrator",
    "kepala_sekolah": "Kepala Sekolah",
    "wali_kelas": "Wali Kelas",
    "guru": "Guru",
}

def can_access_pengaturan(role): return role == "admin"

# ================================================================
# SESSION STATE
# ================================================================
for key, val in {
    "logged_in": False, "user_nama": None, "user_role": None, "user_kelas": None,
    "database_siswa": load_database(),
    "config": load_config(),
    "log": load_log(),
    "current_page": "home", "last_saved": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

def add_log(aksi, detail=""):
    entry = {
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": st.session_state.user_nama or "-",
        "role": st.session_state.user_role or "-",
        "aksi": aksi,
        "detail": detail,
    }
    st.session_state.log.insert(0, entry)
    st.session_state.log = st.session_state.log[:200]
    save_log(st.session_state.log)

# ================================================================
# DATA 8 FAKTOR
# ================================================================
BASELINE_ASPEK = {
    "Self-Efficacy Akademik": 4.63,
    "Keterlibatan Orang Tua": 3.51,
    "Harapan Orang Tua": 3.34,
    "Dukungan Sekolah": 4.60,
    "Motivasi Belajar": 3.34,
    "Kecemasan Akademik": 2.89,
    "Kemalasan Belajar": 1.49,
    "Fasilitas Sekolah": 4.88,
}
PENGARUH_DATA = {
    "Self-Efficacy Akademik": 2.1995,
    "Keterlibatan Orang Tua": 1.7559,
    "Harapan Orang Tua": -0.6987,
    "Dukungan Sekolah": -1.0351,
    "Motivasi Belajar": -1.9093,
    "Kecemasan Akademik": 0.7197,
    "Kemalasan Belajar": 0.7320,
    "Fasilitas Sekolah": 0.6182,
}
KEPENTINGAN_DATA = {
    "Self-Efficacy Akademik": 0.8197,
    "Keterlibatan Orang Tua": 0.6717,
    "Harapan Orang Tua": 0.5766,
    "Dukungan Sekolah": 0.4325,
    "Motivasi Belajar": 0.3601,
    "Kecemasan Akademik": 0.1553,
    "Fasilitas Sekolah": 0.0654,
    "Kemalasan Belajar": 0.0846,
}
BOBOT_PENGARUH = {k: PENGARUH_DATA[k] * KEPENTINGAN_DATA[k] for k in PENGARUH_DATA}
RATA_RATA_NILAI = 83.78
STD_NILAI = 3.64

KELAS_LIST = ([f"VII-{x}" for x in "ABCDEFGH"] + [f"VIII-{x}" for x in "ABCDEFGH"] + [f"IX-{x}" for x in "ABCDEFGH"])

SKALA_PILIHAN = {
    "Self-Efficacy Akademik": {"question": "Seberapa yakin siswa terhadap kemampuan akademiknya?", "options": [
        ("1","Hampir tidak pernah percaya diri"),("2","Jarang percaya diri"),
        ("3","Kadang-kadang percaya diri"),("4","Sering percaya diri"),("5","Hampir selalu percaya diri")]},
    "Keterlibatan Orang Tua": {"question": "Seberapa aktif orang tua mendampingi siswa belajar?", "options": [
        ("1","Hampir tidak pernah mendampingi"),("2","Jarang mendampingi"),
        ("3","Kadang-kadang mendampingi"),("4","Sering mendampingi"),("5","Hampir selalu mendampingi")]},
    "Harapan Orang Tua": {"question": "Seberapa tinggi tuntutan/ekspektasi orang tua terhadap nilai siswa?", "options": [
        ("1","Sangat rendah / tidak menuntut"),("2","Rendah"),("3","Sedang / wajar"),
        ("4","Tinggi"),("5","Sangat tinggi / menekan")]},
    "Dukungan Sekolah": {"question": "Seberapa besar dukungan & perhatian yang diberikan sekolah kepada siswa?", "options": [
        ("1","Sangat kurang / tidak diperhatikan"),("2","Kurang"),("3","Cukup"),
        ("4","Baik"),("5","Sangat baik / sangat diperhatikan")]},
    "Motivasi Belajar": {"question": "Seberapa besar motivasi & semangat belajar siswa?", "options": [
        ("1","Tidak ada motivasi / sangat malas"),("2","Kurang termotivasi"),("3","Cukup termotivasi"),
        ("4","Termotivasi"),("5","Sangat termotivasi / antusias")]},
    "Kecemasan Akademik": {"question": "Seberapa sering siswa merasa cemas / tertekan saat belajar atau ujian?", "options": [
        ("1","Hampir tidak pernah cemas"),("2","Jarang cemas"),("3","Kadang-kadang cemas"),
        ("4","Sering cemas"),("5","Hampir selalu cemas / sangat tertekan")]},
    "Fasilitas Sekolah": {"question": "Seberapa memadai fasilitas belajar yang tersedia di sekolah?", "options": [
        ("1","Sangat kurang memadai"),("2","Kurang memadai"),("3","Cukup memadai"),
        ("4","Memadai"),("5","Sangat memadai / lengkap")]},
    "Kemalasan Belajar": {"question": "Seberapa sering siswa menunjukkan sikap malas belajar?", "options": [
        ("1","Tidak pernah malas"),("2","Jarang malas"),("3","Kadang-kadang malas"),
        ("4","Sering malas"),("5","Hampir selalu malas")]},
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
    total = sum(kontribusi.values())
    if abs(total) > 0.01:
        skala = selisih_nilai / total
        kontribusi = {k: v * skala for k, v in kontribusi.items()}
    return selisih_nilai, kontribusi

def prediksi_nilai(profil_siswa):
    pred = RATA_RATA_NILAI
    for aspek, nilai in profil_siswa.items():
        pred += (nilai - BASELINE_ASPEK[aspek]) * PENGARUH_DATA[aspek] * 0.35
    return max(60, min(100, pred))

def potensi_maksimal(profil_siswa):
    optimum = dict(profil_siswa)
    for aspek in profil_siswa:
        if PENGARUH_DATA[aspek] > 0:
            optimum[aspek] = 5.0
        else:
            optimum[aspek] = 1.0
    return prediksi_nilai(optimum)

def kategori_nilai(nilai):
    if nilai >= 88: return "Sangat Baik", "#10B981", "▲"
    if nilai >= 84: return "Baik", "#2563EB", "●"
    if nilai >= 80: return "Cukup", "#F0B900", "◆"
    return "Perlu Perhatian", "#EF5B67", "▼"

def terjemah_ate(nilai):
    if nilai > 3: return "Sangat kuat MENINGKATKAN nilai", "#10B981"
    if nilai > 2: return "Kuat meningkatkan nilai", "#10B981"
    if nilai > 1: return "Sedang meningkatkan nilai", "#10B981"
    if nilai > 0.5: return "Sedikit meningkatkan nilai", "#10B981"
    if nilai >= -0.5: return "Hampir tidak berpengaruh", "#5C6B85"
    if nilai >= -1: return "Sedikit menurunkan nilai", "#EF5B67"
    if nilai >= -2: return "Sedang menurunkan nilai", "#EF5B67"
    if nilai >= -3: return "Kuat menurunkan nilai", "#EF5B67"
    return "Sangat kuat MENURUNKAN nilai", "#EF5B67"

def terjemah_shap(nilai):
    if nilai > 0.7: return "Sangat menentukan prediksi"
    if nilai > 0.4: return "Cukup menentukan prediksi"
    if nilai > 0.15: return "Kurang menentukan prediksi"
    return "Hampir tidak menentukan"

def goto_page(page):
    st.session_state.current_page = page
    st.session_state.last_saved = None
    st.rerun()

def section_header(num, title, subtitle):
    st.markdown(f"""
    <div class="section-wrap motion">
        <div style="display:flex;align-items:center;gap:.85rem;">
            <div class="section-number">{num}</div>
            <div><h2 class="section-title">{title}</h2><div class="section-sub">{subtitle}</div></div>
        </div>
        <div class="section-line"></div>
    </div>""", unsafe_allow_html=True)

def top_bar(page_title, page_sub):
    c1, c2, c3 = st.columns([3, 1.2, 1])
    with c1:
        role_cls = st.session_state.user_role or "guru"
        st.markdown(f"""
        <div style="padding:.3rem 0;">
            <div style="font-family:'Manrope';font-weight:800;font-size:1.05rem;color:#0F1B33;">{page_title}</div>
            <div style="color:#5C6B85;font-size:.72rem;margin-top:.15rem;">{page_sub}</div>
            <div style="margin-top:.5rem;">
                <span class="role-badge {role_cls}">{st.session_state.user_nama} - {ROLE_LABEL.get(role_cls,'')}</span>
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        if st.button("Menu Utama", use_container_width=True, key=f"home_{page_title}"):
            goto_page("home")
    with c3:
        if st.button("Logout", use_container_width=True, key=f"out_{page_title}"):
            add_log("Logout", st.session_state.user_nama or "")
            st.session_state.logged_in = False
            st.session_state.user_nama = None
            st.session_state.user_role = None
            st.session_state.current_page = "home"
            st.rerun()

def hero_header(eyebrow, title, subtitle, pills=None):
    pills = pills or []
    pills_html = "".join(f'<span class="pill {k}">{t}</span>' for t, k in pills)
    st.markdown(f"""
    <div class="dashboard-hero">
        <div class="eyebrow"><span class="eyebrow-dot"></span>{eyebrow}</div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-sub">{subtitle}</p>
        <div class="hero-meta">{pills_html}</div>
    </div>""", unsafe_allow_html=True)

def stat_card(label, value, note="", accent="blue"):
    st.markdown(f"""
    <div class="card stat-card">
        <div class="topline {accent}"></div>
        <div class="card-label">{label}</div>
        <div class="card-value">{value}</div>
        <div class="card-note">{note}</div>
    </div>""", unsafe_allow_html=True)

def notifikasi_simpan(nama, kelas):
    st.markdown(f"""
    <div class="notif-success">
        <div class="notif-success-title">Data Berhasil Disimpan</div>
        <div class="notif-success-body">
            Data siswa <b>{nama}</b> kelas <b>{kelas}</b> telah tersimpan.<br>
            Lanjutkan ke modul <b>Prediksi Prestasi</b> atau <b>Rekomendasi</b> untuk analisis.
        </div>
    </div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Lihat Prediksi", use_container_width=True, key="go_pred"): goto_page("prediksi")
    with c2:
        if st.button("Lihat Rekomendasi", use_container_width=True, key="go_rek"): goto_page("rekomendasi")
    with c3:
        if st.button("Input Siswa Lain", use_container_width=True, key="reset_form"):
            st.session_state.last_saved = None; st.rerun()

def plot_pengaruh(df):
    df = df.sort_values("Pengaruh", ascending=True)
    fig, ax = plt.subplots(figsize=(11, 6.3))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    vals = df["Pengaruh"].values; labels = df["Faktor"].values; y = np.arange(len(df))
    bars = ax.barh(y, vals, height=.58, color=["#EF5B67" if x < 0 else "#10B981" for x in vals], alpha=.9)
    ax.axvline(0, color="#0F1B33", linewidth=1.3)
    mx = max(abs(vals.min()), abs(vals.max())); pad = mx * .15
    ax.set_xlim(vals.min()-pad, vals.max()+pad)
    for bar, val in zip(bars, vals):
        off = mx*.04; ha = "left" if val >= 0 else "right"
        ax.text(val + (off if val>=0 else -off), bar.get_y()+bar.get_height()/2,
                f"{val:+.2f} poin", va="center", ha=ha, fontsize=9.5, fontweight="bold",
                color="#10B981" if val>=0 else "#EF5B67")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", labelsize=8, colors="#5C6B85")
    ax.grid(axis="x", alpha=.12, linewidth=.7); ax.set_axisbelow(True)
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8E0EB")
    ax.set_xlabel("<- MENURUNKAN nilai    |    MENINGKATKAN nilai ->",
                  fontsize=10, fontweight="bold", color="#5C6B85", labelpad=12)
    plt.tight_layout(); return fig

def plot_kepentingan(df):
    df = df.sort_values("Kepentingan", ascending=True)
    fig, ax = plt.subplots(figsize=(11, 6.3))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    vals = df["Kepentingan"].values; labels = df["Faktor"].values; y = np.arange(len(df))
    bars = ax.barh(y, vals, height=.58, color="#7C5CFC", alpha=.9)
    ax.set_xlim(0, max(vals)*1.18)
    for bar, val in zip(bars, vals):
        ax.text(val + max(vals)*.018, bar.get_y()+bar.get_height()/2,
                f"{val:.4f}", va="center", fontsize=9.5, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", labelsize=8, colors="#5C6B85")
    ax.grid(axis="x", alpha=.12, linewidth=.7); ax.set_axisbelow(True)
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8E0EB")
    ax.set_xlabel("Semakin panjang -> semakin penting untuk prediksi",
                  fontsize=10, fontweight="bold", color="#5C6B85", labelpad=12)
    plt.tight_layout(); return fig

def input_kategori(key_name, faktor_name):
    config = SKALA_PILIHAN[faktor_name]
    st.markdown(f"""
    <div style="margin-bottom:.5rem;">
        <div style="font-family:'Manrope';font-weight:800;font-size:.88rem;color:#0F1B33;">{faktor_name}</div>
        <div style="font-size:.72rem;color:#5C6B85;margin-top:.15rem;margin-bottom:.6rem;">{config['question']}</div>
    </div>""", unsafe_allow_html=True)
    labels = [o[1] for o in config["options"]]
    values = [float(o[0]) for o in config["options"]]
    default_idx = 2
    for i, v in enumerate(values):
        if abs(v - BASELINE_ASPEK[faktor_name]) < 0.5:
            default_idx = i; break
    pilihan = st.radio(f"{faktor_name}_radio", labels, index=default_idx,
                       key=key_name, label_visibility="collapsed")
    return values[labels.index(pilihan)]

def form_profil_siswa(prefix, default_nama="", default_kelas="IX-A", default_absen=1, default_nilai=83.78):
    c1, c2, c3 = st.columns([1.6, .8, .7])
    with c1: nama = st.text_input("Nama Siswa", value=default_nama, placeholder="Nama lengkap siswa", key=f"{prefix}_nama")
    with c2: kelas = st.selectbox("Kelas", KELAS_LIST, index=KELAS_LIST.index(default_kelas), key=f"{prefix}_kelas")
    with c3: absen = st.number_input("No. Absen", 1, 50, default_absen, key=f"{prefix}_absen")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        nilai = st.number_input("Nilai Rata-rata Rapor", min_value=60.0, max_value=100.0,
                                value=default_nilai, step=.01, format="%.2f",
                                help=f"Rata-rata sekolah: {RATA_RATA_NILAI:.2f}", key=f"{prefix}_nilai")
    with c2:
        gap = nilai - RATA_RATA_NILAI
        stat_card("Posisi Nilai", f"{gap:+.2f}",
                  f"poin - {'di atas' if gap>=0 else 'di bawah'} rata-rata",
                  "mint" if gap>=0 else "coral")
    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="card card-blue"><div class="card-label">FAKTOR INTERNAL</div>'
                    '<div style="color:#5C6B85;font-size:.72rem;margin-top:.25rem;">Kondisi dari dalam diri siswa.</div></div>',
                    unsafe_allow_html=True)
        se = input_kategori(f"{prefix}_in_se", "Self-Efficacy Akademik")
        mot = input_kategori(f"{prefix}_in_mot", "Motivasi Belajar")
        cem = input_kategori(f"{prefix}_in_cem", "Kecemasan Akademik")
        mal = input_kategori(f"{prefix}_in_mal", "Kemalasan Belajar")
    with right:
        st.markdown('<div class="card card-yellow"><div class="card-label">FAKTOR EKSTERNAL</div>'
                    '<div style="color:#5C6B85;font-size:.72rem;margin-top:.25rem;">Lingkungan keluarga & sekolah.</div></div>',
                    unsafe_allow_html=True)
        ket = input_kategori(f"{prefix}_ex_ket", "Keterlibatan Orang Tua")
        har = input_kategori(f"{prefix}_ex_har", "Harapan Orang Tua")
        duk = input_kategori(f"{prefix}_ex_duk", "Dukungan Sekolah")
        fas = input_kategori(f"{prefix}_ex_fas", "Fasilitas Sekolah")
    profil = {
        "Self-Efficacy Akademik": se, "Keterlibatan Orang Tua": ket,
        "Harapan Orang Tua": har, "Dukungan Sekolah": duk,
        "Motivasi Belajar": mot, "Kecemasan Akademik": cem,
        "Fasilitas Sekolah": fas, "Kemalasan Belajar": mal,
    }
    return nama, kelas, absen, nilai, profil

# ================================================================
# LOGIN
# ================================================================
def halaman_login():
    st.markdown("""
    <div class="login-page-header">
        <div></div>
        <div class="login-logo-area">
            <div class="login-logo-icon">🎓</div>
            <div class="login-logo-text">
                <div class="login-logo-title">SAA.<span class="blue-part">Analytics</span></div>
                <div class="login-logo-sub">Smart Academic Analytics - SMPN 6 Salatiga</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="login-content">', unsafe_allow_html=True)

    hari_ini = datetime.now()
    hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][hari_ini.weekday()]
    bulan = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus",
             "September","Oktober","November","Desember"][hari_ini.month-1]
    tanggal_str = f"{hari}, {hari_ini.day} {bulan} {hari_ini.year}"

    st.markdown(f"""
    <div class="login-date-logout">
        <div class="login-date">{tanggal_str}</div>
        <div class="login-logout-link">| Logout</div>
    </div>""", unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        col1, col2 = st.columns([1, 3])
        with col1: st.markdown('<div class="siasat-label" style="padding-top:.65rem;padding-left:.3rem;">Nama Pengguna</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="siasat-input">', unsafe_allow_html=True)
            u = st.text_input("u", placeholder="Masukkan nama pengguna", label_visibility="collapsed", key="lu")
            st.markdown('</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1: st.markdown('<div class="siasat-label" style="padding-top:.65rem;padding-left:.3rem;">Kata Sandi</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="siasat-input">', unsafe_allow_html=True)
            p = st.text_input("p", type="password", placeholder="Masukkan kata sandi", label_visibility="collapsed", key="lp")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:.5rem;"></div>', unsafe_allow_html=True)
        _, b1, b2, _ = st.columns([1,1,1,2])
        with b1:
            st.markdown('<div class="siasat-btn-login">', unsafe_allow_html=True)
            submit = st.form_submit_button("Login", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with b2:
            st.markdown('<div class="siasat-btn-lupa">', unsafe_allow_html=True)
            lupa = st.form_submit_button("Lupa Password", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        if submit:
            if u in USERS and USERS[u]["password"] == hash_password(p):
                st.session_state.logged_in = True
                st.session_state.user_nama = USERS[u]["nama"]
                st.session_state.user_role = USERS[u]["role"]
                st.session_state.user_kelas = USERS[u]["kelas_ampu"]
                st.session_state.current_page = "home"
                add_log("Login", f"{USERS[u]['nama']} ({USERS[u]['role']})")
                st.rerun()
            else:
                st.markdown("""<div class="siasat-alert-danger">
                    <div class="siasat-alert-danger-title">Login Gagal</div>
                    <div class="siasat-alert-danger-body">Nama pengguna atau kata sandi salah. Silakan coba lagi.</div>
                </div>""", unsafe_allow_html=True)
        if lupa:
            st.markdown("""<div class="siasat-alert-info">
                <div class="siasat-alert-info-title">Lupa Password</div>
                <div class="siasat-alert-info-body">
                    Hubungi Administrator sekolah untuk reset password.<br>
                    Email: admin@smpn6salatiga.sch.id
                </div></div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="siasat-info-box">
        <div class="siasat-info-header">
            <div class="siasat-info-icon">💡</div>
            <div class="siasat-info-title">Informasi Login</div>
        </div>
        <div class="siasat-info-list">
            <div><span class="num">1.</span><span>Gunakan akun resmi yang diberikan sekolah.</span></div>
            <div><span class="num">2.</span><span>Setiap role memiliki hak akses berbeda (Administrator, Kepala Sekolah, Wali Kelas, Guru).</span></div>
            <div><span class="num">3.</span><span>Jangan bagikan akun kepada orang lain.</span></div>
            <div><span class="num">4.</span><span>Logout setelah selesai menggunakan dashboard.</span></div>
            <div><span class="num">5.</span><span>Semua aktivitas tercatat dalam log sistem.</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    if os.environ.get("SHOW_DEMO_ACCOUNTS", "true").lower() == "true":
        with st.expander("Lihat Akun Demo (mode development)"):
            st.markdown("""
            | Username | Password | Role |
            |----------|----------|------|
            | `admin` | `admin123` | Administrator |
            | `kepsek` | `kepsek123` | Kepala Sekolah |
            | `wali` | `wali123` | Wali Kelas (IX-A) |
            | `guru` | `guru123` | Guru |
            | `regina` | `regina2026` | Peneliti |
            """)

    st.markdown("""
    <div class="siasat-footer">
        <strong>Smart Academic Analytics (SAA)</strong> - Sub-brand: SIA.Prestasi<br>
        Hilirisasi Penelitian Hybrid Causal-Explainable Machine Learning<br>
        Program Studi Magister Sains Data - Universitas Kristen Satya Wacana - 2026
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


if not st.session_state.logged_in:
    halaman_login()
    st.stop()

# ================================================================
# LANDING
# ================================================================
if st.session_state.current_page == "home":
    st.markdown("""
    <div class="menu-hero">
        <div class="menu-hero-kicker">SMART ACADEMIC ANALYTICS</div>
        <h1 class="menu-hero-title">
            Data-driven education.<br>
            <em>Bukan sekadar angka.</em>
        </h1>
        <p class="menu-hero-sub">
            SAA menggabungkan <b>causal inference</b> dan <b>explainable AI</b> untuk membantu guru
            memahami faktor yang membentuk prestasi akademik siswa SMP Negeri 6 Salatiga.
        </p>
        <div class="menu-hero-meta">
            <span>DATA-DRIVEN</span>
            <span>CAUSAL INFERENCE</span>
            <span>EXPLAINABLE AI</span>
            <span>6 MODUL</span>
            <span>SMPN 6 SALATIGA</span>
        </div>
    </div>""", unsafe_allow_html=True)

    role_cls = st.session_state.user_role or "guru"
    st.markdown(f"""
    <div class="profile-card" style="margin-bottom:2rem;">
        <div style="display:flex;align-items:center;gap:.85rem;">
            <div class="profile-avatar">{st.session_state.user_nama[0].upper()}</div>
            <div>
                <div class="profile-name">Halo, {st.session_state.user_nama}</div>
                <div class="profile-meta">
                    <span class="role-badge {role_cls}">{ROLE_LABEL.get(role_cls,'')}</span>
                    &nbsp;-&nbsp; Sesi aktif {datetime.now().strftime('%d %B %Y')}
                </div>
            </div>
        </div>
        <span class="pill mint">ONLINE</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-wrap motion">
        <div style="display:flex;align-items:center;gap:.85rem;">
            <div class="section-number">*</div>
            <div><h2 class="section-title">Modul Dashboard</h2>
            <div class="section-sub">PILIH UNTUK MEMULAI</div></div>
        </div>
        <div class="section-line"></div>
    </div>""", unsafe_allow_html=True)

    modules = [
        ("MODUL 01", "Profil Siswa", "Input data & lihat profil personal siswa berdasarkan 8 faktor determinan.", "mc-blue", "👤", "analisis", "Buka Profil"),
        ("MODUL 02", "Prediksi Prestasi", "Prediksi nilai akademik & potensi maksimal siswa berdasarkan model kausal.", "mc-purple", "📈", "prediksi", "Lihat Prediksi"),
        ("MODUL 03", "Faktor Pengaruh", "Faktor apa yang secara sebab-akibat & prediktif mempengaruhi prestasi?", "mc-mint", "🔬", "kausal", "Lihat Faktor"),
        ("MODUL 04", "Rekomendasi", "Rekomendasi intervensi tingkat sekolah & catatan personal untuk guru.", "mc-pink", "💡", "rekomendasi", "Lihat Rekomendasi"),
        ("MODUL 05", "Monitoring Kelas", "Pantau perkembangan akademik per kelas, identifikasi siswa yang perlu perhatian.", "mc-yellow", "📊", "monitoring", "Lihat Monitoring"),
        ("MODUL 06", "Pengaturan", "Manajemen akun, konfigurasi sekolah, dan log aktivitas sistem.", "mc-teal", "⚙️", "pengaturan", "Buka Pengaturan"),
    ]

    row1 = st.columns(3); row2 = st.columns(3)
    for i, (num, title, desc, color, icon, page, cta) in enumerate(modules):
        target_row = row1 if i < 3 else row2
        with target_row[i % 3]:
            st.markdown(f"""
            <div class="menu-card {color}">
                <div class="menu-card-num">{num}</div>
                <div class="menu-card-icon">{icon}</div>
                <div class="menu-card-title">{title}</div>
                <div class="menu-card-desc">{desc}</div>
                <div class="menu-card-cta">{cta} -></div>
            </div>""", unsafe_allow_html=True)
            disabled = (page == "pengaturan" and not can_access_pengaturan(st.session_state.user_role))
            if st.button(f"{title} ->", key=f"btn_{page}", use_container_width=True,
                         type="primary", disabled=disabled):
                goto_page(page)

    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="siasat-footer">
        <strong>Smart Academic Analytics (SAA)</strong> - SMP Negeri 6 Salatiga<br>
        Tahun Ajaran {st.session_state.config.get('tahun_ajaran','-')} - Semester {st.session_state.config.get('semester','-')}<br>
        2026 - Magister Sains Data UKSW
    </div>""", unsafe_allow_html=True)

# ================================================================
# MODUL 01 - PROFIL SISWA
# ================================================================
elif st.session_state.current_page == "analisis":
    top_bar("Profil Siswa", "Modul 01 - Input & profil personal siswa")

    hero_header(
        "MODUL 01 - PROFIL SISWA",
        "Kenali siswa.<br><span class='accent'>Pahami konteksnya.</span>",
        "Input data siswa, lihat profil personal berdasarkan 8 faktor determinan, "
        "dan bandingkan dengan rata-rata sekolah.",
        [("8 FAKTOR", "blue"), ("PROFIL PERSONAL", "mint"), ("PER SISWA", "yellow")],
    )

    if st.session_state.last_saved:
        notifikasi_simpan(st.session_state.last_saved["nama"], st.session_state.last_saved["kelas"])
        st.stop()

    section_header("01", "Input Data Siswa", "IDENTITAS & PROFIL 8 FAKTOR")
    st.markdown("""
    <div class="info-box blue" style="margin-bottom:1.5rem;">
        <div class="info-title">Cara Mengisi</div>
        <div class="info-text">
            Isi identitas siswa, nilai rapor, lalu pilih salah satu kondisi yang paling
            menggambarkan siswa untuk masing-masing faktor. Semua data langsung tersimpan
            di database setelah klik Simpan.
        </div>
    </div>""", unsafe_allow_html=True)

    nama, kelas, absen, nilai, profil = form_profil_siswa("m1")
    selisih, kontribusi = analisis_kausal(nilai, profil)
    kategori, warna_kategori, simbol = kategori_nilai(nilai)

    section_header("02", "Ringkasan Profil", "KONDISI SAAT INI")
    if nama:
        initials = "".join(x[0] for x in nama.split()[:2]).upper()
        st.markdown(f"""
        <div class="profile-card">
            <div style="display:flex;align-items:center;gap:.85rem;">
                <div class="profile-avatar">{initials}</div>
                <div>
                    <div class="profile-name">{nama}</div>
                    <div class="profile-meta">{kelas} - No. Absen {absen:02d}</div>
                </div>
            </div>
            <span class="pill blue">SUBJEK ANALISIS</span>
        </div>""", unsafe_allow_html=True)

    a, b, c, d = st.columns(4)
    with a: stat_card("Nilai Akademik", f"{nilai:.2f}", "nilai rata-rata rapor", "blue")
    with b: stat_card("Selisih Rata-rata", f"{selisih:+.2f}", "poin dari rata-rata sekolah",
                      "mint" if selisih>=0 else "coral")
    with c:
        accent = 'mint' if kategori=='Sangat Baik' else 'blue' if kategori=='Baik' else 'yellow' if kategori=='Cukup' else 'coral'
        st.markdown(f"""<div class="card stat-card"><div class="topline {accent}"></div>
            <div class="card-label">KATEGORI</div>
            <div class="card-value" style="font-size:1.55rem;color:{warna_kategori};">{kategori}</div>
            <div class="card-note">berdasarkan rentang nilai</div></div>""", unsafe_allow_html=True)
    with d:
        potensi = potensi_maksimal(profil)
        st.markdown(f"""<div class="card stat-card"><div class="topline purple"></div>
            <div class="card-label">POTENSI MAKSIMAL</div>
            <div class="card-value" style="color:#7C5CFC;font-size:1.55rem;">{potensi:.2f}</div>
            <div class="card-note">jika semua faktor dioptimalkan</div></div>""", unsafe_allow_html=True)

    section_header("03", "Profil vs Rata-rata Sekolah", "DETAIL PER FAKTOR")
    df = pd.DataFrame([
        {"Aspek": k, "Kontribusi": v, "Nilai_Siswa": profil[k],
         "Baseline": BASELINE_ASPEK[k], "Selisih": profil[k]-BASELINE_ASPEK[k]}
        for k, v in kontribusi.items()
    ]).sort_values("Kontribusi", key=abs, ascending=False)
    tabel = df.copy()
    tabel["Status"] = tabel["Selisih"].apply(lambda x: "Di atas" if x>0 else "Di bawah" if x<0 else "Sama")
    tabel = tabel[["Aspek","Nilai_Siswa","Baseline","Selisih","Kontribusi","Status"]]
    tabel.columns = ["Faktor","Nilai Siswa","Rata-rata","Selisih","Pengaruh (poin)","Status"]
    st.dataframe(tabel, use_container_width=True, hide_index=True, column_config={
        "Nilai Siswa": st.column_config.NumberColumn(format="%.2f"),
        "Rata-rata": st.column_config.NumberColumn(format="%.2f"),
        "Selisih": st.column_config.NumberColumn(format="%+.2f"),
        "Pengaruh (poin)": st.column_config.NumberColumn(format="%+.2f"),
    })

    section_header("04", "Simpan Data", "ARSIPKAN HASIL ANALISIS")
    if not nama:
        st.markdown("""<div class="info-box yellow"><div class="info-title">Data belum siap disimpan</div>
            <div class="info-text">Isi nama siswa terlebih dahulu.</div></div>""", unsafe_allow_html=True)
    else:
        dup = False; dup_absen = None
        for s in st.session_state.database_siswa:
            ns = s["Nama"].strip().lower() == nama.strip().lower()
            ks = s["Kelas"] == kelas; abs_ = int(s["Absen"]) == int(absen)
            if ns and ks and abs_: dup = True; break
            elif ks and abs_ and not ns: dup_absen = s["Nama"]

        if dup:
            st.markdown(f"""<div class="info-box coral"><div class="info-title">Data sudah ada</div>
                <div class="info-text">Siswa <b>{nama}</b> kelas <b>{kelas}</b> absen <b>{absen:02d}</b> sudah tersimpan.</div></div>""",
                unsafe_allow_html=True)
        elif dup_absen:
            st.markdown(f"""<div class="info-box coral"><div class="info-title">Nomor absen sudah dipakai</div>
                <div class="info-text">Di kelas <b>{kelas}</b>, absen <b>{absen:02d}</b> sudah dipakai oleh <b>{dup_absen}</b>.</div></div>""",
                unsafe_allow_html=True)
        else:
            if st.button("Simpan Hasil Siswa", type="primary", use_container_width=True):
                data = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nama": nama, "Kelas": kelas, "Absen": absen,
                    "Nilai Akademik": round(nilai,2),
                    "Selisih": round(selisih,2), "Kategori": kategori,
                    "Self-Efficacy": profil["Self-Efficacy Akademik"],
                    "Keterlibatan Ortu": profil["Keterlibatan Orang Tua"],
                    "Harapan Ortu": profil["Harapan Orang Tua"],
                    "Dukungan Sekolah": profil["Dukungan Sekolah"],
                    "Motivasi": profil["Motivasi Belajar"],
                    "Kecemasan": profil["Kecemasan Akademik"],
                    "Fasilitas": profil["Fasilitas Sekolah"],
                    "Kemalasan": profil["Kemalasan Belajar"],
                    "Dicatat Oleh": st.session_state.user_nama,
                }
                st.session_state.database_siswa.append(data)
                save_database(st.session_state.database_siswa)
                add_log("Input siswa", f"{nama} ({kelas})")
                st.session_state.last_saved = {"nama": nama, "kelas": kelas, "absen": absen}
                st.rerun()

# ================================================================
# MODUL 02 - PREDIKSI PRESTASI
# ================================================================
elif st.session_state.current_page == "prediksi":
    top_bar("Prediksi Prestasi", "Modul 02 - Prediksi nilai & potensi siswa")

    hero_header(
        "MODUL 02 - PREDIKSI PRESTASI",
        "Lihat ke depan.<br><span class='accent'>Bukan hanya saat ini.</span>",
        "Prediksi nilai akademik siswa berdasarkan model kausal (Structural Causal Model) "
        "dan perbandingan antara kondisi saat ini dengan potensi maksimalnya.",
        [("PREDIKSI", "purple"), ("CAUSAL MODEL", "blue"), ("POTENSI", "mint")],
    )

    if len(st.session_state.database_siswa) == 0:
        st.warning("Database masih kosong. Input siswa terlebih dahulu di Modul 01 - Profil Siswa.")
        st.stop()

    section_header("01", "Pilih Siswa", "DARI DATABASE ATAU INPUT MANUAL")
    opsi_sumber = st.radio("Sumber data siswa", ["Ambil dari database", "Input manual"], horizontal=True)

    if opsi_sumber == "Ambil dari database":
        df_db = pd.DataFrame(st.session_state.database_siswa)
        opsi = df_db.apply(lambda x: f"{x['Nama']} - {x['Kelas']} (Absen {x['Absen']})", axis=1).tolist()
        pilihan = st.selectbox("Pilih Siswa", opsi, key="pred_pilih")
        idx = opsi.index(pilihan); b = df_db.iloc[idx]
        nama = b["Nama"]; kelas = b["Kelas"]; absen = int(b["Absen"])
        nilai = float(b["Nilai Akademik"])
        profil = {
            "Self-Efficacy Akademik": float(b["Self-Efficacy"]),
            "Keterlibatan Orang Tua": float(b["Keterlibatan Ortu"]),
            "Harapan Orang Tua": float(b["Harapan Ortu"]),
            "Dukungan Sekolah": float(b["Dukungan Sekolah"]),
            "Motivasi Belajar": float(b["Motivasi"]),
            "Kecemasan Akademik": float(b["Kecemasan"]),
            "Fasilitas Sekolah": float(b["Fasilitas"]),
            "Kemalasan Belajar": float(b["Kemalasan"]),
        }
    else:
        nama, kelas, absen, nilai, profil = form_profil_siswa("m2")

    pred = prediksi_nilai(profil)
    potensi = potensi_maksimal(profil)
    kategori, warna_kategori, simbol = kategori_nilai(nilai)
    kat_pred, warna_pred, simbol_pred = kategori_nilai(pred)

    section_header("02", "Hasil Prediksi", "NILAI SAAT INI VS PREDIKSI VS POTENSI")

    a, b_, c = st.columns(3)
    with a:
        st.markdown(f"""<div class="card stat-card"><div class="topline blue"></div>
            <div class="card-label">NILAI SAAT INI</div>
            <div class="card-value" style="color:#2563EB;">{nilai:.2f}</div>
            <div class="card-note">nilai rata-rata rapor</div></div>""", unsafe_allow_html=True)
    with b_:
        delta = pred - nilai
        st.markdown(f"""<div class="card stat-card"><div class="topline purple"></div>
            <div class="card-label">PREDIKSI NILAI</div>
            <div class="card-value" style="color:#7C5CFC;">{pred:.2f}</div>
            <div class="card-note">{delta:+.2f} poin dari nilai saat ini</div></div>""", unsafe_allow_html=True)
    with c:
        gap = potensi - nilai
        st.markdown(f"""<div class="card stat-card"><div class="topline mint"></div>
            <div class="card-label">POTENSI MAKSIMAL</div>
            <div class="card-value" style="color:#10B981;">{potensi:.2f}</div>
            <div class="card-note">{gap:+.2f} poin - jika faktor dioptimalkan</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div class="card" style="border-left:5px solid {warna_pred};">
        <div class="card-label">INTERPRETASI PREDIKSI</div>
        <div style="font-family:'Manrope';font-size:1.15rem;font-weight:800;margin-top:.5rem;">
            Nilai prediksi: <span style="color:{warna_pred};">{kat_pred}</span> ({pred:.2f})
        </div>
        <div style="font-size:.85rem;line-height:1.7;color:#475467;margin-top:.6rem;">
            Berdasarkan profil 8 faktor siswa saat ini, model kausal memprediksi nilai akademik sekitar
            <b>{pred:.2f}</b>. Ini adalah estimasi berbasis <i>backdoor linear regression</i>
            (Structural Causal Model) menggunakan nilai ATE 8 faktor.<br><br>
            Rentang kepercayaan: <b>+/- {STD_NILAI:.2f} poin</b>, yaitu sekitar
            <b>{max(0,pred-STD_NILAI):.2f} hingga {min(100,pred+STD_NILAI):.2f}</b>.<br><br>
            Jika seluruh faktor positif dimaksimalkan dan faktor negatif diminimalkan,
            siswa berpotensi mencapai <b style="color:#10B981;">{potensi:.2f}</b>
            (selisih <b>+{potensi-nilai:.2f}</b> dari nilai saat ini).
        </div>
    </div>""", unsafe_allow_html=True)

    section_header("03", "Visualisasi Trajectory", "POSISI RELATIF")
    fig, ax = plt.subplots(figsize=(10, 3.6))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    posisi = [nilai, pred, potensi]
    labels = ["Nilai Sekarang", "Prediksi", "Potensi Max"]
    colors = ["#2563EB", "#7C5CFC", "#10B981"]
    bars = ax.barh([0,1,2], posisi, height=.5, color=colors, alpha=.85)
    for i, (p, lab) in enumerate(zip(posisi, labels)):
        ax.text(p + 0.5, i, f"{p:.2f}", va="center", fontsize=11, fontweight="bold", color=colors[i])
    ax.axvline(RATA_RATA_NILAI, color="#EF5B67", linestyle="--", alpha=.6, linewidth=1.5)
    ax.text(RATA_RATA_NILAI, 2.6, f"Rata-rata sekolah ({RATA_RATA_NILAI:.2f})",
            color="#EF5B67", fontsize=9, fontweight="bold", ha="center")
    ax.set_yticks([0,1,2]); ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlim(60, 100); ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", alpha=.15); ax.set_axisbelow(True)
    for s in ["top","right","left"]: ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#D8E0EB")
    ax.set_xlabel("Nilai Akademik (skala 60-100)", fontsize=9.5, color="#5C6B85", labelpad=8)
    plt.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

    with st.expander("Catatan Teknis Prediksi"):
        st.markdown(f"""
        **Bagaimana prediksi dihitung?**

        Prediksi menggunakan **Structural Causal Model (SCM)** dengan pendekatan
        *backdoor linear regression*:
Prediksi = Rata-rata + Sigma (nilai_faktor - baseline) x ATE_faktor x faktor_skala

text

- **ATE** = *Average Treatment Effect* (efek kausal) tiap faktor
- **baseline** = rata-rata sekolah per faktor
- **faktor_skala** = 0.35 (koefisien konservatif dari hasil validasi model)

**Bukan prediksi langsung dari Random Forest**, melainkan prediksi kausal
yang menjelaskan *mengapa* nilai diprediksi demikian.

**Rentang kepercayaan** +/- {STD_NILAI:.2f} poin diambil dari simpangan baku nilai
akademik di penelitian (n=117 siswa).
""")

# ================================================================
# MODUL 03 - FAKTOR PENGARUH
# ================================================================
elif st.session_state.current_page == "kausal":
top_bar("Faktor Pengaruh", "Modul 03 - Sebab-akibat & kepentingan prediktif")

hero_header(
"MODUL 03 - FAKTOR PENGARUH",
"Apa yang <em>menyebabkan</em><br>dan apa yang <em>memprediksi</em>?",
"Analisis sebab-akibat (ATE) dan tingkat kepentingan prediktif (SHAP) untuk 8 faktor "
"yang mempengaruhi prestasi akademik siswa.",
[("CAUSAL - ATE", "blue"), ("PREDICTIVE - SHAP", "purple"), ("TINGKAT SEKOLAH", "mint")],
)

section_header("01", "Apa Bedanya?", "DUA JENIS PENGARUH")
st.markdown("""
<div class="info-box blue" style="margin-bottom:1rem;">
<div class="info-title">Perbedaan Mendasar</div>
<div class="info-text">
    <b>Sebab-Akibat (ATE)</b> menjawab: <i>"Jika faktor X diubah, apakah nilai siswa berubah?"</i><br>
    <b>Kepentingan Prediktif (SHAP)</b> menjawab: <i>"Faktor apa yang paling dipakai model untuk memprediksi?"</i>
    <br><br>
    Keduanya <b>berbeda</b>: faktor bisa penting untuk prediksi tapi bukan penyebab (dan sebaliknya).
</div>
</div>""", unsafe_allow_html=True)

tab_ate, tab_shap = st.tabs(["Sebab-Akibat (ATE)", "Kepentingan Prediktif (SHAP)"])

with tab_ate:
df_ate = pd.DataFrame([{"Faktor": k, "Pengaruh": v} for k, v in PENGARUH_DATA.items()])
pos_ate = df_ate[df_ate["Pengaruh"]>0].sort_values("Pengaruh", ascending=False)
neg_ate = df_ate[df_ate["Pengaruh"]<0].sort_values("Pengaruh")

a, b_, c = st.columns(3)
with a:
    t = pos_ate.iloc[0]
    stat_card("Paling MENINGKATKAN", t["Faktor"], f"skor +{t['Pengaruh']:.2f}", "mint")
with b_:
    t = neg_ate.iloc[0]
    stat_card("Paling MENURUNKAN", t["Faktor"], f"skor {t['Pengaruh']:.2f}", "coral")
with c: stat_card("Jumlah faktor", "8", "variabel dianalisis", "blue")

st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.pyplot(plot_pengaruh(df_ate), use_container_width=True); plt.close()
st.markdown("</div>", unsafe_allow_html=True)

tabel_ate = df_ate.copy()
tabel_ate["Penjelasan"] = tabel_ate["Pengaruh"].apply(lambda x: terjemah_ate(x)[0])
tabel_ate["Arah"] = tabel_ate["Pengaruh"].apply(lambda x: "MENINGKATKAN" if x>0 else "MENURUNKAN" if x<0 else "NETRAL")
tabel_ate = tabel_ate.sort_values("Pengaruh", ascending=False)[["Faktor","Penjelasan","Arah","Pengaruh"]]
tabel_ate.columns = ["Faktor","Artinya untuk Nilai Siswa","Arah","Skor ATE"]
st.dataframe(tabel_ate, use_container_width=True, hide_index=True,
             column_config={"Skor ATE": st.column_config.NumberColumn(format="%+.4f")})

with tab_shap:
df_shap = pd.DataFrame([{"Faktor": k, "Kepentingan": v} for k, v in KEPENTINGAN_DATA.items()])
ranked = df_shap.sort_values("Kepentingan", ascending=False).reset_index(drop=True)
a, b_, c = st.columns(3)
with a: stat_card("Faktor #1", ranked.iloc[0]["Faktor"], "Sangat menentukan", "purple")
with b_: stat_card("Faktor #2", ranked.iloc[1]["Faktor"], "Cukup menentukan", "blue")
with c: stat_card("Jumlah faktor", "8", "faktor dianalisis", "yellow")

st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.pyplot(plot_kepentingan(df_shap), use_container_width=True); plt.close()
st.markdown("</div>", unsafe_allow_html=True)

for i, row in ranked.iterrows():
    pct = row["Kepentingan"] / ranked["Kepentingan"].max() * 100
    label = terjemah_shap(row["Kepentingan"])
    st.markdown(f"""
    <div class="factor-card">
        <div class="factor-head">
            <div style="display:flex;align-items:center;gap:.7rem;">
                <div class="rank-num">{i+1:02d}</div>
                <div>
                    <div class="factor-name">{row['Faktor']}</div>
                    <div style="font-size:.7rem;color:#5C6B85;margin-top:.2rem;">{label}</div>
                </div>
            </div>
            <div class="factor-value" style="color:#7C5CFC;">{row['Kepentingan']:.4f}</div>
        </div>
        <div class="factor-bar"><div class="factor-fill fill-purple" style="width:{pct:.1f}%"></div></div>
    </div>""", unsafe_allow_html=True)

with st.expander("Catatan Teknis"):
st.markdown("""
**ATE (Average Treatment Effect)** dihitung dengan DoWhy library - Structural Causal Model
dengan backdoor linear regression. Nilai positif = meningkatkan nilai, negatif = menurunkan.

**SHAP (SHapley Additive exPlanations)** menggunakan TreeExplainer pada model Random Forest
(n_estimators=100, max_depth=7). Nilai mean |SHAP| menunjukkan seberapa sering faktor
dipakai model untuk prediksi.

**Catatan penting**: SHAP bukan kausal. Nilai SHAP hanya menunjukkan kontribusi prediktif.
Arah sebab-akibat tetap mengacu pada ATE dan DAG.
""")

# ================================================================
# MODUL 04 - REKOMENDASI
# ================================================================
elif st.session_state.current_page == "rekomendasi":
top_bar("Rekomendasi", "Modul 04 - Intervensi tingkat sekolah & personal")

hero_header(
"MODUL 04 - REKOMENDASI",
"Dari analisis<br><span class='accent'>menjadi tindakan.</span>",
"Rekomendasi intervensi tingkat sekolah berdasarkan CEI & kuadran prioritas, "
"serta catatan personal untuk guru per siswa.",
[("PRIORITAS", "yellow"), ("SEKOLAH", "mint"), ("PERSONAL", "blue")],
)

tab_umum, tab_personal = st.tabs(["Rekomendasi Umum (Tingkat Sekolah)", "Catatan untuk Guru (Personal)"])

with tab_umum:
section_header("01", "Prioritas Intervensi", "FAKTOR DENGAN PENGARUH TERKUAT")
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="card card-mint">
        <div class="card-label">FAKTOR YANG PERLU DIPERKUAT</div>
        <div style="font-family:'Manrope';font-size:1.25rem;font-weight:800;margin-top:.45rem;">
            Faktor pendorong prestasi</div>""", unsafe_allow_html=True)
    pos_priority = [
        ("Self-Efficacy Akademik", "Dorong kepercayaan diri akademik melalui mentoring, apresiasi proses, dan pengalaman belajar bertahap."),
        ("Keterlibatan Orang Tua", "Perkuat komunikasi dan pendampingan belajar antara sekolah dan keluarga."),
        ("Kemalasan Belajar", "Meskipun efeknya positif, tetap pantau agar siswa tidak terjebak pola belajar pasif."),
    ]
    for i, (name, desc) in enumerate(pos_priority, 1):
        ate = PENGARUH_DATA[name]; label, _ = terjemah_ate(ate)
        st.markdown(f"""<div style="padding:1rem 0;border-bottom:1px solid #CBEBDD;">
            <div style="display:flex;justify-content:space-between;gap:.7rem;">
                <div style="font-weight:800;font-size:.88rem;">{i:02d} - {name}</div>
                <div style="font-weight:800;color:#10B981;font-size:.78rem;">{label}</div>
            </div>
            <div style="font-size:.69rem;color:#5C6B85;margin-top:.35rem;">{terjemah_shap(KEPENTINGAN_DATA[name])}</div>
            <div style="font-size:.76rem;line-height:1.55;margin-top:.45rem;color:#475467;">{desc}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="card card-yellow">
        <div class="card-label">FAKTOR YANG PERLU DIEVALUASI</div>
        <div style="font-family:'Manrope';font-size:1.25rem;font-weight:800;margin-top:.45rem;">
            Faktor penghambat prestasi</div>""", unsafe_allow_html=True)
    neg_priority = [
        ("Motivasi Belajar", "Identifikasi hambatan belajar, kaitkan materi dengan kehidupan nyata, berikan pilihan tugas."),
        ("Dukungan Sekolah", "Evaluasi bentuk pendampingan agar tidak mengurangi kemandirian siswa (over-support)."),
        ("Harapan Orang Tua", "Dorong target akademik yang realistis dan komunikasi yang tidak menambah tekanan."),
    ]
    for i, (name, desc) in enumerate(neg_priority, 1):
        ate = PENGARUH_DATA[name]; label, _ = terjemah_ate(ate)
        st.markdown(f"""<div style="padding:1rem 0;border-bottom:1px solid #F1DF96;">
            <div style="display:flex;justify-content:space-between;gap:.7rem;">
                <div style="font-weight:800;font-size:.88rem;">{i:02d} - {name}</div>
                <div style="font-weight:800;color:#EF5B67;font-size:.78rem;">{label}</div>
            </div>
            <div style="font-size:.69rem;color:#5C6B85;margin-top:.35rem;">{terjemah_shap(KEPENTINGAN_DATA[name])}</div>
            <div style="font-size:.76rem;line-height:1.55;margin-top:.45rem;color:#475467;">{desc}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.markdown("""<div class="card card-dark">
    <div class="card-label">CATATAN PENELITIAN</div>
    <div style="font-family:'Manrope';font-size:1.35rem;line-height:1.25;font-weight:800;margin-top:.7rem;">
        Gunakan hasil sebab-akibat untuk memahami <i>apa yang perlu diubah</i>,
        dan hasil kepentingan prediktif untuk memahami <i>apa yang paling menentukan</i>.
    </div></div>""", unsafe_allow_html=True)

with tab_personal:
if len(st.session_state.database_siswa) == 0:
    st.warning("Database masih kosong. Input siswa terlebih dahulu di Modul 01.")
else:
    df_db = pd.DataFrame(st.session_state.database_siswa)
    opsi = df_db.apply(lambda x: f"{x['Nama']} - {x['Kelas']} (Absen {x['Absen']})", axis=1).tolist()
    pilihan = st.selectbox("Pilih Siswa", opsi, key="rek_pilih")
    idx = opsi.index(pilihan); b = df_db.iloc[idx]

    nama = b["Nama"]; kelas = b["Kelas"]; absen = int(b["Absen"]); nilai = float(b["Nilai Akademik"])
    profil = {
        "Self-Efficacy Akademik": float(b["Self-Efficacy"]),
        "Keterlibatan Orang Tua": float(b["Keterlibatan Ortu"]),
        "Harapan Orang Tua": float(b["Harapan Ortu"]),
        "Dukungan Sekolah": float(b["Dukungan Sekolah"]),
        "Motivasi Belajar": float(b["Motivasi"]),
        "Kecemasan Akademik": float(b["Kecemasan"]),
        "Fasilitas Sekolah": float(b["Fasilitas"]),
        "Kemalasan Belajar": float(b["Kemalasan"]),
    }
    selisih, kontribusi = analisis_kausal(nilai, profil)
    kategori, warna_kategori, simbol = kategori_nilai(nilai)

    df_k = pd.DataFrame([
        {"Aspek": k, "Kontribusi": v, "Nilai_Siswa": profil[k],
         "Baseline": BASELINE_ASPEK[k], "Selisih": profil[k]-BASELINE_ASPEK[k]}
        for k, v in kontribusi.items()
    ]).sort_values("Kontribusi")
    neg = df_k[df_k["Kontribusi"] < -0.2].sort_values("Kontribusi")
    pos = df_k[df_k["Kontribusi"] > 0.2].sort_values("Kontribusi", ascending=False)

    posisi = "di atas" if selisih >= 0 else "di bawah"
    fn = neg.iloc[0] if len(neg) > 0 else None
    fp = pos.iloc[0] if len(pos) > 0 else None
    narasi_neg = (f"Faktor yang paling menekan nilai <b>{nama}</b> adalah "
                  f"<b style='color:#EF5B67;'>{fn['Aspek']}</b> (kontribusi {fn['Kontribusi']:.2f} poin). "
                  f"Nilai faktor ini {fn['Nilai_Siswa']:.2f}, rata-rata sekolah {fn['Baseline']:.2f}."
                 ) if fn is not None else "Tidak ada faktor yang signifikan menekan nilai."
    narasi_pos = (f"Kekuatan utama terletak pada <b style='color:#10B981;'>{fp['Aspek']}</b> "
                  f"(kontribusi +{fp['Kontribusi']:.2f} poin)."
                 ) if fp is not None else "Belum ada faktor kekuatan dominan."

    st.markdown(f"""<div class="card" style="border-left:5px solid {warna_kategori};margin-top:1rem;">
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem;">
            <div class="profile-avatar" style="width:56px;height:56px;font-size:1.2rem;">
                {"".join(x[0] for x in nama.split()[:2]).upper()}</div>
            <div>
                <div style="font-family:'Manrope';font-weight:800;font-size:1.3rem;">{nama}</div>
                <div style="color:#5C6B85;font-size:.8rem;">{kelas} - Absen {absen:02d} - Nilai {nilai:.2f}</div>
            </div>
        </div>
        <div style="font-size:.95rem;line-height:1.75;color:#1F2A44;">
            Nilai saat ini <b>{abs(selisih):.2f} poin {posisi} rata-rata sekolah</b> ({RATA_RATA_NILAI:.2f}).
            <br><br>{narasi_neg}<br><br>{narasi_pos}<br><br>
            <b>Kategori:</b> <span style="color:{warna_kategori};">{kategori}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    section_header("02", "Prioritas Perbaikan", "FOKUSKAN PADA 3 HAL INI")
    prioritas = neg.head(3)
    if len(prioritas) == 0:
        st.success("Tidak ada prioritas perbaikan mendesak.")
    else:
        cols = st.columns(len(prioritas))
        for i, (_, row) in enumerate(prioritas.iterrows()):
            with cols[i]:
                gap_val = row['Selisih']
                level = "Urgent" if gap_val < -1 else "Perhatian" if gap_val < -0.5 else "Monitor"
                st.markdown(f"""<div class="card" style="border-top:4px solid #EF5B67;min-height:200px;">
                    <div style="font-size:.65rem;font-weight:800;letter-spacing:1.5px;color:#EF5B67;">PRIORITAS {i+1}</div>
                    <div style="font-family:'Manrope';font-weight:800;font-size:1rem;margin:.6rem 0 .3rem;">{row['Aspek']}</div>
                    <div style="font-size:.7rem;color:#5C6B85;margin-bottom:.5rem;">{level}</div>
                    <div style="font-size:.75rem;line-height:1.6;color:#475467;">
                        Nilai siswa: <b>{row['Nilai_Siswa']:.2f}</b><br>
                        Rata-rata: <b>{row['Baseline']:.2f}</b><br>
                        <span style="color:#EF5B67;font-weight:700;">Selisih: {row['Selisih']:+.2f}</span>
                    </div></div>""", unsafe_allow_html=True)

    section_header("03", "Tindak Lanjut", "CHECKLIST GURU & SISWA")
    TINDAK = {
        "Self-Efficacy Akademik": {
            "guru": ["Berikan tugas bertahap (mudah ke sulit)", "Pujian spesifik atas usaha, bukan hasil",
                     "Ajak refleksi pencapaian kecil mingguan", "Pasangkan dengan peer-mentor"],
            "siswa": ["Jurnal harian '1 hal yang berhasil hari ini'", "Tetapkan target kecil yang realistis mingguan"]},
        "Keterlibatan Orang Tua": {
            "guru": ["Kirim WA ke orang tua dengan kabar positif", "Ajak orang tua ikut sesi belajar bersama",
                     "Panduan 'cara mendampingi anak belajar 15 menit/hari'", "Komunikasi rutin 2 minggu sekali"],
            "siswa": ["Ceritakan 1 hal yang dipelajari ke orang tua", "Minta orang tua periksa PR minimal 2x/minggu"]},
        "Harapan Orang Tua": {
            "guru": ["Pertemuan dengan orang tua untuk ekspektasi realistis", "Bantu pahami tahap perkembangan anak",
                     "Sarankan fokus pada usaha, bukan nilai", "Contoh memotivasi tanpa menekan"],
            "siswa": ["Belajar menyampaikan perasaan dengan tenang", "Fokus pada usaha yang bisa dikontrol"]},
        "Dukungan Sekolah": {
            "guru": ["Refleksi: apakah bantuan justru mengurangi kemandirian?",
                     "Kurangi bantuan pada hal yang siswa bisa lakukan sendiri",
                     "Berikan kesempatan mencoba & gagal (safe to fail)", "Fokus pada scaffolding, bukan taking over"],
            "siswa": ["Coba selesaikan tugas sulit 10 menit sebelum bertanya", "Catat apa yang sudah dicoba"]},
        "Motivasi Belajar": {
            "guru": ["Kaitkan materi dengan kehidupan nyata", "Berikan pilihan tugas",
                     "Apresiasi proses, bukan hanya hasil", "Ciptakan suasana kelas menyenangkan"],
            "siswa": ["Cari 1 hal menarik dari tiap pelajaran", "Belajar bersama teman"]},
        "Kecemasan Akademik": {
            "guru": ["Ajarkan teknik relaksasi sebelum ujian", "Ubah suasana ujian lebih santai",
                     "Ujian formatif yang tidak menakutkan", "Normalisasi cemas itu wajar"],
            "siswa": ["Latihan pernapasan 4-7-8 sebelum ujian", "Persiapan lebih awal"]},
        "Fasilitas Sekolah": {
            "guru": ["Informasikan fasilitas yang bisa dimanfaatkan",
                     "Bantu akses perpustakaan/lab di luar jam", "Cek hambatan akses fasilitas"],
            "siswa": ["Manfaatkan perpustakaan minimal 1x/minggu", "Tanyakan ke guru jika butuh bantuan fasilitas"]},
        "Kemalasan Belajar": {
            "guru": ["Cari akar kemalasan (bosan/sulit/tidak paham)", "Beri tugas lebih menantang jika bosan",
                     "Pecah tugas besar jadi langkah kecil", "Buat sistem reward sederhana"],
            "siswa": ["Mulai dari tugas 5 menit saja", "Teknik Pomodoro (25 menit belajar, 5 menit istirahat)"]},
    }
    if len(prioritas) == 0:
        st.info("Tidak ada tindak lanjut khusus. Pertahankan kondisi baik siswa ini.")
    else:
        for i, (_, row) in enumerate(prioritas.iterrows()):
            aspek = row["Aspek"]
            tugas = TINDAK.get(aspek, {"guru": [], "siswa": []})
            with st.expander(f"Prioritas {i+1}: {aspek}", expanded=(i==0)):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Yang bisa dilakukan GURU:**")
                    for j, t in enumerate(tugas["guru"], 1):
                        st.markdown(f"""<div style="display:flex;gap:.7rem;padding:.6rem 0;border-bottom:1px solid #EEF2F7;">
                            <div style="width:22px;height:22px;border-radius:6px;background:#EAF1FF;color:#2563EB;
                                display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:800;flex-shrink:0;">{j}</div>
                            <div style="font-size:.82rem;line-height:1.55;color:#1F2A44;">{t}</div></div>""",
                            unsafe_allow_html=True)
                with c2:
                    st.markdown("**Yang bisa dilakukan SISWA:**")
                    for j, s in enumerate(tugas["siswa"], 1):
                        st.markdown(f"""<div style="display:flex;gap:.7rem;padding:.6rem 0;border-bottom:1px solid #EEF2F7;">
                            <div style="width:22px;height:22px;border-radius:6px;background:#E8F8F1;color:#10B981;
                                display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:800;flex-shrink:0;">{j}</div>
                            <div style="font-size:.82rem;line-height:1.55;color:#1F2A44;">{s}</div></div>""",
                            unsafe_allow_html=True)

    section_header("04", "Download Catatan", "ARSIP GURU")
    txt = f"""CATATAN KONSULTASI GURU - SAA
=================================
Nama Siswa  : {nama}
Kelas       : {kelas}
Absen       : {absen}
Nilai       : {nilai:.2f}
Kategori    : {kategori}

KESIMPULAN
----------
Nilai siswa {abs(selisih):.2f} poin {"di atas" if selisih>=0 else "di bawah"} rata-rata sekolah.

Faktor paling menekan : {prioritas.iloc[0]['Aspek'] if len(prioritas) > 0 else "-"}
Faktor kekuatan       : {pos.iloc[0]['Aspek'] if len(pos) > 0 else "-"}

PRIORITAS PERBAIKAN
-------------------
"""
    for i, (_, row) in enumerate(prioritas.iterrows(), 1):
        txt += f"{i}. {row['Aspek']} (selisih {row['Selisih']:+.2f})\n"
    txt += f"\nDibuat oleh : {st.session_state.user_nama}\nTanggal     : {datetime.now().strftime('%d %B %Y, %H:%M')}\n"
    st.download_button("Download Catatan (.txt)", data=txt.encode("utf-8"),
                       file_name=f"catatan_{nama.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                       mime="text/plain", use_container_width=True)

# ================================================================
# MODUL 05 - MONITORING KELAS
# ================================================================
elif st.session_state.current_page == "monitoring":
top_bar("Monitoring Kelas", "Modul 05 - Pantau perkembangan akademik per kelas")

hero_header(
"MODUL 05 - MONITORING KELAS",
"Pantau kelas.<br><span class='accent'>Deteksi lebih awal.</span>",
"Monitoring agregat per kelas: distribusi nilai, siswa yang perlu perhatian, "
"dan perbandingan antar kelas untuk mendukung keputusan akademik.",
[("PER KELAS", "yellow"), ("AGREGAT", "blue"), ("EARLY WARNING", "coral")],
)

if len(st.session_state.database_siswa) == 0:
st.warning("Database masih kosong. Input siswa terlebih dahulu di Modul 01.")
st.stop()

df_db = pd.DataFrame(st.session_state.database_siswa)

if st.session_state.user_role == "wali_kelas" and st.session_state.user_kelas:
df_db = df_db[df_db["Kelas"].isin(st.session_state.user_kelas)]
st.info(f"Anda login sebagai Wali Kelas. Data ditampilkan hanya untuk kelas: **{', '.join(st.session_state.user_kelas)}**")

section_header("01", "Ringkasan Sekolah", "STATISTIK AGREGAT")
a, b_, c, d = st.columns(4)
with a: stat_card("Total Siswa", len(df_db), "siswa terarsip", "blue")
with b_: stat_card("Rata-rata", f"{df_db['Nilai Akademik'].mean():.2f}", "nilai seluruh siswa", "mint")
with c: stat_card("Tertinggi", f"{df_db['Nilai Akademik'].max():.2f}", "nilai maksimum", "yellow")
with d: stat_card("Terendah", f"{df_db['Nilai Akademik'].min():.2f}", "nilai minimum", "coral")

section_header("02", "Distribusi Kategori Nilai", "SEBARAN SELURUH SISWA")
dist = df_db["Kategori"].value_counts().to_dict()
kategori_list = ["Sangat Baik", "Baik", "Cukup", "Perlu Perhatian"]
warna_map = {"Sangat Baik": "#10B981", "Baik": "#2563EB", "Cukup": "#F0B900", "Perlu Perhatian": "#EF5B67"}
cols = st.columns(4)
for i, kat in enumerate(kategori_list):
jml = dist.get(kat, 0)
pct = jml / len(df_db) * 100 if len(df_db) > 0 else 0
with cols[i]:
    st.markdown(f"""<div class="card stat-card" style="border-left:5px solid {warna_map[kat]};">
        <div class="card-label" style="color:{warna_map[kat]};">{kat.upper()}</div>
        <div class="card-value" style="color:{warna_map[kat]};">{jml}</div>
        <div class="card-note">{pct:.1f}% dari {len(df_db)} siswa</div>
    </div>""", unsafe_allow_html=True)

section_header("03", "Perbandingan Antar Kelas", "RATA-RATA PER KELAS")
per_kelas = df_db.groupby("Kelas").agg(
Jumlah=("Nama", "count"),
Rata2=("Nilai Akademik", "mean"),
Tertinggi=("Nilai Akademik", "max"),
Terendah=("Nilai Akademik", "min"),
).reset_index().sort_values("Rata2", ascending=False)
per_kelas["Rata2"] = per_kelas["Rata2"].round(2)
per_kelas["Tertinggi"] = per_kelas["Tertinggi"].round(2)
per_kelas["Terendah"] = per_kelas["Terendah"].round(2)

fig, ax = plt.subplots(figsize=(11, max(4, len(per_kelas)*0.42)))
fig.patch.set_alpha(0); ax.set_facecolor("none")
colors = ["#10B981" if x >= RATA_RATA_NILAI else "#EF5B67" for x in per_kelas["Rata2"]]
bars = ax.barh(per_kelas["Kelas"], per_kelas["Rata2"], color=colors, alpha=.85)
ax.axvline(RATA_RATA_NILAI, color="#2563EB", linestyle="--", alpha=.6, linewidth=1.5)
for bar, val in zip(bars, per_kelas["Rata2"]):
ax.text(val + 0.15, bar.get_y() + bar.get_height()/2, f"{val:.2f}",
        va="center", fontsize=9.5, fontweight="bold")
ax.set_xlim(70, 100); ax.tick_params(axis="y", length=0)
ax.grid(axis="x", alpha=.15); ax.set_axisbelow(True)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#D8E0EB")
ax.set_xlabel(f"Rata-rata nilai (garis biru = rata-rata sekolah {RATA_RATA_NILAI:.2f})",
          fontsize=9.5, color="#5C6B85", labelpad=8)
plt.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

st.dataframe(per_kelas, use_container_width=True, hide_index=True)

section_header("04", "Early Warning", "SISWA YANG PERLU PERHATIAN")
st.markdown("""<div class="info-box coral" style="margin-bottom:1rem;">
<div class="info-title">Kriteria</div>
<div class="info-text">
    Siswa dengan kategori <b>Perlu Perhatian</b> (nilai &lt; 80) atau nilai <b>di bawah rata-rata sekolah</b>
    lebih dari 1 standar deviasi.
</div></div>""", unsafe_allow_html=True)

df_perhatian = df_db[df_db["Nilai Akademik"] < RATA_RATA_NILAI - STD_NILAI].copy()
df_perhatian = df_perhatian.sort_values("Nilai Akademik")
if len(df_perhatian) == 0:
st.success("Tidak ada siswa yang memerlukan perhatian khusus saat ini.")
else:
st.markdown(f"**{len(df_perhatian)} siswa** memerlukan perhatian:")
tabel_warn = df_perhatian[["Nama","Kelas","Absen","Nilai Akademik","Kategori","Dicatat Oleh"]].copy()
tabel_warn.columns = ["Nama","Kelas","Absen","Nilai","Kategori","Dicatat Oleh"]
st.dataframe(tabel_warn, use_container_width=True, hide_index=True)

csv = tabel_warn.to_csv(index=False).encode("utf-8")
st.download_button("Download Daftar Early Warning (CSV)", data=csv,
                   file_name=f"early_warning_{datetime.now().strftime('%Y%m%d')}.csv",
                   mime="text/csv", use_container_width=True)

section_header("05", "Distribusi Nilai Per Kelas", "SEBARAN")
kelas_pilih = st.selectbox("Pilih Kelas", sorted(df_db["Kelas"].unique().tolist()), key="mon_kelas")
df_k = df_db[df_db["Kelas"] == kelas_pilih]
if len(df_k) > 0:
fig, ax = plt.subplots(figsize=(11, 4))
fig.patch.set_alpha(0); ax.set_facecolor("none")
ax.hist(df_k["Nilai Akademik"], bins=10, color="#2563EB", alpha=.7, edgecolor="white")
ax.axvline(df_k["Nilai Akademik"].mean(), color="#EF5B67", linestyle="--", linewidth=2,
           label=f"Rata-rata kelas: {df_k['Nilai Akademik'].mean():.2f}")
ax.axvline(RATA_RATA_NILAI, color="#10B981", linestyle=":", linewidth=2,
           label=f"Rata-rata sekolah: {RATA_RATA_NILAI:.2f}")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=.15); ax.set_axisbelow(True)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#D8E0EB")
ax.set_xlabel("Nilai Akademik", fontsize=9.5, color="#5C6B85")
ax.set_ylabel("Jumlah Siswa", fontsize=9.5, color="#5C6B85")
plt.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)

st.markdown(f"**Detail kelas {kelas_pilih}** - {len(df_k)} siswa")
st.dataframe(df_k[["Nama","Absen","Nilai Akademik","Kategori"]],
             use_container_width=True, hide_index=True)

# ================================================================
# MODUL 06 - PENGATURAN
# ================================================================
elif st.session_state.current_page == "pengaturan":
top_bar("Pengaturan", "Modul 06 - Manajemen sistem & konfigurasi")

if not can_access_pengaturan(st.session_state.user_role):
st.error("Akses ditolak. Modul Pengaturan hanya dapat diakses oleh Administrator.")
st.stop()

hero_header(
"MODUL 06 - PENGATURAN",
"Konfigurasi<br><span class='accent'>dan tata kelola.</span>",
"Kelola akun pengguna, konfigurasi sekolah, dan pantau log aktivitas sistem SAA.",
[("ADMIN ONLY", "coral"), ("KONFIGURASI", "blue"), ("AUDIT", "purple")],
)

tab1, tab2, tab3 = st.tabs(["Konfigurasi Sekolah", "Manajemen Pengguna", "Log Aktivitas"])

with tab1:
section_header("01", "Identitas Sekolah", "INFORMASI UMUM")
cfg = st.session_state.config
c1, c2 = st.columns(2)
with c1:
    cfg["nama_sekolah"] = st.text_input("Nama Sekolah", value=cfg.get("nama_sekolah", ""))
    cfg["tahun_ajaran"] = st.text_input("Tahun Ajaran", value=cfg.get("tahun_ajaran", ""))
with c2:
    cfg["semester"] = st.selectbox("Semester", ["Ganjil", "Genap"],
                                   index=0 if cfg.get("semester")=="Ganjil" else 1)
    cfg["kepala_sekolah"] = st.text_input("Nama Kepala Sekolah", value=cfg.get("kepala_sekolah", ""))

if st.button("Simpan Konfigurasi", type="primary"):
    st.session_state.config = cfg
    save_config(cfg)
    add_log("Update konfigurasi sekolah")
    st.success("Konfigurasi berhasil disimpan.")
    st.rerun()

with tab2:
section_header("01", "Daftar Pengguna", "AKUN AKTIF SISTEM")
df_users = pd.DataFrame([
    {"Username": u, "Nama": d["nama"], "Role": ROLE_LABEL.get(d["role"], d["role"]),
     "Kelas Diampu": ", ".join(d["kelas_ampu"]) if d.get("kelas_ampu") else "-"}
    for u, d in USERS.items()
])
st.dataframe(df_users, use_container_width=True, hide_index=True)

section_header("02", "Tambah Pengguna Baru", "USER BARU")
with st.form("form_user_baru"):
    c1, c2 = st.columns(2)
    with c1:
        new_u = st.text_input("Username", placeholder="huruf kecil, tanpa spasi")
        new_nama = st.text_input("Nama Lengkap")
        new_role = st.selectbox("Role", ["admin", "kepala_sekolah", "wali_kelas", "guru"],
                                format_func=lambda x: ROLE_LABEL.get(x, x))
    with c2:
        new_pw = st.text_input("Password", type="password")
        new_kelas = st.text_input("Kelas Diampu (pisah koma, isi hanya jika Wali Kelas)",
                                  placeholder="IX-A, IX-B")
    submit_user = st.form_submit_button("Tambah Pengguna", use_container_width=True)

    if submit_user:
        if not new_u or not new_pw or not new_nama:
            st.error("Username, nama, dan password wajib diisi.")
        elif new_u in USERS:
            st.error(f"Username '{new_u}' sudah ada.")
        else:
            kelas_ampu = [k.strip() for k in new_kelas.split(",") if k.strip()] if new_kelas else None
            USERS[new_u] = {
                "password": hash_password(new_pw),
                "nama": new_nama, "role": new_role, "kelas_ampu": kelas_ampu,
            }
            add_log("Tambah pengguna", f"{new_u} ({new_role})")
            st.success(f"Pengguna '{new_u}' berhasil ditambahkan (bersifat sesi ini; untuk permanen edit di kode sumber).")
            st.rerun()

with tab3:
section_header("01", "Log Aktivitas", "AUDIT TRAIL")
st.markdown("""<div class="info-box blue" style="margin-bottom:1rem;">
    <div class="info-title">Info</div>
    <div class="info-text">Log menampilkan 200 aktivitas terakhir. Semua aksi pengguna tercatat
    untuk keperluan audit dan keamanan.</div></div>""", unsafe_allow_html=True)

if len(st.session_state.log) == 0:
    st.info("Belum ada aktivitas tercatat.")
else:
    df_log = pd.DataFrame(st.session_state.log)
    st.dataframe(df_log, use_container_width=True, hide_index=True)

    csv_log = df_log.to_csv(index=False).encode("utf-8")
    st.download_button("Download Log (CSV)", data=csv_log,
                       file_name=f"log_saa_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", use_container_width=True)

    if st.button("Bersihkan Log"):
        st.session_state.log = []
        save_log([])
        st.rerun()

# ================================================================
# END
# ================================================================
