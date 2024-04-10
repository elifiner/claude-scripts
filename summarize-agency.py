import os
import sys
import json
import requests
import anthropic
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

prompt_template = lambda data: f'''
You will be provided with web page of an agency off the Clutch.co website.

Your task is to:

1. Produce a summary report about the agency
2. Include their name, website, focus, core compentencies, typical project size, number of employees, years in business, location
3. List their prior clients, and for each client list the company name, size, industry, the type of project the agency did for them, and the size of that project

<page>
{data}
</page>
'''

if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} <agency.html>')
    sys.exit(1)

html = open(sys.argv[1]).read()
text = BeautifulSoup(html, 'html.parser').get_text()

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    system="",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": prompt_template(text)}
    ]
)

print(response.content[0].text)
