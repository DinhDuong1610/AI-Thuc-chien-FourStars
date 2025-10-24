from openai import OpenAI
import json
import os


# --- Cấu hình ---
client = OpenAI(
    api_key="sk-ztNiIbZQsJ_vckcX6RE3cQ",
    base_url="https://api.thucchien.ai"
)

file_path = os.path.dirname(os.path.abspath(__file__))

#--- Hàm tiện ích ---
def load_prompt(path):
    full_path = os.path.join(file_path, path)
    with open(full_path, encoding="utf-8") as f:
        return f.read()

def save_output(path, content, mode="w"):
    full_path = os.path.join(file_path, path)
    with open(full_path, mode, encoding="utf-8") as f:
        if isinstance(content, str):
            f.write(content)
        else:
            json.dump(content, f, ensure_ascii=False, indent=2)

def get_text(resp):
    try:
        # ---- OpenAI ----
        if hasattr(resp, "choices") and resp.choices:
            msg = getattr(resp.choices[0], "message", None)
            if msg:
                # Một số gateway set content = None nhưng thêm trường text riêng
                if getattr(msg, "content", None):
                    return msg.content
                if isinstance(msg, dict) and msg.get("content"):
                    return msg["content"]

        # ---- LiteLLM/Gemini (AI Thực Chiến) ----
        data = resp.model_dump()  # ép sang dict
        if "choices" in data:
            choice = data["choices"][0]
            # Một số hệ thống nhét text ở provider_specific_fields
            psf = choice.get("provider_specific_fields", {})
            for v in psf.values():
                if isinstance(v, str) and len(v) > 10:
                    return v
            # Còn nếu text ẩn trong 'response' hoặc 'raw_text'
            if "response" in choice:
                return str(choice["response"])
            if "raw_text" in choice:
                return str(choice["raw_text"])

        # ---- Nếu vẫn rỗng ----
        return ""
    except Exception as e:
        print(f"⚠️ get_text error: {e}")
        return ""
