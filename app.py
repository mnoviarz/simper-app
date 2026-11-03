import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Generator Mine Permit", page_icon="🪪", layout="centered"
)

st.title("🪪 Generator Mine Permit (Depan & Belakang)")
st.write(
    "Masukkan data karyawan di bawah ini, lalu pilih sisi kartu yang ingin"
    " ditampilkan atau diunduh."
)

# Sidebar untuk Input Data & Pilihan Sisi Kartu
with st.sidebar:
  st.header("1. Pilih Tampilan")
  sisi_pilihan = st.radio(
      "Tampilkan Sisi:", ("Sisi Depan", "Sisi Belakang", "Tampilkan Keduanya")
  )

  st.header("2. Input Data Karyawan")
  nama = st.text_input("Nama Lengkap", "Maikel Pandori")
  nik = st.text_input("NIP / No. Induk", "MN-PTBSA 0002")
  jabatan = st.text_input("Jabatan / Role", "DRIVER")
  lokasi_alat = st.text_input("Lokasi Op. Alat (SIMPER)", "AB")
  izin_alat = st.text_input("Izin Op. Alat", "Light Vehicle ( LV )")
  expired_date = st.text_input("Masa Berlaku (Expired)", "19 Oktober 2027")

  st.header("3. Upload Foto")
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
    base_image = Image.new("RGBA", (850, 1200), (255, 255, 255, 255))

  draw = ImageDraw.Draw(base_image)

  # Mengatur Font dengan aman (Menggunakan font default PIL jika file .ttf tidak ada di Linux)
# Konfigurasi Font secara aman per baris agar tidak saling memengaruhi error
  try:
    font_nama = ImageFont.truetype("arial_narrow_7.ttf", 55)
  except IOError:
    font_nama = ImageFont.load_default()

  try:
    # Jika font detail lain belum ada, gunakan font_narrow atau load_default khusus bagian itu
    font_detail = ImageFont.truetype("arial_narrow_7.ttf", 30)
    font_box = ImageFont.truetype("arial_narrow_7.ttf", 55)
    font_izin = ImageFont.truetype("arial_narrow_7.ttf", 30)
    font_expired = ImageFont.truetype("arial_narrow_7.ttf", 25)
  except IOError:
    font_detail = ImageFont.load_default()
    font_box = ImageFont.load_default()
    font_izin = ImageFont.load_default()
    font_expired = ImageFont.load_default()

  text_color_dark = (20, 20, 20)
  text_color_yellow = (230, 175, 40)
  text_color_white = (255, 255, 255)

  if photo_file is not None:
    photo = Image.open(photo_file).convert("RGBA")
    photo_size = (280, 350)
    photo = photo.resize(photo_size, Image.Resampling.LANCZOS)
    photo_position = (150, 160)
    base_image.paste(photo, photo_position, photo)

  # Tulis Teks Identitas
  draw.text((50, 500), f"{nama}", fill=text_color_dark, font=font_nama)
  draw.text((50, 570), f"{nik}", fill=text_color_dark, font=font_detail)
  draw.text((50, 615), f"{jabatan}", fill=text_color_dark, font=font_detail)
  draw.text(
      (500, 520), f"{lokasi_alat}", fill=text_color_dark, font=font_box
  )
  draw.text(
      (200, 715), f"{izin_alat}", fill=text_color_yellow, font=font_izin
  )
  draw.text(
      (150, 950),
      f"Expired : {expired_date}",
      fill=text_color_white,
      font=font_expired,
  )

  return base_image


# Fungsi untuk memproses Sisi Belakang
def generate_sisi_belakang():
  try:
    base_image = Image.open("template_belakang.png").convert("RGBA")
  except FileNotFoundError:
    base_image = Image.new("RGBA", (850, 1200), (255, 255, 255, 255))
  return base_image


# --- TAMPILAN UTAMA APLIKASI ---
st.subheader("Pratinjau Mine Permit")

if sisi_pilihan == "Sisi Depan":
  final_card = generate_sisi_depan(
      nama, nik, jabatan, lokasi_alat, izin_alat, expired_date, uploaded_photo
  )
  st.image(
      final_card, caption="Pratinjau Mine Permit (Depan)", use_container_width=True
  )

  buffered = io.BytesIO()
  final_card.convert("RGB").save(buffered, format="PNG")
  st.download_button(
      label="📥 Unduh Sisi Depan (PNG)",
      data=buffered.getvalue(),
      file_name=f"MinePermit_Depan_{nik}.png",
      mime="image/png",
  )

elif sisi_pilihan == "Sisi Belakang":
  final_card = generate_sisi_belakang()
  st.image(
      final_card,
      caption="Pratinjau Mine Permit (Belakang)",
      use_container_width=True,
  )

  buffered = io.BytesIO()
  final_card.convert("RGB").save(buffered, format="PNG")
  st.download_button(
      label="📥 Unduh Sisi Belakang (PNG)",
      data=buffered.getvalue(),
      file_name="MinePermit_Belakang.png",
      mime="image/png",
  )

else:
  card_depan = generate_sisi_depan(
      nama, nik, jabatan, lokasi_alat, izin_alat, expired_date, uploaded_photo
  )
  card_belakang = generate_sisi_belakang()

  st.image(
      card_depan, caption="Pratinjau Mine Permit (Depan)", use_container_width=True
  )
  st.image(
      card_belakang,
      caption="Pratinjau Mine Permit (Belakang)",
      use_container_width=True,
  )
