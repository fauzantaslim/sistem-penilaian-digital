# Sistem Penilaian Digital 🎓

Sistem Penilaian Digital adalah aplikasi web berbasis **Flask** yang digunakan untuk membantu guru atau tenaga pendidik dalam mengelola penilaian lembar jawaban secara digital. Aplikasi ini dilengkapi dengan antarmuka (UI) modern menggunakan Jinja2 Template, dilengkapi dengan fitur pengelolaan siswa, mata pelajaran, kunci jawaban, serta fitur pelaporan hasil yang dapat diekspor ke format Excel.

## 🌟 Fitur Utama

- **Autentikasi (Satu Aktor: Guru)**: Login, Register, dan sesi yang aman.
- **Dashboard Ringkasan**: Statistik data siswa, mapel, dan grafik aktivitas penilaian.
- **Kelola Data Siswa**: CRUD data siswa beserta pencarian.
- **Kelola Mata Pelajaran**: Manajemen mapel dan kodenya.
- **Kunci Jawaban**: Pengaturan kunci jawaban (A, B, C, D, E) untuk tiap mata pelajaran.
- **Upload Lembar Jawaban**: Mendukung upload *batch* file gambar (JPG/PNG) via drag & drop.
- **Laporan Penilaian**: Menampilkan hasil penilaian dengan skor dan status, dilengkapi filter pencarian.
- **Export Laporan**: Ekspor data laporan hasil penilaian ke format **Microsoft Excel (.xlsx)**.

---

## 🛠️ Persyaratan Sistem

- **Python**: Versi 3.x (disarankan 3.8 ke atas)
- **Pip**: Package manager bawaan Python.

---

## 🚀 Cara Instalasi & Menjalankan Aplikasi

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di komputer/laptop Anda:

### 1. Buka Direktori Proyek
Buka terminal (Command Prompt / PowerShell) dan arahkan ke direktori proyek ini:
```bash
cd path/to/Sistempenilaiandigital
```

### 2. (Opsional) Buat Virtual Environment
Disarankan untuk membuat virtual environment agar *dependencies* tidak bentrok dengan aplikasi Python lainnya:
```bash
python -m venv venv

# Aktivasi venv (Windows Command Prompt):
venv\Scripts\activate

# Aktivasi venv (Windows PowerShell):
.\venv\Scripts\activate

# Aktivasi venv (macOS/Linux):
source venv/bin/activate
```

### 3. Install Dependencies
Install semua pustaka (library) yang dibutuhkan aplikasi melalui file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Jalankan Server Flask
Gunakan file `run.py` untuk menjalankan server aplikasi. Database SQLite (`app.db`) akan otomatis dibuat pada saat pertama kali program dijalankan.
```bash
python run.py
```

### 5. Buka di Web Browser
Jika server sudah berjalan dengan pesan indikator seperti `Running on http://127.0.0.1:5000`, buka URL berikut di web browser Anda (Chrome, Edge, Firefox):
```
http://localhost:5000
```
- Buat akun terlebih dahulu melalui halaman **Daftar Akun** (Register).
- Setelah akun dibuat, silakan **Login** untuk masuk ke Dashboard.

---

## 📁 Struktur Proyek
```text
Sistempenilaiandigital/
├── app/
│   ├── routes/              # Controller / Endpoint logic
│   ├── templates/           # File HTML (Jinja2)
│   ├── static/              # CSS, JavaScript, Images, dan folder Upload
│   ├── __init__.py          # Flask App Factory Blueprint
│   ├── extensions.py        # Inisialisasi DB, CSRF, & Login Manager
│   └── models.py            # Skema Database (SQLite)
├── config.py                # Konfigurasi Environment & Flask
├── run.py                   # File utama (Entry Point)
├── requirements.txt         # Daftar Dependencies Pustaka
└── app.db                   # (Otomatis dibuat) File Database SQLite
```

## 📝 Catatan Tambahan
* Folder `app/static/uploads` akan terbuat secara otomatis untuk menyimpan file gambar lembar jawaban.
* Untuk saat ini, integrasi pemrosesan gambar OCR / OMR AI dilakukan pada modul terpisah atau di tahap pengembangan berikutnya.
