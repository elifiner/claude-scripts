import os
import sys
import json
import requests
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))
HUMAN_HUMAN = 'Eli'

prompt_template = lambda data: f'''
You will be provided with a transcript of a conversation between you (Claude) and a human by the name of {HUMAN_HUMAN}.

Your task is to:

1. Summarize each part of the conversation and present them in the order they happened
2. Note special insights or realizations on the part of the human (but ignore insights by Claude)
3. Note tasks that the human noted to be completed at a later date

<transcript>
{data}
</transcript>
'''

if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} <transcript>')
    sys.exit(1)

transcript = open(sys.argv[1]).read()

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    system="",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": prompt_template(transcript)}
    ]
)

print(response.content[0].text)
