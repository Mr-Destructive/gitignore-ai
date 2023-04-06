import requests
import argparse
import subprocess
import os

from dotenv import load_dotenv

OPENAI_API_ENDPOINT = "https://api.openai.com/v1/completions"
load_dotenv()

def generate_gitignore(directory_path):
    command = f"ls -aR {directory_path}"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    prompt = f"Generate a .gitignore file for the following directory:\n{output}"
    API_KEY = os.getenv("OPENAI_API_KEYS")

    response = requests.post(
        OPENAI_API_ENDPOINT,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "prompt": prompt,
            "model": "text-davinci-003",
            "temperature": 0.5,
        },
    )

    if response.status_code == 200:
        gitignore_text = response.json()
        with open(directory_path / ".gitignore", 'w') as f:
            f.write(gitignore_text)
    else:
        print("Unable to call OPEN AI API")

def main():
    parser = argparse.ArgumentParser(description='Generate a .gitignore file based on directory contents.')
    parser.add_argument('dir_path', help='Path to the directory')
    args = parser.parse_args()
    try:
        generate_gitignore(args.dir_path)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")


if __name__ == '__main__':
    main()
