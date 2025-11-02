import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="Prediksi Cuaca Indonesia", layout="wide")

st.title("🌦️ Prediksi Cuaca Indonesia")
st.write("Aplikasi ini menampilkan data cuaca dari OpenWeather API dan prediksi sederhana.")

# Contoh grafik dummy
x = np.arange(1, 8)
y = np.random.randint(25, 35, size=7)

fig, ax = plt.subplots()
ax.plot(x, y, marker='o')
ax.set_title("Perkiraan Suhu (Dummy Data)")
ax.set_xlabel("Hari ke-")
ax.set_ylabel("Suhu (°C)")

st.pyplot(fig)

st.info("Versi Streamlit Cloud: Python 3.11.9")