import config
import os
from hf import generate_response
# from groq import generate_response

def save_log(filename, content):
    os.makedirs("activity_results", exist_ok=True)
    filepath = os.path.join("activity_results", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def run_prompting_activity():
    topic = "French revolution"

    zero_shot_prompt = (
        f"Explain the primary cause of the {topic}."
    )
    
    one_shot_prompt = (
        f"Context: Historical Event Summaries\n"
        f"Example:\n"
        f"Topic: American Revolution\n"
        f"Summary: A political disruption between 1775 and 1783 where thirteen North American colonies broke from the British Empire, primarily triggered by taxation without direct parliamentary representation.\n\n"
        f"Topic: {topic}\n"
        f"Summary:"
    )
    
    few_shot_prompt = (
        f"Context: Educational Question Answering\n"
        f"Q: What triggered the Industrial Revolution?\n"
        f"A: The transition to new manufacturing processes in Europe and the US, sparked by the steam engine, mechanization of textiles, and access to raw coal resources.\n\n"
        f"Q: What triggered the Fall of Rome?\n"
        f"A: A complex combination of internal economic crises, constant barbarian invasions, political instability, and the administrative overexpansion of the empire.\n\n"
        f"Q: What triggered the {topic}?\n"
        f"A:"
    )

    print("Running Zero-Shot prompt configuration...")
    zero_shot_response = generate_response(zero_shot_prompt)

    print("Running One-Shot prompt configuration...")
    one_shot_response = generate_response(one_shot_prompt)

    print("Running Few-Shot prompt configuration...")
    few_shot_response = generate_response(few_shot_prompt)

    reflection = (
        "PROMPTING TECHNIQUES REFLECTION\n"
        "==============================\n\n"
        "1. Compare how different styles of prompting influence AI output:\n"
        "Zero-Shot prompt structures give the model complete creative freedom, resulting in highly detailed narratives but less structural predictability. "
        "One-Shot structures immediately constrain the output style, forcing the response to match the exact length and tone provided in the baseline example. "
        "Few-Shot structures establish an undeniable syntactic and contextual rhythm, steering the model to return factual, tightly targeted insights that perfectly mimic the prefix tokens.\n\n"
        "2. Reflect on real-world applications of each technique:\n"
        "- Zero-Shot: Ideal for open-ended brainstorming, creative writing drafts, and exploratory conversational agents where rigid structure isn't required.\n"
        "- One-Shot: Useful when adapting an AI output to a specific corporate voice, template, or documentation format without feeding massive examples.\n"
        "- Few-Shot: Essential for precise production classification pipelines, parsing messy data points into strict formats, or standardizing specialized training datasets."
    )

    log_content = (
        f"PROMPTING STRATEGIES EXPERIMENTATION LOG\n"
        f"Target Topic: {topic}\n"
        f"========================================\n\n"
        f"--- 1. ZERO-SHOT APPROACH ---\n"
        f"Prompt: {zero_shot_prompt}\n"
        f"Output:\n{zero_shot_response}\n\n"
        f"--- 2. ONE-SHOT APPROACH ---\n"
        f"Prompt:\n{one_shot_prompt}\n"
        f"Output:\n{one_shot_response}\n\n"
        f"--- 3. FEW-SHOT APPROACH ---\n"
        f"Prompt:\n{few_shot_prompt}\n"
        f"Output:\n{few_shot_response}\n\n"
        f"{reflection}"
    )

    save_log("prompt_techniques_results.txt", log_content)
    print("Execution complete. Log outputs successfully written to activity_results/prompt_techniques_results.txt")

if __name__ == "__main__":
    run_prompting_activity()