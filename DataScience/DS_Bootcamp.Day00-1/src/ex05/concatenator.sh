#!/bin/sh

OUTPUT_FILE="hh_concatenated.csv"

{
    echo "\"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\""

    for file in $(find . -name "*.csv")
    do
        awk 'NR > 1' "$file"
    done
} > $OUTPUT_FILE
