import os  # Thư viện để truy cập biến môi trường hệ thống
from dotenv import load_dotenv  # Đọc file .env để nạp biến môi trường vào chương trình
from groq import Groq  # Thư viện gọi API của Groq (tương tự OpenAI)

load_dotenv()  # Nạp các biến từ file .env vào os.environ
my_api_key_groq = os.getenv("GROQ_API_KEY")  # Lấy API key từ biến môi trường

if not my_api_key_groq:  # Nếu không tìm thấy key thì báo lỗi ngay
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key_groq)  # Tạo client kết nối tới Groq API

model = "openai/gpt-oss-120b"  # Tên model AI sẽ dùng
role = "user"  # Vai trò của người gửi tin nhắn (user = người dùng)

# --- PYDANTIC: Định nghĩa cấu trúc dữ liệu mong muốn ---
from pydantic import BaseModel  # Thư viện để khai báo schema (cấu trúc) dữ liệu

class Ticket(BaseModel):  # Khai báo class Ticket kế thừa BaseModel
    name : str   # Tên khách hàng - kiểu chuỗi
    email : str  # Email khách hàng - kiểu chuỗi
    issue : str  # Vấn đề khách hàng gặp phải - kiểu chuỗi

# Tự động tạo JSON Schema từ class Ticket ở trên
# Kết quả ví dụ: {'properties': {'name': {'type': 'string'}, ...}, 'required': [...]}
schema = Ticket.model_json_schema()

# Yêu cầu API trả kết quả dạng JSON
# LƯU Ý: Khi dùng "json_object", trong prompt BẮT BUỘC phải chứa từ "JSON",
# nếu không API sẽ báo lỗi
response_format = {
    "type" : "json_object"
}

# --- SYSTEM PROMPT: Hướng dẫn cho AI biết nó phải làm gì ---
# Gắn schema vào để AI biết cần trả về đúng cấu trúc nào
system_prompt = f"""
Trích xuất thông tin cá nhân từ ticket, tuân thủ nghiêm ngặt theo schema này và trả về kết quả dưới dạng json.{schema}
"""
message_system = {"role": "system", "content": system_prompt}  # Tin nhắn hệ thống (AI đọc nhưng user không thấy)

# --- DỮ LIỆU ĐẦU VÀO: Ticket giả lập của khách hàng ---
# Dùng dấu \ để nối nhiều dòng thành 1 chuỗi dài
text="Xin chào! Tôi tên là Huy. " \
"Hiện tại máy điện thoại tôi đang bi hỏng do rơi vào nước. " \
"Số điện thoại tôi là 0123. " \
"Địa chỉ tôi ở Hanoi. " \
"Email tôi là haha@gmail.com"

# --- USER PROMPT: Câu hỏi gửi cho AI ---
# Dùng f-string để chèn biến text vào prompt
prompt = f"""
Đây là ticket của khách hàng. Hãy trích xuất thông tin khách hàng từ đây {text}
"""

message = {"role": role, "content": prompt}  # Tin nhắn của user gửi cho AI

# Ghép system prompt + user prompt thành danh sách tin nhắn
# API yêu cầu messages là 1 list chứa các dict
messages = [message_system, message]

# --- GỌI API: Gửi tin nhắn cho AI và nhận phản hồi ---
# response_format=response_format: bắt AI trả về JSON
response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
answer = response.choices[0].message.content  # Lấy nội dung câu trả lời từ kết quả
print(answer)  # In kết quả JSON ra màn hình



# --- PARSE JSON: Chuyển chuỗi JSON thành object Python ---
import json  # Thư viện xử lý JSON có sẵn trong Python
raw_json = answer  # Chuỗi JSON thô mà AI trả về (vẫn là kiểu str)

# json.loads() chuyển chuỗi JSON (str) thành dict Python
# Ví dụ: '{"name": "Huy"}' -> {"name": "Huy"}
data_file = json.loads(raw_json)

# ** là toán tử "unpack" dict, truyền từng key-value vào Ticket() như tham số
# Tương đương: Ticket(name="Huy", email="haha@gmail.com", issue="...")
# Pydantic sẽ tự kiểm tra dữ liệu có đúng kiểu (str) không, sai thì báo lỗi
ticket = Ticket(**data_file)

print(ticket.email)  # Truy cập trường email như thuộc tính bình thường
print(ticket.issue)  # Truy cập trường issue - lợi ích của Pydantic: gõ ticket. sẽ gợi ý các trường


