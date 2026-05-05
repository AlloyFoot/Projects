"""
Simple Text-to-Image Generator

Uses primary model, automatically falls back to alternatives only if needed

INSTALLATION:

pip install huggingface-hub pillow
"""

from huggingface_hub import InferenceClient
from datetime import datetime
from PIL import Image
from config import HF_API_KEY

# MODEL PRIORITY LIST - Primary model first, fallbacks only if it fails
MODELS = [
    "ByteDance/SDXL-Lightning",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5",  # Fallback 2
]

client = InferenceClient(api_key=HF_API_KEY)

print(f"Primary model: {MODELS[0]}")
print("Type a prompt to generate an image. Enter 'quit', 'exit', or 'q' to stop.")

while True:
    prompt = input("Prompt: ").strip()

    if prompt.lower() in {"quit", "exit", "q"}:
        break

    if not prompt:
        continue

    print("Generating image...")
    image = None

    for model in MODELS:
        try:
            image = client.text_to_image(prompt, model=model)
            break
        except Exception as e:
            print(f"Model failed: {model} -> {e}")

    if image is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_{timestamp}.png"
        image.save(filename)
        print(f"Saved image as: {filename}")
        image.show()
        print()
    else:
        print("All models failed. Check your API key and try again.")

print("Program terminated. Goodbye!")