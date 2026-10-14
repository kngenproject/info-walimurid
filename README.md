# 📚 Info Walimurid — MIT Al Falah

Sistem Informasi Perkembangan Siswa berbasis web statis, terintegrasi Firebase Firestore.

## 🌟 Fitur

**Walimurid (tanpa login):**
- Cari nama anak / pilih kelas
- Nilai 4 aspek (Membaca, Menulis, Berhitung, Menghafal)
- Absensi, grafik tren, catatan guru
- Cetak, share WhatsApp, favorit

**Guru (login):**
- Input nilai manual per siswa
- Import CSV & Excel (.xlsx dropdown + validasi)
- Export CSV per kelas
- Kelola siswa, atur identitas sekolah
- Seed data awal 68 siswa contoh

**Teknis:**
- PWA, offline-first, auto-seed, force server fetch

## 🚀 Menjalankan Lokal

1. Clone repo & masuk folder
2. `cp .env.example .env` lalu isi kredensial Firebase
3. `bash generate-config.sh`
4. `python3 -m http.server 8000`
5. Buka http://localhost:8000

## 🌐 Deploy GitHub Pages

1. Push semua file
2. `.env` & `config.js` tidak ikut ter-push (sudah di-`.gitignore`)
3. Untuk Pages: commit `config.js` manual ke `gh-pages`, atau pakai GitHub Actions secrets
4. Aktifkan di Settings → Pages

## 🔐 Firestore Rules

Wajib di-publish ke Firebase Console:
1. Buka https://console.firebase.google.com/project/NAMA-PROJECT/firestore/rules
2. Paste isi `firestore.rules`
3. Klik Publish

- **Publik baca** — siswa, nilai, absensi, catatan, kelas, settings
- **Guru tulis** — semua koleksi (login Firebase Auth)

## 📖 Dokumentasi

- `PANDUAN_GURU.md` — cara mengisi nilai
- `DATA_MODEL.md` — struktur Firestore
- `templates/` — contoh CSV

## 📄 Lisensi

MIT — lihat `LICENSE`.
