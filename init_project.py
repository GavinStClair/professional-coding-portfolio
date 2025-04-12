import os
import subprocess
from pathlib import Path

def create_project_structure(project_name):
    # Define the directory structure
    dirs = [
        f"{project_name}/src/{project_name}",
        f"{project_name}/tests",
        f"{project_name}/docs",
        f"{project_name}/data",
        f"{project_name}/notebooks"
    ]

    # Create directories
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    # Create essential files
    files = {
        f"{project_name}/README.md": f"# {project_name.capitalize()}\n\nProject description.",
        f"{project_name}/requirements.txt": "",
        f"{project_name}/setup.py": f"""from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
)
""",
        f"{project_name}/src/{project_name}/__init__.py": "",
        f"{project_name}/tests/__init__.py": ""
    }

    for file_path, content in files.items():
        with open(file_path, "w") as f:
            f.write(content)

    # Initialize Git repository
    subprocess.run(["git", "init", project_name])
    subprocess.run(["git", "-C", project_name, "add", "."])
    subprocess.run(["git", "-C", project_name, "commit", "-m", "Initial commit"])

    # Set up virtual environment
    subprocess.run(["python3", "-m", "venv", f"{project_name}/venv"])

    print(f"Project '{project_name}' has been initialized successfully.")

if __name__ == "__main__":
    project_name = input("Enter the project name: ").strip()
    create_project_structure(project_name)