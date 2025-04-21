#!/bin/bash

validate() {
    if [ "$#" -ne 6 ]; then
        echo "ERROR: Exactly 6 parameters are required."
        return 1
    fi

    local path=$1
    local num_dirs=$2
    local dir_chars=$3
    local num_files=$4
    local file_chars=$5
    local file_size=$6

    if [[ "${path: -1}" != "/" ]]; then
        echo "ERROR: Path must end with '/'"
        return 1
    fi

    if [ ! -d "$path" ]; then
        echo " Directory $path does not exist. Creating it..."
        mkdir -p "$path"
    fi

    if ! [[ "$num_dirs" =~ ^[0-9]+$ ]]; then
        echo " ERROR: Parameter 2 must be a number."
        return 1
    fi

    if [[ ! "$dir_chars" =~ ^[a-zA-Z]{1,7}$ ]]; then
        echo "ERROR: Parameter 3 must be 1-7 unique Latin letters."
        return 1
    fi

    if [[ $(echo "$dir_chars" | grep -o . | sort | uniq | wc -l) -ne ${#dir_chars} ]]; then
        echo "ERROR: Letters in parameter 3 must be unique."
        return 1
    fi

    if ! [[ "$num_files" =~ ^[0-9]+$ ]]; then
        echo "ERROR: Parameter 4 must be a number."
        return 1
    fi

    if [[ ! "$file_chars" =~ ^[a-zA-Z]{1,7}\.[a-zA-Z]{1,3}$ ]]; then
        echo "ERROR: Parameter 5 must be in format name.ext with valid Latin letters."
        return 1
    fi

    file_name_part="${file_chars%.*}"
    file_ext="${file_chars#*.}"

    if [[ $(echo "$file_name_part" | grep -o . | sort | uniq | wc -l) -ne ${#file_name_part} ]]; then
        echo "ERROR: File name letters must be unique."
        return 1
    fi

    if [[ $(echo "$file_ext" | grep -o . | sort | uniq | wc -l) -ne ${#file_ext} ]]; then
        echo "ERROR: File extension letters must be unique."
        return 1
    fi

    if [[ ! "$file_size" =~ ^[0-9]+kb$ ]]; then
        echo "ERROR: Parameter 6 must be in the format [number]kb."
        return 1
    fi

    local size="${file_size%kb}"
    if (( size > 100 )); then
        echo "ERROR: File size must be 100kb or less."
        return 1
    fi

    return 0
}
