from hf import generate_response
import time
def temperature_prompt_activity():
    print("=" * 70)
    print("Advanced Prompt Activity: Temperature")
    print("=" * 70)

    print("Part 1: Temperature Exploration")
    base = input("Enter a creative prompt (e.g., 'Write a short story about a dragon'): ")
    for t, label in [(0.1, "LOW (0.1) - Deterministic"), (0.5, "MEDIUM (0.5) - Balanced"), (0.9, "HIGH (1.0) - Creative")]:
        print(f"\n{label}")
        print("-" * len(label))
        response = generate_response(base, temperature=t)
        print(response)
        time.sleep(1)
    print("\nPart 2: Instruction-Based Prompts")
    topic = input("Enter a topic for an instruction-based prompt (e.g., 'Explain quantum computing in simple terms'): ")
    prompts = [
        f"Summarize key facts about {topic} in 3-4 sentences.",
        f"Explain {topic} to a 5-year-old.",
        f"Write a pro/con list about {topic}.",
        f"Create a fictional news headline from 2050 about {topic}."
    ]
    for i, p in enumerate(prompts, 1):
        print(f"\nPrompt {i}: {p}")
        response = generate_response(p, temperature=0.7)
        print(response)
        time.sleep(1)
    print("\nPart 3: Your Own Instruction Prompt")
    user_prompt = input("Enter your own instruction-based prompt: ")
    try:
        temp = float(input("Enter a temperature value (0.0 to 1.0): "))
        if not (0.0 <= temp <= 1.0):
            raise ValueError("Temperature must be between 0.0 and 1.0.")
    except ValueError as ve:
        print(f"Invalid temperature input: {ve}. Using default temperature of 0.7.")
        temp = 0.7
    print(f"\nYour Prompt: {user_prompt} (Temperature: {temp})")
    print(generate_response(user_prompt, temperature=temp, max_tokens=512))
    print("\nREFELECTION:")
    print("1. what changed when prompts became more specific or detailed?")
    print("2. what improved when context was provided in the prompts?")
    print("3. which prompt felt most useful and why?")
    print("\nChanllenge: create a prompt chain: ")
    print("Start with a base prompt, then iteratively refine it based on the model's responses to achieve a more detailed or specific output.")
def pseudo_stream(text, delay= 0.013):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
def bonus_stream():
    choice = input("\nBONUS: streaming output? (y/n): ").lower().strip()
    if choice == 'y':
        p = input("Enter a prompt for streaming output: ").strip()
        out = generate_response(p, temperature=0.7, max_tokens=512)
        print("\nStreaming Output:")
        pseudo_stream(out)
if __name__ == "__main__":
    temperature_prompt_activity()
    bonus_stream()