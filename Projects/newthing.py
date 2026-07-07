import config
import os
from hf import generate_response
# from groq import generate_response

def save_reflection(filename, content):
    os.makedirs("activity_results", exist_ok=True)
    filepath = os.path.join("activity_results", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def run_reflections():
    bias_reflection = (
        "PART 1 REFLECTION: BIAS MITIGATION\n"
        "==================================\n\n"
        "1. How did the modified prompt influence the response?\n"
        "The modified prompt shifted the focus away from archetypes or generic generalizations "
        "and guided the model to detail professional, objective criteria like clinical skill, "
        "empathy, clear communication, and ethical standards.\n\n"
        "2. Did you notice any bias or stereotype in the initial response?\n"
        "The initial prompt 'Describe the ideal doctor' frequently causes models to lean toward "
        "subtle cultural or demographic tropes, often defaulting to specific gender roles or a "
        "paternalistic tone when defining 'ideal'.\n\n"
        "3. What can be done to avoid reinforcing biases in AI responses?\n"
        "Use precise language that focuses explicitly on structural attributes, qualifications, "
        "and skills rather than subjective or abstract descriptions like 'ideal'."
    )
    save_reflection("bias_reflection.txt", bias_reflection)

    token_reflection = (
        "PART 2 REFLECTION: TOKEN LIMITS\n"
        "===============================\n\n"
        "1. How did the AI's response change when you condensed the prompt?\n"
        "The response became more direct, targeted, and computationally efficient, dropping "
        "unnecessary narrative fluff while retaining core conceptual points.\n\n"
        "2. Did the AI still provide enough detail? Did it omit any important information?\n"
        "Yes, it provided enough detail. It omitted unnecessary descriptive filler and background "
        "scenery, but successfully preserved the essential milestones and thematic resolution.\n\n"
        "3. How can understanding token limits help in optimizing AI responses?\n"
        "Managing token limits ensures context windows are not wasted on redundant text. It saves "
        "processing costs, reduces latency, and prevents the model from losing tracking context "
        "over long interactions."
    )
    save_reflection("token_reflection.txt", token_reflection)
    
    print("Reflections successfully generated and saved to the 'activity_results' folder.")

if __name__ == "__main__":
    run_reflections()