import os
import sys
import json
import requests
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

prompt_template = lambda files: f'''\
You will be provided with multiple files.
Please compress each file in a separate section in a way that the content will still be fully readable by an AI such as yourself.
You can use any means you deem fit to represent the information (including other languages if it helps).


''' + '\n'.join([f'<file filename="{os.path.basename(file)}">\n{open(file).read()}\n</file>\n\n' for file in files])

if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} <file> [file...]')
    sys.exit(1)

transcript = open(sys.argv[1]).read()

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    system="",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": prompt_template(sys.argv[1:])}
    ]
)

print(response.content[0].text)
