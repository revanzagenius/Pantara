# social_media.py
import streamlit as st
import pandas as pd
import requests, time
from datetime import datetime
from config import SOCMED_API_KEY, SOCMED_CX

def run_social_media():
    st.subheader("🌐 Pencarian Mentions Social Media (GCS API)")

    with st.form("socmed_form"):
        keyword = st.text_input("🔍 Kata kunci", value="Bank BTN", placeholder="Contoh: Bank BTN, Telkom, PLN, dll")
        platforms = st.multiselect("🌐 Pilih platform", [
            "Facebook", "Instagram", "YouTube", "Twitter", "LinkedIn",
            "TikTok", "Telegram", "Reddit", "GitHub", "Vimeo",
            "RSS Feed", "Comment/Forum", "Scribd"
        ], default=["Facebook", "Instagram", "YouTube"])
        tanggal_mulai = st.date_input("🗓️ Tanggal mulai pencarian (opsional)", value=None)
        jumlah = st.selectbox("📦 Jumlah hasil per query", [10, 20, 30])
        submit_socmed = st.form_submit_button("🚀 Jalankan Dorking Social Media")

    platform_map = {
        "Facebook": f'site:facebook.com "{keyword}"',
        "Instagram": f'site:instagram.com "{keyword}"',
        "YouTube": f'site:youtube.com "{keyword}"',
        "Twitter": f'site:twitter.com "{keyword}"',
        "LinkedIn": f'site:linkedin.com "{keyword}"',
        "TikTok": f'site:tiktok.com "{keyword}"',
        "Telegram": f'site:t.me "{keyword}"',
        "Reddit": f'site:reddit.com "{keyword}"',
        "GitHub": f'site:github.com "{keyword}"',
        "Vimeo": f'site:vimeo.com "{keyword}"',
        "RSS Feed": [f'inurl:rss "{keyword}"', f'inurl:feed "{keyword}"'],
        "Comment/Forum": [f'inurl:comment "{keyword}"', f'inurl:forum "{keyword}"'],
        "Scribd": f'"{keyword}" site:scribd.com'
    }

    def google_search_socmed(query, num_pages=3, date_restrict=None):
        links = set()
        for page in range(num_pages):
            start = page * 10 + 1
            url = f"https://www.googleapis.com/customsearch/v1"
            params = {
                'q': query,
                'key': SOCMED_API_KEY,
                'cx': SOCMED_CX,
                'start': start
            }
            if date_restrict:
                params["dateRestrict"] = date_restrict

            response = requests.get(url, params=params)
            if response.status_code == 200:
                results = response.json()
                if "items" in results:
                    for item in results["items"]:
                        links.add(item["link"])
            time.sleep(1)
        return links

    if submit_socmed:
        if not platforms:
            st.warning("⚠️ Pilih minimal satu platform.")
        else:
            # Hitung selisih hari dari tanggal_mulai
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
                    st.warning("⚠️ Tanggal pencarian melebihi 30 hari, hasil akan mencakup semua waktu.")

            final_queries = []
            for plat in platforms:
                q = platform_map[plat]
                final_queries.extend(q) if isinstance(q, list) else final_queries.append(q)

            all_links = set()
            progress = st.progress(0)
            for idx, query in enumerate(final_queries):
                st.write(f"🔍 Mencari: `{query}`")
                results = google_search_socmed(query, num_pages=int(jumlah)//10, date_restrict=date_restrict)
                all_links.update(results)
                progress.progress((idx + 1) / len(final_queries))
            progress.empty()

            if all_links:
                df = pd.DataFrame(sorted(all_links), columns=["URL"])
                st.success(f"✅ Total hasil ditemukan: {len(df)}")
                st.dataframe(df)
                csv = df.to_csv(index=False)
                st.download_button("⬇️ Download CSV", csv, file_name="social_media_results.csv", mime="text/csv")
            else:
                st.info("😕 Tidak ada hasil ditemukan.")
