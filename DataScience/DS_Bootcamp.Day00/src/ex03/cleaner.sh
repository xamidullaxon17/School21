#!/bin/sh

INPUT_FILE="../ex02/hh_sorted.csv"
OUTPUT_FILE="hh_positions.csv"

{
    head -n 1 $INPUT_FILE
    tail -n +2 $INPUT_FILE | awk -F',' '
    {
        match($3, /(Junior|Middle|Senior)/, result)
        if (result[1] != "") {
            $3 = "\"" result[1] "\""
        } else {
            $3 = "\"-\""
        }
        print $1 "," $2 "," $3 "," $4 "," $5
    }' OFS=',' 
} > $OUTPUT_FILE
