import requests
from config import HF_API_KEY

MODEL = "google/pegasus-xsum"
API_URL=f"https://router.huggingface.co/hf-inference/models/{MODEL}"

SUMMARY_PRESETS = {
    "standard": {"min_length": 25, "max_length": 80},
    "enhanced": {"min_length": 60, "max_length": 180},
}

def validate_lengths(min_length, max_length):
    if not isinstance(min_length, int) or not isinstance(max_length, int):
        raise TypeError("min_length and max_length must be integers.")
    if min_length < 1:
        raise ValueError("min_length must be at least 1.")
    if max_length < min_length:
        raise ValueError("max_length must be greater than or equal to min_length.")

def summarize_text(text, mode="standard", tone="formal"):
    if not isinstance(text, str):
        raise TypeError("input must be string")
    if not text.strip():
        raise ValueError("input must not be empty")
    if mode not in SUMMARY_PRESETS:
        raise ValueError("mode must be either 'standard' or 'enhanced'.")
    
    settings = SUMMARY_PRESETS[mode]
    min_length = settings["min_length"]
    max_length = settings["max_length"]

    if min_length < 1 or max_length < min_length:
        raise ValueError("invalid summary length settings")
    
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": text,
        "parameters": {
            "min_length": min_length, 
            "max_length": max_length, 
            "do_sample": False
        },
        "options": {
            "wait_for_model": True
        }

    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        try:
            detail = response.json()
        except Exception:
            detail = response.text
        raise RuntimeError(f"API request failed ({response.status_code}): {detail}")

    data = response.json()

    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected API response: {data}")

    summary = data[0].get("summary_text")
    if not summary:
        raise RuntimeError(f"Summary not found in response: {data}")

    return summary

def main():
    text = input("Enter text to summarize: ").strip()
    mode = input("Choose mode (standard/enhanced): ").lower().strip()
    print(summarize_text(text, mode))




if __name__=="__main__": 
    main()