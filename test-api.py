import requests, json

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": "AIzaSyASlq8m04eh9QX4tkmX5B6iv26lENkfOK8"
}
payload = {
    "contents": [
        {"parts": [{"text": "Explain how AI works in a few words"}]}
    ]
}

resp = requests.post(url, headers=headers, json=payload)
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
