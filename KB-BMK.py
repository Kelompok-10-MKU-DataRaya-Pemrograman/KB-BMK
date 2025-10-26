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


