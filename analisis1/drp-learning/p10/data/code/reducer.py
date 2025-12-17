#!/usr/bin/env python3

import sys

current_pelabuhan = None
current_total = 0
pelabuhan = None

for line in sys.stdin:
    line = line.strip()
    
    # Parse input dari mapper (Key<tab>Value)
    try:
        pelabuhan, biaya = line.split('\t', 1)
        biaya = int(biaya)
    except ValueError:
        continue

    # Logika Reduce (Grouping)
    if current_pelabuhan == pelabuhan:
        current_total += biaya
    else:
        if current_pelabuhan:
            print("{0}\t{1}".format(current_pelabuhan, current_total))
        
        current_pelabuhan = pelabuhan
        current_total = biaya

# Cetak baris terakhir
if current_pelabuhan == pelabuhan:
    print("{0}\t{1}".format(current_pelabuhan, current_total))