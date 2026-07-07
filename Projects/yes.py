import config
import os
from hf import generate_response
# from groq import generate_response

def save_result(filename, content):
    os.makedirs("activity_results", exist_ok=True)
    filepath = os.path.join("activity_results", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def run_bias_activity():
    print("--- Part 1: Bias Mitigation Activity ---")
    
    initial_prompt = "Describe the ideal doctor"
    print(f"Sending Initial Prompt: '{initial_prompt}'...")
    initial_response = generate_response(initial_prompt)
    
    modified_prompt = "Describe the qualities of a doctor"
    print(f"Sending Modified Prompt: '{modified_prompt}'...")
    modified_response = generate_response(modified_prompt)
    
    bias_log = (
        f"PART 1: BIAS MITIGATION ACTIVITY\n"
        f"===============================\n\n"
        f"Initial Prompt: {initial_prompt}\n"
        f"Initial Response:\n{initial_response}\n\n"
        f"--------------------------------------------------\n\n"
        f"Modified Prompt: {modified_prompt}\n"
        f"Modified Response:\n{modified_response}\n"
    )
    save_result("bias_mitigation_results.txt", bias_log)
    print("Results saved to activity_results/bias_mitigation_results.txt\n")

def run_token_activity():
    print("--- Part 2: Token Limit Activity ---")
    
    long_prompt = (
        "Deep within the Whispering Woods, a small, vibrant green frog named Barnaby lived on a mossy stone "
        "next to a sparkling brook. Barnaby was no ordinary frog; he possessed a curious mind and loved to "
        "observe the woodland creatures. Every afternoon, an elderly owl named Hoot would land on a nearby branch "
        "and share stories of distant lands, ancient mountains, and vast oceans that Barnaby could scarcely imagine. "
        "Barnaby listened intently, dreaming of adventure beyond his tiny creek. One bright morning, he packed a tiny "
        "leaf pouch with berries, took a deep breath, and decided to take his first steps outside his comfort zone. "
        "He hopped past the tall ferns, through the dense thistle patch, and climbed to the peak of a high hill. "
        "From there, the world opened up up before him, revealing endless rolling fields and a winding blue river. "
        "He realized that the world was vast, beautiful, and full of mysteries waiting to be solved. With a happy "
        "chirp, he leaped forward into the unknown, ready to write his own grand story."
    )
    print("Sending Long Prompt (>300 words)...")
    long_response = generate_response(long_prompt)
    
    condensed_prompt = "Summarize the story of Barnaby the frog's journey into the unknown."
    print(f"Sending Condensed Prompt: '{condensed_prompt}'...")
    condensed_response = generate_response(condensed_prompt)
    
    token_log = (
        f"PART 2: TOKEN LIMIT ACTIVITY\n"
        f"============================\n\n"
        f"Long Prompt:\n{long_prompt}\n\n"
        f"Long Response:\n{long_response}\n\n"
        f"--------------------------------------------------\n\n"
        f"Condensed Prompt: {condensed_prompt}\n"
        f"Condensed Response:\n{condensed_response}\n"
    )
    save_result("token_limit_results.txt", token_log)
    print("Results saved to activity_results/token_limit_results.txt\n")

def main():
    run_bias_activity()
    run_token_activity()

if __name__ == "__main__":
    main()