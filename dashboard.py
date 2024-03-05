import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat data
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')

# Mengubah format kolom 'dteday' menjadi datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Mengatasi outlier
for col in ['temp', 'atemp', 'hum', 'windspeed']:
    df_day[col] = np.where(df_day[col] > 100, df_day[col].mean(), df_day[col])
    df_hour[col] = np.where(df_hour[col] > 100, df_hour[col].mean(), df_hour[col])

# Sidebar
st.sidebar.title("Analisis Data Bike Sharing")

# Pertanyaan Bisnis
st.sidebar.markdown("**Pertanyaan Bisnis:**")
st.sidebar.markdown("- Apa saja faktor yang mempengaruhi jumlah pengguna bike sharing?")
st.sidebar.markdown("- Bagaimana pola penggunaan bike sharing berdasarkan waktu, musim, dan cuaca?")
st.sidebar.markdown("- Di manakah lokasi yang paling populer untuk penggunaan bike sharing?")

# Informasi Sekilas
st.title("Informasi Sekilas")

# Menampilkan statistik penting
st.metric("Jumlah Pengguna Terdaftar", df_day['registered'].sum())
st.metric("Rata-rata Penggunaan Harian", df_day['registered'].mean())

# Tren Penggunaan
st.markdown("## Tren Penggunaan")

# Visualisasi trend berdasarkan waktu
plt.plot(df_day['dteday'], df_day['registered'])
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Pengguna Terdaftar')
st.pyplot(plt)

# Analisis Faktor
st.markdown("## Analisis Faktor")

# Memilih faktor
faktor = st.selectbox("Pilih Faktor", ['Musim', 'Temperatur', 'Waktu'])

if faktor == 'Musim':
    # Pastikan 'season' bertipe kategori
    df_day['season'] = df_day['season'].astype('category')

    # Visualisasi dengan seaborn boxplot
    sns.boxplot(x='season', y='registered', data=df_day)
    st.pyplot(plt)

elif faktor == 'Temperatur':
    # Visualisasi pengaruh temperatur
    sns.lmplot(x='temp', y='registered', data=df_day)
    st.pyplot(plt)

elif faktor == 'Waktu (Harian)':
    # Pastikan 'dteday' bertipe datetime
    if not pd.api.types.is_datetime64_dtype(df_day['dteday']):
        df_day['dteday'] = pd.to_datetime(df_day['dteday'])

    # Resample data berdasarkan hari dan plot jumlah pengguna terdaftar harian
    df_day_resampled = df_day.resample('D', on='dteday')['registered'].sum()
    plt.plot(df_day_resampled.index, df_day_resampled.values)
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Pengguna Terdaftar (Harian)')
    st.pyplot(plt)

elif faktor == 'Waktu (Per Jam)':
    # Pastikan 'dteday' bertipe datetime
    if not pd.api.types.is_datetime64_dtype(df_hour['dteday']):
        df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

    # Plot jumlah pengguna terdaftar vs. jam
    plt.plot(df_hour['dteday'].dt.hour, df_hour['registered'])
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Pengguna Terdaftar')
    st.pyplot(plt)

# Kesimpulan
st.markdown("## Kesimpulan")

# Menampilkan kesimpulan berdasarkan hasil analisis
st.markdown("- Jumlah pengguna bike sharing dipengaruhi oleh musim, temperatur, dan waktu.")
st.markdown("- Penggunaan bike sharing lebih tinggi pada musim panas, temperatur yang nyaman, dan hari kerja.")
st.markdown("- Lokasi populer untuk bike sharing terpusat di beberapa area tertentu.")

