import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Prestasi Akademik", page_icon="📊", layout="wide")

# ================================================================
# DATA HASIL ANALISIS
# ================================================================

data_ate = {
    'Konstruk': ['Fasilitas Sekolah', 'Keterlibatan Orang Tua', 'Self-Efficacy Akademik',
                 'Kecemasan Akademik', 'Kemalasan Belajar', 'Motivasi Belajar',
                 'Harapan Orang Tua', 'Dukungan Sekolah'],
    'ATE': [2.4295, 2.2100, 2.0698, 0.4522, -0.0902, -0.2850, -1.5323, -3.8797],
    'Arah': ['Positif', 'Positif', 'Positif', 'Positif', 'Negatif', 'Negatif', 'Negatif', 'Negatif']
}

data_shap = {
    'Konstruk': ['Self-Efficacy Akademik', 'Keterlibatan Orang Tua', 'Harapan Orang Tua',
                 'Dukungan Sekolah', 'Motivasi Belajar', 'Kecemasan Akademik',
                 'Fasilitas Sekolah', 'Kemalasan Belajar'],
    'Mean_SHAP': [0.8008, 0.6806, 0.5823, 0.4352, 0.3667, 0.1308, 0.0654, 0.0793]
}

df_ate = pd.DataFrame(data_ate)
df_shap = pd.DataFrame(data_shap)

# ================================================================
# SIDEBAR
# ================================================================

st.sidebar.title("📊 Navigasi")
menu = st.sidebar.radio(
    "Pilih Menu",
    ["🏠 Ringkasan", "📈 Analisis Kausal", "📊 Analisis SHAP", "🔗 Integrasi", "💡 Rekomendasi"]
)

# ================================================================
# MENU 1: RINGKASAN
# ================================================================

if menu == "🏠 Ringkasan":
    st.title("📊 Dashboard Analisis Prestasi Akademik")
    st.markdown("### SMP Negeri 6 Salatiga")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Jumlah Siswa", "117")
    with col2:
        st.metric("📈 Rata-rata Nilai", "83.78")
    with col3:
        st.metric("🎯 R² Model", "0.85")
    with col4:
        st.metric("✅ Faktor Signifikan", "3")
    
    st.subheader("📊 Ringkasan Hasil Analisis")
    st.dataframe(df_ate, use_container_width=True)

# ================================================================
# MENU 2: ANALISIS KAUSAL
# ================================================================

elif menu == "📈 Analisis Kausal":
    st.title("📈 Analisis Kausal (ATE)")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['green' if x > 0 else 'red' for x in df_ate['ATE']]
    bars = ax.barh(df_ate['Konstruk'], df_ate['ATE'], color=colors, alpha=0.7)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    ax.set_xlabel('ATE (Average Treatment Effect)')
    ax.set_title('Efek Kausal terhadap Prestasi Akademik')
    
    for bar, val in zip(bars, df_ate['ATE']):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2, f'{val:.2f}', va='center')
    
    st.pyplot(fig)
    st.dataframe(df_ate, use_container_width=True)

# ================================================================
# MENU 3: ANALISIS SHAP
# ================================================================

elif menu == "📊 Analisis SHAP":
    st.title("📊 Analisis SHAP")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    df_sorted = df_shap.sort_values('Mean_SHAP', ascending=True)
    bars = ax.barh(df_sorted['Konstruk'], df_sorted['Mean_SHAP'], color='steelblue', alpha=0.7)
    ax.set_xlabel('Mean |SHAP Value|')
    ax.set_title('Kontribusi Fitur terhadap Prediksi')
    
    for bar, val in zip(bars, df_sorted['Mean_SHAP']):
        ax.text(val + 0.02, bar.get_y() + bar.get_height()/2, f'{val:.4f}', va='center', fontsize=9)
    
    st.pyplot(fig)
    st.dataframe(df_shap.sort_values('Mean_SHAP', ascending=False), use_container_width=True)

# ================================================================
# MENU 4: INTEGRASI
# ================================================================

elif menu == "🔗 Integrasi":
    st.title("🔗 Integrasi SCM dan SHAP")
    
    df_integrasi = pd.merge(df_ate, df_shap, on='Konstruk', how='inner')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['green' if x > 0 else 'red' for x in df_integrasi['ATE']]
    ax.scatter(df_integrasi['ATE'], df_integrasi['Mean_SHAP'], s=100, c=colors, alpha=0.7, edgecolors='black')
    
    for _, row in df_integrasi.iterrows():
        ax.annotate(row['Konstruk'], (row['ATE'], row['Mean_SHAP']), fontsize=8, ha='center')
    
    ax.axhline(y=df_integrasi['Mean_SHAP'].mean(), color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    ax.set_xlabel('ATE (Efek Kausal)')
    ax.set_ylabel('Mean |SHAP| (Kontribusi)')
    ax.set_title('Integrasi ATE dan SHAP')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    st.dataframe(df_integrasi, use_container_width=True)

# ================================================================
# MENU 5: REKOMENDASI
# ================================================================

else:
    st.title("💡 Rekomendasi Intervensi")
    
    st.success("""
    ### ✅ PRIORITAS TINGGI
    
    **1. Fasilitas Sekolah** (ATE: +2.43)
    - Tingkatkan kualitas perpustakaan dan laboratorium
    
    **2. Self-Efficacy Akademik** (ATE: +2.07)
    - Program penguatan kepercayaan diri siswa
    
    **3. Keterlibatan Orang Tua** (ATE: +2.21)
    - Program parenting dan komunikasi rutin
    """)
    
    st.warning("""
    ### ⚠️ PERLU EVALUASI
    
    **1. Dukungan Sekolah** (ATE: -3.88)
    - Evaluasi program pendampingan, kurangi intervensi berlebihan
    
    **2. Harapan Orang Tua** (ATE: -1.53)
    - Edukasi orang tua tentang tekanan belajar
    """)
