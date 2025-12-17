@REM #!/bin/
@echo off

echo === MEMULAI ANALISIS 1 (Total Pendapatan per Pelabuhan) ===

@REM 1. Pastikan folder data ada di namenode
docker-compose exec namenode mkdir -p /data

@REM 2. Copy file JAR Hadoop Streaming
echo [1/5] Menyalin Hadoop Streaming JAR...
docker cp ./data/tools/hadoop-streaming-2.7.3.jar namenode:/data/hadoop-streaming.jar

@REM 3. Copy mapper, reducer, dan input BIG DATA
echo [2/5] Menyalin script Python dan Big Data...
docker cp ./data/code/mapper.py namenode:/data/mapper.py
docker cp ./data/code/reducer.py namenode:/data/reducer.py
@REM Perhatikan nama file sumber di bawah ini disesuaikan dengan yang kita generate
docker cp ./data/input/big_data_biaya_pelabuhan.csv namenode:/data/input.csv

@REM 4. Siapkan HDFS (Hapus output lama jika ada)
echo [3/5] Membersihkan HDFS...
docker-compose exec namenode hdfs dfs -mkdir -p /user/student/input
docker-compose exec namenode hdfs dfs -rm -r /user/student/output_analisis1

@REM 5. Upload data ke HDFS (Ini akan dipecah ke DataNodes karena > 2MB)
echo [4/5] Upload input ke HDFS...
docker-compose exec namenode hdfs dfs -put -f /data/input.csv /user/student/input/input.csv

@REM 6. Jalankan Hadoop Streaming
echo [5/5] Menjalankan MapReduce Job...
docker-compose exec namenode hadoop jar /data/hadoop-streaming.jar ^
 -files /data/mapper.py,/data/reducer.py ^
 -mapper "python3 mapper.py" ^
 -reducer "python3 reducer.py" ^
 -input /user/student/input/input.csv ^
 -output /user/student/output_analisis1

@REM 7. Lihat Hasil
echo.
echo === HASIL ANALISIS 1 (Total Pendapatan per Pelabuhan) ===
docker-compose exec namenode hdfs dfs -cat /user/student/output_analisis1/part-00000

echo.
echo Selesai.
pause