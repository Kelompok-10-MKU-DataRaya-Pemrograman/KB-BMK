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

@REM 3. Copy mapper, reducer, dan input BIG DATA
echo [3/6] Menyalin script Python dan Big Data...
docker cp ./data/code/mapper.py namenode:/data/mapper.py
docker cp ./data/code/reducer.py namenode:/data/reducer.py
docker cp ./data/input/big_data_biaya_pelabuhan.csv namenode:/data/input.csv

@REM 4. Siapkan HDFS (Hapus output lama jika ada)
echo [4/6] Membersihkan HDFS...
docker-compose exec namenode hdfs dfs -mkdir -p /user/student/input
docker-compose exec namenode hdfs dfs -rm -r /user/student/output_analisis1

@REM 5. Upload data ke HDFS
echo [5/6] Upload input ke HDFS...
docker-compose exec namenode hdfs dfs -put -f /data/input.csv /user/student/input/input.csv

@REM 6. Jalankan Hadoop Streaming
echo [6/6] Menjalankan MapReduce Job...
docker-compose exec namenode hadoop jar /data/hadoop-streaming.jar ^
 -files /data/mapper.py,/data/reducer.py ^
 -mapper "python3 mapper.py" ^
 -reducer "python3 reducer.py" ^
 -input /user/student/input/input.csv ^
 -output /user/student/output_analisis1

@REM 7. Lihat Hasil
echo.
echo === HASIL ANALISIS 2 (Total Jumlah Kontainer per Jenis) ===
docker-compose exec namenode hdfs dfs -cat /user/student/output_analisis1/part-00000

echo.
echo Selesai.
pause
