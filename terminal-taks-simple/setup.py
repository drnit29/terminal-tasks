import subprocess
import sys
import venv
import os

def create_venv():
    venv_dir = ".venv"
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in {venv_dir}...")
        venv.create(venv_dir, with_pip=True)
        print("Virtual environment created.")
    else:
        print(f"Virtual environment already exists in {venv_dir}.")

def install_dependencies():
    venv_dir = ".venv"
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found.")
        sys.exit(1)

    print(f"Installing dependencies from {requirements_file}...")
    # Determine the correct pip executable path within the venv
    if sys.platform == "win32":
        pip_executable = os.path.join(venv_dir, "Scripts", "pip")
    else:
        pip_executable = os.path.join(venv_dir, "bin", "pip")

    try:
        subprocess.check_call([pip_executable, "install", "-r", requirements_file])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_venv()
    install_dependencies()
