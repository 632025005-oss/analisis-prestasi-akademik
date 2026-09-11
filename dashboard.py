import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Dashboard Prediksi Prestasi", page_icon="🎯", layout="wide")

# ================================================================
# LOAD MODEL & DATA HASIL ANALISIS
# ================================================================

# ATE (efek kausal)
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

# Bobot pengaruh (dari ATE + SHAP, dinormalisasi)
# Semakin besar absolut nilainya, semakin besar pengaruhnya
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

# Rata-rata baseline (dari data penelitian)
BASELINE = {
    'Self-Efficacy Akademik': 4.63,
    'Keterlibatan Orang Tua': 4.35,
    'Harapan Orang Tua': 3.45,
    'Dukungan Sekolah': 4.60,
    'Motivasi Belajar': 2.52,
    'Kecemasan Akademik': 2.89,
    'Kemalasan Belajar': 1.49,
    'Fasilitas Sekolah': 4.88,
}

RATA_RATA_NILAI = 83.78  # Baseline nilai

# ================================================================
# SIDEBAR
# ================================================================

st.sidebar.title("🎯 Navigasi")
menu = st.sidebar.radio(
    "Pilih Menu",
    ["🎯 Prediksi Nilai Siswa", "📊 Analisis Kausal", "📈 Analisis SHAP", "💡 Rekomendasi"]
)

st.sidebar.markdown("---")
st.sidebar.info("**SMP Negeri 6 Salatiga**\n\nDashboard Prediksi Prestasi Akademik\n\n2026")

# ================================================================
# MENU 1: PREDIKSI NILAI SISWA (INTERAKTIF)
# ================================================================

if menu == "🎯 Prediksi Nilai Siswa":
    st.title("🎯 Prediksi Nilai Siswa")
    st.markdown("### Masukkan profil siswa untuk melihat prediksi nilai dan faktor pengaruhnya")
    
    st.markdown("---")
    
    # FORM INPUT
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Input Nilai Siswa")
        st.caption("Skala 1-5 (1=Sangat Rendah, 5=Sangat Tinggi)")
        
        input_self_efficacy = st.slider(
            "🧠 Self-Efficacy Akademik",
            min_value=1.0, max_value=5.0, value=4.63, step=0.1,
            help="Keyakinan siswa terhadap kemampuan sendiri"
        )
        
        input_keterlibatan = st.slider(
            "👨‍👩‍👧 Keterlibatan Orang Tua",
            min_value=1.0, max_value=5.0, value=4.35, step=0.1,
            help="Seberapa aktif orang tua mendampingi belajar"
        )
        
        input_harapan = st.slider(
            "🎯 Harapan Orang Tua",
            min_value=1.0, max_value=5.0, value=3.45, step=0.1,
            help="Tingkat tuntutan/ekspektasi orang tua"
        )
        
        input_dukungan_sekolah = st.slider(
            "🏫 Dukungan Sekolah",
            min_value=1.0, max_value=5.0, value=4.60, step=0.1,
            help="Perhatian guru dan suasana sekolah"
        )
    
    with col2:
        st.subheader(" ")
        st.caption(" ")
        
        input_motivasi = st.slider(
            "🔥 Motivasi Belajar",
            min_value=1.0, max_value=5.0, value=2.52, step=0.1,
            help="Dorongan internal untuk belajar"
        )
        
        input_kecemasan = st.slider(
            "😰 Kecemasan Akademik",
            min_value=1.0, max_value=5.0, value=2.89, step=0.1,
            help="Tingkat kecemasan menghadapi ujian"
        )
        
        input_fasilitas = st.slider(
            "📚 Fasilitas Sekolah",
            min_value=1.0, max_value=5.0, value=4.88, step=0.1,
            help="Kualitas fasilitas belajar di sekolah"
        )
        
        input_kemalasan = st.slider(
            "😴 Kemalasan Belajar",
            min_value=1.0, max_value=5.0, value=1.49, step=0.1,
            help="Tingkat kemalasan siswa"
        )
    
    # ============================================================
    # PROSES PREDIKSI
    # ============================================================
    
    # Data input siswa
    input_data = {
        'Self-Efficacy Akademik': input_self_efficacy,
        'Keterlibatan Orang Tua': input_keterlibatan,
        'Harapan Orang Tua': input_harapan,
        'Dukungan Sekolah': input_dukungan_sekolah,
        'Motivasi Belajar': input_motivasi,
        'Kecemasan Akademik': input_kecemasan,
        'Fasilitas Sekolah': input_fasilitas,
        'Kemalasan Belajar': input_kemalasan,
    }
    
    # Hitung prediksi nilai
    # Nilai = baseline + Σ (input - baseline_variabel) × bobot
    delta_nilai = 0
    faktor_pengaruh = {}
    
    for konstruk, nilai_input in input_data.items():
        selisih = nilai_input - BASELINE[konstruk]
        pengaruh = selisih * BOBOT_PENGARUH[konstruk]
        delta_nilai += pengaruh
        faktor_pengaruh[konstruk] = pengaruh
    
    # Normalisasi delta (agar realistis dalam skala nilai)
    # Dibagi 2 sebagai faktor skala
    delta_nilai = delta_nilai / 2
    
    prediksi_nilai = RATA_RATA_NILAI + delta_nilai
    
    # Batasi nilai dalam range realistis (77-94)
    prediksi_nilai = max(77.0, min(94.0, prediksi_nilai))
    
    # ============================================================
    # HASIL PREDIKSI
    # ============================================================
    
    st.markdown("---")
    st.subheader("🎯 Hasil Prediksi")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric(
            label="📊 Prediksi Nilai",
            value=f"{prediksi_nilai:.2f}",
            delta=f"{delta_nilai:+.2f} dari rata-rata"
        )
    
    with col2:
        # Kategori nilai
        if prediksi_nilai >= 88:
            kategori = "🌟 Sangat Baik"
            warna = "success"
        elif prediksi_nilai >= 83:
            kategori = "✅ Baik"
            warna = "info"
        elif prediksi_nilai >= 80:
            kategori = "⚠️ Cukup"
            warna = "warning"
        else:
            kategori = "❗ Perlu Perhatian"
            warna = "error"
        
        st.metric(label="📈 Kategori", value=kategori)
    
    with col3:
        st.metric(
            label="🎯 Baseline",
            value=f"{RATA_RATA_NILAI:.2f}",
            delta="Rata-rata sekolah"
        )
    
    # ============================================================
    # VISUALISASI FAKTOR PENGARUH
    # ============================================================
    
    st.markdown("---")
    st.subheader("🔍 Faktor yang Mempengaruhi Prediksi")
    
    # Urutkan berdasarkan pengaruh
    faktor_df = pd.DataFrame([
        {'Konstruk': k, 'Pengaruh': v, 
         'Nilai_Siswa': input_data[k], 
         'Baseline': BASELINE[k],
         'Selisih': input_data[k] - BASELINE[k]}
        for k, v in faktor_pengaruh.items()
    ]).sort_values('Pengaruh', key=abs, ascending=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['green' if x > 0 else 'red' for x in faktor_df['Pengaruh']]
        bars = ax.barh(faktor_df['Konstruk'], faktor_df['Pengaruh'], color=colors, alpha=0.7)
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
        ax.set_xlabel('Pengaruh terhadap Nilai (poin)')
        ax.set_title('Kontribusi Setiap Faktor terhadap Prediksi Nilai')
        
        for bar, val in zip(bars, faktor_df['Pengaruh']):
            pos = val + 0.05 if val > 0 else val - 0.15
            ax.text(pos, bar.get_y() + bar.get_height()/2, 
                    f'{val:+.2f}', va='center', fontsize=9)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("### 📖 Cara Membaca")
        st.markdown("""
        **🟢 Hijau (Positif)**:
        Faktor ini **meningkatkan** nilai siswa
        
        **🔴 Merah (Negatif)**:
        Faktor ini **menurunkan** nilai siswa
        
        **Panjang bar**:
        Semakin panjang, semakin besar pengaruhnya
        """)
    
    # ============================================================
    # TABEL DETAIL
    # ============================================================
    
    st.markdown("---")
    st.subheader("📋 Detail Perbandingan dengan Baseline")
    
    # Format tabel
    tabel_detail = faktor_df.copy()
    tabel_detail['Status'] = tabel_detail['Selisih'].apply(
        lambda x: '⬆️ Di atas rata-rata' if x > 0 else '⬇️ Di bawah rata-rata' if x < 0 else '➡️ Sama'
    )
    tabel_detail = tabel_detail[['Konstruk', 'Nilai_Siswa', 'Baseline', 'Selisih', 'Pengaruh', 'Status']]
    tabel_detail.columns = ['Konstruk', 'Nilai Siswa', 'Baseline', 'Selisih', 'Pengaruh (poin)', 'Status']
    tabel_detail = tabel_detail.sort_values('Pengaruh (poin)', key=abs, ascending=False)
    
    st.dataframe(tabel_detail, use_container_width=True, hide_index=True)
    
    # ============================================================
    # REKOMENDASI PERSONAL
    # ============================================================
    
    st.markdown("---")
    st.subheader("💡 Rekomendasi Personal untuk Siswa Ini")
    
    # Faktor yang perlu ditingkatkan (pengaruh negatif = harus diperbaiki)
    faktor_negatif = faktor_df[faktor_df['Pengaruh'] < -0.3].sort_values('Pengaruh')
    faktor_positif = faktor_df[faktor_df['Pengaruh'] > 0.3].sort_values('Pengaruh', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(faktor_negatif) > 0:
            st.error("### ⚠️ Faktor yang Perlu Diperbaiki")
            for _, row in faktor_negatif.iterrows():
                st.markdown(f"""
                **{row['Konstruk']}** (Pengaruh: {row['Pengaruh']:+.2f})
                - Nilai siswa: **{row['Nilai_Siswa']:.2f}** vs Baseline: {row['Baseline']:.2f}
                - 📌 Perlu ditingkatkan
                """)
        else:
            st.success("### ✅ Tidak ada faktor negatif signifikan")
    
    with col2:
        if len(faktor_positif) > 0:
            st.success("### ✅ Faktor Kekuatan Siswa")
            for _, row in faktor_positif.iterrows():
                st.markdown(f"""
                **{row['Konstruk']}** (Pengaruh: {row['Pengaruh']:+.2f})
                - Nilai siswa: **{row['Nilai_Siswa']:.2f}** vs Baseline: {row['Baseline']:.2f}
                - 📌 Pertahankan!
                """)
        else:
            st.info("### ℹ️ Belum ada faktor kekuatan dominan")

# ================================================================
# MENU 2: ANALISIS KAUSAL
# ================================================================

elif menu == "📊 Analisis Kausal":
    st.title("📊 Analisis Kausal (ATE)")
    st.markdown("### Efek Kausal Setiap Faktor terhadap Prestasi Akademik")
    
    df_ate = pd.DataFrame([
        {'Konstruk': k, 'ATE': v} for k, v in ATE_DATA.items()
    ]).sort_values('ATE', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['green' if x > 0 else 'red' for x in df_ate['ATE']]
    bars = ax.barh(df_ate['Konstruk'], df_ate['ATE'], color=colors, alpha=0.7)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    ax.set_xlabel('ATE (Average Treatment Effect)')
    ax.set_title('Efek Kausal terhadap Prestasi Akademik')
    
    for bar, val in zip(bars, df_ate['ATE']):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2, f'{val:+.2f}', va='center')
    
    st.pyplot(fig)
    st.dataframe(df_ate, use_container_width=True, hide_index=True)

# ================================================================
# MENU 3: ANALISIS SHAP
# ================================================================

elif menu == "📈 Analisis SHAP":
    st.title("📈 Analisis SHAP")
    st.markdown("### Kontribusi Prediktif Setiap Faktor")
    
    df_shap = pd.DataFrame([
        {'Konstruk': k, 'Mean_SHAP': v} for k, v in SHAP_DATA.items()
    ]).sort_values('Mean_SHAP', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(df_shap['Konstruk'], df_shap['Mean_SHAP'], color='steelblue', alpha=0.7)
    ax.set_xlabel('Mean |SHAP Value|')
    ax.set_title('Kontribusi Fitur terhadap Prediksi')
    
    for bar, val in zip(bars, df_shap['Mean_SHAP']):
        ax.text(val + 0.02, bar.get_y() + bar.get_height()/2, f'{val:.4f}', va='center', fontsize=9)
    
    st.pyplot(fig)
    st.dataframe(df_shap, use_container_width=True, hide_index=True)

# ================================================================
# MENU 4: REKOMENDASI UMUM
# ================================================================

else:
    st.title("💡 Rekomendasi Intervensi Umum")
    st.markdown("### Berdasarkan Hasil Analisis Keseluruhan")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ### ✅ PRIORITAS TINGGI
        
        **1. Fasilitas Sekolah** (ATE: +2.43)
        - Tingkatkan kualitas perpustakaan
        - Optimalkan laboratorium
        
        **2. Keterlibatan Orang Tua** (ATE: +2.21)
        - Program parenting
        - Komunikasi rutin sekolah-orang tua
        
        **3. Self-Efficacy Akademik** (ATE: +2.07)
        - Program penguatan kepercayaan diri
        - Pelatihan motivasi belajar
        """)
    
    with col2:
        st.warning("""
        ### ⚠️ PERLU EVALUASI
        
        **1. Dukungan Sekolah** (ATE: -3.88)
        - Evaluasi program pendampingan
        - Kurangi intervensi berlebihan
        
        **2. Harapan Orang Tua** (ATE: -1.53)
        - Edukasi orang tua
        - Target realistis
        """)
