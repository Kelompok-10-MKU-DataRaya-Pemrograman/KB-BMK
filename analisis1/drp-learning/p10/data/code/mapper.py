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
        
    # Skip header
    if first_line:
        # Cek apakah baris ini header (mengandung kata 'Pelabuhan')
        if "Pelabuhan" in line:
            first_line = False
            continue
        # Jika baris pertama bukan header tapi data, matikan flag first_line
        first_line = False

    # Split data menggunakan delimiter titik koma (;)
    parts = line.split(";")
    
    # Validasi struktur data (harus ada 5 kolom)
    if len(parts) == 5:
        pelabuhan = parts[0]
        try:
            # Ambil Total Biaya (index 4)
            total_biaya = int(parts[4])
            
            print("{0}\t{1}".format(pelabuhan, total_biaya))
        except ValueError:
            continue