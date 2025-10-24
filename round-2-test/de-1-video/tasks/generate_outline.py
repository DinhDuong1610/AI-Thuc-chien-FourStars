import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_setting import client, load_prompt, save_output, get_text

def generate_outline():
    prompt = load_prompt("prompt/prompt-1.txt")
    
    # Check prompt
    if not prompt or len(prompt) < 20:
        print("⚠️ Prompt outline quá ngắn hoặc không tồn tại.")
        return "[EMPTY_PROMPT_WARNING] Hãy kiểm tra prompt/prompt-1.txt."

    response = client.chat.completions.create(
        model="gemini-2.5-pro",
        # model="google-genai/gemini-2.5-pro",
        messages=[
            {"role": "system", "content": "Bạn là Biên tập viên truyền hình Việt Nam."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500,
        tool_choice="none"
    )

    os.makedirs("output", exist_ok=True) 
    save_output("output/outline.raw.json", response.model_dump())

    text = get_text(response)
    if not text:
        print("Không có message.content, hãy mở file output/outline.raw.json để xem chi tiết.")
        text = "[EMPTY_CONTENT_WARNING] Hãy kiểm tra outline.raw.json."

    save_output("output/outline.json", text)
    print("[📰] Outline generated successfully!")
    return text

if __name__ == "__main__":
    generate_outline()
