from groq import generate_response
def run_activity():
    print("Zero-Shot, One-Shot, and Few-Shot Prompting")
    category = input("Enter the category of the activity (e.g., 'math', 'science', 'history'): ").strip().lower()
    item = input(f"Enter a specific {category} to classify\: ").strip().lower()
    if not category or not item:
        print("Invalid input. Please try again.")
        return
    zero_shot = f"Is '{item}' a valid {category}? Answer yes or no."
    print("\nZero-Shot Prompting:")
    print(f"Response: {generate_response(zero_shot, temperature=0.3, max_tokens=1024)}")
    one_shot = f"""Example:
    Category: fruit
    Item: apple
    Is 'apple' a valid fruit? Answer: yes
    Now, you try:
    Category: {category}
    Item: {item}
    Is '{item}' a valid {category}? Answer yes or no."""
    print("\nOne-Shot Prompting:")
    print(f"Response: {generate_response(one_shot, temperature=0.3, max_tokens=1024)}")
    few_shot = f"""Example 1:
    Category: fruit
    Item: apple
    Is 'apple' a valid fruit? Answer: yes
    Example 2:
    Category: fruit
    Item: carrot
    Is 'carrot' a valid fruit? Answer: no
    Now, you try:
    Category: {category}
    Item: {item}
    Is '{item}' a valid {category}? Answer yes or no."""
    print("\nFew-Shot Prompting:")
    print(f"Response: {generate_response(few_shot, temperature=0.3, max_tokens=1024)}")
    creative_prompt = f"""Write a one-sentece story about the given word.
    Example 1:
    Word: moon
    Story: The moon shone brightly over the quiet village, casting silver shadows on the cobblestone streets.
    Word: {item}
    Story:"""
    print("\nCreative Prompting:")
    print(f"Response: {generate_response(creative_prompt, temperature=0.7, max_tokens=1024)}")
    print("Reflection Questions:")
    print("1. How did the model's responses differ between zero-shot, one-shot, and few-shot prompting?")
    print("2. Which approach gave the most helpful or accurate response for your specific item?")
    print("3. How did the examples influence the model's output?")
if __name__ == "__main__":
    run_activity()