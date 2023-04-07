import cohere
import requests
import argparse
import subprocess
import os

from dotenv import load_dotenv

OPENAI_API_ENDPOINT = "https://api.openai.com/v1/completions"
COHERE_API_ENDPOINT = "https://api.cohere.ai/v1/generate"
load_dotenv()

def generate_gitignore(directory_path):
    command = f"ls -a {directory_path}"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    prompt = f"Generate a .gitignore file for the following directory:\n{output}"
    API_KEY = os.getenv("COHERE_API_KEYS")
    print(API_KEY)
    co = cohere.Client(API_KEY)
    response = co.generate(
        model='command-xlarge-nightly',  
        prompt = prompt,  
        max_tokens=40,  
        temperature=0.6,  
    )
    response = response.generations[0].text

    print(response)
    #response = requests.post(
    #    COHERE_API_ENDPOINT,
    #    headers={"Authorization": f"Bearer {API_KEY}"},
    #    json={
    #        "prompt": prompt,
    #        "max_tokens": 20,
    #        "return_likelihoods": "NONE",
    #        "truncate": "END",
    #    },
    #)

    #if response.status_code == 200:
    #    gitignore_text = response.json()
    #    with open(directory_path / ".gitignore", 'w') as f:
    #        f.write(gitignore_text)
    #else:
    #    print(response.content)
    #    print("Unable to call OPEN AI API")

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
