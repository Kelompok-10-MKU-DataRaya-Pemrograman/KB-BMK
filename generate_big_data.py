import csv
import random
from datetime import datetime

# Konfigurasi Data
FILENAME = "big_data_biaya_pelabuhan.csv"
TARGET_SIZE_MB = 2.5  # Target ukuran file > 2MB
DELIMITER = ";"

# Data Sampel
pelabuhan_list = [
    "Tanjung Priok", "Tanjung Perak", "Belawan", "Makassar", 
    "Tanjung Emas", "Teluk Bayur", "Pontianak", "Palembang", 
    "Panjang", "Benoa"
]
jenis_list = ["20", "40"]
tarif_map = {"20": 500000, "40": 900000}

def generate_data():
    print(f"Sedang men-generate data ke '{FILENAME}'...")
    
    with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=DELIMITER)
        writer.writerow(['Pelabuhan', 'Jenis Kontainer', 'Jumlah', 'Tarif per Kontainer', 'Total Biaya'])
        
        file_size = 0
        rows = 0
        
        # Loop sampai ukuran file mencapai target
        while file_size < (TARGET_SIZE_MB * 1024 * 1024):
            pelabuhan = random.choice(pelabuhan_list)
            jenis = random.choice(jenis_list)
            jumlah = random.randint(1, 50) # Random jumlah 1-50 kontainer
            tarif = tarif_map[jenis]
            total = jumlah * tarif
            
            writer.writerow([pelabuhan, f"{jenis} feet", jumlah, tarif, total])
            
            rows += 1
            if rows % 1000 == 0:
                file.flush()
                file_size = file.tell()

    print(f"Selesai! {rows} baris data berhasil dibuat.")
    print(f"Ukuran file: {file_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    generate_data()