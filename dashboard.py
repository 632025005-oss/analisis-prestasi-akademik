# -*- coding: utf-8 -*-
# ================================================================
# SMART ACADEMIC ANALYTICS (SAA) - SMP Negeri 6 Salatiga
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
DB_FILE = "database_siswa.json"
CONFIG_FILE = "config_school.json"
LOG_FILE = "log_aktivitas.json"

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
def load_config():
    return _load_json(CONFIG_FILE, {
        "nama_sekolah": "SMP Negeri 6 Salatiga",
        "tahun_ajaran": "2025/2026",
        "semester": "Genap",
        "kepala_sekolah": "Kepala SMPN 6 Salatiga",
    })
def save_config(c): _save_json(CONFIG_FILE, c)
def load_log(): return _load_json(LOG_FILE, [])
def save_log(l): _save_json(LOG_FILE, l)

st.set_page_config(
    page_title="SAA - Smart Academic Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ================================================================
# CSS
# ================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
:root{
    --ink:#0F1B33; --muted:#5C6B85; --line:#E4EAF2;
    --blue:#2563EB; --blue-soft:#EAF1FF;
    --violet:#7C5CFC; --violet-soft:#F1EDFF;
    --yellow:#F6C945; --yellow-soft:#FFF7D6;
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
@keyframes sparkle{0%,100%{opacity:.3;transform:scale(1);}50%{opacity:1;transform:scale(1.35);}}
@keyframes gradientShift{0%,100%{background-position:0% 50%;}50%{background-position:100% 50%;}}
.motion{animation:riseIn .5s ease both;}

.login-page-header{display:flex;justify-content:space-between;align-items:center;padding:1rem 2rem;
    background:linear-gradient(135deg,#FFFFFF 0%,#F3F6FF 100%);border-bottom:1px solid #DCE4F2;
    margin:-1.6rem -2.7rem 0 -2.7rem;box-shadow:0 4px 20px rgba(37,99,235,.06);}
.login-logo-area{display:flex;align-items:center;gap:.8rem;justify-content:flex-end;width:100%;}
.login-logo-icon{font-size:2.2rem;line-height:1;}
.login-logo-text{text-align:right;line-height:1.15;}
.login-logo-title{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.6rem;font-weight:800;
    color:#0F1B33;letter-spacing:-.8px;}
.login-logo-title .blue-part{background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.login-logo-sub{font-size:.72rem;color:#5C6B85;letter-spacing:.3px;margin-top:.15rem;}
.login-content{max-width:1050px;margin:2rem auto;padding:0 2rem;}
.login-date-logout{display:flex;justify-content:space-between;align-items:center;padding:.9rem 1.1rem;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 100%);border:1px solid #DCE4F2;
    border-left:5px solid #2563EB;border-radius:12px;margin-bottom:2rem;}
.login-date{font-family:'Manrope',sans-serif;font-weight:800;font-size:.95rem;color:#0F1B33;}
.login-logout-link{font-size:.8rem;color:#2563EB;font-weight:700;padding:.35rem .8rem;}
.siasat-label{font-family:'DM Sans',sans-serif;font-weight:700;font-size:.9rem;color:#0F1B33;padding-top:.65rem;}
.siasat-info-box{background:linear-gradient(135deg,#FFF9E6 0%,#FFF4CC 100%);
    border:1px solid #F3DF8D;border-left:5px solid #F6C945;
    border-radius:12px;padding:1.2rem 1.4rem;margin-top:2.5rem;}
.siasat-info-header{display:flex;align-items:center;gap:.6rem;margin-bottom:.7rem;}
.siasat-info-title{font-family:'Manrope',sans-serif;font-weight:800;font-size:.9rem;color:#0F1B33;}
.siasat-info-list{font-size:.8rem;color:#475467;line-height:1.85;}
.siasat-info-list div{display:flex;gap:.5rem;}
.siasat-info-list .num{color:#2563EB;font-weight:800;min-width:18px;}
.siasat-footer{text-align:center;padding:2rem 0;margin-top:3rem;
    border-top:1px solid #DCE4F2;font-size:.72rem;color:#5C6B85;line-height:1.8;}
.siasat-footer strong{color:#2563EB;font-weight:800;}

.dashboard-hero{position:relative;overflow:hidden;
    background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 50%,#EEF3FF 100%);
    border:1px solid #DCE4F2;border-radius:28px;padding:2.3rem 2.5rem;
    box-shadow:0 20px 55px rgba(30,50,90,.10);animation:riseIn .5s ease both;}

.menu-hero{position:relative;overflow:hidden;
    background:linear-gradient(135deg,#0B1730 0%,#16294A 30%,#1E3A8A 60%,#7C5CFC 100%);
    border-radius:32px;padding:3.5rem 3rem;color:#fff;margin-bottom:2.5rem;
    box-shadow:0 30px 80px rgba(11,23,48,.40);animation:riseIn .5s ease both;}
.menu-hero-kicker{display:inline-flex;align-items:center;gap:8px;font-size:.7rem;font-weight:800;
    letter-spacing:2px;color:#F6C945;text-transform:uppercase;margin-bottom:1rem;}
.menu-hero-title{font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.5rem,5vw,4.5rem);line-height:.98;letter-spacing:-3px;font-weight:800;margin:0;max-width:900px;}
.menu-hero-title em{background:linear-gradient(135deg,#F6C945 0%,#FFA94D 50%,#F6C945 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    font-style:italic;}
.menu-hero-sub{color:#C6D1E5;font-size:1.05rem;line-height:1.6;max-width:680px;margin:1.2rem 0 0;}
.menu-hero-meta{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.8rem;}
.menu-hero-meta span{padding:.55rem .9rem;border-radius:999px;
    background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);
    color:#F0F5FF;font-size:.68rem;font-weight:800;letter-spacing:.7px;}

.menu-card{position:relative;overflow:hidden;
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    border:1px solid #DCE4F2;border-radius:24px;padding:1.75rem 1.6rem 1.6rem;
    transition:transform .3s ease, box-shadow .3s ease;
    box-shadow:0 14px 40px rgba(30,50,90,.08);min-height:230px;
    display:flex;flex-direction:column;justify-content:space-between;animation:riseIn .55s ease both;}
.menu-card:hover{transform:translateY(-8px);box-shadow:0 28px 65px rgba(30,50,90,.18);}
.menu-card.mc-blue{background:linear-gradient(135deg,#FFFFFF 0%,#EAF1FF 100%);border-color:#D4E0FF;}
.menu-card.mc-yellow{background:linear-gradient(135deg,#FFFFFF 0%,#FFF7D6 100%);border-color:#F3DF8D;}
.menu-card.mc-mint{background:linear-gradient(135deg,#FFFFFF 0%,#E8F8F1 100%);border-color:#BCE8D7;}
.menu-card.mc-purple{background:linear-gradient(135deg,#FFFFFF 0%,#F1EDFF 100%);border-color:#DDD5FF;}
.menu-card.mc-pink{background:linear-gradient(135deg,#FFFFFF 0%,#FCE7F3 100%);border-color:#F8C7DF;}
.menu-card.mc-teal{background:linear-gradient(135deg,#FFFFFF 0%,#CFFAFE 100%);border-color:#A5E8EF;}
.menu-card-num{font-family:'Plus Jakarta Sans',sans-serif;font-size:.68rem;font-weight:800;
    letter-spacing:1.6px;color:#5C6B85;text-transform:uppercase;}
.menu-card-icon{width:56px;height:56px;border-radius:16px;display:flex;align-items:center;
    justify-content:center;font-size:1.7rem;margin:.9rem 0;box-shadow:0 6px 14px rgba(0,0,0,.06);}
.menu-card.mc-blue .menu-card-icon{background:linear-gradient(135deg,#DBE7FF,#B8CEFF);color:#2563EB;}
.menu-card.mc-yellow .menu-card-icon{background:linear-gradient(135deg,#FFF1B8,#FFE37A);color:#936F00;}
.menu-card.mc-mint .menu-card-icon{background:linear-gradient(135deg,#C9F2E0,#9BE5C8);color:#087453;}
.menu-card.mc-purple .menu-card-icon{background:linear-gradient(135deg,#E2DBFF,#C9BEFF);color:#5B3FCC;}
.menu-card.mc-pink .menu-card-icon{background:linear-gradient(135deg,#FBD5E8,#F8AFD0);color:#BE185D;}
.menu-card.mc-teal .menu-card-icon{background:linear-gradient(135deg,#B6EFF6,#7FE0EC);color:#0E7490;}
.menu-card-title{font-family:'Manrope',sans-serif;font-size:1.15rem;font-weight:800;
    letter-spacing:-.4px;line-height:1.2;margin:0 0 .35rem;}
.menu-card-desc{color:#5C6B85;font-size:.78rem;line-height:1.55;margin:0;}
.menu-card-cta{display:inline-flex;align-items:center;gap:.45rem;
    font-size:.72rem;font-weight:800;letter-spacing:.5px;margin-top:1rem;text-transform:uppercase;color:#2563EB;}

.section-wrap{margin-top:2rem;margin-bottom:1rem;}
.section-number{display:inline-flex;width:42px;height:42px;align-items:center;justify-content:center;
    border-radius:14px;background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 100%);
    color:#fff;font-size:.8rem;font-weight:800;box-shadow:0 10px 24px rgba(37,99,235,.35);}
.section-title{font-size:1.45rem;letter-spacing:-.7px;margin:0;}
.section-sub{color:#5C6B85;font-size:.72rem;text-transform:uppercase;
    letter-spacing:1.1px;font-weight:800;margin-top:.2rem;}
.section-line{height:1px;background:linear-gradient(90deg,#DCE4F2 0%,transparent 100%);margin-top:.9rem;}

.card{background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    border:1px solid #E4EAF2;border-radius:20px;padding:1.25rem 1.35rem;
    box-shadow:0 10px 30px rgba(30,50,90,.06);animation:riseIn .5s ease both;}
.card-blue{background:linear-gradient(135deg,#FFFFFF 0%,#EAF1FF 100%);border-color:#D4E0FF;}
.card-yellow{background:linear-gradient(135deg,#FFFFFF 0%,#FFF7D6 100%);border-color:#F3DF8D;}
.card-mint{background:linear-gradient(135deg,#FFFFFF 0%,#E8F8F1 100%);border-color:#BCE8D7;}
.card-purple{background:linear-gradient(135deg,#FFFFFF 0%,#F1EDFF 100%);border-color:#DDD5FF;}
.card-dark{background:linear-gradient(135deg,#0B1730 0%,#16294A 100%);
    border-color:#0B1730;color:#fff;box-shadow:0 20px 50px rgba(11,23,48,.35);}
.card-label{font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#5C6B85;}
.card-dark .card-label{color:#9DBBFF;}
.card-value{font-family:'Manrope',sans-serif;font-size:2rem;font-weight:800;
    letter-spacing:-1.2px;line-height:1;margin-top:.5rem;}
.card-note{color:#5C6B85;font-size:.74rem;margin-top:.45rem;}
.card-dark .card-note{color:#9DBBFF;}

.stat-card{min-height:122px;position:relative;overflow:hidden;}
.stat-card .topline{width:40px;height:5px;border-radius:99px;margin-bottom:.85rem;}
.topline.blue{background:linear-gradient(90deg,#2563EB,#7C5CFC);}
.topline.yellow{background:linear-gradient(90deg,#F6C945,#FFA94D);}
.topline.mint{background:linear-gradient(90deg,#10B981,#06B6D4);}
.topline.coral{background:linear-gradient(90deg,#EF5B67,#EC4899);}
.topline.purple{background:linear-gradient(90deg,#7C5CFC,#EC4899);}

.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:.68rem;font-weight:800;
    letter-spacing:1.5px;text-transform:uppercase;color:#2563EB;margin-bottom:.7rem;}
.eyebrow-dot{width:8px;height:8px;background:#F6C945;border-radius:50%;display:inline-block;}

.hero-title{font-family:'Plus Jakarta Sans',sans-serif;
    font-size:clamp(2.15rem,4vw,3.8rem);line-height:1.02;letter-spacing:-2.4px;margin:0;max-width:850px;}
.hero-title .accent{background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 50%,#EC4899 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{color:#5C6B85;font-size:.98rem;line-height:1.65;max-width:790px;margin:.9rem 0 0;}
.hero-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:1.25rem;}
.pill{display:inline-flex;align-items:center;gap:7px;padding:.42rem .7rem;border-radius:999px;
    font-size:.65rem;font-weight:800;letter-spacing:.5px;border:1px solid #E4EAF2;background:#fff;}
.pill.blue{background:#EAF1FF;color:#2563EB;border-color:#D4E0FF;}
.pill.yellow{background:#FFF7D6;color:#936F00;border-color:#F3DF8D;}
.pill.mint{background:#E8F8F1;color:#087453;border-color:#BCE8D7;}
.pill.purple{background:#F1EDFF;color:#5B3FCC;border-color:#DDD5FF;}
.pill.coral{background:#FFF0F2;color:#B91C1C;border-color:#F4CDD3;}

.profile-card{display:flex;align-items:center;justify-content:space-between;gap:1rem;
    padding:1.15rem 1.3rem;background:linear-gradient(135deg,#FFFFFF 0%,#F5F8FF 100%);
    border:1px solid #DCE4F2;border-radius:18px;box-shadow:0 8px 24px rgba(30,50,90,.05);}
.profile-avatar{width:48px;height:48px;border-radius:15px;display:flex;align-items:center;
    justify-content:center;background:linear-gradient(135deg,#2563EB 0%,#7C5CFC 50%,#EC4899 100%);
    color:#fff;font-weight:800;font-size:1rem;box-shadow:0 8px 18px rgba(37,99,235,.3);}
.profile-name{font-family:'Manrope',sans-serif;font-weight:800;font-size:1.05rem;}
.profile-meta{color:#5C6B85;font-size:.72rem;margin-top:.2rem;}

.factor-card{border:1px solid #E4EAF2;border-radius:18px;
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);
    padding:1rem 1.05rem;margin:.65rem 0;}
.factor-head{display:flex;justify-content:space-between;align-items:center;gap:1rem;}
.factor-name{font-weight:700;font-size:.86rem;}
.factor-value{font-family:'Manrope',sans-serif;font-weight:800;font-size:1rem;}
.factor-bar{height:7px;background:#EEF2F7;border-radius:99px;overflow:hidden;margin-top:.75rem;}
.factor-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,#7C5CFC,#EC4899);}

.rank-row{display:grid;grid-template-columns:34px 1fr auto;
    align-items:center;gap:.8rem;padding:.75rem 0;border-bottom:1px solid #E4EAF2;}
.rank-row:last-child{border-bottom:0;}
.rank-num{width:30px;height:30px;border-radius:10px;
    background:linear-gradient(135deg,#EAF1FF 0%,#F1EDFF 100%);
    color:#2563EB;display:flex;align-items:center;justify-content:center;
    font-size:.68rem;font-weight:800;}
.rank-name{font-weight:700;font-size:.8rem;}
.rank-desc{font-size:.67rem;color:#5C6B85;margin-top:.15rem;}
.rank-value{font-family:'Manrope',sans-serif;font-size:.86rem;font-weight:800;}
.positive{color:#10B981;}
.negative{color:#EF5B67;}

.info-box{border-radius:18px;padding:1.1rem 1.2rem;border:1px solid #E4EAF2;
    background:linear-gradient(135deg,#FFFFFF 0%,#FBFDFF 100%);}
.info-box.blue{background:linear-gradient(135deg,#EAF1FF 0%,#DBE7FF 100%);border-color:#D5E1FF;}
.info-box.yellow{background:linear-gradient(135deg,#FFF7D6 0%,#FFF1B8 100%);border-color:#F1DF96;}
.info-box.mint{background:linear-gradient(135deg,#E8F8F1 0%,#C9F2E0 100%);border-color:#C5EBDD;}
.info-box.coral{background:linear-gradient(135deg,#FFF0F2 0%,#FFD9DF 100%);border-color:#F4CDD3;}
.info-title{font-weight:800;font-size:.9rem;}
.info-text{font-size:.78rem;line-height:1.6;margin-top:.35rem;color:#475467;}

.notif-success{background:linear-gradient(135deg,#ECFDF5 0%,#D1FAE5 100%);
    border:2px solid #10B981;border-left:6px solid #10B981;
    border-radius:14px;padding:1.2rem 1.4rem;margin:1rem 0;animation:riseIn .5s ease both;}
.notif-success-title{font-family:'Manrope',sans-serif;font-weight:800;
    font-size:1rem;color:#065F46;}
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
    .menu-hero{padding:2.5rem 1.7rem;}
    .login-logo-title{font-size:1.2rem;}
}
</style>
""", unsafe_allow_html=True)

# ================================================================
# AUTENTIKASI & ROLE
# ================================================================
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

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

def can_access_pengaturan(role):
    return role == "admin"

# ================================================================
# SESSION STATE
# ================================================================
_default_state = {
    "logged_in": False,
    "user_nama": None,
    "user_role": None,
    "user_kelas": None,
    "database_siswa": load_database(),
    "config": load_config(),
    "log": load_log(),
    "current_page": "home",
    "last_saved": None,
}
for key, val in _default_state.items():
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
        ],
    },
    "Keterlibatan Orang Tua": {
        "question": "Seberapa aktif orang tua mendampingi siswa belajar?",
        "options": [
            ("1", "Hampir tidak pernah mendampingi"),
            ("2", "Jarang mendampingi"),
            ("3", "Kadang-kadang mendampingi"),
            ("4", "Sering mendampingi"),
            ("5", "Hampir selalu mendampingi"),
        ],
    },
    "Harapan Orang Tua": {
        "question": "Seberapa tinggi tuntutan orang tua terhadap nilai siswa?",
        "options": [
            ("1", "Sangat rendah"),
            ("2", "Rendah"),
            ("3", "Sedang / wajar"),
            ("4", "Tinggi"),
            ("5", "Sangat tinggi / menekan"),
        ],
    },
    "Dukungan Sekolah": {
        "question": "Seberapa besar dukungan sekolah kepada siswa?",
        "options": [
            ("1", "Sangat kurang"),
            ("2", "Kurang"),
            ("3", "Cukup"),
            ("4", "Baik"),
            ("5", "Sangat baik"),
        ],
    },
    "Motivasi Belajar": {
        "question": "Seberapa besar motivasi dan semangat belajar siswa?",
        "options": [
            ("1", "Tidak ada motivasi"),
            ("2", "Kurang termotivasi"),
            ("3", "Cukup termotivasi"),
            ("4", "Termotivasi"),
            ("5", "Sangat termotivasi"),
        ],
    },
    "Kecemasan Akademik": {
        "question": "Seberapa sering siswa merasa cemas saat belajar atau ujian?",
        "options": [
            ("1", "Hampir tidak pernah cemas"),
            ("2", "Jarang cemas"),
            ("3", "Kadang-kadang cemas"),
            ("4", "Sering cemas"),
            ("5", "Hampir selalu cemas"),
        ],
    },
    "Fasilitas Sekolah": {
        "question": "Seberapa memadai fasilitas belajar di sekolah?",
        "options": [
            ("1", "Sangat kurang memadai"),
            ("2", "Kurang memadai"),
            ("3", "Cukup memadai"),
            ("4", "Memadai"),
            ("5", "Sangat memadai"),
        ],
    },
    "Kemalasan Belajar": {
        "question": "Seberapa sering siswa menunjukkan sikap malas belajar?",
        "options": [
            ("1", "Tidak pernah malas"),
            ("2", "Jarang malas"),
            ("3", "Kadang-kadang malas"),
            ("4", "Sering malas"),
            ("5", "Hampir selalu malas"),
        ],
    },
}

# ================================================================
# FUNGSI ANALITIK
# ================================================================
