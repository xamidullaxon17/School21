import os
import sys
import subprocess

def check_virtual_env():
    if sys.prefix == sys.base_prefix:
        raise EnvironmentError("Not inside a virtual environment!")

def install_libraries():
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def save_installed_libraries():
    installed_packages = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
    with open("requirements.txt", "w") as f:
        f.write(installed_packages.stdout)
    print(installed_packages.stdout)

if __name__ == "__main__":
    try:
        check_virtual_env()
        install_libraries()
        save_installed_libraries()
    except EnvironmentError as e:
        print(e)
        sys.exit(1)
