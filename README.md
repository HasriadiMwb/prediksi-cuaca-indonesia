# 🌦️ Prediksi Cuaca Indonesia – Machine Learning + OpenWeather API

Aplikasi Streamlit interaktif yang menampilkan data cuaca real-time dari OpenWeather (5-day forecast, step 3 hours),
meliputi tabel, grafik minimalis, kondisi cuaca lokal (Bahasa Indonesia + emoji), prediksi suhu berikutnya menggunakan Linear Regression,
dan fitur ekspor hasil (CSV + PNG).

## Fitur
- Data real-time dari OpenWeather API (API key disematkan di script)
- 41 kota besar / ibu kota provinsi Indonesia
- UI modern dengan gradient biru muda dan desain minimalis
- Grafik suhu dengan gaya "minimal grid" dan warna oranye lembut
- Prediksi suhu berikutnya (1-step) menggunakan Linear Regression
- Ekspor hasil: unduh CSV dan grafik PNG langsung dari dashboard

## Cara Jalankan (Lokal)
1. Pastikan Python 3.10+ terinstall.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Jalankan aplikasi:
```bash
streamlit run prediksi_cuaca_app.py
```
4. Buka browser ke http://localhost:8501

## Deploy ke Streamlit Cloud
1. Buat repository GitHub dan commit file-file ini (`prediksi_cuaca_app.py`, `requirements.txt`, `README.md`).
2. Login ke https://share.streamlit.io dan hubungkan GitHub.
3. Buat New app -> pilih repo -> pilih `prediksi_cuaca_app.py` -> Deploy.
4. Aplikasi akan tersedia di URL Streamlit Cloud.

## Catatan Keamanan
File ini berisi API key OpenWeather yang tertanam. Jangan membagikan repositori publik jika tidak ingin API key digunakan pihak lain.

## Footer
© 2025 Kelompok 11 AI Ganjil 2025 UNSIA | Powered by OpenWeather & Streamlit
