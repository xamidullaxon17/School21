#!/bin/bash

default_bg1=6
default_fg1=1
default_bg2=2
default_fg2=4

config_file="config.conf"
if [ -f "$config_file" ]; then
    source "$config_file"
fi

bg_name="${column1_background:-$default_bg1}"
fg_name="${column1_font_color:-$default_fg1}"
bg_value="${column2_background:-$default_bg2}"
fg_value="${column2_font_color:-$default_fg2}"


for param in "$bg_name" "$fg_name" "$bg_value" "$fg_value"; do
    case "$param" in
        1|2|3|4|5|6) ;;
        *)
	    echo "Error: Parameter should be 1 to 6 (1-white, 2-red, 3-green, 4-blue, 5-purple, 6-black)"
            exit 1
	    ;;
    esac
done

if [ "$bg_name" -eq "$fg_name" ]; then
    echo "Error: The background and front colors should not be the same"
    exit 1
fi

if [ "$bg_value" -eq "$fg_value" ]; then
    echo "Error: The background and front colors should not be the same"
    exit 1
fi

convert_to_bg_color() {
    case $1 in
	1) echo -e "\e[47m";; #white
	2) echo -e "\e[41m";; #red
	3) echo -e "\e[42m";; #green
	4) echo -e "\e[44m";; #blue
	5) echo -e "\e[45m";; #purple
	6) echo -e "\e[40m";; #black
    esac
}

convert_to_fg_color() {
    case $1 in
	1) echo -e "\e[97m";;
	2) echo -e "\e[31m";;
	3) echo -e "\e[42m";;
	4) echo -e "\e[34m";;
	5) echo -e "\e[95m";;
	6) echo -e "\e[30m";;
    esac
}

BG_NAME=$(convert_to_bg_color "$bg_name")
FG_NAME=$(convert_to_fg_color "$fg_name")
BG_VALUE=$(convert_to_bg_color "$bg_value")
FG_VALUE=$(convert_to_fg_color "$fg_value")
RESET="\e[0m"

print_system_info() {
    echo -e "${BG_NAME}${FG_NAME}HOSTNAME${RESET} = ${BG_VALUE}${FG_VALUE}$(hostname)${RESET}"
    echo -e "${BG_NAME}${FG_NAME}TIMEZONE${RESET} = ${BG_VALUE}${FG_VALUE}$(timedatectl | grep "Time zone" | awk '{print $3}') UTC  $(date +%z | sed 's/00$//')${RESET}"
    echo -e "${BG_NAME}${FG_NAME}USER${RESET} = ${BG_VALUE}${FG_VALUE}$(whoami)${RESET}"
    echo -e "${BG_NAME}${FG_NAME}OS${RESET} = ${BG_VALUE}${FG_VALUE}$(cat /etc/os-release | grep "PRETTY_NAME" | cut -d '"' -f2)${RESET}"
    echo -e "${BG_NAME}${FG_NAME}DATE${RESET} = ${BG_VALUE}${FG_VALUE}$(date '+%d %B %Y %H:%M:%s')${RESET}"
    echo -e "${BG_NAME}${FG_NAME}UPTIME${RESET} = ${BG_VALUE}${FG_VALUE}$(uptime -p)${RESET}"
    echo -e "${BG_NAME}${FG_NAME}UPTIME_SEC${RESET} = ${BG_VALUE}${FG_VALUE}$(cat /proc/uptime | cut -d'.' -f1)${RESET}"
    echo -e "${BG_NAME}${FG_NAME}IP${RESET} = ${BG_VALUE}${FG_VALUE}$(ip -4 addr show | grep inet | awk '{print $2}' | cut -d'/' -f1 | head -n1)${RESET}"
    echo -e "${BG_NAME}${FG_NAME}MASK${RESET} = ${BG_VALUE}${FG_VALUE}$(ip -4 addr show | grep inet | awk '{print $2}' | cut -d'/' -f2 | head -n1)${RESET}"
    echo -e "${BG_NAME}${FG_NAME}GATEWAY${RESET} = ${BG_VALUE}${FG_VALUE}$(ip route | grep default | awk '{print $3}' | head -n1)${RESET}"
    echo -e "${BG_NAME}${FG_NAME}RAM_TOTAL${RESET} = ${BG_VALUE}${FG_VALUE}$(free -m | awk '/^Mem:/{printf "%.3f GB", $2/1024}')${RESET}"
    echo -e "${BG_NAME}${FG_NAME}RAM_USED${RESET} = ${BG_VALUE}${FG_VALUE}$(free -m | awk '/^Mem:/{printf "%.3f GB", $3/1024}')${RESET}"
    echo -e "${BG_NAME}${FG_NAME}RAM_FREE${RESET} = ${BG_VALUE}${FG_VALUE}$(free -m | awk '/^Mem:/{printf "%.3f GB", $4/1024}')${RESET}"
    echo -e "${BG_NAME}${FG_NAME}SPACE_ROOT${RESET} = ${BG_VALUE}${FG_VALUE}$(df -m / | awk 'NR==2{printf "%.2f MB", $2}')${RESET}"
    echo -e "${BG_NAME}${FG_NAME}SPACE_ROOT_USED${RESET} = ${BG_VALUE}${FG_VALUE}$(df -m / | awk 'NR==2{printf "%.2f MB", $3}')${RESET}"
    echo -e "${BG_NAME}${FG_NAME}SPACE_ROOT_FREE${RESET} = ${BG_VALUE}${FG_VALUE}$(df -m / | awk 'NR==2{printf "%.2f MB", $4}')${RESET}"
}

get_color_name() {
    case $1 in
        1) echo "white";;
        2) echo "red";;
        3) echo "green";;
        4) echo "blue";;
        5) echo "purple";;
        6) echo "black";;
    esac
}


print_system_info

echo "Column 1 background = ${column1_background:-defaut} ($(get_color_name "$bg_name"))"
echo "Column 1 font color = ${column1_font_color:-defaut} ($(get_color_name "$fg_name"))"
echo "Column 2 background = ${column2_background:-defaut} ($(get_color_name "$bg_value"))"
echo "Column 2 font color = ${column2_font_color:-defaut} ($(get_color_name "$fg_value"))"


exit 0









