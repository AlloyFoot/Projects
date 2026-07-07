import config
import os
from hf import generate_response
# from groq import generate_response

def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def refine_essay_pipeline():
    original_essay = read_file("essay.txt")
    if not original_essay:
        print("Error: essay.txt is empty or missing.")
        return

    audience_style = input("Select writing style (formal / conversational): ").strip().lower()
    if audience_style not in ["formal", "conversational"]:
        audience_style = "formal"

    refine_prompt = (
        f"You are an expert editor. Refine the following essay to fit a {audience_style} style. "
        f"Ensure the introduction is engaging and hooks the reader. "
        f"Structure the body paragraphs clearly, breaking down long blocks of text into shorter, "
        f"fully developed points. Revise the conclusion to wrap up with strong, impactful statements.\n\n"
        f"Essay:\n{original_essay}"
    )

    print("\nRefining essay structure and tone...")
    refined_essay = generate_response(refine_prompt)
    write_file("refined_essay.txt", refined_essay)
    print("Saved structural adjustments to refined_essay.txt")

    feedback = read_file("feedback.txt")
    if feedback:
        print("\nApplying feedback adjustments from feedback.txt...")
        feedback_prompt = (
            f"Review the following essay and incorporate this specific feedback regarding its structure, "
            f"tone, and content to maximize clarity and effectiveness.\n\n"
            f"Feedback:\n{feedback}\n\n"
            f"Essay:\n{refined_essay}"
        )
        final_essay = generate_response(feedback_prompt)
        write_file("final_essay.txt", final_essay)
        print("Saved final version to final_essay.txt")
    else:
        print("\nNo feedback found in feedback.txt. Process complete.")

if __name__ == "__main__":
    refine_essay_pipeline()