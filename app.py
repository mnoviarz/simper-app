import io
import zipfile
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Generator Mine Permit", page_icon="🪪", layout="centered"
)

st.title("🪪 Generator Mine Permit (Depan & Belakang)")
st.write(
    "Pilih mode penginputan data di sidebar: secara satuan atau massal via"
    " Excel/CSV."
)

# Sidebar untuk Input Data & Pengaturan
with st.sidebar:
  st.header("1. Pilih Mode Pembuatan")
  mode = st.radio("Mode:", ("Input Satuan", "Input Massal (Excel/CSV)"))

  st.header("2. Pilih Tampilan Sisi")
  sisi_pilihan = st.radio(
      "Tampilkan Sisi:", ("Sisi Depan", "Sisi Belakang", "Tampilkan Keduanya")
  )

  st.header("3. Pengaturan Cetak")
  tampilkan_garis_potong = st.checkbox(
      "Tampilkan Garis Potong (Cutting Guide)", value=False
  )

  st.header("4. Upload Foto Utama")
  uploaded_photo = st.file_uploader(
      "Pilih Foto (JPG/PNG)", type=["jpg", "jpeg", "png"]
  )


# Fungsi untuk memproses Sisi Depan
def generate_sisi_depan(
    nama,
    nik,
    jabatan,
    lokasi_alat,
    izin_alat,
    expired_date,
    photo_file,
    tampilkan_garis_potong=False,
):
  try:
    base_image = Image.open("template_depan.png").convert("RGBA")
  except FileNotFoundError:
    base_image = Image.new("RGBA", (850, 1200), (255, 255, 255, 255))

  draw = ImageDraw.Draw(base_image)

  # Konfigurasi Font secara aman per baris
  try:
    font_nama = ImageFont.truetype("arial_narrow_7.ttf", 55)
  except IOError:
    font_nama = ImageFont.load_default()

  try:
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
  text_color_green = (35, 115, 110)

  if photo_file is not None:
    try:
      photo = Image.open(photo_file).convert("RGBA")
      photo_size = (250, 300)
      photo = photo.resize(photo_size, Image.Resampling.LANCZOS)
      photo_position = (100, 200)
      base_image.paste(photo, photo_position, photo)
    except Exception:
      pass

  # Tulis Teks Identitas
  draw.text((50, 500), f"{nama}", fill=text_color_dark, font=font_nama)
  draw.text((50, 570), f"{nik}", fill=text_color_dark, font=font_detail)
  draw.text((50, 615), f"{jabatan}", fill=text_color_dark, font=font_detail)
  draw.text(
      (500, 520), f"{lokasi_alat}", fill=text_color_green, font=font_box
  )
  draw.text(
      (200, 715), f"{izin_alat}", fill=text_color_yellow, font=font_izin
  )
  draw.text(
      (150, 980),
      f" {expired_date}",
      fill=text_color_white,
      font=font_expired,
  )

  # Tambahkan Garis Potong (Cutting Guide) jika dicentang di sidebar
  if tampilkan_garis_potong:
    draw.rectangle(
        [0, 0, base_image.width - 1, base_image.height - 1],
        outline=(150, 150, 150),
        width=2,
    )

  return base_image


# Fungsi untuk memproses Sisi Belakang
def generate_sisi_belakang(tampilkan_garis_potong=False):
  try:
    base_image = Image.open("template_belakang.png").convert("RGBA")
  except FileNotFoundError:
    base_image = Image.new("RGBA", (850, 1200), (255, 255, 255, 255))

  if tampilkan_garis_potong:
    draw = ImageDraw.Draw(base_image)
    draw.rectangle(
        [0, 0, base_image.width - 1, base_image.height - 1],
        outline=(150, 150, 150),
        width=2,
    )

  return base_image


# --- LOGIKA UTAMA APLIKASI ---

if mode == "Input Satuan":
  st.subheader("Form Input Data Satuan")
  col1, col2 = st.columns(2)
  with col1:
    nama = st.text_input("Nama Lengkap", "Maikel Pandori")
    nik = st.text_input("NIP / No. Induk", "MN-PTBSA 0002")
    jabatan = st.text_input("Jabatan / Role", "DRIVER")
  with col2:
    lokasi_alat = st.text_input("Lokasi Op. Alat (SIMPER)", "AB")
    izin_alat = st.text_input("Izin Op. Alat", "Light Vehicle ( LV )")
    expired_date = st.text_input("Masa Berlaku (Expired)", "19 Oktober 2027")

  st.subheader("Pratinjau Mine Permit")

  if sisi_pilihan == "Sisi Depan":
    final_card = generate_sisi_depan(
        nama,
        nik,
        jabatan,
        lokasi_alat,
        izin_alat,
        expired_date,
        uploaded_photo,
        tampilkan_garis_potong,
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
    final_card = generate_sisi_belakang(tampilkan_garis_potong)
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
        mime="application/octet-stream",
    )

  else:
    card_depan = generate_sisi_depan(
        nama,
        nik,
        jabatan,
        lokasi_alat,
        izin_alat,
        expired_date,
        uploaded_photo,
        tampilkan_garis_potong,
    )
    card_belakang = generate_sisi_belakang(tampilkan_garis_potong)

    st.image(
        card_depan, caption="Pratinjau Mine Permit (Depan)", use_container_width=True
    )
    st.image(
        card_belakang,
        caption="Pratinjau Mine Permit (Belakang)",
        use_container_width=True,
    )

else:
  st.subheader("📁 Generator Batch / Massal via File Excel/CSV")
  st.write(
      "Unggah file Excel (`.xlsx`) atau CSV berisi data karyawan untuk"
      " digenerate secara otomatis."
  )

  with st.expander("💡 Contoh Format Kolom yang Dibutuhkan"):
    sample_df = pd.DataFrame({
        "Nama": ["Maikel Pandori", "Amon Rouw"],
        "NIK": ["MN-PTBSA 0002", "MN-PTBSA 0005"],
        "Jabatan": ["DRIVER", "FOREMAN"],
        "Lokasi_Alat": ["AB", "A"],
        "Izin_Alat": ["Light Vehicle ( LV )", "Dump Truck"],
        "Expired": ["19 Oktober 2027", "20 Desember 2027"],
    })
    st.dataframe(sample_df)

  uploaded_file = st.file_uploader(
      "Upload File Data (Excel/CSV)", type=["xlsx", "csv"]
  )

  if uploaded_file is not None:
    try:
      if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
      else:
        df = pd.read_excel(uploaded_file)

      st.success(
          f"Berhasil memuat {len(df)} data karyawan dari file."
      )
      st.dataframe(df.head())

      if st.button("🚀 Proses & Generate Semua Kartu (ZIP)"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(
            zip_buffer, "w", zipfile.ZIP_DEFLATED
        ) as zip_file:
          for index, row in df.iterrows():
            p_nama = str(row.get("Nama", ""))
            p_nik = str(row.get("NIK", ""))
            p_jabatan = str(row.get("Jabatan", ""))
            p_lokasi = str(row.get("Lokasi_Alat", ""))
            p_izin = str(row.get("Izin_Alat", ""))
            p_expired = str(row.get("Expired", ""))

            # Buat Sisi Depan
            card_d = generate_sisi_depan(
                p_nama,
                p_nik,
                p_jabatan,
                p_lokasi,
                p_izin,
                p_expired,
                uploaded_photo,
                tampilkan_garis_potong,
            )
            img_io_d = io.BytesIO()
            card_d.convert("RGB").save(img_io_d, format="PNG")
            zip_file.writestr(
                f"MinePermit_Depan_{p_nik.replace(' ', '_')}.png",
                img_io_d.getvalue(),
            )

            # Buat Sisi Belakang
            card_b = generate_sisi_belakang(tampilkan_garis_potong)
            img_io_b = io.BytesIO()
            card_b.convert("RGB").save(img_io_b, format="PNG")
            zip_file.writestr(
                f"MinePermit_Belakang_{p_nik.replace(' ', '_')}.png",
                img_io_b.getvalue(),
            )

        zip_buffer.seek(0)
        st.success(
            "Semua kartu berhasil digenerate! Silakan klik tombol di bawah untuk"
            " mengunduh file ZIP."
        )
        st.download_button(
            label="📥 Unduh Semua Kartu (ZIP)",
            data=zip_buffer,
            file_name="Batch_Mine_Permits.zip",
            mime="application/zip",
        )

    except Exception as e:
      st.error(
          f"Terjadi kesalahan saat membaca file atau memproses data: {e}"
      )
