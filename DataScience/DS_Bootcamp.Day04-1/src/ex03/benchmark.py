#!/usr/bin/env python3

import timeit as t
import sys
from functools import reduce

def loop_function(n):
    sum = 0
    for i in range(1,n+1):
        sum += i * i
    return sum

def reduce_function(n):
    return reduce(lambda x, y: x + y * y, range(1, n+1),0)

def benchmark(func, num, n):
    if func == "loop":
        time_taken = t.timeit(lambda: loop_function(n), number=num)
    else:
        time_taken = t.timeit(lambda: reduce_function(n), number=num)
    print(time_taken)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./benchmark.py <name_function> <number_of_calls> <number>")
        sys.exit(1)

    func = sys.argv[1]

    if func not in ["loop", "reduce"]:
        print("Error: Invalid function name. Choose from: loop, reduce")
        sys.exit(1)

    try:
        num = int(sys.argv[2])
        n = int(sys.argv[3])
    except ValueError:
        print("Error: input must be integer")
        sys.exit(1)    
        
    benchmark(func, num, n)


