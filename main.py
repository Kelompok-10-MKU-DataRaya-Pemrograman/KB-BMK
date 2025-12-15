# Program: Kalkulator Biaya Bongkar Muat Kontainer (KB-BMK)

import csv
from datetime import datetime
import sqlite3

class Kontainer:
    def __init__(self, jenis):
        self.jenis = jenis
        if self.jenis == "20":
            self.tarif = 500000
        elif self.jenis == "40":
            self.tarif = 900000
        else:
            self.tarif = 0

    def hitung_biaya(self, jumlah):
        return self.tarif * jumlah

def hitung_biaya(jenis, jumlah):
    kontainer = Kontainer(jenis)
    return kontainer.hitung_biaya(jumlah)

def setup_database(db_name):
    """Membuat koneksi DB dan tabel 'perhitungan' jika belum ada."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Tabel untuk menyimpan riwayat semua hasil perhitungan
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS perhitungan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        waktu_eksekusi TEXT,
        pelabuhan TEXT,
        jenis_kontainer TEXT,
        jumlah INTEGER,
        tarif_per_kontainer INTEGER,
        total_biaya INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

def simpan_ke_db(db_name, data_list, timestamp):
    """Menyimpan list data hasil perhitungan ke database."""
    
    # Menambahkan timestamp di awal setiap baris data
    data_untuk_db = []
    for row in data_list:
        data_untuk_db.append( (timestamp, row[0], row[1], row[2], row[3], row[4]) )

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.executemany('''
    INSERT INTO perhitungan (
        waktu_eksekusi, pelabuhan, jenis_kontainer, jumlah, tarif_per_kontainer, total_biaya
    ) VALUES (?, ?, ?, ?, ?, ?)
    ''', data_untuk_db)
    
    conn.commit()
    conn.close()


def main():
    print("=" * 50)
    print("KALKULATOR BIAYA BONGKAR MUAT KONTAINER (KB-BMK)")
    print("=" * 50)
    
    db_name = 'riwayat_biaya.db' # Nama file Database
    setup_database(db_name)    # Memanggil fungsi setup database

    output_data = []
    
    # FITUR IMPORT CSV
    input_filename = input("Masukkan nama file CSV input (contoh: daftar_kapal.csv): ")

    print("\nTarif 20 feet/kontainer : Rp 500,000")
    print("Tarif 20 feet/kontainer : Rp 900,000")

    try:
        with open(input_filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            
            print(f"\nMemproses data dari {input_filename}...")

            # PROSES DATA CSV
            for row in csv_reader:
                try:
                    pelabuhan = row['Pelabuhan']
                    jenis = row['Jenis']
                    jumlah = int(row['Jumlah'])

                    total = hitung_biaya(jenis, jumlah)

                    if jenis == "20":
                        tarif = 500000
                    elif jenis == "40":
                        tarif = 900000
                    else:
                        tarif = 0
                    
                    if tarif > 0:
                        print(f"  - {pelabuhan} ({jumlah} kontainer @ {jenis} feet): Rp {total:,}")
                        output_data.append([pelabuhan, jenis, jumlah, tarif, total])
                    else:
                        print(f"  - {pelabuhan}: Jenis kontainer '{jenis}' tidak valid.")

                except ValueError:
                    print(f"  - Error: 'Jumlah' pada baris {csv_reader.line_num} bukan angka.")
                except KeyError as e:
                    print(f"  - Error: Kolom {e} tidak ditemukan di CSV.")

        # FITUR EXPORT CSV
        if not output_data:
            print("\nTidak ada data valid yang diproses.")
            return

        # Buat nama file output dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"output_biaya_{timestamp}.csv"

        # Menyimpan Riwayat ke Database
        try:
            simpan_ke_db(db_name, output_data, timestamp)
            print(f"\nData telah disimpan ke database: {db_name}")
        except Exception as e:
            print(f"\nError saat menyimpan ke database: {e}")

        with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Pelabuhan', 'Jenis Kontainer', 'Jumlah', 'Tarif per Kontainer', 'Total Biaya'])
            writer.writerows(output_data)

        print(f"\nPerhitungan selesai. Hasil telah diekspor ke: {output_filename}")

    except FileNotFoundError:
        print(f"Error: File '{input_filename}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi error: {e}")


if __name__ == "__main__":
    main()

