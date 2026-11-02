import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Generator Mine Permit", page_icon="🪪", layout="centered"
)

st.title("🪪 Generator Mine Permit (Sisi Depan)")
st.write(
    "Masukkan data karyawan di bawah ini. Ukuran font dan posisi telah disesuaikan."
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
    base_image = Image.new("RGBA", (1200, 1700), (255, 255, 255, 255))

  # Ambil ukuran asli gambar template agar dinamis
  img_width, img_height = base_image.size

  draw = ImageDraw.Draw(base_image)

  # Konfigurasi Font dengan ukuran yang jauh lebih besar (disesuaikan untuk template beresolusi tinggi)
  try:
    font_nama = ImageFont.truetype("arial.ttf", 75)
    font_detail = ImageFont.truetype("arial.ttf", 50)
    font_box = ImageFont.truetype("arial.ttf", 110)
    font_izin = ImageFont.truetype("arial.ttf", 60)
    font_expired = ImageFont.truetype("arial.ttf", 45)
  except IOError:
    font_nama = ImageFont.load_default()
    font_detail = ImageFont.load_default()
    font_box = ImageFont.load_default()
    font_izin = ImageFont.load_default()
    font_expired = ImageFont.load_default()

  text_color_dark = (20, 20, 20)  # Warna teks gelap
  text_color_yellow = (210, 155, 20)  # Warna kuning untuk izin alat
  text_color_white = (255, 255, 255)  # Warna putih untuk expired

  # 1. Tempel Foto Karyawan (Sesuaikan ukuran dan koordinat X, Y)
  if photo_file is not None:
    photo = Image.open(photo_file).convert("RGBA")
    photo_size = (
        420,
        520,
    )  # Ukuran kotak foto diperbesar menyesuaikan template
    photo = photo.resize(photo_size, Image.Resampling.LANCZOS)
    photo_position = (200, 240)  # Posisi (X, Y) foto
    base_image.paste(photo, photo_position, photo)

  # 2. Tulis Teks Identitas (Nama, NIK, Jabatan) di sebelah kiri bawah foto
  draw.text((100, 800), f"{nama}", fill=text_color_dark, font=font_nama)
  draw.text((100, 895), f"{nik}", fill=text_color_dark, font=font_detail)
  draw.text((100, 960), f"{jabatan}", fill=text_color_dark, font=font_detail)

  # 3. Tulis Kode Lokasi Alat di Kotak Sebelah Kanan (Contoh: AB)
  draw.text(
      (880, 820), f"{lokasi_alat}", fill=text_color_dark, font=font_box
  )

  # 4. Tulis Keterangan Izin Alat di Dalam Kotak Panjang Tengah
  draw.text(
      (360, 1145), f"{izin_alat}", fill=text_color_yellow, font=font_izin
  )

  # 5. Tulis Tanggal Expired di Bagian Bawah Area Hijau (Digeser ke kanan sedikit agar tidak terpotong)
  draw.text(
      (150, 1610),
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
