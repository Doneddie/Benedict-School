
import os
import sys
import platform
import subprocess

def create_venv():
    # Define the name of the virtual environment folder
    venv_folder = 'venv'

    # Check if 'venv' module is available
    if sys.version_info < (3, 3):
        print("You need Python 3.3 or later to use the 'venv' module.")
        sys.exit(1)

    # Create the virtual environment
    if not os.path.exists(venv_folder):
        print(f"Creating virtual environment in '{venv_folder}'...")
        subprocess.run([sys.executable, '-m', 'venv', venv_folder])
    else:
        print(f"Virtual environment '{venv_folder}' already exists.")

def activate_venv():
    # Detect the current OS
    current_os = platform.system()

    activate_script = ""

    if current_os == "Windows":
        activate_script = os.path.join('venv', 'Scripts', 'activate.bat')
    elif current_os == "Linux" or current_os == "Darwin":  # Darwin refers to macOS
        activate_script = os.path.join('venv', 'bin', 'activate')
    else:
        print(f"Unsupported OS: {current_os}")
        sys.exit(1)

    # Activate the virtual environment
    if current_os == "Windows":
        print(f"To activate the virtual environment, run:\n{activate_script}")
    else:
        print(f"To activate the virtual environment, run:\nsource {activate_script}")

def main():
    create_venv()
    activate_venv()

if __name__ == "__main__":
    main()
