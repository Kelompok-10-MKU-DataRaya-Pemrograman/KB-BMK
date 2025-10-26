# Katheelin Quina

# Program: Kalkulator Biaya Bongkar Muat Kontainer (KB-BMK)

class Kontainer:
    def __init__(self, jenis):
        self.jenis = jenis
        if self.jenis == "20":
            self.tarif = 500000
        elif self.jenis == "40":
            self.tarif = 900000
        else:
            self.tarif = 0

    # Anggita Nayla

    def hitung_biaya(self, jumlah):
        return self.tarif * jumlah

def hitung_biaya(jenis, jumlah):
    kontainer = Kontainer(jenis)
    return kontainer.hitung_biaya(jumlah)

# Siti Nurhaliza

def main():
    print("=" * 50)
    print("KALKULATOR BIAYA BONGKAR MUAT KONTAINER (KB-BMK)")
    print("=" * 50)

    skenario = int(input("Masukkan jumlah skenario perhitungan: "))

    for i in range(skenario):
        print(f"\nSkenario {i+1}")
        print("Jenis Kontainer: 20 feet / 40 feet")
        jenis = input("Pilih jenis kontainer (20/40): ")
        jumlah = int(input("Masukkan jumlah kontainer: "))

        total = hitung_biaya(jenis, jumlah)

        if jenis == "20":
            tarif = 500000
        elif jenis == "40":
            tarif = 900000
        else:
            tarif = 0

        if tarif > 0:
            print(f"Tarif per kontainer: Rp {tarif:,}")
            print(f"Jumlah kontainer: {jumlah}")
            print(f"Total biaya: Rp {total:,}")
        else:
            print("Jenis kontainer tidak valid. Gunakan 20 atau 40.")

    print("\nPerhitungan selesai.")
