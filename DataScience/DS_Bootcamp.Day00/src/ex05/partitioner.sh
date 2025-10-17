#!/bin/sh

INPUT_FILE="../ex03/hh_positions.csv"
OUTPUT_DIR="partitions"

mkdir -p $OUTPUT_DIR

header=$(head -n 1 $INPUT_FILE)

tail -n +2 $INPUT_FILE | while IFS=, read -r id created_at name has_test alternate_url
do
    date=$(echo $created_at | cut -d'T' -f1)
    output_file="${OUTPUT_DIR}/${date}.csv"

    if [ ! -f "$output_file" ]; then
        echo "$header" > "$output_file"
    fi

    echo "$id,$created_at,$name,$has_test,$alternate_url" >> "$output_file"
done
