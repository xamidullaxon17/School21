#!/bin/bash

# Agar argumentlar soni 3 ta bo'lmasa, xato xabarini chiqarish
if [ "$#" -ne 3 ]; then
    echo "ERROR: The number of arguments should be 3 "
    exit 1
fi

# Disk bo'sh joyini olish (kilobaytlar formatida)
avail_size=$(df -k | grep /dev/sda2 | awk '{print $4}')

# Agar diskda bo'sh joy 1 GB (1048576 KB) dan kam bo'lsa, xatolikni chiqarish
if [ $avail_size -le 1048576 ]; then
    echo "Error: Not enough memory"
    exit 1
fi

# Boshlanish vaqti
START_TIME_NANOSEC=$(date +%s%N)
START_TIME=$(date +%H:%M:%S)

# Xatoliklar flagini sozlash
error_target=0

# Kiruvchi argumentlarni tekshirish

# 1-argument (papka nomi uchun) tekshirish
character_for_name_dir=$1
no_repeat_cheker_dir=$(echo $character_for_name_dir | sed 's/\(.\)\1/\1/g')

if [ ${#character_for_name_dir} -gt 7 ]; then
    echo "ERROR: The number of characters to generate a folder name should not exceed 7"
    error_target=1
elif [[ $character_for_name_dir =~ [^a-zA-Z] ]]; then
    echo "ERROR: Only Latin letters should be used to generate the folder name"
    error_target=1
elif [[ ${#no_repeat_cheker_dir} -ne ${#character_for_name_dir} ]]; then
    echo "ERROR: The letters for generating folder names should not be repeated"
    error_target=1
fi

# 2-argument (fayl nomi uchun) tekshirish
character_for_file=$2
character_for_name_file=${character_for_file%.*}
character_for_expansion_file=${character_for_file#*.}
no_repeat_cheker_file_name=$(echo $character_for_name_file | sed 's/\(.\)\1/\1/g')
no_repeat_cheker_file_expansion=$(echo $character_for_expansion_file | sed 's/\(.\)\1/\1/g')

if [[ ! $character_for_file == *.* ]]; then
    echo "ERROR: There should be a dot between the file name and the extension"
    error_target=1
else
    if [ ${#character_for_name_file} -gt 7 ]; then
        echo "ERROR: The number of characters to generate a file name should not exceed 7"
        error_target=1
    elif [[ $character_for_name_file =~ [^a-zA-Z] ]]; then
        echo "ERROR: Only Latin letters should be used to generate the file name"
        error_target=1
    elif [[ ${#no_repeat_cheker_file_name} -ne ${#character_for_name_file} ]]; then
        echo "ERROR: The letters for generating file names should not be repeated"
        error_target=1
    fi

    if [ ${#character_for_expansion_file} -gt 3 ]; then
        echo "ERROR: The number of characters to generate a file expansion should not exceed 3"
        error_target=1
    elif [[ $character_for_expansion_file =~ [^a-zA-Z] ]]; then
        echo "ERROR: Only Latin letters should be used to generate the file expansion"
        error_target=1
    elif [[ ${#no_repeat_cheker_file_expansion} -ne ${#character_for_expansion_file} ]]; then
        echo "ERROR: The letters for generating file expansion should not be repeated"
        error_target=1
    fi
fi

# 3-argument (fayl hajmi) tekshirish
size_file=$3
size_num_files=${size_file%Mb*}

if [[ $size_num_files =~ [^0-9] || ! $size_file == *Mb ]]; then
    echo "ERROR: The file size should be described by the number and signature Mb after."
    error_target=1
elif [ $size_num_files -gt 100 ]; then
    echo "ERROR: The amount of memory for the file should not exceed 100 Mb"
    error_target=1
fi

# Agar xatoliklar bo'lmasa, davom etish
if [ $error_target -eq 0 ]; then
    # Logger faylini yaratish
    touch "logger.log"
    data="_$(date +"%d%m%y")"
    number_of_subfolders=$((RANDOM % 100))
    
    # Subfolderlar yaratish
    for (( i=1; i<=${number_of_subfolders}; i++ )); do
        avail_size=$(df -k | grep /dev/sda2 | awk '{print $4}')
        if [ $avail_size -le 1048576 ]; then
            echo "Error: Not enough memory"
            break
        fi

        # Tasodifiy yo'lni tanlash
        path=$(find /home -type d 2>/dev/null | grep -E '[^(bin|sbin)]' | head -n $((RANDOM % 650)) | tail -n 1)/
        name_dir=$(./gen.sh $character_for_name_dir $i)
        mkdir "${path}${name_dir}${data}"
        echo -e "${path}${name_dir}${data}/\t\t\t\t\t$(date +"%d.%m.%y")" >> logger.log

        number_of_file=$((RANDOM % 100))
        
        # Fayllar yaratish
        for (( j=1; j<=${number_of_file}; j++ )); do
            avail_size=$(df -k | grep /dev/sda2 | awk '{print $4}')
            if [ $avail_size -le 1048576 ]; then
                echo "Error: Not enough memory"
                break
            fi

            name_file=$(./gen.sh $character_for_name_file $j)
            fallocate -l ${size_file} "${path}${name_dir}${data}/${name_file}${data}.${character_for_expansion_file}"
            echo -e "${path}${name_dir}${data}/${name_file}${data}.${character_for_expansion_file}\t$(date +"%d.%m.%y") ${size_num_files}" >> logger.log
        done
    done

    # Ish tugagandan keyin vaqtni chiqarish
    END_TIME=$(date +%H:%M:%S)
    END_TIME_NANOSEC=$(date +%s%N)
    echo "Start time: $START_TIME"
    echo "End time: $END_TIME"
    echo "Total working time: $((($END_TIME_NANOSEC - $START_TIME_NANOSEC) / 1000000000)) seconds"
    echo "Start time: $START_TIME" >> logger.log
    echo "End time: $END_TIME" >> logger.log
    echo "Total working time: $((($END_TIME_NANOSEC - $START_TIME_NANOSEC) / 1000000000)) seconds" >> logger.log
fi
