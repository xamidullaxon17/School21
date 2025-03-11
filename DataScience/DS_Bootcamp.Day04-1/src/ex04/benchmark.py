#!/usr/bin/env python3

import timeit as t
import random as r
from collections import Counter

def random_list():
    return [r.randint(0,100) for _ in range(1000000)]

def count_dict(list):
    counts = {}
    for num in list:
        counts[num] = counts.get(num, 0) + 1
    return counts

def count_counter(list):
    return Counter(list)

def top_10_dict(counts):
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

def top_10_counter(counter):
    return counter.most_common(10)

def benchmark():
    list = random_list()
    dict_time = t.timeit(lambda: count_dict(list), number=1)
    counter_time = t.timeit(lambda: count_counter(list), number=1)
    
    dict_counts = count_dict(list)
    dict_top_time = t.timeit(lambda: top_10_dict(dict_counts), number=1)

    counter_counts = count_counter(list)
    counter_top_time = t.timeit(lambda: top_10_counter(counter_counts), number=1)

    print(f"My function: {dict_time:.7f}")
    print(f"Counter: {counter_time:.7f}")
    print(f"My top: {dict_top_time:.7f}")
    print(f"Counter's top: {counter_top_time:.7f}")

if __name__ == "__main__":
    benchmark()





