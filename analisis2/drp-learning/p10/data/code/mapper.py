#!/usr/bin/env python3

import sys

# Lewati header CSV
first_line = True

for line in sys.stdin:
    # Bersihkan whitespace
    line = line.strip()
    
    # Skip baris kosong
    if not line:
        continue
        
    # Skip header logic
    if first_line:
        
        if "Pelabuhan" in line:
            first_line = False
            continue

        first_line = False

    # Split data menggunakan delimiter titik koma (;)
    parts = line.split(";")
    
    # Validasi struktur data (harus ada 5 kolom)
    if len(parts) == 5:
        # Index 1: Jenis Kontainer (Contoh: "20 feet")
        jenis = parts[1]
        
        try:
            # Index 2: Jumlah Kontainer
            jumlah = int(parts[2])
            
            # Output: Key<tab>Value
            # MENGGUNAKAN .format() agar aman di Python versi lama
            print("{0}\t{1}".format(jenis, jumlah))
        except ValueError:
            continue