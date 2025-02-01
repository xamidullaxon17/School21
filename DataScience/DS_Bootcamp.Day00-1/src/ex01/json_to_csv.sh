#!/bin/sh

INPUT_FILE="../ex00/hh.json"
OUTPUT_FILE="hh.csv"
FILTER_FILE="filter.jq"

echo "\"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\"" > $OUTPUT_FILE

jq -r '.items[] | select(.name | test("data scientist|scientist"; "i")) | [.id, .created_at, .name, .has_test, .alternate_url] | @csv' $INPUT_FILE | sort -t, -k2,2 -k1,1 >> $OUTPUT_FILE
