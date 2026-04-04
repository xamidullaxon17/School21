import json
import sys

try:
    with open("text.txt", "r") as f:
        data = json.load(f)
except Exception:
    print("Error: invalid input")
    sys.exit()

if "list1" not in data or "list2" not in data:
    print("Error: invalid input")
    sys.exit()

list1 = data["list1"]
list2 = data["list2"]

def check_list(lst):
    if not isinstance(lst, list):
        return False
    for item in lst:
        if not isinstance(item, dict):
            return False
        if "title" not in item or "year" not in item:
            return False
        if not isinstance(item["title"], str):
            return False
        if not isinstance(item["year"], int):
            return False
    return True

if not check_list(list1) or not check_list(list2):
    print("Error: invalid input")
    sys.exit()

merged = list1 + list2
merged.sort(key=lambda x: x["year"])

output = {"list0": merged}
print(json.dumps(output, indent=2))


# no input 
