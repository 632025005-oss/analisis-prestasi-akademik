import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="Dashboard Analisis Prestasi", page_icon="🔍", layout="wide")

# ================================================================
# DATA BASELINE & BOBOT (DARI HASIL ANALISIS)
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

# Bobot pengaruh (dari ATE × SHAP)
BOBOT_PENGARUH = {
    'Self-Efficacy Akademik': 2.0698 * 0.8008,   # +1.658
    'Keterlibatan Orang Tua': 2.2100 * 0.6806,   # +1.504
    'Harapan Orang Tua': -1.5323 * 0.5823,       # -0.892
    'Dukungan Sekolah': -3.8797 * 0.4352,        # -1.688
    'Motivasi Belajar': -0.2850 * 0.3667,        # -0.105
    'Kecemasan Akademik': 0.4522 * 0.1308,       # +0.059
    'Fasilitas Sekolah': 2.4295 * 0.0654,        # +0.159
    'Kemalasan Belajar': -0.0902 * 0.0793,       # -0.007
}

RATA_RATA_NILAI = 83.78
STD_NILAI = 3.64

# ================================================================
# SESSION STATE
# ================================================================

if 'database_siswa' not in st.session_state:
    st.session_state.database_siswa = []

# ================================================================
# FUNGSI ANALISIS KAUSAL
# ================================================================

def analisis_kausal(nilai_akademik, profil_siswa):
    """
    Menganalisis faktor penyebab nilai akademik siswa
    berdasarkan perbandingan profil dengan baseline
    """
    selisih_nilai = nilai_akademik - RATA_RATA_NILAI
    
    kontribusi = {}
    for aspek, nilai_input in profil_siswa.items():
        selisih_aspek = nilai_input - BASELINE_ASPEK[aspek]
        # Kontribusi = selisih × bobot
        kontribusi[aspek] = selisih_aspek * BOBOT_PENGARUH[aspek]
    
    # Normalisasi kontribusi agar total = selisih nilai
    total_kontribusi = sum(kontribusi.values())
    
    if abs(total_kontribusi) > 0.01:
        # Skala faktor agar proporsional
        skala = selisih_nilai / total_kontribusi
        kontribusi = {k: v * skala for k, v in kontribusi.items()}
    
    return selisih_nilai, kontribusi


def kategori_nilai(nilai):
    """Kategori posisi nilai siswa"""
    if nilai >= 88:
        return "🌟 Sangat Baik", "success"
    elif nilai >= 84:
        return "✅ Baik", "info"
    elif nilai >= 80:
        return "⚠️ Cukup", "warning"
    else:
        return "❗ Perlu Perhatian", "error"

# ================================================================
# SIDEBAR
# ================================================================

st.sidebar.title("🔍 Navigasi")
menu = st.sidebar.radio(
    "Pilih Menu",
    ["🔍 Analisis Sebab-Akibat", "🗄️ Database Siswa", "📊 Analisis Kausal Global", "📈 Analisis SHAP"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**SMP Negeri 6 Salatiga**\n\n"
    "Dashboard Analisis Sebab-Akibat Prestasi Akademik\n\n"
    "© 2026"
)

# ================================================================
# MENU 1: ANALISIS SEBAB-AKIBAT
# ================================================================

if menu == "🔍 Analisis Sebab-Akibat":
    st.title("🔍 Analisis Sebab-Akibat Nilai Siswa")
    st.markdown("### Masukkan data siswa untuk menganalisis faktor penyebab nilai akademiknya")
    
    st.markdown("---")
    
    # ============================================================
    # FORM DATA SISWA
    # ============================================================
    
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
    
    # ============================================================
    # INPUT NILAI AKADEMIK RIIL
    # ============================================================
    
    st.subheader("📊 Nilai Akademik Siswa")
    st.caption(f"Rata-rata nilai rapor siswa (baseline sekolah: {RATA_RATA_NILAI})")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        nilai_akademik = st.number_input(
            "Nilai Akademik (dari rapor)",
            min_value=60.0,
            max_value=100.0,
            value=83.78,
            step=0.01,
            format="%.2f"
        )
    with col2:
        st.metric(
            "Posisi Nilai",
            f"{nilai_akademik - RATA_RATA_NILAI:+.2f}",
            "dari rata-rata"
        )
    
    st.markdown("---")
    
    # ============================================================
    # INPUT PROFIL SISWA
    # ============================================================
    
    st.subheader("📝 Profil Siswa")
    st.caption("Skala 1-5 (1=Sangat Rendah, 5=Sangat Tinggi)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🧠 Aspek Internal**")
        input_self_efficacy = st.slider("Self-Efficacy Akademik", 1.0, 5.0, 4.63, 0.1)
        input_motivasi = st.slider("Motivasi Belajar", 1.0, 5.0, 2.52, 0.1)
        input_kecemasan = st.slider("Kecemasan Akademik", 1.0, 5.0, 2.89, 0.1)
        input_kemalasan = st.slider("Kemalasan Belajar", 1.0, 5.0, 1.49, 0.1)
    
    with col2:
        st.markdown("**🌍 Aspek Eksternal**")
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
    
    # ============================================================
    # PROSES ANALISIS KAUSAL
    # ============================================================
    
    selisih_nilai, kontribusi = analisis_kausal(nilai_akademik, profil_siswa)
    kategori, tipe = kategori_nilai(nilai_akademik)
    
    st.markdown("---")
    
    # ============================================================
    # HASIL ANALISIS
    # ============================================================
    
    st.subheader("🎯 Hasil Analisis Sebab-Akibat")
    
    if nama_siswa:
        st.markdown(f"**Siswa**: {nama_siswa} | **Kelas**: {kelas_siswa} | **Absen**: {absen_siswa}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Nilai Akademik", f"{nilai_akademik:.2f}")
    with col2:
        delta_text = f"{selisih_nilai:+.2f} dari rata-rata"
        st.metric("📈 Posisi", delta_text)
    with col3:
        st.metric("🏆 Kategori", kategori)
    
    # ============================================================
    # GRAFIK POSISI NILAI
    # ============================================================
    
    st.markdown("---")
    st.subheader("📍 Posisi Nilai Siswa")
    
    fig, ax = plt.subplots(figsize=(12, 2.5))
    
    # Range nilai
    nilai_min, nilai_max = 75, 95
    
    # Warna background
    ax.barh(0, RATA_RATA_NILAI - nilai_min, left=nilai_min, 
            color='lightcoral', alpha=0.3, label='Di bawah rata-rata')
    ax.barh(0, nilai_max - RATA_RATA_NILAI, left=RATA_RATA_NILAI,
            color='lightgreen', alpha=0.3, label='Di atas rata-rata')
    
    # Garis rata-rata
    ax.axvline(RATA_RATA_NILAI, color='red', linestyle='--', linewidth=2, 
               label=f'Rata-rata ({RATA_RATA_NILAI})')
    
    # Titik nilai siswa
    ax.scatter(nilai_akademik, 0, s=300, color='blue', zorder=5, 
               edgecolors='black', linewidth=2, label=f'Nilai {nama_siswa or "Siswa"}')
    
    ax.set_xlim(nilai_min, nilai_max)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xlabel('Nilai Akademik', fontsize=12)
    ax.set_title(f'Posisi Nilai: {nilai_akademik:.2f} (selisih {selisih_nilai:+.2f})', fontsize=14)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.4), ncol=4)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # ============================================================
    # ANALISIS FAKTOR PENYEBAB
    # ============================================================
    
    st.markdown("---")
    st.subheader("🔍 Faktor Penyebab Nilai Siswa")
    st.caption(f"Nilai siswa berada {abs(selisih_nilai):.2f} poin {'di atas' if selisih_nilai > 0 else 'di bawah'} rata-rata. Berikut faktor yang mempengaruhinya:")
    
    # Buat DataFrame kontribusi
    df_kontribusi = pd.DataFrame([
        {
            'Aspek': k, 
            'Kontribusi': v,
            'Nilai_Siswa': profil_siswa[k],
            'Baseline': BASELINE_ASPEK[k],
            'Selisih': profil_siswa[k] - BASELINE_ASPEK[k]
        }
        for k, v in kontribusi.items()
    ]).sort_values('Kontribusi', key=abs, ascending=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['green' if x > 0 else 'red' for x in df_kontribusi['Kontribusi']]
        bars = ax.barh(df_kontribusi['Aspek'], df_kontribusi['Kontribusi'], 
                       color=colors, alpha=0.7, edgecolor='black')
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
        ax.set_xlabel('Kontribusi terhadap Nilai (poin)', fontsize=12)
        ax.set_title('Kontribusi Setiap Faktor', fontsize=14)
        
        for bar, val in zip(bars, df_kontribusi['Kontribusi']):
            pos = val + 0.05 if val > 0 else val - 0.15
            ax.text(pos, bar.get_y() + bar.get_height()/2, 
                    f'{val:+.2f}', va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("### 📖 Cara Membaca")
        st.markdown("""
        **🟢 Hijau (Positif)**:
        Faktor ini **meningkatkan** nilai siswa
        
        **🔴 Merah (Negatif)**:
        Faktor ini **menurunkan** nilai siswa
        
        **Angka**:
        Kontribusi dalam **poin nilai**
        """)
    
    # ============================================================
    # TABEL DETAIL
    # ============================================================
    
    st.markdown("---")
    st.subheader("📋 Detail Perbandingan dengan Rata-rata Sekolah")
    
    tabel = df_kontribusi.copy()
    tabel['Status'] = tabel['Selisih'].apply(
        lambda x: '⬆️ Di atas rata-rata' if x > 0 else '⬇️ Di bawah rata-rata' if x < 0 else '➡️ Sama'
    )
    tabel = tabel[['Aspek', 'Nilai_Siswa', 'Baseline', 'Selisih', 'Kontribusi', 'Status']]
    tabel.columns = ['Aspek', 'Nilai Siswa', 'Rata-rata Sekolah', 'Selisih', 'Kontribusi (poin)', 'Status']
    tabel = tabel.sort_values('Kontribusi (poin)', key=abs, ascending=False)
    
    st.dataframe(tabel, use_container_width=True, hide_index=True)
    
    # ============================================================
    # REKOMENDASI PERSONAL
    # ============================================================
    
    st.markdown("---")
    st.subheader("💡 Rekomendasi Personal")
    
    faktor_positif = df_kontribusi[df_kontribusi['Kontribusi'] > 0.3].sort_values('Kontribusi', ascending=False)
    faktor_negatif = df_kontribusi[df_kontribusi['Kontribusi'] < -0.3].sort_values('Kontribusi')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("### ✅ KEKUATAN SISWA")
        st.caption("Faktor yang sudah baik dan meningkatkan nilai:")
        if len(faktor_positif) > 0:
            for _, row in faktor_positif.iterrows():
                st.markdown(f"""
                **{row['Aspek']}** 
                - Kontribusi: **{row['Kontribusi']:+.2f} poin**
                - Nilai: {row['Nilai_Siswa']:.2f} (baseline: {row['Baseline']:.2f})
                - 📌 **Pertahankan!**
                """)
        else:
            st.info("Belum ada faktor kekuatan dominan")
    
    with col2:
        st.error("### ⚠️ PERLU DIPERBAIKI")
        st.caption("Faktor yang menurunkan nilai siswa:")
        if len(faktor_negatif) > 0:
            for _, row in faktor_negatif.iterrows():
                st.markdown(f"""
                **{row['Aspek']}**
                - Kontribusi: **{row['Kontribusi']:+.2f} poin**
                - Nilai: {row['Nilai_Siswa']:.2f} (baseline: {row['Baseline']:.2f})
                - 📌 **Perlu ditingkatkan!**
                """)
        else:
            st.info("Tidak ada faktor negatif signifikan")
    
    # ============================================================
    # SIMPAN KE DATABASE
    # ============================================================
    
    st.markdown("---")
    st.subheader("💾 Simpan ke Database")
    
    if not nama_siswa:
        st.warning("⚠️ Isi **Nama Siswa** terlebih dahulu sebelum menyimpan.")
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
                    'Selisih dari Rata-rata': round(selisih_nilai, 2),
                    'Kategori': kategori,
                    'Self-Efficacy': input_self_efficacy,
                    'Keterlibatan Ortu': input_keterlibatan,
                    'Harapan Ortu': input_harapan,
                    'Dukungan Sekolah': input_dukungan,
                    'Motivasi': input_motivasi,
                    'Kecemasan': input_kecemasan,
                    'Fasilitas': input_fasilitas,
                    'Kemalasan': input_kemalasan,
                    'Faktor Positif Terkuat': faktor_positif.iloc[0]['Aspek'] if len(faktor_positif) > 0 else '-',
                    'Faktor Negatif Terkuat': faktor_negatif.iloc[0]['Aspek'] if len(faktor_negatif) > 0 else '-',
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
        st.info("📭 Belum ada data siswa. Silakan input di menu **🔍 Analisis Sebab-Akibat**.")
    else:
        df_db = pd.DataFrame(st.session_state.database_siswa)
        
        # Statistik
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total Siswa", len(df_db))
        with col2:
            st.metric("📊 Rata-rata Nilai", f"{df_db['Nilai Akademik'].mean():.2f}")
        with col3:
            st.metric("🏆 Nilai Tertinggi", f"{df_db['Nilai Akademik'].max():.2f}")
        with col4:
            st.metric("📉 Nilai Terendah", f"{df_db['Nilai Akademik'].min():.2f}")
        
        st.markdown("---")
        
        # Filter
        col1, col2 = st.columns([1, 3])
        with col1:
            filter_kelas = st.selectbox(
                "Filter Kelas",
                ["Semua"] + sorted(df_db['Kelas'].unique().tolist())
            )
        
        df_tampil = df_db if filter_kelas == "Semua" else df_db[df_db['Kelas'] == filter_kelas]
        
        st.subheader(f"📋 Daftar Siswa ({len(df_tampil)} siswa)")
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
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
            with st.expander("🗑️ Hapus Data"):
                if st.button("Hapus Semua", type="secondary"):
                    st.session_state.database_siswa = []
                    st.rerun()

# ================================================================
# MENU 3: ANALISIS KAUSAL GLOBAL
# ================================================================

elif menu == "📊 Analisis Kausal Global":
    st.title("📊 Analisis Kausal Global")
    st.markdown("### Efek Kausal Setiap Faktor (dari seluruh data)")
    
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

else:
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
