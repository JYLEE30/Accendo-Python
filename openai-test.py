''' OpenAI Guide
from openai import OpenAI
# client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
'''

# COde fixed by ChatGPT
import openai

# Assuming you have set up your OpenAI API key
openai.api_key = "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"

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message["content"])