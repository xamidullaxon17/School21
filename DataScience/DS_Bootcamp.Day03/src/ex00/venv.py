#!/usr/bin/env python3

import os
def venv():
  venv_path = os.getenv("VIRTUAL_ENV")
  if venv_path:
    print(f"Your current virtual env is {venv_path}")
  else:
    print("No virtual enviroment is currently active")

if __name__ == "__main__":
  venv()

