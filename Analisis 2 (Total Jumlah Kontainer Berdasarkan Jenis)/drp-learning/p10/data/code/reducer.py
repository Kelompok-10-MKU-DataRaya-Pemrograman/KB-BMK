#!/usr/bin/env python3

import sys

current_jenis = None
current_count = 0
jenis = None

for line in sys.stdin:
    line = line.strip()
    
    # Parse input dari mapper
    try:
        jenis, count = line.split('\t', 1)
        count = int(count)
    except ValueError:
        continue

    # Logika Grouping (Reduce)
    if current_jenis == jenis:
        current_count += count
    else:
        if current_jenis:
            # Cetak hasil untuk jenis sebelumnya
            print("{0}\t{1}".format(current_jenis, current_count))
        
        current_jenis = jenis
        current_count = count

# Cetak baris terakhir
if current_jenis == jenis:
    print("{0}\t{1}".format(current_jenis, current_count))