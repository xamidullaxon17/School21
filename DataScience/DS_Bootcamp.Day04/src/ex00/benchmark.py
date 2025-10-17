#!/usr/bin/env python3

import timeit as t

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
        'anna@live.com', 'philipp@gmail.com'] * 5

def email_loop(emails):
    list1 = []
    for i in emails:
        if i.endswith("@gmail.com"):
            list1.append(i)
    return list1
    

def email_compr(emails):
    return [emails for i in emails if i.endswith("@gmail.com")]


if __name__ == "__main__":
    loop_time = t.timeit(lambda: email_loop(emails), number=90000000)
    compr_time = t.timeit(lambda: email_compr(emails), number=90000000)

    if loop_time <= compr_time:
        print(f"It's better to use a list comprehension")
    else:
        print("It is better to use a list loop")

    print(f"{min(compr_time, loop_time)} vs {max(compr_time, loop_time)}")
