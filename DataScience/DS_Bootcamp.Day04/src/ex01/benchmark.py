#!/usr/bin/env python3

import timeit as t

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
          'anna@live.com', 'philipp@gmail.com'] * 5

def loop_emails(emails):
    email_list = []
    for i in emails:
        if i.endswith("@gmail.com"):
            email_list.append(i)
    return email_list

def compr_emails(emails):
    return [i for i in emails if i.endswith("@gmail.com")]

def map_emails(emails):
    return [email for email in map(lambda email: email if email.endswith('@gmail.com') else None, emails) if email is not None]

if __name__ == "__main__":
    loop_time = t.timeit(lambda: loop_emails(emails), number=90000000)
    compr_time = t.timeit(lambda: compr_emails(emails), number=90000000)
    map_time = t.timeit(lambda: map_emails(emails), number=90000000)

    times = {
        "loop": loop_time,
        "comprehension": compr_time,
        "map": map_time
    }

    sorted_times = sorted(times.items(), key=lambda item: item[1])
    print(f"It is best to use a {sorted_times[0][0]}")
    print(f"{sorted_times[0][1]} vs {sorted_times[1][1]} vs {sorted_times[2][1]}")