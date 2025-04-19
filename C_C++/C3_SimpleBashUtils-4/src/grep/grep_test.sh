#!/bin/bash
clear

# Uchta alohida katalog yaratish
mkdir -p result_1 result_2 result_3

BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
RESET="\033[0m"

TEST_FILES=("../test.txt" "../test1.txt" "../test2.txt")
PATTERN_FILE="../patterns.txt"
PATTERN="of"

compare_files() {
    if diff -i "$1" "$2" > /dev/null; then
        echo -e "$3: ${GREEN}OK${RESET}"
    else
        echo -e "$3: ${RED}FAIL${RESET}"
    fi
}

test_grep() {
    local result_dir=$1
    shift
    local files=("$@")
    local test_name="Test with ${#files[@]} file(s)"

    echo -e "\n${GREEN}${test_name}:${RESET}\n"
    
    for flag in "-e" "-i" "-v" "-c" "-l" "-n" "-h" "-o" "-s"  "-in" "-iv" "-vc" "-lc" "-nc" "-vh" "-so"  ; do
        grep $flag "$PATTERN" "${files[@]}" > "${result_dir}/log_${flag//-/}.txt"
        ./s21_grep $flag "$PATTERN" "${files[@]}" > "${result_dir}/log_s21_${flag//-/}.txt"
        compare_files "${result_dir}/log_${flag//-/}.txt" "${result_dir}/log_s21_${flag//-/}.txt" "Test $flag option"
    done
    for flag in "-f" "-hf"; do
        grep $flag "$PATTERN_FILE" "${files[@]}" > "${result_dir}/log_${flag//-/}.txt"
        ./s21_grep $flag "$PATTERN_FILE" "${files[@]}" > "${result_dir}/log_s21_${flag//-/}.txt"
        compare_files "${result_dir}/log_${flag//-/}.txt" "${result_dir}/log_s21_${flag//-/}.txt" "Test $flag option"
    done


}

# Step 1: Test with 1 file, results saved to result_1
test_grep "result_1" "${TEST_FILES[0]}"

# Step 2: Test with 2 files, results saved to result_2
test_grep "result_2" "${TEST_FILES[0]}" "${TEST_FILES[1]}"

# Step 3: Test with 3 files, results saved to result_3
test_grep "result_3" "${TEST_FILES[@]}"
