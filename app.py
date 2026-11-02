import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="ID Card Generator - PT Samudera Mulia Abadi",
    page_icon="🪪",
    layout="centered",
)

st.title("🪪 Generator & Editor ID Card")
st.write(
    "Masukkan data di bawah untuk menghasilkan ID Card secara otomatis dan presisi."
)

# Sidebar untuk Input Data
with st.sidebar:
    st.header("1. Input Data Karyawan")
    nama = st.text_input("Nama Lengkap", "M. Noviar Zulfikri")
    jabatan = st.text_input("Jabatan", "IT Support")
    nik = st.text_input("NIK / ID", "SMO-2021-001")

    st.header("2. Upload Foto")
    uploaded_photo = st.file_uploader(
        "Pilih Foto (JPG/PNG)", type=["jpg", "jpeg", "png"]
    )


# Fungsi untuk memproses pembuatan ID Card
def generate_id_card(nama, jabatan, nik, photo_file):
    # Load template.png yang sudah Anda siapkan
    try:
        base_image = Image.open("template.png").convert("RGBA")
    except FileNotFoundError:
        # Cadangan jika file template.png belum terbaca
        base_image = Image.new("RGBA", (1012, 638), (240, 240, 240, 255))

    draw = ImageDraw.Draw(base_image)

    # Konfigurasi Font (Menggunakan default PIL atau kustom ttf jika ada)
    try:
        font_nama = ImageFont.truetype("arial.ttf", 36)
        font_detail = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font_nama = ImageFont.load_default()
        font_detail = ImageFont.load_default()

    # 1. Tempel & Ukur Foto (Sesuaikan ukuran dan koordinat x, y)
    if photo_file is not None:
        photo = Image.open(photo_file).convert("RGBA")
        photo_size = (200, 200)  # Sesuaikan ukuran kotak foto di template
        photo = photo.resize(photo_size, Image.Resampling.LANCZOS)

        # Koordinat posisi foto (x, y)
        photo_position = (100, 180)
        base_image.paste(photo, photo_position, photo)

    # 2. Tulis Teks ke Template (Sesuaikan koordinat x, y untuk teks)
    text_color = (30, 30, 30)  # Warna teks RGB (Hitam/Gelap)

    draw.text((350, 200), f"Nama: {nama}", fill=text_color, font=font_nama)
    draw.text((350, 260), f"Jabatan: {jabatan}", fill=text_color, font=font_detail)
    draw.text((350, 310), f"NIK: {nik}", fill=text_color, font=font_detail)

    return base_image


# Proses Preview di Halaman Utama
st.subheader("Preview ID Card")

# Jalankan fungsi generator
final_card = generate_id_card(nama, jabatan, nik, uploaded_photo)

# Tampilkan gambar hasil pratinjau di Streamlit
st.image(
    final_card, caption="Hasil Pratinjau ID Card", use_container_width=True
)

# Konversi gambar ke format bytes untuk tombol unduh
buffered = io.BytesIO()
final_card.convert("RGB").save(buffered, format="PNG")
img_bytes = buffered.getvalue()

# Tombol Unduh
st.download_button(
    label="📥 Unduh ID Card (PNG)",
    data=img_bytes,
    file_name=f"ID_Card_{nik}.png",
    mime="image/png",
)
