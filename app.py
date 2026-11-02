import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Mine Permit Generator", page_icon="🪪", layout="centered"
)

st.title("🪪 Generator Mine Permit (Depan & Belakang)")
st.write(
    "Masukkan data karyawan secara lengkap, lalu pilih sisi kartu yang ingin ditampilkan."
)

# Sidebar untuk Input Data & Pilihan Sisi Kartu
with st.sidebar:
  st.header("1. Pilih Tampilan")
  sisi_pilihan = st.radio(
      "Tampilkan Sisi:", ("Sisi Depan", "Sisi Belakang", "Tampilkan Keduanya")
  )

  st.header("2. Input Data Karyawan")
  nama = st.text_input("Nama Lengkap", "Maikel Pandori")
  jabatan = st.text_input("Jabatan / Role", "DRIVER")
  nik = st.text_input("NIP / No. Induk", "MN-PTBSA 0002")

  # Input tambahan sesuai permintaan
  izin_alat = st.text_input(
      "Izin Op Alat Berat (Simper / Ket)", "Light Vehicle ( LV )"
  )
  lokasi_alat = st.text_input("Lokasi Area Op Alat Berat", "AB")
  expired_date = st.text_input("Masa Berlaku (Expired)", "19 Oktober 2027")

  st.header("3. Upload Foto")
  uploaded_photo = st.file_uploader(
      "Pilih Foto (JPG/PNG)", type=["jpg", "jpeg", "png"]
  )


# Fungsi untuk memproses Sisi Depan
def generate_sisi_depan(
    nama, jabatan, nik, izin_alat, lokasi_alat, expired_date, photo_file
):
  try:
    base_image = Image.open("template_depan.png").convert("RGBA")
  except FileNotFoundError:
    base_image = Image.new("RGBA", (1012, 638), (240, 240, 240, 255))

  draw = ImageDraw.Draw(base_image)

  # Konfigurasi Font
  try:
    font_nama = ImageFont.truetype("arial.ttf", 32)
    font_detail = ImageFont.truetype("arial.ttf", 22)
    font_kecil = ImageFont.truetype("arial.ttf", 18)
  except IOError:
    font_nama = ImageFont.load_default()
    font_detail = ImageFont.load_default()
    font_kecil = ImageFont.load_default()

  text_color = (0, 0, 0)

  # 1. Tempel Foto (Sesuaikan koordinat x, y dan ukuran kotak foto)
  if photo_file is not None:
    photo = Image.open(photo_file).convert("RGBA")
    photo_size = (180, 220)  # Sesuaikan ukuran foto
    photo = photo.resize(photo_size, Image.Resampling.LANCZOS)
    photo_position = (265, 375)  # Sesuaikan titik koordinat (x, y) foto
    base_image.paste(photo, photo_position, photo)

  # 2. Tulis Teks ke Sisi Depan (Sesuaikan koordinat x, y teks dengan template Anda)
  draw.text((265, 620), f"{nama}", fill=text_color, font=font_nama)
  draw.text((265, 675), f"{nik}", fill=text_color, font=font_detail)
  draw.text((265, 710), f"{jabatan}", fill=text_color, font=font_detail)

  # Menambahkan teks baru ke template (Sesuaikan koordinat x, y sesuai posisi di gambar Anda)
  draw.text(
      (500, 480), f"{lokasi_alat}", fill=text_color, font=font_detail
  )  # Contoh koordinat Lokasi Alat
  draw.text(
      (350, 630), f"{izin_alat}", fill=text_color, font=font_detail
  )  # Contoh koordinat Izin Alat
  draw.text(
      (350, 780), f"{expired_date}", fill=text_color, font=font_kecil
  )  # Contoh koordinat Expired

  return base_image


# Fungsi untuk memproses Sisi Belakang
def generate_sisi_belakang():
  try:
    base_image = Image.open("template_belakang.png").convert("RGBA")
  except FileNotFoundError:
    base_image = Image.new("RGBA", (1012, 638), (240, 240, 240, 255))
  return base_image


# --- TAMPILAN UTAMA APLIKASI ---
st.subheader("Pratinjau Mine Permit")

if sisi_pilihan == "Sisi Depan":
  final_card = generate_sisi_depan(
      nama, jabatan, nik, izin_alat, lokasi_alat, expired_date, uploaded_photo
  )
  st.image(
      final_card, caption="Mine Permit - Sisi Depan", use_container_width=True
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
      final_card, caption="Mine Permit - Sisi Belakang", use_container_width=True
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
  # Tampilkan Keduanya Sekaligus
  card_depan = generate_sisi_depan(
      nama, jabatan, nik, izin_alat, lokasi_alat, expired_date, uploaded_photo
  )
  card_belakang = generate_sisi_belakang()

  st.image(
      card_depan, caption="Mine Permit - Sisi Depan", use_container_width=True
  )
  st.image(
      card_belakang,
      caption="Mine Permit - Sisi Belakang",
      use_container_width=True,
  )
