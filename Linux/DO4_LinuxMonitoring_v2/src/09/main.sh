#!/bin/bash

# CPU foydalanish foizini olish
function scrape_cpu {
    echo "# HELP cpu_used_in_percent The total CPU used as percent value" >> metrics.html
    echo "# TYPE cpu_used_in_percent gauge" >> metrics.html 
    # CPU foydalanish foizini olish
    echo "cpu_used_in_percent $(ps -eo pcpu | awk '{s+=$1} END {print s}')" >> metrics.html
}

# Diskdagi bo'sh joyni olish
function scrape_free_hd_space {
    echo "# HELP free_hd_space_in_bytes The total number of bytes free in home directory" >> metrics.html
    echo "# TYPE free_hd_space_in_bytes gauge" >> metrics.html
    # /home papkasidagi bo'sh joyni olish
    echo "free_hd_space_in_bytes $(df -B1 /home | awk 'NR==2{print $4}')" >> metrics.html
}

# RAMdagi bo'sh joyni olish
function scrape_free_mem {
    echo "# HELP free_mem_in_bytes The free RAM left in bytes" >> metrics.html
    echo "# TYPE free_mem_in_bytes gauge" >> metrics.html
    # Bo'sh RAM miqdorini olish
    echo "free_mem_in_bytes $(free -b | awk 'NR==2{print $4}')" >> metrics.html
}

# Agar parametrlar bo'lsa, skriptni to'xtatadi
if [ $# != 0 ]; then
    echo "Script takes no arguments"
    exit 1
else
    # Doimiy ravishda 3 sekundda ma'lumotlarni yangilash
    while true; do
        scrape_cpu
        scrape_free_hd_space
        scrape_free_mem
        sleep 3
    done
fi
