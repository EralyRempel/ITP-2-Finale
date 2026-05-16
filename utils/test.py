from groq import Groq

client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[{"role": "user", "content": "привет"}]
)

print(response.choices[0].message.content)