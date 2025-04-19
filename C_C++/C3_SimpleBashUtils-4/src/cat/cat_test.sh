#!/bin/bash
clear

mkdir -p results

BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
RESET="\033[0m"

TEST_FILE="../test.txt"

echo -e "\n${RED}Test file content:${RESET}\n"
echo -e "${BLUE}$(cat "$TEST_FILE")${RESET}\n"

cat "$TEST_FILE" > results/log_.txt
./s21_cat "$TEST_FILE" > results/log_s21_.txt


cat -b "$TEST_FILE" > results/log_b.txt
./s21_cat -b "$TEST_FILE" > results/log_s21_b.txt

cat -e "$TEST_FILE" > results/log_e.txt
./s21_cat -e "$TEST_FILE" > results/log_s21_e.txt

cat -n "$TEST_FILE" > results/log_n.txt
./s21_cat -n "$TEST_FILE" > results/log_s21_n.txt

cat -s "$TEST_FILE" > results/log_s.txt
./s21_cat -s "$TEST_FILE" > results/log_s21_s.txt

cat -t "$TEST_FILE" > results/log_t.txt
./s21_cat -t "$TEST_FILE" > results/log_s21_t.txt

cat --number-nonblank "$TEST_FILE" > results/log_gnu_b.txt
./s21_cat --number-nonblank "$TEST_FILE" > results/log_s21_gnu_b.txt

cat -E "$TEST_FILE" > results/log_E.txt
./s21_cat -E "$TEST_FILE" > results/log_s21_E.txt

cat --number "$TEST_FILE" > results/log_gnu_n.txt
./s21_cat --number "$TEST_FILE" > results/log_s21_gnu_n.txt

cat --squeeze-blank "$TEST_FILE" > results/log_gnu_s.txt
./s21_cat --squeeze-blank "$TEST_FILE" > results/log_s21_gnu_s.txt

cat -T "$TEST_FILE" > results/log_T.txt
./s21_cat -T "$TEST_FILE" > results/log_s21_T.txt



compare_files() {
    if diff -i "$1" "$2" > /dev/null; then
        echo -e "$3: ${GREEN}OK${RESET}"
    else
        echo -e "$3: ${RED}FAIL${RESET}"
    fi
}


echo -e "\n${GREEN}Simple version tests:${RESET}"
compare_files results/log_.txt results/log_s21_.txt "Test 1  flag"
compare_files results/log_b.txt results/log_s21_b.txt "Test 1 -b flag"
compare_files results/log_e.txt results/log_s21_e.txt "Test 2 -e flag"
compare_files results/log_n.txt results/log_s21_n.txt "Test 3 -n flag"
compare_files results/log_s.txt results/log_s21_s.txt "Test 4 -s flag"
compare_files results/log_t.txt results/log_s21_t.txt "Test 5 -t flag"


echo -e "\n${GREEN}GNU version tests:${RESET}"
compare_files results/log_gnu_b.txt results/log_s21_gnu_b.txt "Test 6 --number-nonblank"
compare_files results/log_E.txt results/log_s21_E.txt "Test 7 -E"
compare_files results/log_gnu_n.txt results/log_s21_gnu_n.txt "Test 8 --number"
compare_files results/log_gnu_s.txt results/log_s21_gnu_s.txt "Test 9 --squeeze-blank"
compare_files results/log_T.txt results/log_s21_T.txt "Test 10 -T"
