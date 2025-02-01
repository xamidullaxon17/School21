#!/bin/sh

INPUT_FILE="../ex03/hh_positions.csv"
OUTPUT_FILE="hh_uniq_positions.csv"

{
    echo "\"name\",\"count\""
    tail -n +2 $INPUT_FILE | cut -d',' -f3 | sed 's/"//g' | sort | uniq -c | sort -nr | awk '{print "\"" $2 "\"", $1 }' OFS=','
} > $OUTPUT_FILE
