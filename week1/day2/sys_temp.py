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
prompt = "Hãy đặt tên cho con con gái tôi."
message_system = {

    "role": "system",
    "content": "Bạn là một người thích Việt Nam, bạn sẽ trả lời bằng tiếng Việt. Bạn chỉ trả lời 1 cái tên."
}

message = {"role": role, "content": prompt}

messages = [message_system, message]

response = client.chat.completions.create(model=model, messages=messages, temperature=1)

answer = response.choices[0].message.content
print(answer)


# Sytem Role: là để xác định vai trò danh tính nó thiết lập cho llm ngay từ đâu
# Temperature: mức độ sáng tạo từ 0 đến 2 , cao sáng tạo cao
