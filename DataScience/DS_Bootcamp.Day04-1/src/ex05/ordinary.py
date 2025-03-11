#!/usr/bin/env python3

import sys
import os
import psutil
import time

def read_file_to_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def main():
    if len(sys.argv) != 2:
        print("Usage: ./ordinary.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    process = psutil.Process(os.getpid()) # Joriy jarayonni olish
    start_time = time.time()

    lines = read_file_to_list(file_path)

    for _ in lines:
        pass

    peak_memory = process.memory_info().peak_wset / (1024 ** 3) # GB ga o‘tkazish
    elapsed_time = time.time() - start_time

    print(f"Peak Memory Usage = {peak_memory:.3f} GB")
    print(f"User Mode Time + System Mode Time = {elapsed_time:.2f}s")

if __name__ == "__main__":
    main()
