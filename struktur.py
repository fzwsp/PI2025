import streamlit as st

# Judul utama
st.title("Dashboard Perkebunan Teh - Navigasi Non-Linier")

# Sidebar multi-select untuk navigasi bebas
pages = st.sidebar.multiselect(
    "Pilih Halaman yang Ingin Dibuka (Bisa Pilih Lebih dari Satu):",
    options=[
        "Produksi",
        "Tren Produktivitas",
        "Perbandingan Rakyat dan Swasta",
        "Klasterisasi",
        "Peta Geografis"
    ],
    default=["Produksi"]  # default bisa diatur sesuai kebutuhan
)

# Jika tidak pilih halaman apapun
if not pages:
    st.warning("Pilih minimal satu halaman di navigasi sidebar!")

# Render konten halaman sesuai pilihan user (bisa lebih dari satu)
if "Produksi" in pages:
    st.header("📦 Gambaran Umum Produksi")
    st.write("Konten halaman Produksi...")

if "Tren Produktivitas" in pages:
    st.header("📈 Tren Produktivitas")
    st.write("Konten halaman Tren Produktivitas...")

if "Perbandingan Rakyat dan Swasta" in pages:
    st.header("🔍 Perbandingan Rakyat dan Swasta")
    st.write("Konten halaman Perbandingan...")

if "Klasterisasi" in pages:
    st.header("📋 Klasterisasi")
    st.write("Konten halaman Klasterisasi...")

if "Peta Geografis" in pages:
    st.header("🗺 Peta Geografis")
    st.write("Konten halaman Peta Geografis...")
