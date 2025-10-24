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
    "https://app.osolar.io/home",
    "https://app.osolar.io/generation",
    "https://app.osolar.io/billing/generation",
    "https://app.osolar.io/billing/rec",
    "https://app.osolar.io/transaction/ledger",
    "https://app.osolar.io/management",
    "https://app.osolar.io/bootstrap",
    "https://app.osolar.io/settings#solarspace",
    "https://app.osolar.io/settings#powerplant",
    "https://app.osolar.io/settings#certificate",
]

def is_xhr(r):  
    return r.request.resource_type == "xhr" or \
           r.request.headers.get("x-requested-with") == "XMLHttpRequest"

def run_capture():
    captured_urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Login
        page.goto("https://app.osolar.io/login")
        page.fill('input[placeholder="아이디"]', USER)
        page.fill('input[placeholder="비밀번호"]', PW)
        page.click('button:has-text("로그인")')
        page.wait_for_url("https://app.osolar.io/home")

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
