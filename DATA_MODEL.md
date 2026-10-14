# 📊 Model Data — Info Walimurid

## Struktur Koleksi Firestore

### 1. siswa/{KODE} — Data master siswa
Contoh ID: 4B-001, 4C-015. Kode = ID dokumen, tidak bisa diubah.

| Field | Tipe | Wajib |
|---|---|---|
| nama | string | ✅ |
| kelas | string | ✅ |
| access_code | string | ✅ |

### 2. nilai/{KODE}__{PERIODE} — Nilai aspek per periode
Contoh ID: 4B-001__STS 1

| Field | Tipe | Keterangan |
|---|---|---|
| siswaId | string | Kode siswa |
| period | string | STS 1 / STS 2 / SAS |
| a0 | string | Membaca |
| a1 | string | Menulis |
| a2 | string | Berhitung |
| a3 | string | Menghafal |

### 3. absensi/{KODE}__{PERIODE}

| Field | Tipe |
|---|---|
| siswaId | string |
| period | string |
| hadir | number |
| sakit | number |
| izin | number |
| alfa | number |

### 4. catatan/{auto-id}

| Field | Tipe |
|---|---|
| siswaId | string |
| period | string |
| text | string |
| ts | timestamp |

### 5. kelas/{KELAS} — Wali kelas

| Field | Tipe |
|---|---|
| wali | string |

### 6. settings/main — Identitas sekolah

| Field | Tipe |
|---|---|
| name | string |
| npsn | string |
| address | string |
| logo | string |
| year | string |
| headmaster | string |

## Skor Aspek

| Kode | Arti | Skor |
|---|---|---|
| L | Lancar | 90 |
| CL | Cukup Lancar | 80 |
| KL | Kurang Lancar | 70 |
| (kosong) | Belum dinilai | — |

## Kategori Nilai Akhir

| Rentang | Kategori |
|---|---|
| >= 85 | Baik |
| 75-84 | Cukup |
| < 75 | Perlu pendampingan |

## Urutan Aspek (a0-a3)
- a0 = Membaca
- a1 = Menulis
- a2 = Berhitung
- a3 = Menghafal
