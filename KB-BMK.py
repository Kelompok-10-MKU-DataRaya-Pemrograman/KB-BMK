# Program: Kalkulator Biaya Bongkar Muat Kontainer (KB-BMK)

import csv
from datetime import datetime

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


def main():
    print("=" * 50)
    print("KALKULATOR BIAYA BONGKAR MUAT KONTAINER (KB-BMK)")
    print("=" * 50)
    
    output_data = []
    
    # FITUR IMPORT CSV
    input_filename = input("Masukkan nama file CSV input (contoh: daftar_kapal.csv): ")

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

