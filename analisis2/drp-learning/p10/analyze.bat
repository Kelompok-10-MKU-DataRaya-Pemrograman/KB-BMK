@REM #!/bin/
@echo off

echo === MEMULAI ANALISIS 2 (Total Jumlah Kontainer per Jenis) ===

echo [0/6] Membersihkan container...
docker-compose exec namenode rm -rf /data

@REM 1. Buat ulang folder data
echo [1/6] Membuat direktori baru di container...
docker-compose exec namenode mkdir -p /data

@REM 2. Copy file JAR Hadoop Streaming
echo [2/6] Menyalin Hadoop Streaming JAR...
docker cp ./data/tools/hadoop-streaming-2.7.3.jar namenode:/data/hadoop-streaming.jar

@REM 3. Copy script Python KHUSUS ANALISIS 2 dan Big Data
echo [3/6] Menyalin script Python Analisis 2...
@REM Pastikan Anda sudah membuat mapper_jenis.py dan reducer_jenis.py di folder data/code
docker cp ./data/code/mapper_jenis.py namenode:/data/mapper_jenis.py
docker cp ./data/code/reducer_jenis.py namenode:/data/reducer_jenis.py
docker cp ./data/input/big_data_biaya_pelabuhan.csv namenode:/data/input.csv

@REM 4. Siapkan HDFS (Hapus output_analisis2 lama jika ada)
echo [4/6] Membersihkan HDFS...
docker-compose exec namenode hdfs dfs -mkdir -p /user/student/input
@REM Hapus output khusus analisis 2 agar bersih
docker-compose exec namenode hdfs dfs -rm -r /user/student/output_analisis2

@REM 5. Upload data ke HDFS
echo [5/6] Upload input ke HDFS...
docker-compose exec namenode hdfs dfs -put -f /data/input.csv /user/student/input/input.csv

@REM 6. Jalankan Hadoop Streaming
echo [6/6] Menjalankan MapReduce Job Analisis 2...
docker-compose exec namenode hadoop jar /data/hadoop-streaming.jar ^
 -files /data/mapper_jenis.py,/data/reducer_jenis.py ^
 -mapper "python3 mapper_jenis.py" ^
 -reducer "python3 reducer_jenis.py" ^
 -input /user/student/input/input.csv ^
 -output /user/student/output_analisis2

@REM 7. Lihat Hasil
echo.
echo === HASIL ANALISIS 2 (Total Jumlah Kontainer per Jenis) ===
docker-compose exec namenode hdfs dfs -cat /user/student/output_analisis2/part-00000

echo.
echo Selesai.
pause
