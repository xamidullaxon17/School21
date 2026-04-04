import threading
import queue
import random
import time
import os
from math import sqrt

F = (1 + sqrt(5)) / 2 # Golden ratio ≈ 1.618

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def golden_probs(n): # ehtimollik taqsimoti bo'yicha so'z tanlash uchun
    probs = []
    remaining = 1
    for _ in range(n - 1):
        p = remaining / F
        probs.append(p)
        remaining -= p
    probs.append(remaining)
    return probs

def choose_word(words, gender): # agar qiz bo'lsa, ehtimollikni teskari qilib tanlash
    probs = golden_probs(len(words))
    if gender == "F":
        probs.reverse()
    return random.choices(words, weights=probs, k=1)[0]

def examiner_correct(words): # har bir savol uchun to'g'ri javoblarni tanlash
    correct = set()
    while True:
        correct.add(random.choice(words))
        if random.random() > 1/3 or len(correct) == len(words):
            break
    return correct

def examiner_thread(name): # har bir imtihon oluvchi uchun alohida liner yaratish  
    global students, examiners, questions, start_time

    lunch_taken = False

    while True:
        try:
            student = q.get_nowait() # navbatdagi talabani olish, agar bo'sh bo'lsa, xato beradi va sikl tugaydi
        except:
            break

        students[student]["status"] = "In exam" 
        examiners[name]["current"] = student

        duration = random.uniform(len(name)-1, len(name)+1) # a va b orasida tasodifiy float son qaytaradi
        time.sleep(duration)

        correct = 0
        incorrect = 0

        for question in questions:
            words = question.split()
            answer = choose_word(words, students[student]["gender"])
            correct_set = examiner_correct(words)

            if answer in correct_set:
                correct += 1
                students[student]["questions"][question] += 1
            else:
                incorrect += 1

        mood = random.random() 

        if mood < 1/8:
            result = "Failed"
        elif mood < 3/8:
            result = "Passed"
        else:
            result = "Passed" if correct > incorrect else "Failed"

        students[student]["status"] = result
        students[student]["finish"] = time.time()

        examiners[name]["total"] += 1
        if result == "Failed":
            examiners[name]["failed"] += 1

        examiners[name]["work"] += duration
        examiners[name]["current"] = "-"

        if not lunch_taken and time.time() - start_time >= 30:
            lunch_taken = True
            time.sleep(random.uniform(12, 18))


def display():
    clear()

    in_queue = [s for s in students if students[s]["status"] == "In Queue"]
    passed = [s for s in students if students[s]["status"] == "Passed"]
    failed = [s for s in students if students[s]["status"] == "Failed"]

    print("+------------+----------+")
    print("| Student    |  Status  |")
    print("+------------+----------+")

    for s in in_queue + passed + failed:
        print(f"| {s:<10} | {students[s]['status']:<8} |")
    print("+------------+----------+\n")

    print("+-------------+-----------------+-----------------+---------+--------------+")
    print("| Examiner    | Current student | Total students  | Failed  | Work time    |")
    print("+-------------+-----------------+-----------------+---------+--------------+")

    for e in examiners:
        ex = examiners[e]
        print(f"| {e:<11} | {ex['current']:<15} | {ex['total']:^15} | {ex['failed']:^7} | {ex['work']:^12.2f} |")

    print("+-------------+-----------------+-----------------+---------+--------------+\n")

    print(f"Remaining in queue: {len(in_queue)} out of {len(students)}")
    print(f"Time since exam started: {time.time() - start_time:.2f}")

def final():
    clear()

    passed = sorted([s for s in students if students[s]["status"] == "Passed"],
                    key=lambda x: students[x]["finish"])
    failed = sorted([s for s in students if students[s]["status"] == "Failed"],
                    key=lambda x: students[x]["finish"])

    print("+------------+----------+")
    print("| Student    |  Status  |")
    print("+------------+----------+")

    for s in passed + failed:
        print(f"| {s:<10} | {students[s]['status']:<8} |")

    print("+------------+----------+\n")

    print("+-------------+-----------------+---------+--------------+")
    print("| Examiner    | Total students  | Failed  | Work time    |")
    print("+-------------+-----------------+---------+--------------+")

    for e in examiners:
        ex = examiners[e]
        print(f"| {e:<11} | {ex['total']:^15} | {ex['failed']:^7} | {ex['work']:^12.2f} |")

    print("+-------------+-----------------+---------+--------------+\n")

    total_time = max(students[s]["finish"] for s in students) - start_time
    print(f"Time from exam start to finish: {total_time:.2f}")

    #  eng tez tugatgan Passed
    if passed:
        fastest = min(students[s]["finish"] - start_time for s in passed)
        top_students = [s for s in passed
                        if students[s]["finish"] - start_time == fastest]
        print("Top-performing students:", ", ".join(top_students))
    else:
        print("Top-performing students: -")

    # Top examiners eng past fail rate
    rates = [(e, examiners[e]["failed"]/examiners[e]["total"])
             for e in examiners if examiners[e]["total"] > 0]

    if rates:
        best_rate = min(rate for _, rate in rates)
        top_ex = [e for e, rate in rates if rate == best_rate]
        print("Top examiners:", ", ".join(top_ex))
    else:
        print("Top examiners: -")

    # eng tez yiqilgan
    if failed:
        expelled = failed[0]
        print("Students to be expelled:", expelled)
    else:
        print("Students to be expelled: -")

    # Best questions
    q_stats = {}
    for s in students:
        for q in students[s]["questions"]:
            q_stats[q] = q_stats.get(q, 0) + students[s]["questions"][q]

    if q_stats:
        max_q = max(q_stats.values())
        best_q = [q for q in q_stats if q_stats[q] == max_q]
        print("Best questions:", ", ".join(best_q))
    else:
        print("Best questions: -")

    success = len(passed)/len(students) > 0.85
    print("Result:", "Exam successful" if success else "Exam failed")



# Main
students = {}
examiners = {}
questions = []
q = queue.Queue() # talabalar navbati uchun liner

with open("students.txt") as f:
    for line in f:
        if line.strip():
            name, gender = line.strip().split()
            students[name] = {
                "gender": gender,
                "status": "In Queue",
                "finish": None,
                "questions": {}
            }
            q.put(name)

with open("questions.txt") as f:
    questions = [line.strip() for line in f if line.strip()]

for s in students:
    students[s]["questions"] = {q: 0 for q in questions} # har bir talabaga har bir savol uchun javoblarni hisoblash uchun lug'at

with open("examiners.txt") as f:
    for line in f:
        if line.strip():
            name, _ = line.strip().split()
            examiners[name] = {
                "total": 0,
                "failed": 0,
                "work": 0.0,
                "current": "-"
            }

start_time = time.time()

threads = []
for name in examiners:
    t = threading.Thread(target=examiner_thread, args=(name,))
    t.start()
    threads.append(t)

while any(t.is_alive() for t in threads): # barcha linerlar tugaguncha davom etadi. is_alive() - ishlavokkan bo'lsa True bo'ladi
    display()
    time.sleep(1)

for t in threads:
    t.join()

final()
