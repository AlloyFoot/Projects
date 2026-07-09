import os
import sys
from PIL import Image
import torch
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer

def main():
    print("===== Image Captioning & Text Expansion Pipeline =====")
    
    # Define target image path (change this to your image's filename)
    image_path = "pipeline_output.png" 
    
    # Step 1: Open image safely with error handling
    print(f"\n📂 Step 1: Opening image file '{image_path}'...")
    if not os.path.exists(image_path):
        print(f"❌ Error: The file '{image_path}' was not found. Please place an image in this directory.")
        return
    
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"❌ Error: Failed to open the image. Details: {e}")
        return

    # Step 2: Call Hugging Face's vit-gpt2 to generate a caption
    print("\n🔍 Step 2: Running Hugging Face ViT-GPT2 Image Captioning...")
    try:
        captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
        results = captioner(img)
        base_caption = results[0]['generated_text']
        print(f"📝 Base Caption Generated: \"{base_caption}\"")
    except Exception as e:
        print(f"❌ Error during image captioning: {e}")
        return

    # Step 3: Ask if user wants a longer version
    print("\n❓ Step 3: Prompting user for expansion...")
    user_choice = input("Do you want a longer version of this description? (yes/no): ").strip().lower()

    # Step 4: If yes, send that caption to GPT-2 for ~30-word description
    if user_choice in ["yes", "y"]:
        print("\n📝 Step 4: Sending caption to GPT-2 for extended description...")
        try:
            tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            model = GPT2LMHeadModel.from_pretrained("gpt2")
            tokenizer.pad_token = tokenizer.eos_token

            # Formulate prompt to encourage a descriptive sentence block
            input_prompt = f"A detailed description of a picture showing {base_caption}:"
            inputs = tokenizer(input_prompt, return_tensors="pt", padding=True)
            
            # 30 words translates roughly to 40-50 tokens total (including prompt tokens)
            outputs = model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=40, 
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7
            )
            
            expanded_description = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Step 5: Display results
            print("\n==================== FINAL RESULTS ====================")
            print(f"Original Base Caption: {base_caption}")
            print(f"Expanded Description (~30 words added):\n{expanded_description}")
            print("=======================================================")

        except Exception as e:
            # Step 5: Show errors gracefully
            print(f"❌ Error during GPT-2 text generation expansion: {e}")
            
    elif user_choice in ["no", "n"]:
        # Step 5: Display results (Base only if no expansion is chosen)
        print("\n==================== FINAL RESULTS ====================")
        print(f"Original Base Caption: {base_caption}")
        print("User opted out of generating an expanded version.")
        print("=======================================================")
    else:
        # Step 5: Handle invalid menu inputs as a structural choice error
        print("\n⚠️  Invalid input option selected. Exiting pipeline without expansion loops.")

if __name__ == "__main__":
    main()
