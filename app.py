import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Generator Mine Permit", page_icon="🪪", layout="centered"
)

st.title("🪪 Generator Mine Permit (Sisi Depan)")
st.write(
    "Masukkan data karyawan di bawah ini. Posisi dan ukuran font telah disesuaikan"
    " persis dengan contoh."
)

# Sidebar untuk Input Data
with st.sidebar:
  st.header("Input Data Karyawan")
  nama = st.text_input("Nama Lengkap", "Maikel Pandori")
  nik = st.text_input("NIP / No. Induk", "MN-PTBSA 0002")
  jabatan = st.text_input("Jabatan / Role", "DRIVER")
  lokasi_alat = st.text_input("Lokasi Op. Alat (SIMPER)", "AB")
  izin_alat = st.text_input("Izin Op. Alat", "Light Vehicle ( LV )")
  expired_date = st.text_input("Masa Berlaku (Expired)", "19 Oktober 2027")

  st.header("Upload Foto")
  uploaded_photo = st.file_uploader(
      "Pilih Foto (JPG/PNG)", type=["jpg", "jpeg", "png"]
  )


# Fungsi untuk memproses Sisi Depan
def generate_sisi_depan(
    nama, nik, jabatan, lokasi_alat, izin_alat, expired_date, photo_file
):
  try:
    base_image = Image.open("template_depan.png").convert("RGBA")
  except FileNotFoundError:
    # Cadangan jika file belum terbaca (resolusi besar)
    base_image = Image.new("RGBA", (1200, 1700), (255, 255, 255, 255))

  draw = ImageDraw.Draw(base_image)

  # Konfigurasi Font dengan ukuran yang besar dan proporsional sesuai contoh
  try:
    font_nama = ImageFont.truetype("arial.ttf", 60)
    font_detail = ImageFont.truetype("arial.ttf", 42)
    font_box = ImageFont.truetype("arial.ttf", 110)
    font_izin = ImageFont.truetype("arial.ttf", 65)
    font_expired = ImageFont.truetype("arial.ttf", 38)
  except IOError:
    font_nama = ImageFont.load_default()
    font_detail = ImageFont.load_default()
    font_box = ImageFont.load_default()
    font_izin = ImageFont.load_default()
    font_expired = ImageFont.load_default()

  text_color_dark = (20, 20, 20)  # Warna teks gelap
  text_color_yellow = (230, 175, 40)  # Warna kuning untuk izin alat
  text_color_white = (255, 255, 255)  # Warna putih untuk expired

  # 1. Tempel Foto Karyawan (Sesuai posisi di bawah header MINE PERMIT sebelah kiri)
  if photo_file is not None:
    photo = Image.open(photo_file).convert("RGBA")
    photo_size = (380, 480)  # Ukuran foto
    photo = photo.resize(photo_size, Image.Resampling.LANCZOS)
    photo_position = (220, 220)  # Koordinat (X, Y) foto
    base_image.paste(photo, photo_position, photo)

  # 2. Tulis Teks Identitas (Nama, NIK, Jabatan) di bawah foto sebelah kiri
  draw.text((100, 730), f"{nama}", fill=text_color_dark, font=font_nama)
  draw.text((100, 815), f"{nik}", fill=text_color_dark, font=font_detail)
  draw.text((100, 875), f"{jabatan}", fill=text_color_dark, font=font_detail)

  # 3. Tulis Kode Lokasi Alat di Kotak Sebelah Kanan (Contoh: AB)
  draw.text(
      (760, 760), f"{lokasi_alat}", fill=text_color_dark, font=font_box
  )

  # 4. Tulis Keterangan Izin Alat di Dalam Kotak Panjang Tengah (Teks rata tengah secara visual)
  draw.text(
      (350, 1060), f"{izin_alat}", fill=text_color_yellow, font=font_izin
  )

  # 5. Tulis Tanggal Expired di Bagian Bawah Area Hijau (Pojok kiri bawah)
  draw.text(
      (120, 1610),
      f"Expired : {expired_date}",
      fill=text_color_white,
      font=font_expired,
  )

  return base_image


# --- TAMPILAN UTAMA APLIKASI ---
st.subheader("Pratinjau Mine Permit")

final_card = generate_sisi_depan(
    nama, nik, jabatan, lokasi_alat, izin_alat, expired_date, uploaded_photo
)
st.image(
    final_card, caption="Pratinjau Mine Permit (Depan)", use_container_width=True
)

# Tombol Unduh
buffered = io.BytesIO()
final_card.convert("RGB").save(buffered, format="PNG")
st.download_button(
    label="📥 Unduh Mine Permit (PNG)",
    data=buffered.getvalue(),
    file_name=f"MinePermit_{nik}.png",
    mime="image/png",
)
