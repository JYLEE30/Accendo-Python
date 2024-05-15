import anthropic

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=4000,
    temperature=0.2,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "how are you\n"
                }
            ]
        }
    ]
)
print(message.content)