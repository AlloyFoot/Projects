import base64, requests
from pathlib import Path
from config import HF_API_KEY

API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
MODEL = "Qwen/Qwen2.5-VL-72B-Instruct"

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

def generate_text(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 128,
        "temperature": 0.3,
    }

    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    j = r.json()

    return j["choices"][0]["message"]["content"].strip()

def generate_caption(image_input: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Generate a basic caption for this image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_input
                        }
                    }
                ]
            }
        ],
        "max_tokens": 64,
        "temperature": 0.2,
    }

    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    j = r.json()

    return j["choices"][0]["message"]["content"].strip()

filename = input("Enter image filename: ").strip()

with open(filename, "rb") as f:
    img_bytes = f.read()

image_input = data_url(filename, img_bytes)

caption = generate_caption(image_input)

print(f"\nBasic Caption:\n{caption}")

print("\nOptions:")
print("1. Truncate")
print("2. Expand to 30-word description")
print("3. Summarize to 50-word summary")

choice = input("Choose an option (1/2/3): ").strip()

if choice == "1":
    result = generate_text(f"Shorten this caption: {caption}")
elif choice == "2":
    result = generate_text(f"Expand this into a detailed 30-word description: {caption}")
elif choice == "3":
    result = generate_text(f"Write a 50-word summary of this caption: {caption}")
else:
    result = "Invalid option."

print(f"\nResult:\n{result}")
