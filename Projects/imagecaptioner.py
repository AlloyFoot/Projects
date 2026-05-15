import base64, requests
from pathlib import Path
from config import HF_API_KEY

API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
MODELS = ["zai-org/GLM-4.5V", "Qwen/Qwen2.5-VL-72B-Instruct", "Qwen/Qwen2.5-VL-32B-Instruct", "google/gemma-3-27b-it",]

def data_url(filename: str, b: bytes) -> str:
    ext = Path(filename).suffix.lower().lstrip(".")
    
    if ext in ("jpg", "jpeg"):
        mime = "image/jpeg"
    elif ext == "png":
        mime = "image/png"
    elif ext == "webp":
        mime = "image/webp"
    else:
        mime = "application/octet-stream"

    enc = base64.b64encode(b).decode("utf-8")

    return f"data:{mime};base64,{enc}"

def extract_err(r: requests.Response) -> str:
    try:
        j = r.json()
        if isinstance(j, dict):
            return (
                j.get("error")
                or j.get("message")
                or j.get("detail")
                or j.get("error_message")
                or "Request failed."
            )
    except Exception:
        pass
    return r.text.strip() or "Request failed."

def box(title: str, lines: list[str], icon: str):
    items = [f"{icon} {title}"] + lines
    width = max(len(line) for line in items) + 4
    border = "+" + "-" * (width - 2) + "+"
    print(border)
    for i, line in enumerate(items):
        print(f"| {line.ljust(width - 4)} |")
        if i == 0 and len(items) > 1:
            print("|" + "-" * (width - 2) + "|")
    print(border)

def caption_single_image():
    filename = input("Enter image filename [test.jpg]: ").strip() or "test.jpg"

    try:
        with open(filename, "rb") as f:
            img_bytes = f.read()
    except Exception as e:
        box("Failed", [f"File: {filename}", f"Reason: {e}"], "✗")
        return

    image_input = data_url(filename, img_bytes)

    base = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Give a short caption for this image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_input
                        }
                    }
                ],
            }
        ],
        "max_tokens": 64,
        "temperature": 0.2,
    }

    last = "No caption found."

    for model in MODELS:
        payload = dict(base)
        payload["model"] = model

        try:
            r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        except requests.RequestException as e:
            last = str(e)
            continue

        if r.status_code != 200:
            last = extract_err(r)
            continue

        try:
            j = r.json()
            caption = j["choices"][0]["message"]["content"].strip()
        except Exception:
            last = "No caption found."
            continue

        if caption:
            box("Success", [f"File: {filename}", f"Caption: {caption}"], "✓")
            return

        last = "No caption found."

    box("Failed", [f"File: {filename}", f"Reason: {last}"], "✗")

def main():
    caption_single_image()

if __name__ == "__main__":
    main()
