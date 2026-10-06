import os  # Thư viện để truy cập biến môi trường hệ thống
from dotenv import load_dotenv  # Đọc file .env để nạp biến môi trường vào chương trình
from groq import Groq  # Thư viện gọi API của Groq (tương tự OpenAI)

load_dotenv()  # Nạp các biến từ file .env vào os.environ
my_api_key_groq = os.getenv("GROQ_API_KEY")  # Lấy API key từ biến môi trường

if not my_api_key_groq:  # Nếu không tìm thấy key thì báo lỗi ngay
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key_groq)  # Tạo client kết nối tới Groq API

model = "openai/gpt-oss-120b" 

def llm_ans(prompt):
    message = {"role": "user", "content": prompt}  # Tin nhắn của user gửi cho AI
    messages = [message]  # API yêu cầu messages là 1 list chứa các dict
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        
    )
    ans = response.choices[0].message.content  # Lấy nội dung trả lời từ API
    return ans
bad_prompt = """
# VAI TRÒ:

Bạn là nhân viên chăm sóc khách hàng của một nhà cung cấp Internet.

# NHIỆM VỤ:

Đọc tin nhắn của khách hàng và xác định khách hàng đang gặp vấn đề gì.

# CÁC LOẠI VẤN ĐỀ:

Chỉ có 3 loại:

* INTERNET: vấn đề liên quan đến mạng, Wi-Fi hoặc kết nối Internet.
* PAYMENT: vấn đề liên quan đến tiền cước, hóa đơn hoặc thanh toán.
* SERVICE: vấn đề liên quan đến đăng ký, hủy hoặc thay đổi gói dịch vụ.

# QUY TẮC:

Bạn phải chọn đúng một trong ba loại:
INTERNET, PAYMENT hoặc SERVICE.

Nếu nội dung khách hàng không thuộc bất kỳ loại nào ở trên thì sử dụng OTHER.

# ĐỊNH DẠNG TRẢ LỜI:

Chỉ trả về đúng một từ.
Không giải thích.
Không thêm dấu câu.

# VÍ DỤ:

Khách hàng: "Wi-Fi nhà tôi không vào được mạng."
Trả lời: INTERNET

Khách hàng: "Tại sao tháng này tôi bị tính tiền nhiều hơn?"
Trả lời: PAYMENT

Khách hàng: "Tôi muốn đăng ký gói Internet mới."
Trả lời: SERVICE

# TRƯỜNG HỢP KHÔNG PHÙ HỢP:

Nếu khách hàng hỏi hoặc nói về vấn đề không liên quan đến Internet, thanh toán hoặc dịch vụ thì trả lời:
OTHER

# TIN NHẮN CỦA KHÁCH HÀNG:

may tính của tôi bị hỏng, tôi không thể truy cập Internet.
"""
print(llm_ans(bad_prompt))


