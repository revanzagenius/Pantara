# phishing_intel.py
import streamlit as st
import pandas as pd
import requests, time
from config import SOCMED_API_KEY, SOCMED_CX

def run_phishing_intelligence():
    st.subheader("🚨 Pencarian Potensi Phishing dan Ancaman Digital")

    queries = [
        '"Bank BTN" inurl:login',
        '"Bank BTN" inurl:verify',
        '"Bank BTN" inurl:secure',
        '"Bank BTN" inurl:update',
        '"Bank BTN" inurl:reset',
        '"Bank BTN" inurl:auth',
        '"Bank BTN" intitle:login',
        '"Bank BTN" filetype:html',
        '"Bank BTN" filetype:php',
        '"Bank BTN" site:pastebin.com',
        '"Bank BTN" site:ghostbin.com',
        '"Bank BTN" site:anonfiles.com',
        '"Bank BTN" site:mega.nz',
    ]

    with st.form("phishing_form"):
        jumlah = st.selectbox("🔢 Jumlah hasil per query", [10, 20, 30])
        submit_phishing = st.form_submit_button("🚀 Jalankan Pencarian")

    def google_search_phishing(query, num_pages=3):
        links = set()
        for page in range(num_pages):
            start = page * 10 + 1
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={SOCMED_API_KEY}&cx={SOCMED_CX}&start={start}&sort=date"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    results = response.json()
                    for item in results.get("items", []):
                        links.add(item["link"])
                time.sleep(1)
            except Exception as e:
                st.error(f"Terjadi kesalahan saat mencari: {query} → {e}")
        return links

    if submit_phishing:
        all_links = set()
        progress = st.progress(0)
        for i, q in enumerate(queries):
            st.write(f"🔍 Mencari: `{q}`")
            result = google_search_phishing(q, num_pages=int(jumlah) // 10)
            all_links.update(result)
            progress.progress((i + 1) / len(queries))
        progress.empty()

        if all_links:
            df = pd.DataFrame(sorted(all_links), columns=["URL"])
            st.success(f"✅ Total hasil ditemukan: {len(df)}")
            st.dataframe(df)
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download CSV", csv, file_name="phishing_intel_results.csv", mime="text/csv")
        else:
            st.info("😕 Tidak ada hasil ditemukan.")
