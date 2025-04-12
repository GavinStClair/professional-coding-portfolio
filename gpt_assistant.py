# gpt_assistant.py
import openai
import os
from dotenv import load_dotenv
load_dotenv()
import argparse
import pathlib

# Load API key from .env
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt templates
def build_prompt(mode, input_text):
    if mode == "command":
        return f"Generate a Linux shell command for: {input_text}"
    elif mode == "code":
        return f"Help me with this code task: {input_text}"
    elif mode == "init_project":
        return (
            "Create a full GitHub-ready folder structure called 'Professional Coding Portfolio' that includes organized subfolders like 'tools/', 'projects/', 'shared_libs/', and 'ideas/'. "
            "Inside 'tools/', create two projects: 'code-helper/' and 'sysadmin-assistant/', each with their own main.py, README.md, .env.example, and requirements.txt. "
            "Also include a top-level README.md and .gitignore, plus a shared_libs/gpt_utils.py template and an ideas/roadmap.md file. "
            "Output each file prefixed by its path in markdown style (### filename.ext) with its full content below."
        )
    else:
        return input_text

# Ask GPT-3.5
def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Write files from GPT output
def write_project_files(gpt_output):
    files = {}
    current_file = None

    for line in gpt_output.splitlines():
        if line.strip().startswith("###") and "." in line:
            current_file = line.strip("# ").strip()
            files[current_file] = []
        elif current_file:
            files[current_file].append(line)

    for filename, content in files.items():
        path = pathlib.Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write("\n".join(content).strip())
        print(f"✅ Created {filename}")

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Assistant for Commands, Code, and Project Scaffolding")
    parser.add_argument("mode", choices=["command", "code", "init_project"], help="Type of help you need")
    parser.add_argument("query", nargs="*", help="Your prompt for the assistant")
    args = parser.parse_args()

    user_input = " ".join(args.query) if args.query else ""
    full_prompt = build_prompt(args.mode, user_input)
    result = ask_gpt(full_prompt)

    print("\n🤖 GPT Says:\n")
    print(result)

    if args.mode == "init_project":
        write_project_files(result)