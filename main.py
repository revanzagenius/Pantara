# main.py
import streamlit as st
from mobile_apps import run_mobile_apps
from social_media import run_social_media
from phishing_intel import run_phishing_intelligence

st.set_page_config(page_title="Dorking OSINT Tools", layout="wide")
st.title("🎯 Dorking OSINT Tools")

with st.sidebar:
    st.markdown("## 🧰 Menu Fitur OSINT")
    st.caption("Gunakan alat ini untuk melakukan pencarian berbasis dork Google.")
    fitur = st.radio("📌 Pilih Jenis Pencarian", [
        "📱 Mobile Apps",
        "🌐 Social Media",
        "🚨 Phishing Intelligence"
    ])
    st.divider()
    st.markdown("#### 👨‍💻 Tentang Tools Ini")
    st.caption("Dibuat untuk keperluan threat intelligence dan pencarian artefak digital dari berbagai platform online.")
    st.caption("Powered by Google Custom Search API")

if fitur == "📱 Mobile Apps":
    run_mobile_apps()
elif fitur == "🌐 Social Media":
    run_social_media()
elif fitur == "🚨 Phishing Intelligence":
    run_phishing_intelligence()
