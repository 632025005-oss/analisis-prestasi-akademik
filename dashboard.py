import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="Dashboard Prediksi Prestasi", page_icon="🎯", layout="wide")

# ================================================================
# DATA BASELINE & BOBOT
# ================================================================

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

# ================================================================
# SESSION STATE (Penyimpanan sementara)
# ================================================================

if 'database_siswa' not in st.session_state:
    st.session_state.database_siswa = []

# ================================================================
# FUNGSI PREDIKSI
# ================================================================

def hitung_prediksi(input_data):
    """Menghitung prediksi nilai berdasarkan input siswa"""
    delta_nilai = 0
    faktor_pengaruh = {}
    
    for konstruk, nilai_input in input_data.items():
        selisih = nilai_input - BASELINE[konstruk]
        pengaruh = selisih * BOBOT_PENGARUH[konstruk]
        delta_nilai += pengaruh
        faktor_pengaruh[konstruk] = pengaruh
    
    delta_nilai = delta_nilai / 2
    prediksi_nilai = RATA_RATA_NILAI + delta_nilai
    prediksi_nilai = max(77.0, min(94.0, prediksi_nilai))
    
    return prediksi_nilai, delta_nilai, faktor_pengaruh


def kategori_nilai(nilai):
    """Menentukan kategori nilai"""
    if nilai >= 88:
        return "🌟 Sangat Baik"
    elif nilai >= 83:
        return "✅ Baik"
    elif nilai >= 80:
        return "⚠️ Cukup"
    else:
        return "❗ Perlu Perhatian"

# ================================================================
# SIDEBAR
# ================================================================

st.sidebar.title("🎯 Navigasi")
menu = st.sidebar.radio(
    "Pilih Menu",
    ["📝 Input Nilai Siswa", "🗄️ Database Siswa", "📊 Analisis Kausal", "📈 Analisis SHAP", "💡 Rekomendasi"]
)

st.sidebar.markdown("---")
st.sidebar.info("**SMP Negeri 6 Salatiga**\n\nDashboard Prediksi Prestasi Akademik\n\n2026")

# ================================================================
# MENU 1: INPUT NILAI SISWA
# ================================================================

if menu == "📝 Input Nilai Siswa":
    st.title("📝 Input Nilai Siswa")
    st.markdown("### Masukkan data siswa dan nilai setiap aspek")
    
    st.markdown("---")
    
    # FORM DATA DIRI
    st.subheader("👤 Data Siswa")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        nama_siswa = st.text_input("Nama Siswa", placeholder="Contoh: Ahmad Rizki")
    with col2:
        kelas_siswa = st.selectbox(
            "Kelas",
            ["IX-A", "IX-B", "IX-C", "IX-D", "IX-E", "IX-F", "IX-G", "IX-H"]
        )
    with col3:
        absen_siswa = st.number_input("No. Absen", min_value=1, max_value=50, value=1)
    
    st.markdown("---")
    
    # FORM NILAI KONSTRUK
    st.subheader("📊 Penilaian Aspek Siswa")
    st.caption("Skala 1-5 (1=Sangat Rendah, 5=Sangat Tinggi)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🧠 Aspek Internal Siswa**")
        input_self_efficacy = st.slider(
            "Self-Efficacy Akademik", 1.0, 5.0, 4.63, 0.1,
            help="Keyakinan siswa terhadap kemampuan sendiri"
        )
        input_motivasi = st.slider(
            "Motivasi Belajar", 1.0, 5.0, 2.52, 0.1,
            help="Dorongan internal untuk belajar"
        )
        input_kecemasan = st.slider(
            "Kecemasan Akademik", 1.0, 5.0, 2.89, 0.1,
            help="Tingkat kecemasan menghadapi ujian"
        )
        input_kemalasan = st.slider(
            "Kemalasan Belajar", 1.0, 5.0, 1.49, 0.1,
            help="Tingkat kemalasan siswa"
        )
    
    with col2:
        st.markdown("**🌍 Aspek Eksternal Siswa**")
        input_keterlibatan = st.slider(
            "Keterlibatan Orang Tua", 1.0, 5.0, 4.35, 0.1,
            help="Seberapa aktif orang tua mendampingi belajar"
        )
        input_harapan = st.slider(
            "Harapan Orang Tua", 1.0, 5.0, 3.45, 0.1,
            help="Tingkat tuntutan/ekspektasi orang tua"
        )
        input_dukungan_sekolah = st.slider(
            "Dukungan Sekolah", 1.0, 5.0, 4.60, 0.1,
            help="Perhatian guru dan suasana sekolah"
        )
        input_fasilitas = st.slider(
            "Fasilitas Sekolah", 1.0, 5.0, 4.88, 0.1,
            help="Kualitas fasilitas belajar di sekolah"
        )
    
    # ============================================================
    # PROSES PREDIKSI
    # ============================================================
    
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
    
    prediksi_nilai, delta_nilai, faktor_pengaruh = hitung_prediksi(input_data)
    kategori = kategori_nilai(prediksi_nilai)
    
    # ============================================================
    # HASIL PREDIKSI
    # ============================================================
    
    st.markdown("---")
    st.subheader("🎯 Hasil Prediksi")
    
    # Nama siswa
    if nama_siswa:
        st.markdown(f"**Siswa**: {nama_siswa} | **Kelas**: {kelas_siswa} | **Absen**: {absen_siswa}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Prediksi Nilai", f"{prediksi_nilai:.2f}", f"{delta_nilai:+.2f}")
    with col2:
        st.metric("📈 Kategori", kategori)
    with col3:
        st.metric("🎯 Baseline", f"{RATA_RATA_NILAI:.2f}")
    
    # ============================================================
    # VISUALISASI PENGARUH
    # ============================================================
    
    st.markdown("---")
    st.subheader("🔍 Faktor yang Mempengaruhi")
    
    faktor_df = pd.DataFrame([
        {'Konstruk': k, 'Pengaruh': v, 'Nilai': input_data[k]}
        for k, v in faktor_pengaruh.items()
    ]).sort_values('Pengaruh', key=abs, ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['green' if x > 0 else 'red' for x in faktor_df['Pengaruh']]
    bars = ax.barh(faktor_df['Konstruk'], faktor_df['Pengaruh'], color=colors, alpha=0.7)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    ax.set_xlabel('Pengaruh terhadap Nilai (poin)')
    ax.set_title('Kontribusi Setiap Faktor')
    
    for bar, val in zip(bars, faktor_df['Pengaruh']):
        pos = val + 0.05 if val > 0 else val - 0.15
        ax.text(pos, bar.get_y() + bar.get_height()/2, f'{val:+.2f}', va='center', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # ============================================================
    # TOMBOL SIMPAN KE DATABASE
    # ============================================================
    
    st.markdown("---")
    st.subheader("💾 Simpan ke Database")
    
    if not nama_siswa:
        st.warning("⚠️ Isi **Nama Siswa** terlebih dahulu sebelum menyimpan.")
    else:
        col1, col2 = st.columns([1, 3])
        with col1:
            tombol_simpan = st.button("💾 Simpan Data Siswa", type="primary", use_container_width=True)
        
        if tombol_simpan:
            # Cek duplikat
            duplikat = any(
                s['Nama'] == nama_siswa and s['Kelas'] == kelas_siswa
                for s in st.session_state.database_siswa
            )
            
            if duplikat:
                st.warning(f"⚠️ Siswa **{nama_siswa}** di kelas **{kelas_siswa}** sudah ada di database.")
            else:
                # Simpan data
                data_baru = {
                    'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'Nama': nama_siswa,
                    'Kelas': kelas_siswa,
                    'Absen': absen_siswa,
                    'Self-Efficacy': input_self_efficacy,
                    'Keterlibatan Ortu': input_keterlibatan,
                    'Harapan Ortu': input_harapan,
                    'Dukungan Sekolah': input_dukungan_sekolah,
                    'Motivasi': input_motivasi,
                    'Kecemasan': input_kecemasan,
                    'Fasilitas': input_fasilitas,
                    'Kemalasan': input_kemalasan,
                    'Prediksi Nilai': round(prediksi_nilai, 2),
                    'Kategori': kategori,
                }
                
                st.session_state.database_siswa.append(data_baru)
                st.success(f"✅ Data **{nama_siswa}** berhasil disimpan!")
                st.balloons()

# ================================================================
# MENU 2: DATABASE SISWA
# ================================================================

elif menu == "🗄️ Database Siswa":
    st.title("🗄️ Database Siswa")
    st.markdown("### Daftar semua siswa yang sudah dianalisis")
    
    st.markdown("---")
    
    if len(st.session_state.database_siswa) == 0:
        st.info("📭 Belum ada data siswa. Silakan input data terlebih dahulu di menu **📝 Input Nilai Siswa**.")
    else:
        df_db = pd.DataFrame(st.session_state.database_siswa)
        
        # Statistik
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total Siswa", len(df_db))
        with col2:
            st.metric("📊 Rata-rata Prediksi", f"{df_db['Prediksi Nilai'].mean():.2f}")
        with col3:
            st.metric("🏆 Nilai Tertinggi", f"{df_db['Prediksi Nilai'].max():.2f}")
        with col4:
            st.metric("📉 Nilai Terendah", f"{df_db['Prediksi Nilai'].min():.2f}")
        
        st.markdown("---")
        
        # Filter
        col1, col2 = st.columns([1, 3])
        with col1:
            filter_kelas = st.selectbox(
                "Filter Kelas",
                ["Semua"] + sorted(df_db['Kelas'].unique().tolist())
            )
        
        if filter_kelas != "Semua":
            df_tampil = df_db[df_db['Kelas'] == filter_kelas]
        else:
            df_tampil = df_db
        
        # Tampilkan tabel
        st.subheader(f"📋 Daftar Siswa ({len(df_tampil)} siswa)")
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Unduh CSV
        csv = df_tampil.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f"database_siswa_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )
        
        st.markdown("---")
        
        # Hapus data
        with st.expander("🗑️ Hapus Data"):
            if st.button("Hapus Semua Data", type="secondary"):
                st.session_state.database_siswa = []
                st.success("✅ Semua data dihapus.")
                st.rerun()

# ================================================================
# MENU 3: ANALISIS KAUSAL
# ================================================================

elif menu == "📊 Analisis Kausal":
    st.title("📊 Analisis Kausal (ATE)")
    st.markdown("### Efek Kausal Setiap Faktor terhadap Prestasi Akademik")
    
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
# MENU 4: ANALISIS SHAP
# ================================================================

elif menu == "📈 Analisis SHAP":
    st.title("📈 Analisis SHAP")
    st.markdown("### Kontribusi Prediktif Setiap Faktor")
    
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
    bars = ax.barh(df_shap['Konstruk'], df_shap['Mean_SHAP'], color='steelblue', alpha=0.7)
    ax.set_xlabel('Mean |SHAP Value|')
    ax.set_title('Kontribusi Fitur terhadap Prediksi')
    
    for bar, val in zip(bars, df_shap['Mean_SHAP']):
        ax.text(val + 0.02, bar.get_y() + bar.get_height()/2, f'{val:.4f}', va='center', fontsize=9)
    
    st.pyplot(fig)
    st.dataframe(df_shap, use_container_width=True, hide_index=True)

# ================================================================
# MENU 5: REKOMENDASI
# ================================================================

else:
    st.title("💡 Rekomendasi Intervensi")
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
