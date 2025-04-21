#!/bin/bash

generate_name() {
    local chars=$1
    local result=""
    local length=4
    local timestamp=$(date +%s%N | cut -b11-15)

    for ((i=0; i<length; i++)); do
        index=$((i % ${#chars}))
        result+=${chars:$index:1}
    done

    echo "${result}${timestamp}"
}
