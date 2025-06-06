# Pantara 🕵️‍♂️

**Pantara** adalah sebuah alat OSINT (Open Source Intelligence) berbasis Streamlit untuk memantau aktivitas digital terkait APK bertema pemerintah, mention di sosial media, serta ancaman phishing, menggunakan Google Custom Search API.

## 🚀 Fitur Utama

- 🔍 **Pencarian APK Pemerintah** dari apkpure, apkcombo, dan Google Play
- 🌐 **Monitoring Mention di Social Media** (Facebook, Instagram, Twitter, YouTube, dsb)
- 🎣 **Phishing Intelligence** (Opsional/Planned)
- 📅 Filter waktu pencarian berbasis kalender

## 📸 Screenshot
![pantara preview](preview.png) <!-- tambahkan gambar jika ada -->

## ⚙️ Instalasi

1. Clone repository:
    ```bash
    git clone https://github.com/revanzagenius/Pantara.git
    cd Pantara
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Buat file `config.py`:
    ```python
    # config.py
    MOBILE_API_KEY = "your_google_api_key"
    MOBILE_CX = "your_cx_id"

    SOCMED_API_KEY = "your_google_api_key"
    SOCMED_CX = "your_cx_id"
    ```

4. Jalankan aplikasi:
    ```bash
    streamlit run main.py
    ```

## ☁️ Deploy ke Streamlit Cloud

1. Push ke GitHub
2. Login ke [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Klik “New App” → pilih repo `Pantara`
4. Atur file utama `main.py` dan tambahkan Secrets:
    - `MOBILE_API_KEY`
    - `MOBILE_CX`
    - `SOCMED_API_KEY`
    - `SOCMED_CX`

## 🛡️ Lisensi

MIT License © 2025 revanzagenius
