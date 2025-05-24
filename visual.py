# Mengimpor pustaka (Library)
import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px
from PIL import Image

# Konfigurasi streamlit
st.set_page_config(
    page_title="Dashboard Perkebunan Teh",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Membaca data
kebun_total = pd.read_csv('perkebunan_teh.csv')  

st.title("📊 Dashboard Produktivitas Perkebunan Teh Provinsi Jawa Barat Sektor Rakyat dan Swasta")


# Membuat Sidebar Navigasi
image = Image.open('teh.png')

# Tampilkan gambar di sidebar
st.sidebar.image(image, width=150)
st.sidebar.title("🍵 Visualisasi Perkebunanan Teh")
page = st.sidebar.selectbox("Navigasi Halaman", (
    "📦 Produksi",
    "📈 Tren Produktivitas",
    "🔍 Perbandingan Rakyat dan Swasta",
    "📋 Klasterisasi",
    "🗺 Peta Geografis"
))


# Halaman 1 - Produksi
if page == "📦 Produksi":
    st.header("Gambaran Umum Produksi")

    # Membuat metrik rata-rata
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_rakyat = kebun_total['produktivitas_rakyat'].mean()
        st.metric("Rata-Rata Produktivitas Rakyat", f"{avg_rakyat:.2f}")
    with col2:
        avg_swasta = kebun_total['produktivitas_swasta'].mean()
        st.metric("Rata-Rata Produktivitas Swasta", f"{avg_swasta:.2f}")
    with col3:
        avg_prod_rakyat = kebun_total['produksi_rakyat'].mean()
        st.metric("Rata-Rata Produksi Rakyat", f"{avg_prod_rakyat:.2f}")
    with col4:
        avg_prod_swasta = kebun_total['produksi_swasta'].mean()
        st.metric("Rata-Rata Produksi Swasta", f"{avg_prod_swasta:.2f}")

    # Pilih tahun dari dropdown di sidebar
    selected_year = st.selectbox("Pilih Tahun", sorted(kebun_total['tahun'].unique()))

    # Filter data sesuai tahun yang dipilih
    data_filtered = kebun_total[kebun_total['tahun'] == selected_year]

    # Membuat Bar Chart
    col1, col2 = st.columns(2)

    with col1:
        # ==== Top 5 Produksi Rakyat ====
        top_5_rakyat = data_filtered.nlargest(5, 'produksi_rakyat')

        fig_rakyat = px.bar(
            top_5_rakyat, 
            x='kab_kota', 
            y='produksi_rakyat', 
            title='Top 5 Produksi Rakyat', 
            color='produksi_rakyat',
            color_continuous_scale='bluyl'  
        )
        fig_rakyat.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_rakyat, use_container_width=True)

    with col2:
        # ==== Top 5 Produksi Swasta ====
        top_5_swasta = data_filtered.nlargest(5, 'produksi_swasta')

        fig_swasta = px.bar(
            top_5_swasta, 
            x='kab_kota', 
            y='produksi_swasta', 
            title='Top 5 Produksi Swasta', 
            color='produksi_swasta',
            color_continuous_scale='reds'
        )
        fig_swasta.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_swasta, use_container_width=True)
    
    # Pie chart 
    st.subheader("Proporsi Produksi Rakyat vs Swasta")
    produksi_total = pd.DataFrame({
    'Sektor': ['Rakyat', 'Swasta'],
    'Total Produksi': [kebun_total['produksi_rakyat'].sum(), kebun_total['produksi_swasta'].sum()]
    })
    fig1 = px.pie(
        produksi_total, 
        names='Sektor', 
        values='Total Produksi',
        color='Sektor',
        color_discrete_map={
            'Rakyat': '#3D90D7', 
            'Swasta': '#7AC6D2'}
        )
    st.plotly_chart(fig1, use_container_width=True)

    # Line chart produksi
    st.subheader("Tren Produksi per Sektor")
    produksi_tahunan = kebun_total.groupby('tahun')[['produksi_rakyat', 'produksi_swasta']].mean().reset_index()
    fig2 = px.line(produksi_tahunan, x='tahun', y=['produksi_rakyat', 'produksi_swasta'], markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Pilihan tahun
    st.subheader("Perbandingan Produksi antar Kabupaten dan Kota Berdasarkan Tahun")
    tahun_pilihan = st.selectbox("Pilih Tahun:", ["Semua Tahun"] + sorted(kebun_total['tahun'].unique()))

    # Filter data sesuai pilihan
    if tahun_pilihan != "Semua Tahun":
        data_tampil = kebun_total[kebun_total['tahun'] == tahun_pilihan]
    else:
        data_tampil = kebun_total.copy()

    # Bar chart per kabupaten dan kota - Rakyat
    st.subheader("Sektor Rakyat")
    fig3 = px.bar(data_tampil, 
                  y='kab_kota', 
                  x='produksi_rakyat', 
                  orientation='h', 
                  title='Produksi Rakyat per Kabupaten dan Kota',  
                  hover_data=['tahun'])
    st.plotly_chart(fig3, use_container_width=True)

    # Bar chart per kabupaten dan kota - Swasta
    st.subheader("Sektor Swasta")
    fig3 = px.bar(data_tampil, 
                  y='kab_kota', 
                  x='produksi_swasta', 
                  orientation='h', 
                  title='Produksi Swasta per Kabupaten dan Kota',  
                  hover_data=['tahun'])
    st.plotly_chart(fig3, use_container_width=True)

    

# Halaman 2 - Tren per Tahun
elif page == "📈 Tren Produktivitas":
    st.header("Tren Produktivitas Tahunan")
    
    st.subheader("Top 5 Produktivitas Rakyat Tertinggi per Kabupaten/Kota")
    #   Pilih tahun dari dropdown di sidebar
    selected_year = st.selectbox("Pilih Tahun", sorted(kebun_total['tahun'].unique()))

    # Filter data sesuai tahun yang dipilih
    data_filtered = kebun_total[kebun_total['tahun'] == selected_year]

    col1, col2 = st.columns(2)

    # ==== Top 5 Produksi Rakyat ====
    with col1:
        top_5_rakyat = data_filtered.nlargest(5, 'produktivitas_rakyat')

        fig_rakyat = px.bar(
            top_5_rakyat, 
            x='kab_kota', 
            y='produktivitas_rakyat', 
            title='Produktivitas Sektor Rakyat', 
            color='produktivitas_rakyat',
            color_continuous_scale='bluyl'  
        )
        fig_rakyat.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_rakyat, use_container_width=True)

    # ==== Top 5 Produksi Swasta ====
    with col2:
        top_5_swasta = data_filtered.nlargest(5, 'produktivitas_swasta')

        fig_swasta = px.bar(
            top_5_swasta, 
            x='kab_kota', 
            y='produktivitas_swasta', 
            title='Produktivitas Sektor Swasta', 
            color='produktivitas_swasta',
            color_continuous_scale='reds'
        )
        fig_swasta.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_swasta, use_container_width=True)

    # Line chart produktivitas
    st.subheader("Tren Produktivitas per Sektor")
    produksi_tahunan = kebun_total.groupby('tahun')[
        ['produktivitas_rakyat', 'produktivitas_swasta']].mean().reset_index()
    fig2 = px.line(produksi_tahunan, 
                   x='tahun', 
                   y=['produktivitas_rakyat', 'produktivitas_swasta'], 
                   markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Bar Chart Pertumbuhan
    st.subheader("Rata-rata Pertumbuhan Tahunan Produktivitas per Sektor")

    pilihan = st.selectbox("Pilih Tampilan:", 
                           ["Top 5 Teratas Kota dan Kabupaten", "Keseluruhan Kota dan Kabupaten"])

    sektor_map = {'produktivitas_rakyat': 'Rakyat', 'produktivitas_swasta': 'Swasta'}
    sektor_cols = list(sektor_map.keys())

    def pertumbuhan(grp):
        tahun_awal, tahun_akhir = grp['tahun'].min(), grp['tahun'].max()
        tahun_diff = max(tahun_akhir - tahun_awal, 1)
        hasil = []
        for col in sektor_cols:
            awal = grp.loc[grp['tahun'] == tahun_awal, col].values[0]
            akhir = grp.loc[grp['tahun'] == tahun_akhir, col].values[0]
            growth = 100 if awal == 0 and akhir > 0 else ((akhir / awal - 1) * 100 if awal > 0 else 0)
            hasil.append({'sektor': sektor_map[col], 'pertumbuhan_tahunan': growth / tahun_diff})
        return pd.DataFrame(hasil)

    df_growth = kebun_total.groupby('kab_kota').apply(pertumbuhan).reset_index(level=1, drop=True).reset_index()

    if pilihan == "Top 5 Teratas Kota dan Kabupaten":
        avg_growth = df_growth.groupby('kab_kota')['pertumbuhan_tahunan'].mean()
        top5 = avg_growth.nlargest(5).index
        df_growth = df_growth[df_growth['kab_kota'].isin(top5)]

    fig = px.bar(
        df_growth,
        x='kab_kota',
        y='pertumbuhan_tahunan',
        color='sektor',
        barmode='group',
        color_discrete_map={'Rakyat': '#3A59D1', 'Swasta': '#B5FCCD'},
        title="Rata-rata Pertumbuhan Tahunan Produktivitas per Sektor (%)"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Halaman 3 - Perbandingan Rakyat dan Swasta
elif page == "🔍 Perbandingan Rakyat dan Swasta":
    st.header("Perbandingan Produktivitas Sektor Rakyat dan Swasta")

    # Visualisasi Bar Chart
    st.subheader("Perbandingan Bar Chart per Kabupaten dan Kota")
    fig7 = px.bar(kebun_total, 
                  y='kab_kota', 
                  x=['produktivitas_rakyat', 'produktivitas_swasta'], 
                  barmode='group', orientation='h')
    st.plotly_chart(fig7, use_container_width=True)

    # Visualisasi Scatter Plot
    st.subheader("Scatter Plot")
    fig8 = px.scatter(kebun_total, 
                      x='produktivitas_rakyat', 
                      y='produktivitas_swasta', 
                      title='Rakyat vs Swasta', 
                      color='produktivitas_rakyat',
                      color_continuous_scale='viridis')
    st.plotly_chart(fig8, use_container_width=True)

    # Visualisai Korelasi
    # Hitung matriks korelasi
    corr_matrix = kebun_total[
        ['produksi_rakyat', 'produksi_swasta', 'produktivitas_rakyat', 'produktivitas_swasta']].corr()

    # Visualisasi dengan plotly
    st.subheader("Hubungan linear antara sektor rakyat dan swasta")
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        width=1000,
        height=800,
        title="Korelasi Produksi & Produktivitas"
    )
    st.plotly_chart(fig, use_container_width=False)


# Halaman 4 - Klasterisasi
elif page == "📋 Klasterisasi":
    st.header("Klasterisasi Produktivitas")

    # Scatter Plot Hasil Klasterisasi
    st.subheader("Hasil Klasterisasi Produktivitas")
    fig9 = px.scatter(
        kebun_total, 
        x='produktivitas_rakyat', 
        y='produktivitas_swasta', 
        color='cluster_produktivitas', 
        title='Cluster Scatter Plot',
         hover_data=['kab_kota', 'tahun', 'cluster_produktivitas'],
        color_continuous_scale='viridis')
    st.plotly_chart(fig9, use_container_width=True)
    fig9.update_traces(textposition='top center', textfont_size=9)

    # Pie Chart Distribusi Kluster
    st.subheader("Distribusi Kluster Tahun 2017 - 2024")
    cluster_count = kebun_total['cluster_produktivitas'].value_counts().reset_index()
    cluster_count.columns = ['cluster_produktivitas', 'jumlah']
    fig10 = px.pie(cluster_count, names='cluster_produktivitas', values='jumlah')
    st.plotly_chart(fig10, use_container_width=True)

    # Bar Chart Jumlah Wilayah Kluster
    st.subheader("Jumlah Kabupaten dan Kota per Kluster")
    fig = px.bar(
        kebun_total.groupby('cluster_produktivitas')['kab_kota'].nunique().reset_index(name='jumlah'),
        x='cluster_produktivitas',
        y='jumlah',
        text='jumlah',
        color='cluster_produktivitas',
        color_continuous_scale='sunset',
        title='Jumlah Kabupaten per Kluster'
    )

    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Membuat Tabel 
    st.subheader("Perbandingan Produksi antar Kabupaten dan Kota Berdasarkan Tahun")
    tahun_terpilih = st.selectbox("Pilih Tahun:", ["Semua Tahun"] + sorted(kebun_total['tahun'].unique()))

    # Pilih tahun menggunakan selectbox
    if tahun_terpilih != "Semua Tahun":
        tahun_kluster = kebun_total[kebun_total['tahun'] == tahun_terpilih]
    else:
        tahun_kluster = kebun_total.copy()

    # Pilih kolom yang ingin ditampilkan
    tabel_data = tahun_kluster[[
        'kab_kota', 'produktivitas_rakyat', 'produktivitas_swasta', 'cluster_produktivitas']]

    # Tampilkan tabel
    st.dataframe(tabel_data)


# Halaman 5 - Peta
elif page == "🗺 Peta Geografis":
    # Header Peta Persebaran
    st.header("Peta Persebaran Produktivitas dan Produksi")

    lokasi = pd.read_csv("lokasi_wilayah.csv")
    # --- Standarisasi nama kabupaten ---
    kebun_total['kab_kota'] = kebun_total['kab_kota'].str.strip().str.lower()
    lokasi['bps_kota_nama'] = lokasi['bps_kota_nama'].str.strip().str.lower()

    # --- Ambil koordinat unik tiap kota/kabupaten ---
    lokasi_kab = lokasi[['bps_kota_nama', 'latitude', 'longitude']].drop_duplicates()
    lokasi_kab = lokasi_kab.rename(columns={'bps_kota_nama': 'kab_kota'})

    # --- Gabungkan lokasi ke data utama ---
    gabung = pd.merge(kebun_total, lokasi_kab, on='kab_kota', how='left')

    # --- Dropdown untuk pilih tahun ---
    tahun_tersedia = sorted(gabung['tahun'].dropna().unique())
    selected_year = st.sidebar.selectbox("Pilih Tahun", tahun_tersedia)

    # --- Filter data sesuai tahun ---
    data_filtered = gabung[gabung['tahun'] == selected_year]

    # --- Ganti nilai 0 agar tetap terlihat di peta (jangan hilang titiknya) ---
    data_filtered['produktivitas_rakyat_plot'] = data_filtered['produktivitas_rakyat'].replace(0, 0.1).fillna(0.1)

    # --- Slider ukuran titik ---
    size_max = st.slider("Ukuran Maksimal Titik", 5, 25, 8)

    # --- Visualisasi Peta Rakyat ---
    fig = px.scatter_mapbox(
        data_filtered,
        lat="latitude",
        lon="longitude",
        size="produktivitas_rakyat",
        color="produktivitas_rakyat",
        hover_name="kab_kota",
        hover_data={
            "produksi_rakyat": True,
            "produksi_swasta": True,
            "produktivitas_rakyat": True,
            "latitude": False,
            "longitude": False
        },
        size_max=size_max,
        zoom=7,
        mapbox_style="carto-positron",
        title=f"Sebaran Produktivitas Rakyat Tahun {selected_year}",
        color_continuous_scale='reds'
    )

    # Perjelas tampilan marker dan teks
    fig.update_traces(
        text=data_filtered['kab_kota'],
        textposition="top center"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Visualisasi Peta Swasta ---
    fig = px.scatter_mapbox(
        data_filtered,
        lat="latitude",
        lon="longitude",
        size="produktivitas_swasta",
        color="produktivitas_swasta",
        hover_name="kab_kota",
        hover_data={
            "produksi_rakyat": True,
            "produksi_swasta": True,
            "produktivitas_rakyat": True,
            "latitude": False,
            "longitude": False
        },
        size_max=size_max,
        zoom=7,
        mapbox_style="carto-positron",
        title=f"Sebaran Produktivitas Swasta Tahun {selected_year}",
        color_continuous_scale='ylgnbu'
    )

    # Perjelas tampilan marker dan teks
    fig.update_traces(
        text=data_filtered['kab_kota'],
        textposition="top center"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Membuat Metrik Ringkasan
    st.header("Statistik Ringkasan")
    col1, col2, col3 = st.columns(3)

    valid_rakyat = data_filtered['produktivitas_rakyat'].dropna()
    valid_swasta = data_filtered['produktivitas_swasta'].dropna()

    with col1:
        st.metric(
            "Rata-Rata Produktivitas Sektor Rakyat", 
            f"{valid_rakyat.mean():.1f} kg/ha" if not valid_rakyat.empty else "No data"
        )
    with col2:
        st.metric(
            "Rata-Rata Produktivitas Sektor Swasta", 
            f"{valid_swasta.mean():.1f} kg/ha" if not valid_swasta.empty else "No data"
        )
    with col3:
        if not valid_rakyat.empty and not valid_swasta.empty:
            diff = valid_swasta.mean() - valid_rakyat.mean()
            st.metric(
                "Kesenjangan Produktivitas", 
                f"{diff:.1f} kg/ha",
                delta=f"{diff:.1f} kg/ha"
            )
        else:
            st.metric("Productivity Gap", "No data")
