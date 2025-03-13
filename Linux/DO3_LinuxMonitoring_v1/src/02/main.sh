#!/bin/bash
HOSTNAME=$(hostname)
TIMEZONE=$(timedatectl | grep "Time zone" | awk '{print $3, $4, $5}')
USER=$(whoami)
OS=$(lsb_release -d | awk -F'\t' '{print $2}')
DATE=$(date "+%d %B %Y %H:%M:%S")
UPTIME=$(uptime -p)
UPTIME_SEC=$(cat /proc/uptime | awk '{print int($1)}')
IP=$(hostname -I | awk '{print $1}')
MASK=$(ifconfig | grep -w "inet" | grep -v "127.0.0.1" | awk '{print $4}' | head -n 1)
GATEWAY=$(ip route | awk '/default/ {print $3}')
RAM_TOTAL=$(free -m | awk '/Mem/ {printf "%.3f", $2/1024}')
RAM_USED=$(free -m | awk '/Mem/ {printf "%.3f", $3/1024}')
RAM_FREE=$(free -m | awk '/Mem/ {printf "%.3f", $4/1024}')
SPACE_ROOT=$(df -m / | awk 'NR==2 {printf "%.2f", $2}')
SPACE_ROOT_USED=$(df -m / | awk 'NR==2 {printf "%.2f", $3}')
SPACE_ROOT_FREE=$(df -m / | awk 'NR==2 {printf "%.2f", $4}')

echo "HOSTNAME = $HOSTNAME"
echo "TIMEZONE = $TIMEZONE"
echo "USER = $USER"
echo "OS = $OS"
echo "DATE = $DATE"
echo "UPTIME = $UPTIME"
echo "UPTIME_SEC = $UPTIME_SEC"
echo "IP = $IP"
echo "MASK = $MASK"
echo "GATEWAY = $GATEWAY"
echo "RAM_TOTAL = $RAM_TOTAL GB"
echo "RAM_USED = $RAM_USED GB"
echo "RAM_FREE = $RAM_FREE GB"
echo "SPACE_ROOT = $SPACE_ROOT MB"
echo "SPACE_ROOT_USED = $SPACE_ROOT_USED MB"
echo "SPACE_ROOT_FREE = $SPACE_ROOT_FREE MB"
echo -n "Do you want to save the date? (Y/N): "
read answer

if [[ "$answer" == "Y" || "$answer" == "y" ]]; then
    FILE_NAME=$(date "+%d_%m_%Y_%H+%M_%S").status
    {
	echo "HOSTNAME = $HOSTNAME"
	echo "TIMEZONE = $TIMEZONE"
	echo "USER = $USER"
	echo "OS = $OS"
	echo "DATE = $DATE"
	echo "UPTIME = $UPTIME"
	echo "UPTIME_SEC = $UPTIME_SEC"
	echo "IP = $IP"
	echo "MASK = $MASK"
	echo "GATEWAY = $GATEWAY"
	echo "RAM_TOTAL = $RAM_TOTAL GB"
	echo "RAM_USED = $RAM_USED GB"
	echo "RAM_FREE = $RAM_FREE GB"
	echo "SPACE_ROOT = $SPACE_ROOT MB"
	echo "SPACE_ROOT_USED = $SPACE_ROOT_USED MB"
	echo "SPACE_ROOT_FREE = $SPACE_ROOT_FREE MB"
    } > "$FILE_NAME"
    echo "Data saved to $FILE_NAME"
fi
