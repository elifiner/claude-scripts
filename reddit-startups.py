import os
import sys
import json
import requests
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

prompt_template = lambda data: f'''
You will be provided with a JSON file containing recent posts from the r/startups subreddit. Your task is to go through each post and:

1. Summarize the key points/context of the post in 1-2 sentences.
2. Evaluate if this post represents a potential prospect for:
   A) A bootcamp/accelerator program focused on finding product-market fit for EARLY STAGE software startups building B2B or B2B2C products.
   B) Consulting services focused on helping MORE MATURE software startups specifically with improving product-market fit for existing B2B or B2B2C product.
3. For prospects, provide a brief explanation of why they could benefit from a bootcamp or consulting engagement.

The output should be a JSON array, where each element represents one post and contains the following keys:

"url" - The URL of the Reddit post
"summary" - A 1-2 sentence summary of the post
"decision" - Either "EARLY STAGE", "MORE MATURE" or "IGNORE"
"rationale" - If an early stage or mature prospect, explain in 1-2 sentences why they could benefit from a bootcamp or consulting engagement respectively. If not a prospect, leave this blank.

Output JSON only without preamble or explanations.

Example output format:

[
  {{
    "url": "https://reddit.com/r/startups/example1",
    "summary": "Pre-launch B2B software startup seeking validation.",
    "decision": "EARLY STAGE",
    "rationale": "Appears to be at an early stage looking to validate their B2B idea, could benefit from a bootcamp program."
  }},
  {{
    "url": "https://reddit.com/r/startups/example2",
    "summary": "B2B software startup with existing product is struggling with scaling sales and marketing.",
    "decision": "MORE MATURE",
    "rationale": "Seems to have an existing B2B product but is facing traction/optimization challenges, could leverage consulting."
  }},
  {{
    "url": "https://reddit.com/r/startups/example3",
    "summary": "Question about dealing with a difficult co-founder.",
    "decision": "IGNORE",
    "rationale": ""
  }}
]

<json>
{data}
</json>
'''

sys.stderr.write('Loading...\n')
data = requests.get('https://www.reddit.com/r/startups/new.json').text
if ('Too Many Requests' in data):
    sys.stderr.write(f'error: Too many requests\n')
    sys.exit(1)
sys.stderr.write('Parsing...\n')
response = client.messages.create(
    model="claude-3-sonnet-20240229",
    # model="claude-3-haiku-20240307",
    system="",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": prompt_template(data)}
    ]
)
prospects = json.loads(response.content[0].text)
for prospect in prospects:
    if prospect['decision'] != 'IGNORE':
        print(f"{prospect['decision']}: {prospect['url']}")
        print(f"{prospect['rationale']}")
        print()
