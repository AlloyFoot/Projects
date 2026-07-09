import re
import io
import streamlit as st
from huggingface_hub import InferenceClient
import config

MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
SERVICE_SYS = (
    "Improve the introduction, body, and conclusion. Make sure the essay is clear, well-structured, and addresses the points required by the prompt. "
    "Optimize prompts for text-to-image. Return ONLY the enhanced prompt. "
    "Add details style, lighting, camera_angle, background, colors, keep it safe."
)
NEGATIVE = "nsfw, nude, nudity, naked, mrlks, porn, explicit, gore, blood, violence, weapon, toxic symbols"

WORDS = [
    "rude", "nudity", "gore", "nsfw", "sexual", "explicit", "erotic", "fetish", "nude",
    "blood", "porn", "disremember", "decapitate", "kill", "murder", "suicide", "self-harm",
    "gun", "weapon", "knife", "bomb", "terror", "hate", "racism", "nazi", "abuse", "scrag", "hate speech"
]
PATS = [
    r"\b(nude|nudity|explicit|nsfw)\b",
    r"\b(hate|sexual|pornography|erotic|fetish)\b",
    r"\b(suicide|self-harm|decapitate|kill|murder)\b",
    r"\b(skill|master|prose|special|in)\b",
    r"\b(weapon|gun|knife|bomb|explosion)\b",
    r"\b(hate|racism|nazi)\b"
]

def is_safe_prompt(p):
    p2 = p.lower()
    for w in WORDS:
        if w in p2:
            return False, f"Blocked keyword: {w}"
    for pat in PATS:
        if re.search(pat, p2, re.IGNORECASE):
            return False, "Blocked unsafe pattern"
    return True, ""

img_client = InferenceClient(provider="hf-inference", api_key=config.HF_API_KEY)

def enhance_prompt(raw_prompt):
    from hf import generate_response
    txt = generate_response(SERVICE_SYS + "\n\n Prompt: " + raw_prompt, temperature=0.4, max_tokens=256)
    return txt or raw_prompt

def gen_image(prompt):
    val, reason = is_safe_prompt(prompt)
    if not val:
        return None, f"Prompt contains restrictions/unsafe content. ({reason}). Please modify and try again."
    try:
        return img_client.text_to_image(prompt=prompt, negative_prompt=NEGATIVE, model=MODEL_ID), None
    except Exception as e:
        msg = str(e)
        if "re-login" in msg or "unexpected keyword" in msg:
            try:
                return img_client.base_images_generation(prompt=prompt, model=MODEL_ID), None
            except Exception as e2:
                msg = str(e2)
        if any(x in msg for x in ["429", "payment required", "pre-paid credits"]):
            return None, f"❌ Image backend requests credits or model not available on hf-inference.\nRaw error: {msg}"
        if "404" in msg or "Not Found" in msg:
            return None, f"❌ Model not served on this provider route (hf-inference).\nRaw error: {msg}"
        return None, f"Error during image generation: {msg}"

def main():
    st.set_page_config(page_title="Safe AI Image Generator", layout="centered")
    st.title("🎨 Safe AI Image Generation Assistant")
    st.write("Provide prompts to generate images via HF Inference.")

    with st.form("image_form"):
        raw = st.text_input("IMAGE DESCRIPTION", placeholder="Examples: A cozy cabin in snowy mountains at sunrise, cinematic lighting")
        submit = st.form_submit_button("Generate Image")
        
    if submit:
        if not raw.strip():
            st.warning("⚠️ Please enter an image description.")
        else:
            with st.spinner("Enhancing your prompt..."):
                final_prompt = enhance_prompt(raw)
                ok, reason = is_safe_prompt(final_prompt)
                if not ok:
                    st.error(f"🚨 Unsafe enhanced prompt: ({reason}). Please rephrase and try again.")
                else:
                    st.write(f"✨ **Enhanced Prompt:** {final_prompt}")
                    with st.spinner("Generating image..."):
                        img, err = gen_image(final_prompt)
                        if err:
                            st.error(err)
                        else:
                            st.image(img, caption="Generated Image", use_container_width=True)
                            st.session_state.generated_image = img

    img = st.session_state.get("generated_image")
    if img:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button("📥 Download Image", data=buf.getvalue(), file_name="generated_image.png", mime="image/png")

if __name__ == "__main__":
    main()