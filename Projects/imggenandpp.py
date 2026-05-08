from huggingface_hub import InferenceClient
from PIL import ImageEnhance, ImageFilter
from datetime import datetime
from config import HF_API_KEY

# Model priority list
MODELS = [
    "ByteDance/SDXL-Lightning",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5",
]

client = InferenceClient(api_key=HF_API_KEY)

def generate_image_from_text(prompt):
    """Generate an image from text using fallback models."""
    last_err = None

    for model in MODELS:
        try:
            print(f"Trying model: {model}")
            image = client.text_to_image(prompt, model=model)
            return image
        except Exception as e:
            last_err = f"{model} -> {e}"
            print(f"Model failed: {model} -> {e}")

    raise Exception(last_err or "All models failed")

def post_process_image(image):
    """Apply brightness, contrast, and blur effects."""
    image = ImageEnhance.Brightness(image).enhance(1.2)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    image = image.filter(ImageFilter.GaussianBlur(radius=2))
    return image

def main():
    print("Welcome to the Post-Processing Magic Workshop!")
    print("This program generates an image from text and applies post-processing effects.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter a description for the image (or 'exit' to quit):\n").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            print("\nGenerating image...")
            image = generate_image_from_text(user_input)

            print("Applying post-processing effects...\n")
            processed_image = post_process_image(image)
            processed_image.show()

            save_option = input("Do you want to save the processed image? (yes/no): ").strip().lower()
            if save_option == "yes":
                file_name = input("Enter a name for the image file (without extension): ").strip()
                if not file_name:
                    file_name = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                processed_image.save(f"{file_name}.png")
                print(f"Image saved as {file_name}.png\n")

            print("-" * 80 + "\n")

        except Exception as e:
            print(f"An error occurred: {e}\n")

if __name__ == "__main__":
    main()