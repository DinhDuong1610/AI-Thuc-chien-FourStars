import os
import requests
import time
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv(dotenv_path='../../.env')

BASE_URL = "https://api.thucchien.ai"
API_KEY = os.getenv("API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

def save_text(content, filepath):
    """Lưu nội dung văn bản vào file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Đã lưu văn bản vào: {filepath}")

def save_image(image_bytes, filepath):
    """Lưu nội dung ảnh (dạng bytes) vào file."""
    image = Image.open(io.BytesIO(image_bytes))
    image.save(filepath)
    print(f"✅ Đã lưu ảnh vào: {filepath}")

def save_audio(audio_bytes, filepath):
    """Lưu nội dung âm thanh (dạng bytes) vào file."""
    with open(filepath, 'wb') as f:
        f.write(audio_bytes)
    print(f"✅ Đã lưu âm thanh vào: {filepath}")

def save_video(video_bytes, filepath):
    """Lưu nội dung video (dạng bytes) vào file."""
    with open(filepath, 'wb') as f:
        f.write(video_bytes)
    print(f"✅ Đã lưu video vào: {filepath}")

# --- CÁC HÀM GỌI API ---

def generate_text(prompt: str, model: str = "gemini-2.5-pro") -> str:
    """
    Gọi API để sinh văn bản.
    Docs: https://docs.thucchien.ai/docs/api-reference/text-generation
    """
    endpoint = "/text/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    print(f"⏳ Đang sinh văn bản với model {model}...")
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=payload)
        response.raise_for_status()  # Ném lỗi nếu status code là 4xx hoặc 5xx
        result = response.json()
        content = result['choices'][0]['message']['content']
        print("✅ Sinh văn bản thành công!")
        return content
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi gọi API sinh văn bản: {e}")
        return None

def generate_image(prompt: str, size: str = "1024x1024", model: str = "dall-e-3") -> bytes:
    """
    Gọi API để sinh hình ảnh.
    Docs: https://docs.thucchien.ai/docs/api-reference/image-generation
    """
    endpoint = "/images/generations"
    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size
    }
    print(f"⏳ Đang sinh ảnh với model {model}...")
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=payload)
        response.raise_for_status()
        # API này trả về thẳng file ảnh, không phải JSON
        print("✅ Sinh ảnh thành công!")
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi gọi API sinh ảnh: {e}")
        return None

def generate_speech(text: str, model: str = "tfs", voice: str = "female_north", speed: float = 1.0) -> bytes:
    """
    Gọi API để chuyển văn bản thành giọng nói.
    Docs: https://docs.thucchien.ai/docs/api-reference/text-to-speech
    """
    endpoint = "/audio/speech"
    payload = {
        "model": model,
        "input": text,
        "voice": voice,
        "speed": speed
    }
    print("⏳ Đang chuyển văn bản thành giọng nói...")
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=payload)
        response.raise_for_status()
        # API này trả về thẳng file âm thanh, không phải JSON
        print("✅ Chuyển giọng nói thành công!")
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi gọi API TTS: {e}")
        return None

# --- WORKFLOW PHỨC TẠP: SINH VIDEO (3 BƯỚC) ---

def start_video_generation(prompt: str) -> str:
    """
    BƯỚC 1: Bắt đầu yêu cầu sinh video và lấy task_id.
    Docs: https://docs.thucchien.ai/docs/api-reference/video-generation-start
    """
    endpoint = "/videos/generations/start"
    payload = {"prompt": prompt}
    print(f"⏳ Bắt đầu yêu cầu sinh video cho prompt: '{prompt[:50]}...'")
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=payload)
        response.raise_for_status()
        task_id = response.json().get("task_id")
        print(f"✅ Yêu cầu thành công. Task ID: {task_id}")
        return task_id
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi bắt đầu sinh video: {e}")
        return None

def check_video_status(task_id: str) -> dict:
    """
    BƯỚC 2: Kiểm tra trạng thái của tác vụ sinh video.
    Docs: https://docs.thucchien.ai/docs/api-reference/video-generation-status
    """
    endpoint = f"/videos/generations/status/{task_id}"
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi kiểm tra trạng thái video: {e}")
        return None

def download_video(task_id: str) -> bytes:
    """
    BƯỚC 3: Tải video sau khi đã hoàn thành.
    Docs: https://docs.thucchien.ai/docs/api-reference/video-generation-download
    """
    endpoint = f"/videos/generations/download/{task_id}"
    print(f"⏳ Đang tải video cho task ID: {task_id}")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
        response.raise_for_status()
        print("✅ Tải video thành công!")
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi tải video: {e}")
        return None

def generate_video_workflow(prompt: str, poll_interval: int = 10) -> bytes:
    """
    Hàm tổng hợp toàn bộ quy trình sinh video: Start -> Poll Status -> Download.
    """
    task_id = start_video_generation(prompt)
    if not task_id:
        return None

    while True:
        status_info = check_video_status(task_id)
        if not status_info:
            return None # Lỗi đã được in ra trong hàm check_video_status

        status = status_info.get("status")
        print(f"🔄 Trạng thái video: {status}")

        if status == "completed":
            return download_video(task_id)
        elif status == "failed":
            print(f"❌ Tác vụ sinh video đã thất bại. Lý do: {status_info.get('message')}")
            return None
        
        # Chờ trước khi kiểm tra lại
        time.sleep(poll_interval)

def check_api_spend() -> dict:
    """
    Kiểm tra chi phí API đã sử dụng.
    Docs: https://docs.thucchien.ai/docs/api-reference/spend-checking
    """
    endpoint = "/credits/spend"
    print("⏳ Đang kiểm tra chi phí...")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
        response.raise_for_status()
        spend_data = response.json()
        print(f"✅ Kiểm tra chi phí thành công: ${spend_data.get('total_spend', 0):.4f}")
        return spend_data
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi kiểm tra chi phí: {e}")
        return None