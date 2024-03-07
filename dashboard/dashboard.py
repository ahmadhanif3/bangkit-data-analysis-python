import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

@st.cache_data
def load_data():
    data = pd.read_csv("https://raw.githubusercontent.com/ahmadhanif3/bangkit-data-analysis-python/master/dashboard/main_data.csv")
    data_changping = pd.read_csv("https://raw.githubusercontent.com/ahmadhanif3/bangkit-data-analysis-python/master/dashboard/changping_data.csv")

    return data, data_changping

data, data_changping = load_data()

st.title("Analisis Air Quality Dataset")
st.write(""" 
Nama: Ahmad Hanif Adisetya      
\nEmail: m010d4ky1890@bangkit.academy 
\nID Dicoding: ahanif03
""")

st.write("""
Pada dashboard ini, saya akan melakukan analisis terhadap Air Quality Dataset. Dataset ini dapat diakses
melalui https://drive.google.com/file/d/1RhU3gJlkteaAQfyn9XOVAz7a5o1-etgr/view?usp=share_link. Dataset
tersebut diambil lalu dilakukan beberapa modifikasi. Dalam analisis, terdapat 2 pertanyaan bisnis. 
- Pertanyaan 1: Pola turun dan naik tingkat konsentrasi polutan dalam jangka waktu perjam dan perbulan akan seperti apa?
- Pertanyaan 2: Adakah pengaruh hujan terhadap polutan SO2 dan NO2 di suatu stasiun?
""")

st.divider()

st.header("Pertanyaan 1: Tren Polutan Berdasarkan Jam dan Bulan")

st.write("Bagaimana tren polutan dalam jangka waktu jam dan bulan")

pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3', 'CO']

avg_hour_pollutant = data.groupby('hour')[pollutants].mean()
avg_hour_co = avg_hour_pollutant.pop('CO')

monthly_avg_pollutants = data.groupby('month')[pollutants].mean()
monthly_avg_CO = monthly_avg_pollutants.pop('CO')

def plot_pollutants(df, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(15, 6))
    for pollutant in df.columns:
        ax.plot(df.index, df[pollutant], marker='o', label=pollutant)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True)
    return fig

def plot_co(df, title, xlabel, ylabel, color):
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(df.index, df, marker='o', color=color, label='CO')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True)
    return fig

st.write("### Rata-Rata Konsentrasi Polutan Per Jam")
st.pyplot(plot_pollutants(avg_hour_pollutant, 'Rata-Rata Konsentrasi Polutan Selain CO Dalam Interval Jam', 'Jam', 'Rata-Rata Konsentrasi'))
st.pyplot(plot_co(avg_hour_co, 'Rata-Rata Konsentrasi CO Dalam Interval Jam', 'Jam', 'Rata-Rata Konsentrasi', 'blue'))

st.write("### Rata-Rata Konsentrasi Polutan Per Bulan")
st.pyplot(plot_pollutants(monthly_avg_pollutants, 'Rata-Rata Konsentrasi Polutan Selain CO Dalam Interval Bulan', 'Bulan', 'Rata-Rata Konsentrasi'))
st.pyplot(plot_co(monthly_avg_CO, 'Rata-Rata Konsentrasi CO Dalam Interval Bulan', 'Bulan', 'Rata-Rata Konsentrasi', 'blue'))

st.write("""
Berdasarkan visualisasi dari data yang telah dibuat di atas, diperoleh beberapa konklusi:
1. Baik perbulan maupun perjam, tingkat konsentrasi `SO2` adalah yang terendah dibandingkan polutan lainnya
2. Di sekitar jam siang, mulai dari sekitar jam 10, hampir seluruh polutan akan mengalami penurunan. Kecuali untuk `O3`. Hal ini menunjukkan adanya korelasi negatif antara `O3` dan polutan lainnya. 
3. `O3` memiliki perubahan yang paling signifikan, dengan beda value tertinggi dan terendah yaitu sekitar 77 satuan konsentrasi baik perjam maupun perbulan
4. Secara keseluruhan, udara memiliki tingkat polutan yang secara rata-rata paling rendah adalah pada term 3, atau sekitar bulan 7, 8, dan 9.
5. Polutan mendekati tengah malam dan juga mendekati akhir tahun akan meningkat.

Masih banyak lagi kesimpulan yang dapat diambil dari pengolahan di atas. Namun, beberapa poin di atas dapat berguna.
""")

st.divider()

st.header("Pertanyaan 2: Pengaruh Hujan Terhadap Polutan SO2 dan NO2 di Stasiun Changping")

st.write("Pengelompokkan tingkat SO2 dan NO2 berdasarkan kondisi hujan di stasiun Changping")

colors = {'YA': 'blue', 'TIDAK': 'green'}

# Plot scatter plot SO2 vs NO2 by Rain_Status for Changping station
fig, ax = plt.subplots(figsize=(10, 6))
for status, group in data_changping.groupby('Rain_Status'):
    alpha_val = 0.5 if status == 'TIDAK' else 1  # Adjust transparency for non-rainy data
    ax.scatter(group['SO2'], group['NO2'], alpha=alpha_val, c=colors[status], label=status)

ax.set_title('Tingkat SO2 dan NO2 di Stasiun Changping Berdasarkan Status Hujan')
ax.set_xlabel('SO2')
ax.set_ylabel('NO2')
ax.legend(title='Status Hujan')
st.pyplot(fig)

st.write("""
Berdasarkan visualisasi dan pengolahan dari data yang telah dibuat di atas, diperoleh beberapa konklusi:
1. Pada saat hujan, konsentrasi `SO2` akan secara mayoritas berada di bawah 20 satuan.
2. Pada saat hujan, konsentrasi `NO2` akan secara mayoritas berada di bawah 100 satuan.
3. Tidak terbentuk *clustering* dengan sempurna, namun data sedang hujan secara mayoritas terdapat di suatu kelompok di kiri bawah visualisasi.
4. Untuk kedepannya, dapat dimasukkan pula variabel intensitas hujan agar makin terlihat pengelompokkannya.

Menurut saya itu adalah kesimpulan yang dapat diambil, penyempurnaan variabel yang digunakan bisa memperbaiki *clustering* yang terbentuk agar semakin terlihat pengelompokkannya.
""")