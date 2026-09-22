import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key_groq = os.getenv("GROQ_API_KEY")

if not my_api_key_groq:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key_groq)

model = "openai/gpt-oss-120b"
role = "user"
prompt = "Do you know Liên Quân Mobile?"

message = {"role": role, "content": prompt}

messages = [message]

response = client.chat.completions.create(model=model, messages=messages)
answer = response.choices[0].message.content
print(answer)

