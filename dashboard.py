
- **ATE** = *Average Treatment Effect* (efek kausal) tiap faktor
- **baseline** = rata-rata sekolah per faktor
- **faktor_skala** = 0.35 (koefisien konservatif dari hasil validasi model)

**Bukan prediksi langsung dari Random Forest**, melainkan prediksi kausal
yang menjelaskan *mengapa* nilai diprediksi demikian.

**Rentang kepercayaan** ± {STD_NILAI:.2f} poin diambil dari simpangan baku nilai
akademik di penelitian (n=117 siswa).
""")

# ================================================================
# MODUL 03 — FAKTOR PENGARUH
# ================================================================

elif st.session_state.current_page == "kausal":
top_bar("🔬 Faktor Pengaruh", "Modul 03 · Sebab-akibat & kepentingan prediktif")

hero_header(
"MODUL 03 · FAKTOR PENGARUH",
"Apa yang <em>menyebabkan</em><br>dan apa yang <em>memprediksi</em>?",
"Analisis sebab-akibat (ATE) dan tingkat kepentingan prediktif (SHAP) untuk 8 faktor "
"yang mempengaruhi prestasi akademik siswa.",
[("CAUSAL · ATE", "blue"), ("PREDICTIVE · SHAP", "purple"), ("TINGKAT SEKOLAH", "mint")],
)

section_header("01", "Apa Bedanya?", "DUA JENIS PENGARUH")
st.markdown("""
<div class="info-box blue" style="margin-bottom:1rem;">
<div class="info-title">📖 Perbedaan Mendasar</div>
<div class="info-text">
    <b>🟢 Sebab-Akibat (ATE)</b> menjawab: <i>"Jika faktor X diubah, apakah nilai siswa berubah?"</i><br>
    <b>🟣 Kepentingan Prediktif (SHAP)</b> menjawab: <i>"Faktor apa yang paling dipakai model untuk memprediksi?"</i>
    <br><br>
    Keduanya <b>berbeda</b>: faktor bisa penting untuk prediksi tapi bukan penyebab (dan sebaliknya).
</div>
</div>""", unsafe_allow_html=True)

tab_ate, tab_shap = st.tabs(["🟢 Sebab-Akibat (ATE)", "🟣 Kepentingan Prediktif (SHAP)"])

# --- TAB ATE ---
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
tabel_ate["Arah"] = tabel_ate["Pengaruh"].apply(lambda x: "🟢 MENINGKATKAN" if x>0 else "🔴 MENURUNKAN" if x<0 else "➖ NETRAL")
tabel_ate = tabel_ate.sort_values("Pengaruh", ascending=False)[["Faktor","Penjelasan","Arah","Pengaruh"]]
tabel_ate.columns = ["Faktor","Artinya untuk Nilai Siswa","Arah","Skor ATE"]
st.dataframe(tabel_ate, use_container_width=True, hide_index=True,
             column_config={"Skor ATE": st.column_config.NumberColumn(format="%+.4f")})

# --- TAB SHAP ---
with tab_shap:
df_shap = pd.DataFrame([{"Faktor": k, "Kepentingan": v} for k, v in KEPENTINGAN_DATA.items()])
ranked = df_shap.sort_values("Kepentingan", ascending=False).reset_index(drop=True)
a, b_, c = st.columns(3)
with a: stat_card("Faktor #1", ranked.iloc[0]["Faktor"], "⭐⭐⭐ Sangat menentukan", "purple")
with b_: stat_card("Faktor #2", ranked.iloc[1]["Faktor"], "⭐⭐ Cukup menentukan", "blue")
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

with st.expander("📌 Catatan Teknis"):
st.markdown("""
**ATE (Average Treatment Effect)** dihitung dengan DoWhy library — Structural Causal Model
dengan backdoor linear regression. Nilai positif = meningkatkan nilai, negatif = menurunkan.

**SHAP (SHapley Additive exPlanations)** menggunakan TreeExplainer pada model Random Forest
(n_estimators=100, max_depth=7). Nilai mean |SHAP| menunjukkan seberapa sering faktor
dipakai model untuk prediksi.

**Catatan penting**: SHAP ≠ kausal. Nilai SHAP hanya menunjukkan kontribusi prediktif.
Arah sebab-akibat tetap mengacu pada ATE dan DAG.
""")

# ================================================================
# MODUL 04 — REKOMENDASI
# ================================================================

elif st.session_state.current_page == "rekomendasi":
top_bar("💡 Rekomendasi", "Modul 04 · Intervensi tingkat sekolah & personal")

hero_header(
"MODUL 04 · REKOMENDASI",
"Dari analisis<br><span class='accent'>menjadi tindakan.</span>",
"Rekomendasi intervensi tingkat sekolah berdasarkan CEI & kuadran prioritas, "
"serta catatan personal untuk guru per siswa.",
[("PRIORITAS", "yellow"), ("SEKOLAH", "mint"), ("PERSONAL", "blue")],
)

tab_umum, tab_personal = st.tabs(["🏫 Rekomendasi Umum (Tingkat Sekolah)", "🎯 Catatan untuk Guru (Personal)"])

# --- TAB 1: REKOMENDASI UMUM ---
with tab_umum:
section_header("01", "Prioritas Intervensi", "FAKTOR DENGAN PENGARUH TERKUAT")
c1, c2 = st.columns(2)
with c1:
    st.markdown("""<div class="card card-mint">
        <div class="card-label">🟢 FAKTOR YANG PERLU DIPERKUAT</div>
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
                <div style="font-weight:800;font-size:.88rem;">{i:02d} · {name}</div>
                <div style="font-weight:800;color:#10B981;font-size:.78rem;">{label}</div>
            </div>
            <div style="font-size:.69rem;color:#5C6B85;margin-top:.35rem;">{terjemah_shap(KEPENTINGAN_DATA[name])}</div>
            <div style="font-size:.76rem;line-height:1.55;margin-top:.45rem;color:#475467;">{desc}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="card card-yellow">
        <div class="card-label">🔴 FAKTOR YANG PERLU DIEVALUASI</div>
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
                <div style="font-weight:800;font-size:.88rem;">{i:02d} · {name}</div>
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

# --- TAB 2: CATATAN UNTUK GURU ---
with tab_personal:
if len(st.session_state.database_siswa) == 0:
    st.warning("⚠️ Database masih kosong. Input siswa terlebih dahulu di Modul 01.")
else:
    df_db = pd.DataFrame(st.session_state.database_siswa)
    opsi = df_db.apply(lambda x: f"{x['Nama']} — {x['Kelas']} (Absen {x['Absen']})", axis=1).tolist()
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

    # Kesimpulan
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
                <div style="color:#5C6B85;font-size:.8rem;">{kelas} · Absen {absen:02d} · Nilai {nilai:.2f}</div>
            </div>
        </div>
        <div style="font-size:.95rem;line-height:1.75;color:#1F2A44;">
            Nilai saat ini <b>{abs(selisih):.2f} poin {posisi} rata-rata sekolah</b> ({RATA_RATA_NILAI:.2f}).
            <br><br>{narasi_neg}<br><br>{narasi_pos}<br><br>
            <b>Kategori:</b> <span style="color:{warna_kategori};">{simbol} {kategori}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Prioritas
    section_header("02", "Prioritas Perbaikan", "FOKUSKAN PADA 3 HAL INI")
    prioritas = neg.head(3)
    if len(prioritas) == 0:
        st.success("Tidak ada prioritas perbaikan mendesak.")
    else:
        cols = st.columns(len(prioritas))
        for i, (_, row) in enumerate(prioritas.iterrows()):
            with cols[i]:
                gap_val = row['Selisih']
                level = "🔴 Urgent" if gap_val < -1 else "🟡 Perhatian" if gap_val < -0.5 else "🟢 Monitor"
                st.markdown(f"""<div class="card" style="border-top:4px solid #EF5B67;min-height:200px;">
                    <div style="font-size:.65rem;font-weight:800;letter-spacing:1.5px;color:#EF5B67;">PRIORITAS {i+1}</div>
                    <div style="font-family:'Manrope';font-weight:800;font-size:1rem;margin:.6rem 0 .3rem;">{row['Aspek']}</div>
                    <div style="font-size:.7rem;color:#5C6B85;margin-bottom:.5rem;">{level}</div>
                    <div style="font-size:.75rem;line-height:1.6;color:#475467;">
                        Nilai siswa: <b>{row['Nilai_Siswa']:.2f}</b><br>
                        Rata-rata: <b>{row['Baseline']:.2f}</b><br>
                        <span style="color:#EF5B67;font-weight:700;">Selisih: {row['Selisih']:+.2f}</span>
                    </div></div>""", unsafe_allow_html=True)

    # Tindak lanjut
    section_header("03", "Tindak Lanjut", "CHECKLIST GURU & SISWA")
    TINDAK = {
        "Self-Efficacy Akademik": {
            "guru": ["Berikan tugas bertahap (mudah → sulit)", "Pujian spesifik atas usaha, bukan hasil",
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
            with st.expander(f"🎯 Prioritas {i+1}: {aspek}", expanded=(i==0)):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**👨‍🏫 Yang bisa dilakukan GURU:**")
                    for j, t in enumerate(tugas["guru"], 1):
                        st.markdown(f"""<div style="display:flex;gap:.7rem;padding:.6rem 0;border-bottom:1px solid #EEF2F7;">
                            <div style="width:22px;height:22px;border-radius:6px;background:#EAF1FF;color:#2563EB;
                                display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:800;flex-shrink:0;">{j}</div>
                            <div style="font-size:.82rem;line-height:1.55;color:#1F2A44;">{t}</div></div>""",
                            unsafe_allow_html=True)
                with c2:
                    st.markdown("**🎓 Yang bisa dilakukan SISWA:**")
                    for j, s in enumerate(tugas["siswa"], 1):
                        st.markdown(f"""<div style="display:flex;gap:.7rem;padding:.6rem 0;border-bottom:1px solid #EEF2F7;">
                            <div style="width:22px;height:22px;border-radius:6px;background:#E8F8F1;color:#10B981;
                                display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:800;flex-shrink:0;">{j}</div>
                            <div style="font-size:.82rem;line-height:1.55;color:#1F2A44;">{s}</div></div>""",
                            unsafe_allow_html=True)

    # Download catatan
    section_header("04", "Download Catatan", "ARSIP GURU")
    txt = f"""CATATAN KONSULTASI GURU — SAA
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
    st.download_button("📥 Download Catatan (.txt)", data=txt.encode("utf-8"),
                       file_name=f"catatan_{nama.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                       mime="text/plain", use_container_width=True)

# ================================================================
# MODUL 05 — MONITORING KELAS
# ================================================================

elif st.session_state.current_page == "monitoring":
top_bar("📊 Monitoring Kelas", "Modul 05 · Pantau perkembangan akademik per kelas")

hero_header(
"MODUL 05 · MONITORING KELAS",
"Pantau kelas.<br><span class='accent'>Deteksi lebih awal.</span>",
"Monitoring agregat per kelas: distribusi nilai, siswa yang perlu perhatian, "
"dan perbandingan antar kelas untuk mendukung keputusan akademik.",
[("PER KELAS", "yellow"), ("AGREGAT", "blue"), ("EARLY WARNING", "coral")],
)

if len(st.session_state.database_siswa) == 0:
st.warning("⚠️ Database masih kosong. Input siswa terlebih dahulu di Modul 01.")
st.stop()

df_db = pd.DataFrame(st.session_state.database_siswa)

# Filter kelas untuk wali kelas
if st.session_state.user_role == "wali_kelas" and st.session_state.user_kelas:
df_db = df_db[df_db["Kelas"].isin(st.session_state.user_kelas)]
st.info(f"ℹ️ Anda login sebagai Wali Kelas. Data ditampilkan hanya untuk kelas: **{', '.join(st.session_state.user_kelas)}**")

section_header("01", "Ringkasan Sekolah", "STATISTIK AGREGAT")
a, b_, c, d = st.columns(4)
with a: stat_card("Total Siswa", len(df_db), "siswa terarsip", "blue")
with b_: stat_card("Rata-rata", f"{df_db['Nilai Akademik'].mean():.2f}", "nilai seluruh siswa", "mint")
with c: stat_card("Tertinggi", f"{df_db['Nilai Akademik'].max():.2f}", "nilai maksimum", "yellow")
with d: stat_card("Terendah", f"{df_db['Nilai Akademik'].min():.2f}", "nilai minimum", "coral")

# Distribusi kategori
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

# Perbandingan antar kelas
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

# Early warning
section_header("04", "Early Warning", "SISWA YANG PERLU PERHATIAN")
st.markdown("""<div class="info-box coral" style="margin-bottom:1rem;">
<div class="info-title">⚠️ Kriteria</div>
<div class="info-text">
    Siswa dengan kategori <b>Perlu Perhatian</b> (nilai &lt; 80) atau nilai <b>di bawah rata-rata sekolah</b>
    lebih dari 1 standar deviasi.
</div></div>""", unsafe_allow_html=True)

df_perhatian = df_db[df_db["Nilai Akademik"] < RATA_RATA_NILAI - STD_NILAI].copy()
df_perhatian = df_perhatian.sort_values("Nilai Akademik")
if len(df_perhatian) == 0:
st.success("✅ Tidak ada siswa yang memerlukan perhatian khusus saat ini.")
else:
st.markdown(f"**{len(df_perhatian)} siswa** memerlukan perhatian:")
tabel_warn = df_perhatian[["Nama","Kelas","Absen","Nilai Akademik","Kategori","Dicatat Oleh"]].copy()
tabel_warn.columns = ["Nama","Kelas","Absen","Nilai","Kategori","Dicatat Oleh"]
st.dataframe(tabel_warn, use_container_width=True, hide_index=True)

# Download
csv = tabel_warn.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Daftar Early Warning (CSV)", data=csv,
                   file_name=f"early_warning_{datetime.now().strftime('%Y%m%d')}.csv",
                   mime="text/csv", use_container_width=True)

# Distribusi nilai per kelas
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

st.markdown(f"**Detail kelas {kelas_pilih}** — {len(df_k)} siswa")
st.dataframe(df_k[["Nama","Absen","Nilai Akademik","Kategori"]],
             use_container_width=True, hide_index=True)

# ================================================================
# MODUL 06 — PENGATURAN
# ================================================================

elif st.session_state.current_page == "pengaturan":
top_bar("⚙️ Pengaturan", "Modul 06 · Manajemen sistem & konfigurasi")

if not can_access_pengaturan(st.session_state.user_role):
st.error("🚫 Akses ditolak. Modul Pengaturan hanya dapat diakses oleh Administrator.")
st.stop()

hero_header(
"MODUL 06 · PENGATURAN",
"Konfigurasi<br><span class='accent'>dan tata kelola.</span>",
"Kelola akun pengguna, konfigurasi sekolah, dan pantau log aktivitas sistem SAA.",
[("ADMIN ONLY", "coral"), ("KONFIGURASI", "blue"), ("AUDIT", "purple")],
)

tab1, tab2, tab3 = st.tabs(["🏫 Konfigurasi Sekolah", "👥 Manajemen Pengguna", "📋 Log Aktivitas"])

# --- Konfigurasi ---
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

if st.button("💾 Simpan Konfigurasi", type="primary"):
    st.session_state.config = cfg
    save_config(cfg)
    add_log("Update konfigurasi sekolah")
    st.success("✅ Konfigurasi berhasil disimpan.")
    st.rerun()

# --- Users ---
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
    submit_user = st.form_submit_button("➕ Tambah Pengguna", use_container_width=True)

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
            st.success(f"✅ Pengguna '{new_u}' berhasil ditambahkan (catatan: penambahan user bersifat sesi ini saja; untuk permanen, edit di kode sumber).")
            st.rerun()

# --- Log ---
with tab3:
section_header("01", "Log Aktivitas", "AUDIT TRAIL")
st.markdown("""<div class="info-box blue" style="margin-bottom:1rem;">
    <div class="info-title">ℹ️ Info</div>
    <div class="info-text">Log menampilkan 200 aktivitas terakhir. Semua aksi pengguna tercatat
    untuk keperluan audit dan keamanan.</div></div>""", unsafe_allow_html=True)

if len(st.session_state.log) == 0:
    st.info("Belum ada aktivitas tercatat.")
else:
    df_log = pd.DataFrame(st.session_state.log)
    st.dataframe(df_log, use_container_width=True, hide_index=True)

    csv_log = df_log.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Log (CSV)", data=csv_log,
                       file_name=f"log_saa_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv", use_container_width=True)

    if st.button("🗑️ Bersihkan Log"):
        st.session_state.log = []
        save_log([])
        st.rerun()

# ================================================================
# END
# ================================================================
