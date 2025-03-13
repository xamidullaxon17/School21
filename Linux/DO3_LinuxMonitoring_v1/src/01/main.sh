#!/bin/bash

if [ $# -ne 1 ]; then
    echo "$0 <text>"
    exit 1
fi

input="$1"

if [[ "$input" =~ ^[0-9]+$ ]]; then
    echo "Invalid input"
    exit 1
fi

echo "$input"

