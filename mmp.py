import torch
from PIL import Image
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
from diffusers import StableDiffusionPipeline

def expand_text_gpt2(prompt_text):
    """Step 1: Use GPT-2 to expand a short user prompt into a detailed description."""
    print(f"\n📝 Step 1: Expanding prompt using GPT-2...")
    
    # Load GPT-2 tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    
    # Configure padding token to avoid warnings
    tokenizer.pad_token = tokenizer.eos_token
    
    # Encode input text
    inputs = tokenizer(prompt_text, return_tensors="pt", padding=True)
    
    # Generate expanded text sequence
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=60,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )
    
    expanded_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"✨ Expanded Prompt: {expanded_text}")
    return expanded_text

def generate_image_sd(expanded_prompt, output_path="generated_image.png"):
    """Step 2: Use Stable Diffusion to generate an image from the expanded prompt."""
    print(f"\n🎨 Step 2: Generating image via Stable Diffusion...")
    
    # Load the Stable Diffusion pipeline (v1-5 for efficient local deployment)
    model_id = "runwayml/stable-diffusion-v1-5"
    
    # Use GPU acceleration if available, otherwise fallback to CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if device == "cuda" else torch.float32
    
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch_dtype)
    pipe = pipe.to(device)
    
    # Run text-to-image inference
    print("⏳ Processing diffusion latents (this might take a minute)...")
    image = pipe(expanded_prompt).images[0]
    
    # Save image canvas locally
    image.save(output_path)
    print(f"💾 Image successfully generated and saved to: '{output_path}'")
    return image

def caption_image_vit(image_path):
    """Step 3: Use ViT-GPT2 to generate a descriptive caption for the generated image."""
    print(f"\n🔍 Step 3: Analyzing and captioning image using ViT-GPT2...")
    
    # Initialize the image-to-text pipeline
    captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    
    # Load image file handle
    image = Image.open(image_path)
    
    # Generate structural text summary description
    results = captioner(image)
    caption = results[0]['generated_text']
    
    print(f"📝 Generated Vision Caption: \"{caption}\"")
    return caption

def main():
    print("===== AI Multi-Modal Pipeline Generation Loop =====")
    
    # Capture initial casual user phrase
    user_prompt = input("Enter a creative concept or starter sentence: ").strip()
    if not user_prompt:
        user_prompt = "A serene lake surrounded by mountains"
        print(f"Using default fallback prompt: '{user_prompt}'")
        
    image_filename = "pipeline_output.png"
    
    try:
        # Step 1: Text Expansion (GPT-2)
        detailed_prompt = expand_text_gpt2(user_prompt)
        
        # Step 2: Image Generation (Stable Diffusion)
        generate_image_sd(detailed_prompt, output_path=image_filename)
        
        # Step 3: Image Captioning (ViT-GPT2)
        final_caption = caption_image_vit(image_filename)
        
        print("\n=======================================================")
        print("🎉 Multi-Modal Pipeline Executed Successfully!")
        print(f"📥 Input: {user_prompt}")
        print(f"⚙️  Expanded Context: {detailed_prompt}")
        print(f"🖼️  Image Output Location: {image_filename}")
        print(f"📝 Final Extracted Caption: {final_caption}")
        print("=======================================================")
        
    except Exception as e:
        print(f"\n❌ Pipeline Failure Encountered: {e}")

if __name__ == "__main__":
    main()
