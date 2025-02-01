#!/bin/sh

VACANCY_NAME=$1
OUTPUT_FILE="hh.json"
API_URL="https://api.hh.ru/vacancies?text=${VACANCY_NAME// /+}&per_page=20"

RESPONSE=$(curl -s --ssl-no-revoke "$API_URL")

echo "$RESPONSE" | jq '.' > $OUTPUT_FILE




