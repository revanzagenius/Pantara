import streamlit as st
import pandas as pd
import requests, time
from datetime import datetime
from config import MOBILE_API_KEY, MOBILE_CX

def run_mobile_apps():
    st.subheader("📱 Pencarian APK Pemerintah (Google Custom Search)")

    with st.form("mobile_form"):
        sumber = st.selectbox("Pilih sumber APK", ["apkpure", "apkcombo", "google play"])
        
        tanggal_mulai = st.date_input("🗓️ Tanggal mulai (opsional)", value=None)
        aplikasi = st.text_input("Nama aplikasi yang ingin dicari", placeholder="Contoh: m pajak, pedulilindungi")
        jumlah = st.selectbox("Jumlah hasil", [10, 20, 30])
        submit_mobile = st.form_submit_button("🚀 Jalankan Dorking")

    def google_search_mobile(query, max_results=10, date_restrict=None):
        results = []
        for start in range(1, max_results + 1, 10):
            url = 'https://www.googleapis.com/customsearch/v1'
            params = {
                'q': query,
                'key': MOBILE_API_KEY,
                'cx': MOBILE_CX,
                'start': start,
            }
            if date_restrict:
                params['dateRestrict'] = date_restrict

            try:
                response = requests.get(url, params=params)
                data = response.json()
                items = data.get('items', [])
                for item in items:
                    results.append({
                        'query': query,
                        'title': item.get('title'),
                        'link': item.get('link'),
                        'snippet': item.get('snippet')
                    })
            except Exception as e:
                st.error(f"[!] Error: {e}")
            time.sleep(1)
        return results

    if submit_mobile:
        # Cek dan konversi rentang tanggal ke dateRestrict
        date_restrict = None
        if tanggal_mulai:
            delta = (datetime.now().date() - tanggal_mulai).days
            if delta <= 1:
                date_restrict = "d1"
            elif delta <= 7:
                date_restrict = "w1"
            elif delta <= 30:
                date_restrict = "m1"
            else:
                st.warning("⚠️ Rentang waktu lebih dari 30 hari, hasil akan mencakup semua waktu.")

        if not aplikasi.strip():
            st.warning("⚠️ Mohon masukkan nama aplikasi.")
        else:
            if sumber == "apkpure":
                query = f'site:apkpure.com "{aplikasi}"'
            elif sumber == "apkcombo":
                query = f'site:apkcombo.com "{aplikasi}" filetype:apk'
            elif sumber == "google play":
                query = f'site:play.google.com "{aplikasi}" -site:google.com'
            else:
                query = aplikasi

            st.info(f"🔍 Menjalankan dorking untuk: `{query}`")
            with st.spinner("Sedang mencari..."):
                hasil = google_search_mobile(query, int(jumlah), date_restrict)

            if hasil:
                df = pd.DataFrame(hasil)
                st.success(f"✅ Ditemukan {len(df)} hasil!")
                st.dataframe(df)
                csv = df.to_csv(index=False)
                st.download_button("⬇️ Download CSV", csv, file_name="mobile_apps_results.csv", mime="text/csv")
            else:
                st.info("😕 Tidak ada hasil ditemukan.")
