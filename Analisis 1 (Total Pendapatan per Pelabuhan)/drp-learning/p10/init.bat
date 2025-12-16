@echo off
setlocal enabledelayedexpansion

set containers=namenode datanode1 datanode2 datanode3 nodemanager resourcemanager

for %%c in (%containers%) do (
    echo === Updating container %%c ===

    docker-compose exec %%c sh -c "rm -f /etc/apt/sources.list"

    docker-compose exec %%c sh -c "printf \"deb http://archive.debian.org/debian stretch main contrib non-free\ndeb http://archive.debian.org/debian-security stretch/updates main\n\" > /etc/apt/sources.list"

    docker-compose exec %%c sh -c "echo 'Acquire::Check-Valid-Until \"false\";' > /etc/apt/apt.conf.d/99no-check-valid"

    docker-compose exec %%c sh -c "apt-get update"

    docker-compose exec %%c sh -c "apt-get install -y python3"
)

echo Done.
pause
