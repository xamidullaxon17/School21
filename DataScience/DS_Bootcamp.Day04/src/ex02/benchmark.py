#!/usr/bin/env python3

import timeit
import sys

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
          'anna@live.com', 'philipp@gmail.com'] * 5

def loop_emails():
    email_list = []
    for email in emails:
        if email.endswith('@gmail.com'):
            email_list.append(email)
    return email_list

def compr_emails():
    return [email for email in emails if email.endswith('@gmail.com')]

def map_emails():
    return list(map(lambda email: email if email.endswith('@gmail.com') else None, emails))

def filter_emails():
    return list(filter(lambda email: email.endswith('@gmail.com'), emails))

functions = {
    'loop': loop_emails,
    'list_comprehension': compr_emails,
    'map': map_emails,
    'filter': filter_emails
}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./benchmark.py <name_function> <number>")
        sys.exit(1)

    function_name = sys.argv[1]

    if function_name not in functions:
        print("Error: Invalid function name. Choose from: loop, list_comprehension, map, filter")
        sys.exit(1)
    
    try:
        num_calls = int(sys.argv[2])
    except ValueError:
        print("Error: input must be integer")
        sys.exit(1)

    time_taken = timeit.timeit(functions[function_name], number=num_calls)
    print(time_taken)

