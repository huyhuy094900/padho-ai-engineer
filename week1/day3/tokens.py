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
prompt1 = "Hi!"  
prompt2= "Viết một bai thơ về tình yêu 100 từ"
prompt3 = "Giải thích chi tiết về Machine Learning"

prompts = [prompt1, prompt2, prompt3]
for prompt in prompts:
    message = {"role": role, "content": prompt}
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=50)
    finish_reason = response.choices[0].finish_reason
    usage = response.usage
    print(f"Prompt: {prompt}-->your token:{usage.prompt_tokens}, your completion token: {usage.completion_tokens} your total token: {usage.total_tokens},finish_reason {finish_reason}")




         
# message = {"role": role, "content": prompt}

# messages = [message]

# response = client.chat.completions.create(model=model, messages=messages)
# answer = response.choices[0].message.content
# print(answer)

