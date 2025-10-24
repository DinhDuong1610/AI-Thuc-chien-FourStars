"""
Run:  python capture_endpoints/capture.py
Result: capture_endpoints/captured_endpoints.json
"""
import json, os
from pathlib import Path
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("OSOLAR_USERNAME")
PW   = os.getenv("OSOLAR_PASSWORD")

ROUTES = [
    "https://nda.org.vn/",
    "https://nda.org.vn/gioi-thieu/ve-nda",
    "https://nda.org.vn/tin/dai-hoc-hue-lam-viec-voi-mang-luoi-chuyen-gia-du-lieu-toan-cau-vden-nham-thuc-day-hop-tac-va-chuyen-doi-so-trong-giao-duc",
    "https://nda.org.vn/tin/du-lieu-linh-hon-cua-chuyen-doi-so",
    "https://nda.org.vn/tin/du-lieu-la-trung-tam-cua-chuyen-doi-so",
    "https://nda.org.vn/tin/series-goc-nhin-chuyen-gia-dau-la-thach-thuc-lon-trong-viec-ket-hop-chien-luoc-ai-voi-chien-luoc-du-lieu-va-chuyen-doi-so-tai-viet-nam-hien-nay",
    "https://nda.org.vn/tin/nen-tang-blockchain-quoc-gia-tru-cot-moi-trong-chien-luoc-du-lieu-va-chuyen-doi-so-cua-viet-nam",
    "https://nda.org.vn/tin/gieo-mam-chuyen-doi-so-ben-vung",
    "https://nda.org.vn/tin/chuyen-doi-so-linh-vuc-giao-duc-chu-dong-bat-nhip-tao-buoc-dot-pha",
    "https://nda.org.vn/tin/vai-tro-su-menh-cua-hiep-hoi-du-lieu-quoc-gia-trong-cong-cuoc-chuyen-doi-so-quoc-gia-hinh-thanh-va-phat-trien-nen-kinh-te-du-lieu-vi-mot-viet-nam-thinh-vuong",
    "https://nda.org.vn/tin/nen-tang-chuoi-khoi-quoc-gia",
    "https://nda.org.vn/tin/tro-ly-ao-quoc-gia",
    "https://nda.org.vn/tin/he-thong-thu-dien-tu-quoc-gia",
]

def is_xhr(r):  
    return r.request.resource_type == "xhr" or \
           r.request.headers.get("x-requested-with") == "XMLHttpRequest"

def run_capture():
    captured_urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # # Login
        # page.goto("https://app.osolar.io/login")
        # page.fill('input[placeholder="아이디"]', USER)
        # page.fill('input[placeholder="비밀번호"]', PW)
        # page.click('button:has-text("로그인")')
        # page.wait_for_url("https://app.osolar.io/home")

        # Listen for API responses
        def on_response(resp):
            if is_xhr(resp) and "/api/v1/" in resp.request.url:
                captured_urls.append(resp.request.url)

        page.on("response", on_response)

        # Visit all UI routes
        for route in ROUTES:
            print(f"Visiting {route}")
            page.goto(route)
            page.wait_for_timeout(2000)

        browser.close()

    # Save unique API URLs
    unique_urls = sorted(set(captured_urls))
    out_path = Path("capture_endpoints/captured_endpoints.json")
    out_path.write_text(json.dumps(unique_urls, indent=2), encoding="utf-8")
    print(f"Captured {len(unique_urls)} URLs → {out_path}")

if __name__ == "__main__":
    run_capture()
