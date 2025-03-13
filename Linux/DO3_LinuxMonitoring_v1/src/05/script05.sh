#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: Usage: $0 /path/to/directory/"
    exit 1
fi

if [[ "$1" != */ ]]; then
    echo "Error: Directory path must be end with '/'"
   exit 1
fi

if [ ! -d "$1" ]; then
    echo "Error: Directory $1 doesn't exist"
    exit 1
fi

start_time=$(date +%s)

dir_path="$1"

total_folders=$(find "$dir_path" -type d 2>/dev/null | wc -l)

top_folders=$(find "$dir_path" -type d -exec du -h --apparent-size {} + 2>/dev/null | sort -hr | head -n 5 | awk '{print NR " - " $2 ", " $1}')

total_files=$(find "$dir_path" -type f 2>/dev/null | wc -l)

conf_files=$(find "$dir_path" -type f -name "*.conf" 2>/dev/null | wc -l)

text_files=$(find "$dir_path" -type f -exec file {} \; 2>/dev/null | grep "text" | wc -l)

exec_files=$(find "$dir_path" -type f -executable 2>/dev/null | wc -l)

log_files=$(find "$dir_path" -type f -name "*.log" 2>/dev/null | wc -l)

archive_files=$(find "$dir_path" -type f \( -name "*.zip" -o -name "*.tar" -o -name "*.gz" -o -name "*.bz2" \) 2>/dev/null | wc -l)

symlinks=$(find "$dir_path" -type l 2>/dev/null | wc -l)

top_files=$(find "$dir_path" -type f -exec du -h --apparent-size {} + 2>/dev/null | sort -hr | head -n 10 | awk '{print NR " - " $2 ", " $1}')

top_exec_files=$(find "$dir_path" -type f -executable -exec du -h --apparent-size {} + 2>/dev/null | sort -hr | head -n 10 | while read -r size path; do
    if [ -f "$path" ]; then
	hash=$(md5sum "$path" 2>/dev/null | awk '{print $1}')
        echo "$size $path $hash"
    fi
done | awk '{print NR " - " $2 ", " $1 ", " $3}')

if [ -z "$top_exec_files" ]; then
    top_exec_files="No executable files found"
fi
end_time=$(date +%s)

execution_time=$(echo "$end_time - $start_time" | bc -l)

echo "Total number of folders (including all nesteds ones) = $total_folders"
echo "Top 5 folders of maximum size arranged in descending order (path and size):"
echo "$top_folders"
echo "Total number of files = $total_files"
echo "Number of:"
echo "Configuration files (with the .conf extention) = $conf_files"
echo "Text files = $text_files"
echo "Executable files = $exec_files"
echo "Log files (with the extension .log) = $log_files"
echo "Archive files = $archive_files"
echo "Symbolic links = $symlinks"
echo "Top 10 files of maximum size arranged in descending order (path, size and type):"
echo "$top_files"
echo "Top 10 executable files of the maximum size arranged in descending order (path, size and MDS hash of file):"
echo "$top_exec_files"
echo "Script execution time (in seconds) = $execution_time"

exit 0

