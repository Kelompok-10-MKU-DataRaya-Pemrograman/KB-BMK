=== PETUNJUK PENGGUNAAN APLIKASI HDFS + MapReduce ===

1. Copy semua file ke dalam direktori/folder kerja masing-masing peserta.
2. Pastikan aplikasi Docker sedang aktif.
3. Di dalam direktori ini, run command berikut untuk mengaktifkan HDFS

``` docker-compose up -d ```

4. Tunggu beberapa detik, kemudian bukalah http://localhost:9870 melalui browser. Jika muncul tampilan NameNode, maka HDFS sudah dalam keadaan aktif

5. Run command berikut dalam Command Prompt (cmd) untuk installasi Python di masing-masing container

``` init.bat ```

6. Untuk memulai proses pengolahan data, run command berikut

``` analyze.bat ```

7. Untuk mematikan aplikasi, gunakan command berikut

``` docker-compose down ```