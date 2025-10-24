import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_setting import client, get_text


resp = client.chat.completions.create(
    model="gemini-2.5-pro",
    messages=[
        {"role": "user", "content": "Viết 1 câu giới thiệu về Quốc khánh 2/9 bằng tiếng Việt."}
    ],
    max_tokens=100
)

# In ra toàn bộ cấu trúc để xem text nằm đâu
print(json.dumps(resp.model_dump(), ensure_ascii=False, indent=2))