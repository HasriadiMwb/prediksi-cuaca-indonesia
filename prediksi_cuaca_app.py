import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from io import BytesIO

# ----------------------
# Configuration / API
# ----------------------
API_KEY = "fbe01a9e9e61cc82bc9445491ea077ee"

KOTA_LIST = [
 "Banda Aceh","Medan","Padang","Pekanbaru","Tanjung Pinang","Jambi","Palembang","Pangkal Pinang",
 "Bengkulu","Bandar Lampung","Jakarta","Bandung","Serang","Semarang","Yogyakarta","Surabaya",
 "Denpasar","Mataram","Kupang","Pontianak","Palangkaraya","Banjarmasin","Samarinda","Tanjung Selor",
 "Manado","Gorontalo","Palu","Mamuju","Makassar","Kendari","Ambon","Ternate","Manokwari","Jayapura",
 "Nabire","Wamena","Merauke","Sorong","Bogor","Cirebon","Batam"
]

# ----------------------
# Styling (CSS) - gradient header and container
# ----------------------
st.set_page_config(page_title="Prediksi Cuaca Indonesia", page_icon="🌦️", layout="wide")

CSS = """<style>
/* Page gradient background */
[data-testid="stAppViewContainer"] > .main {
  background: linear-gradient(135deg, #E0F2FE 0%, #F8FAFC 100%);
  padding: 2rem;
}
/* Header card */
.header {
  background: linear-gradient(90deg, #0EA5E9 0%, #38BDF8 100%);
  padding: 18px;
  border-radius: 12px;
  color: white;
}
.header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
}
.header p {
  margin: 4px 0 0 0;
  opacity: 0.95;
}
/* Card style for content areas */
.card {
  background: white;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 1px 6px rgba(30,41,59,0.06);
  margin-bottom: 12px;
}
/* Footer */
.footer {
  color: #1E293B;
  opacity: 0.8;
  font-size: 13px;
  text-align: center;
  padding-top: 8px;
  padding-bottom: 20px;
}
.small-muted {
  color: #475569;
  font-size: 13px;
}
.download-btn {
  background-color: #FACC15 !important;
  color: #1E293B !important;
  font-weight: 600 !important;
}
</style>"""

st.markdown(CSS, unsafe_allow_html=True)

# Header
with st.container():
    st.markdown('<div class="header"><h1>🌦️ Prediksi Cuaca Indonesia – Machine Learning + OpenWeather API</h1><p>Aplikasi AI yang memprediksi tren suhu dan kondisi cuaca di 41 kota besar Indonesia 🇮🇩</p></div>', unsafe_allow_html=True)
    st.markdown('')

# Controls
with st.container():
    with st.expander("Pengaturan / Info", expanded=False):
        st.markdown("**Catatan:** API key sudah disematkan di dalam aplikasi. Jangan bagikan file ini ke publik jika tidak ingin API key tersebar.")
        st.markdown("**Sumber data:** OpenWeather (5-day forecast, 3-hour step).")
    col1, col2 = st.columns([3,1])
    with col1:
        city = st.selectbox("Pilih Kota:", KOTA_LIST, index=KOTA_LIST.index("Ternate"))
    with col2:
        run = st.button("🔄 Ambil Data Cuaca", help="Klik untuk mengambil data cuaca & prediksi")

output_area = st.container()

# Helper
def kondisi_id(main):
    if not isinstance(main, str):
        return ""
    w = main.lower()
    if "rain" in w: return "🌧️ Hujan"
    if "drizzle" in w: return "🌧️ Hujan Ringan"
    if "cloud" in w: return "☁️ Berawan"
    if "clear" in w: return "☀️ Cerah"
    if "thunder" in w or "storm" in w: return "⛈️ Badai / Petir"
    return main

def fetch_forecast(api_key, city_name):
    URL = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric"
    r = requests.get(URL, timeout=15)
    r.raise_for_status()
    return r.json()

def run_pipeline(api_key, city_name):
    data = fetch_forecast(api_key, city_name)
    forecast = data.get("list", [])
    rows = []
    for f in forecast:
        rows.append({
            "Waktu": f.get("dt_txt"),
            "Suhu (°C)": f.get("main", {}).get("temp"),
            "Kelembapan (%)": f.get("main", {}).get("humidity"),
            "Kecepatan Angin (m/s)": f.get("wind", {}).get("speed"),
            "Kondisi API": f.get("weather", [{}])[0].get("main",""),
            "Keterangan": f.get("weather", [{}])[0].get("description","")
        })
    df = pd.DataFrame(rows)
    # Add localized condition
    df["Kondisi"] = df["Kondisi API"].apply(kondisi_id)
    return df

def plot_and_export(df, city_name):
    # Plot minimal grid style
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(figsize=(10,4))
    x = np.arange(len(df))
    ax.plot(x, df["Suhu (°C)"], marker='o', linewidth=2.2, color='#FB923C')
    ax.set_xticks(x[::3])
    labels = df["Waktu"].tolist()
    ax.set_xticklabels(labels[::3], rotation=45, ha='right')
    ax.set_title(f"Trend Suhu Kota {city_name}", fontsize=14, color='#0F172A')
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Suhu (°C)")
    ax.grid(alpha=0.25)
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout()
    # Save to PNG buffer
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    return fig, buf

# Main action
if run:
    with output_area:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        try:
            st.info(f"📡 Mengambil data cuaca untuk {city}...")
            df = run_pipeline(API_KEY, city)
            if df.empty:
                st.warning("Data tidak tersedia.")
            else:
                # Save CSV
                csv_filename = f"data_cuaca_{city.replace(' ','_')}.csv"
                df.to_csv(csv_filename, index=False)
                # Display table
                st.markdown("### 🧾 Tabel Data Cuaca (5 hari, tiap 3 jam)")
                st.dataframe(df.head(15), use_container_width=True)
                # Plot and export
                fig, png_buf = plot_and_export(df, city)
                st.pyplot(fig)
                # Prediction
                df_model = df[["Suhu (°C)","Kelembapan (%)","Kecepatan Angin (m/s)"]].copy()
                df_model["Next"] = df_model["Suhu (°C)"].shift(-1)
                df_model = df_model.dropna()
                if len(df_model) < 2:
                    st.warning("Data tidak cukup untuk melatih model prediksi.")
                else:
                    X = df_model[["Suhu (°C)","Kelembapan (%)","Kecepatan Angin (m/s)"]]
                    y = df_model["Next"]
                    model = LinearRegression().fit(X, y)
                    pred = model.predict([X.iloc[-1].values])[0]
                    last_cond = df["Kondisi"].iloc[-1]
                    st.markdown(f"### 🌤️ Prediksi suhu berikutnya di **{city}**: **{pred:.2f} °C** — {last_cond}")
                # Download links
                st.markdown("---")
                st.markdown("### 💾 Unduh Hasil")
                st.download_button("📥 Unduh CSV", data=open(csv_filename,'rb'), file_name=csv_filename, mime='text/csv')
                st.download_button("🖼️ Unduh Grafik PNG", data=png_buf, file_name=f"grafik_suhu_{city.replace(' ','_')}.png", mime="image/png")
                st.success(f"✅ File disimpan: {csv_filename} dan grafik disiapkan untuk diunduh.")
        except requests.HTTPError as e:
            st.error(f"HTTP error saat mengambil data: {e}")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown('<div class="footer">© 2025 Kelompok 11 AI Ganjil 2025 UNSIA | Powered by OpenWeather & Streamlit</div>', unsafe_allow_html=True)
