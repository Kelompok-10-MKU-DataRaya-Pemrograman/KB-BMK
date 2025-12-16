=== CONTOH APLIKASI MAPREDUCE UNTUK PERHITUNGAN JUMLAH ANGKA ===

1. Input berupa list (JSON Array) yang terdapat pada file /input/input.json, dengan konten:

```
[
    1,
    2,
    3,
    4,
    5
]
```

2. Output berupa file txt yang menampilkan hasil kalkulasi, dapat diakses di /output/output.txt. Dalam kasus ini, output adalah 15.0

3. Terdapat dua progam kalkulasi:

   - Mapper

   Fungsi kalkulasi yang terjadi di masing-masing blok. 
   Source code dapat diakses melalui /code/mapper.py. Contoh source code untuk mapper.py:

    ```
        #!/usr/bin/env python3

        import sys
        import json


        data = json.loads(sys.stdin.read())
        print(sum(data))
    ```

    sys.stdin.read() membaca file input.json dalam bentuk string

   - Reducer

   Fungsi kalkulasi ini dilakukan setelah mapper, yang mengumpulkan semua hasil kalkulasi mapper.py menjadi satu hasil final.
   Source code dapat diakses di /code/mapper.py. Berikut adalah contoh program reducer.py:

   ```

    #!/usr/bin/env python3

    import sys

    s = 0
    for data in sys.stdin:
        s += float(data)

    print(s)

   ```

   sys.stdin membaca hasil print yang diberikan oleh fungsi mapper.py dan dijadikannya sebagai input dari reducer.py.
   Hasil print dari reducer.py kemudian akan mengisi konten dari /output/output.txt