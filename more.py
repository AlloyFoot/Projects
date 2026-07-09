import os
import torch
from PIL import Image, ImageEnhance, ImageFilter
from diffusers import StableDiffusionPipeline

def generate_image_from_text(prompt):
    """Generates a base image from a text prompt using Stable Diffusion."""
    print(f"\n🎨 Loading Stable Diffusion and generating: '{prompt}'...")
    
    model_id = "runwayml/stable-diffusion-v1-5"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if device == "cuda" else torch.float32
    
    # Initialize pipeline
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch_dtype)
    pipe = pipe.to(device)
    
    # Generate and return image object
    image = pipe(prompt).images[0]
    return image

def main():
    print("===== Image Generation & Mood Filter Pipeline =====")
    
    # 1. Prompt the user to enter a creative text description
    print("\n📝 Step 1: User Input")
    user_prompt = input("Enter a creative text description (e.g., 'a magical forest at sunrise'): ").strip()
    if not user_prompt:
        user_prompt = "a magical forest at sunrise"
        print(f"Using default fallback prompt: '{user_prompt}'")
        
    # Standardize a base name for file naming format conversions
    safe_filename = "".join([c if c.isalnum() else "_" for c in user_prompt]).strip("_")
    if not safe_filename:
        safe_filename = "original_prompt"

    try:
        # 2. Generate an image from this prompt
        print("\n⏳ Step 2: Running generation sequence...")
        base_image = generate_image_from_text(user_prompt)
        
        # 3. Apply two separate effects
        print("\n⚙️  Step 3: Processing separate mood effects...")
        
        # --- Daylight Edition ---
        # - Increase brightness by 30% (factor = 1.3)
        # - Enhance contrast by 10% (factor = 1.1)
        # - Apply Gaussian blur with radius 1
        print("☀️  Creating Daylight Edition...")
        daylight_img = base_image.copy()
        
        daylight_img = ImageEnhance.Brightness(daylight_img).enhance(1.3)
        daylight_img = ImageEnhance.Contrast(daylight_img).enhance(1.1)
        daylight_img = daylight_img.filter(ImageFilter.GaussianBlur(radius=1))
        
        # --- Night Mood ---
        # - Increase contrast by 40% (factor = 1.4)
        # - Slightly reduce brightness by 10% (factor = 0.9)
        # - Apply Gaussian blur with radius 0.5
        print("🌙 Creating Night Mood Edition...")
        night_img = base_image.copy()
        
        night_img = ImageEnhance.Contrast(night_img).enhance(1.4)
        night_img = ImageEnhance.Brightness(night_img).enhance(0.9)
        night_img = night_img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # 4. Save both versions with specified suffixes
        print("\n💾 Step 4: Saving processed files to disk...")
        daylight_filename = f"{safe_filename}_daylight.png"
        night_filename = f"{safe_filename}_night.png"
        
        daylight_img.save(daylight_filename)
        night_img.save(night_filename)
        
        print(f" Saved: '{daylight_filename}'")
        print(f" Saved: '{night_filename}'")
        
        # 5. Display both images one after the other
        print("\n🖥️  Step 5: Launching default image viewers for inspection...")
        print("Displaying Daylight Edition...")
        daylight_img.show()
        
        print("Displaying Night Mood Edition...")
        night_img.show()
        
        print("\n=======================================================")
        print("🎉 Filter Loop Complete Success!")
        print("=======================================================")
        
    except Exception as e:
        print(f"\n❌ Pipeline Failure Encountered: {e}")

if __name__ == "__main__":
    main()
