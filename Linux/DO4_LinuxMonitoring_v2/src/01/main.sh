#!/bin/bash

source validate.sh
source gen.sh

if ! validate "$@"; then
    exit 1
fi

path=$1
num_dirs=$2
dir_chars=$3
num_files=$4
file_chars=$5
file_name_part="${file_chars%.*}"
file_ext="${file_chars#*.}"
file_size=$6
size_value="${file_size%kb}"

log_file="logger.log"
touch "$log_file"
date_str="_$(date +%d%m%y)"

for ((i=1; i<=num_dirs; i++)); do
    avail_size=$(df -k / | grep /dev/ | awk '{print $4}')
    if [ "$avail_size" -le 1048576 ]; then
        echo "Not enough disk space (less than 1GB)"
        break
    fi

    dir_name=$(generate_name "$dir_chars")
    mkdir "${path}${dir_name}${date_str}"
    echo -e "${path}${dir_name}${date_str}/\t\t$(date +%d.%m.%y)" >> "$log_file"

    for ((j=1; j<=num_files; j++)); do
        avail_size=$(df -k / | grep /dev/ | awk '{print $4}')
        if [ "$avail_size" -le 1048576 ]; then
            echo "Not enough disk space (less than 1GB)"
            break
        fi

        file_name=$(generate_name "$file_name_part")
        full_path="${path}${dir_name}${date_str}/${file_name}${date_str}.${file_ext}"
        fallocate -l "$file_size" "$full_path"
        echo -e "$full_path\t$(date +%d.%m.%y) ${size_value}kb" >> "$log_file"
    done
done
