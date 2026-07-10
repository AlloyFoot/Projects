import requests
from config import HF_API_KEY

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}


class ImageGenerator:
    def __init__(self, api_url=API_URL, headers=HEADERS):
        self.api_url = api_url
        self.headers = headers

    def generate_image_from_text(self, prompt, negative_prompt="", guidance_scale=7.5):
        payload = {
            "inputs": prompt,
            "options": {
                "negative_prompt": negative_prompt,
                "guidance_scale": guidance_scale
            }
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            file_name = "generated_image.png"
            with open(file_name, "wb") as f:
                f.write(response.content)
            print(f"Image saved as {file_name}")
            print("Used parameters:")
            print(f"Prompt: {prompt}")
            print(f"Negative prompt: {negative_prompt}")
            print(f"Guidance scale: {guidance_scale}")
        else:
            print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    generator = ImageGenerator()

    prompt = input("Enter image prompt: ")
    negative_prompt = input("Enter negative prompt (or leave blank): ")

    guidance_input = input("Enter guidance scale (default 7.5): ").strip()
    guidance_scale = float(guidance_input) if guidance_input else 7.5

    generator.generate_image_from_text(
        prompt=prompt,
        negative_prompt=negative_prompt,
        guidance_scale=guidance_scale
    )
