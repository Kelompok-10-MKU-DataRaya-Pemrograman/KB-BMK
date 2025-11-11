# KB-BMK (Kalkulator Biaya Bongkar Muat Kontainer)

## Deskripsi Proyek
**KB-BMK** adalah program sederhana yang dibuat untuk menghitung **biaya bongkar muat kontainer di pelabuhan**.  
Aplikasi ini dikembangkan sebagai bagian dari pembelajaran berbasis proyek (*Project Based Learning*) untuk program studi **Manajemen Pelabuhan dan Logistik Maritim**, Fakultas Teknik.

Program ini sekarang bekerja dengan memproses data secara batch dari file .csv. Pengguna menyediakan file data (seperti daftar_kapal.csv) yang berisi daftar pelabuhan, jenis kontainer, dan jumlah. Program kemudian akan menghitung total biaya untuk semua entri di dalam file tersebut.

---

## Fitur Utama
- **Import Data Batch**: Membaca data pelabuhan dan kontainer langsung dari file `.csv`.
- **Ekspor Hasil ke CSV**: Menghasilkan file `.csv` baru yang berisi rincian perhitungan, lengkap dengan *timestamp* unik pada nama filenya (contoh: `output_biaya_20251111_220000.csv`).
- **Pencatatan Riwayat (Logging)**: Menyimpan riwayat semua hasil perhitungan ke dalam satu file database SQLite (`riwayat_biaya.db`) untuk pencatatan jangka panjang.
- **Penanganan Error**: Memberikan pesan error jika file input tidak ditemukan atau jika data (misal: kolom 'Jumlah') di dalam CSV tidak valid.
- **Struktur Kode Modular**: Tetap menggunakan fungsi dan kelas untuk struktur kode yang bersih. 

---

## Cara Menjalankan Program
1. **Clone repository** ini ke komputer lokal:
   ```bash
   git clone https://github.com/Kelompok-10-MKU-DataRaya-Pemrograman/KB-BMK.git
   
2. Masuk ke folder proyek:
   ```bash
   cd KB-BMK

3. Pastikan Python versi 3.11 sudah terpasang.

4. **Data Input**: Program ini memerlukan file data `.csv` untuk dijalankan. Sebuah file contoh `daftar_kapal.csv` sudah tersedia di repository.
   > **Penting**: Pastikan file CSV Anda menggunakan **titik koma (`;`)** sebagai pemisah (delimiter) dan memiliki kolom-kolom: `Pelabuhan`, `Jenis`, dan `Jumlah`.

5. **Jalankan program**:
   ```bash
   python KB-BMK.py

6. Saat diminta, masukkan nama file CSV input Anda (contoh: `daftar_kapal.csv`).

7. **Cek Hasil**: Setelah program selesai, Anda akan menemukan dua jenis output di folder Anda:
   * File CSV baru (misal: `output_biaya_20251111_220000.csv`)
   * File database `riwayat_biaya.db` (file ini akan dibuat jika belum ada dan akan diperbarui setiap kali program dijalankan).

---

## Lisensi
Proyek ini dibuat untuk tujuan pendidikan dalam mata kuliah Pemrograman Dasar dan tidak digunakan untuk kepentingan komersial.

---

## Fakultas Teknik - Program Studi Manajemen Pelabuhan dan Logistik Maritim
Universitas Negeri Jakarta
© 2025 Kelompok 10 MKU Data Raya Pemrograman
