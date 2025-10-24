import json
import requests
from pathlib import Path
from utils.save_chart import save_base64_png

DATA = Path("data/raw"); DATA.mkdir(exist_ok=True)

def fetch_all(access_token: str, cookies: list):
    # Load the list of full URLs
    urls = json.loads(Path("capture_endpoints/captured_endpoints.json").read_text())

    headers = {"Authorization": f"Bearer {access_token}"}
    jar = requests.cookies.RequestsCookieJar()
    for c in cookies:
        jar.set(c["name"], c["value"], domain=c["domain"], path=c["path"])

    for url in urls:
        name = url.split("?")[0].rsplit("/",1)[-1]  
        print(f"→ Fetch {name}: {url}")
        r = requests.get(url, headers=headers, cookies=jar, timeout=10)
        r.raise_for_status()
        # nếu JSON
        try:
            data = r.json()
            with open(DATA/f"{name}.json","w",encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except ValueError:
            # có thể là hình ảnh base64 hoặc raw bytes
            text = r.text.strip()
            content_type = r.headers.get("Content-Type", "")

            if text.startswith("data:image/png;base64"):
                save_base64_png(text, DATA / f"{name}.png")

            elif content_type.startswith("image/"):
                ext = content_type.split("/")[-1]
                with open(DATA / f"{name}.{ext}", "wb") as f:
                    f.write(r.content)

            else:
                # unknown format → write as .txt or .bin
                Path(DATA / f"{name}.txt").write_text(text, encoding="utf-8")
        print(f"Saved {name}")
