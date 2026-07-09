import os
import sys
import torch
from PIL import Image
from diffusers import StableDiffusionInpaintPipeline

def generate_inpainting_image(prompt, image_path, mask_path):
    """Loads the Stable Diffusion Inpainting pipeline and processes the image."""
    print("\n🚀 Loading Stable Diffusion Inpainting pipeline...")
    
    # Check if the target image and mask files exist
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Source image '{image_path}' not found.")
    if not os.path.exists(mask_path):
        raise FileNotFoundError(f"Mask image '{mask_path}' not found.")
        
    # Open images and convert to RGB/L format as expected by the pipeline
    init_image = Image.open(image_path).convert("RGB")
    mask_image = Image.open(mask_path).convert("RGB") # Pipeline handles RGB mask profiles well
    
    # Setup device acceleration (Use GPU if available, otherwise fall back to CPU)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if device == "cuda" else torch.float32
    
    # Load pre-trained runwayml stable diffusion inpainting checkpoint
    model_id = "runwayml/stable-diffusion-inpainting"
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        model_id, 
        torch_dtype=torch_dtype
    )
    pipe = pipe.to(device)
    
    print("⏳ Processing inpainting latents (this might take a moment)...")
    # Run image restoration generation
    restored_image = pipe(prompt=prompt, image=init_image, mask_image=mask_image).images[0]
    return restored_image

def main():
    print("===== AI Image Restoration & Inpainting Pipeline =====")
    
    # 1. Prompt the user for a brief restoration description
    # Example: "restore the torn edges and faded areas"
    print("\n📝 Step 1: Describe the restoration adjustments.")
    user_prompt = input("Enter a brief restoration description: ").strip()
    if not user_prompt:
        user_prompt = "restore the torn edges and faded areas"
        print(f"Using default fallback prompt: '{user_prompt}'")
        
    # Default file paths required by instructions
    default_image = "old_photo.png"
    default_mask = "old_photo_mask.png"
    
    # 5. Extra Exploration: Let the user tweak the mask path to try alternative repairs
    print("\n🔍 Step 5: Extra Exploration (Optional)")
    tweak_path = input(f"Press Enter to use default mask ('{default_mask}') or type a custom mask path: ").strip()
    mask_path = tweak_path if tweak_path else default_mask

    try:
        # 2. Call generate_inpainting_image with paths
        print("\n🎨 Step 2: Initiating restoration algorithm...")
        restored_img = generate_inpainting_image(
            prompt=user_prompt, 
            image_path=default_image, 
            mask_path=mask_path
        )
        
        # 3. Display the returned image for quick inspection
        print("\n🖥️  Step 3: Displaying the returned image for inspection...")
        # Note: .show() launches your operating system's default image viewer utility
        restored_img.show()
        
        # 4. Ask whether to save the result
        print("\n💾 Step 4: Save Verification")
        save_choice = input("Would you like to save the restored image? (yes/no): ").strip().lower()
        
        if save_choice in ["yes", "y"]:
            output_filename = "old_photo_restored.png"
            restored_img.save(output_filename)
            print(f"✨ Success! Your restored photo has been saved to: '{output_filename}'")
        else:
            print("⚠️  Exiting script without saving the output image.")
            
    except FileNotFoundError as fnf_error:
        print(f"\n❌ Setup Error: {fnf_error}")
        print(f"💡 Please ensure '{default_image}' and your mask file are placed in this directory.")
    except Exception as e:
        print(f"\n❌ An unexpected pipeline error occurred: {e}")

if __name__ == "__main__":
    main()
