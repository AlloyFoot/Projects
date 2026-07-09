import os
import sys
import requests

# Import API keys from your local config setup
try:
    import config
    HF_TOKEN = getattr(config, "HF_API_KEY", None)
except ImportError:
    print("❌ Error: config.py missing. Please create config.py with HF_API_KEY.")
    sys.exit(1)

# Model configuration
MODEL_ID = "nlpconnect/vit-gpt2-image-captioning"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_caption_api(image_bytes):
    """Sends raw image binary data directly to Hugging Face Inference API."""
    response = requests.post(API_URL, headers=HEADERS, data=image_bytes)
    
    # Catch initial model loading or API errors
    if response.status_code == 503:
        # Model is likely loading on HF servers; try one quick retry or flag it
        raise Exception("Hugging Face model is currently loading/warming up. Try again in a few seconds.")
    elif response.status_code != 200:
        raise Exception(f"API Error (Status {response.status_code}): {response.text}")
        
    result = response.json()
    if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
        return result[0]['generated_text'].strip()
    return "[Unable to extract text caption from API response structure]"

def main():
    print("===== Batch Image Captioning Multi-Processor =====")
    
    # 1. Prompt user for folder path with 'images' as default fallback
    folder_input = input("Enter the path to the folder containing images (Leave empty for 'images'): ").strip()
    folder_path = folder_input if folder_input else "images"
    
    # Optional Challenge: Ask user whether to display captions in the console as they go
    console_show = input("Would you like to print each caption in the console as it's processed? (yes/no): ").strip().lower()
    verbose = console_show in ["yes", "y", ""]

    # 2. Error Handling: Verify folder exists and isn't empty
    if not os.path.exists(folder_path):
        print(f"❌ Error: The directory folder '{folder_path}' does not exist. Ending script.")
        return
        
    if not os.path.isdir(folder_path):
        print(f"❌ Error: '{folder_path}' is a file path, not a valid directory directory folder. Ending script.")
        return

    # Filter out common image formats to avoid trying to process system files (.DS_Store, etc.)
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]

    if not image_files:
        print(f"⚠️  Folder Alert: No valid image files ({', '.join(valid_extensions)}) found inside '{folder_path}'.")
        return

    print(f"📂 Found {len(image_files)} image files to process inside '{folder_path}'. starting pipeline loops...")
    
    records = []
    
    # 3. Process every image file in the directory target loop
    for idx, filename in enumerate(image_files, 1):
        full_image_path = os.path.join(folder_path, filename)
        if verbose:
            print(f"\n🖼️  [{idx}/{len(image_files)}] Processing file: '{filename}'...")
            
        try:
            # Read the target image file explicitly in binary mode ('rb')
            with open(full_image_path, "rb") as img_file:
                binary_data = img_file.read()
            
            # Send binary context to HF Inference API
            caption = query_caption_api(binary_data)
            
            if verbose:
                print(f"✨ Caption: \"{caption}\"")
                
            records.append((filename, caption))
            
        except Exception as e:
            # Handle item exceptions gracefully so one broken image doesn't crash the whole batch run
            error_msg = f"[Error processing file: {e}]"
            print(f"❌ Skipped '{filename}': {error_msg}")
            records.append((filename, error_msg))

    # 4. Report generation: Write image-caption pairs out to captions_summary.txt
    output_filename = "captions_summary.txt"
    try:
        with open(output_filename, "w", encoding="utf-8") as out_file:
            out_file.write("===================================================\n")
            out_file.write(f" BATCH CAPTION SUMMARY REPORT - Directory: {folder_path}\n")
            out_file.write("===================================================\n\n")
            for name, cap in records:
                out_file.write(f"Image File Name: {name}\n")
                out_file.write(f"Generated Caption: {cap}\n")
                out_file.write("-" * 40 + "\n")
                
        print("\n=======================================================")
        print("🎉 Batch Processing Complete!")
        print(f"💾 All results summarized and saved to: '{output_filename}'")
        print("=======================================================")
    except IOError as e:
        print(f"❌ Fatal Write Error: Could not save summary text logging to disk: {e}")

if __name__ == "__main__":
    main()
