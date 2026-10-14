# 📘 Panduan Guru — Info Walimurid

## 🎯 Periode Penilaian

| Periode | Kapan | Yang Diisi |
|---|---|---|
| STS 1 | Akhir semester 1 | Nilai 4 aspek + Absensi |
| STS 2 | Tengah semester 2 | Nilai 4 aspek + Absensi |
| SAS | Akhir semester 2 | Nilai 4 aspek + Absensi |

## 📝 Data yang Harus Diisi

### A. Nilai 4 Aspek (WAJIB)

| Aspek | Kode | Arti | Skor |
|---|---|---|---|
| Membaca | L | Lancar | 90 |
| Menulis | CL | Cukup Lancar | 80 |
| Berhitung | KL | Kurang Lancar | 70 |
| Menghafal | (kosong) | Belum dinilai | — |

### B. Absensi (WAJIB)
Isi jumlah hari: hadir, sakit, izin, alfa (angka).

### C. Catatan Guru (OPSIONAL)
Teks bebas.

## 🖥️ Tiga Cara Mengisi

### Cara 1 — Manual
1. Login Panel Guru
2. Tab Nilai → pilih periode → pilih kelas
3. Klik Edit pada baris siswa
4. Isi 4 aspek + absensi + catatan → Simpan & Berikutnya

### Cara 2 — Import Excel (disarankan)
1. Tab Import → pilih periode
2. Pilih kelas → Unduh Template Excel
3. Isi di Excel/Google Sheets (dropdown L/CL/KL tersedia)
4. Simpan .xlsx → Import Excel

### Cara 3 — Import CSV
1. Tab Import → pilih periode
2. Unduh Template CSV → buka di Excel/Sheets
3. Simpan .csv → Import CSV

## 📄 Format CSV

kode,nama,kelas,membaca,menulis,berhitung,menghafal,hadir,sakit,izin,alfa
4B-001,ADZKIYA RARAS MAHFUDZA,4B,CL,KL,L,L,20,0,0,0

Penting:
- Kolom kode tidak boleh diubah (ID unik siswa)
- Kode sama akan ditimpa — aman untuk koreksi
- Nilai valid: L / CL / KL / kosong

## ❓ FAQ

Q: Kode siswa bisa diubah?
A: Tidak. Kode = ID unik di database.

Q: Siswa pindah kelas?
A: Tab Siswa → Edit → ganti kelas. Nilai lama tetap di kode lama.

Q: Walimurid bisa lihat catatan guru?
A: Ya, catatan tampil di profil siswa.

Q: Walimurid bisa ubah data?
A: Tidak. Hanya akun guru yang bisa menulis.

## 🔐 Akun Guru

- Login di Panel Guru → email + password
- Akun dibuat admin Firebase (tidak bisa self-register)
- Lupa password? Hubungi admin sekolah
