# 📚 Info Walimurid - MIT Al Falah

Sistem Informasi Perkembangan Siswa berbasis Web Statis yang terintegrasi langsung dengan Firebase Firestore.

## 🌟 Fitur Utama
- **Akses Tanpa Login untuk Walimurid**: Cari nama anak atau pilih kelas secara instan.
- **Monitoring Nilai & Absensi**: Menampilkan grafik perkembangan nilai, kehadiran, serta rekomendasi guru.
- **Panel Guru**: Kelola data siswa, input nilai, dan cetak laporan.
- **Progressive Web App (PWA)**: Dapat diinstal langsung di layar utama smartphone.
- **Simpan ke Favorit & QR Code**: Memudahkan walimurid mengakses profil anak.

## 🚀 Cara Menjalankan Lokal
1. Buat berkas `.env` dari contoh `.env.example`:
   ```bash
   cp .env.example .env

Isi kredensial Firebase di .env.
Generate konfigurasi JS:
bash generate-config.sh

Jalankan server lokal:
python -m http.server 8000

Buka http://localhost:8000 di browser.
🌐 Deploy ke GitHub Pages
​Cukup upload seluruh berkas proyek ke repositori GitHub, lalu aktifkan GitHub Pages di menu Settings > Pages repositori Anda.
