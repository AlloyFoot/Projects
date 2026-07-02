from groq import generate_response
def bias_mitigation_activity():
    print("Welcome to the Bias Mitigation Activity!")
    prompt = input("Please enter a scenario or situation where bias may occur (e.g. 'Describe the ideal doctor'): ").strip()
    if not prompt:
        print("You did not enter a scenario. Please try again.")
        return
    initial_response = generate_response(prompt, temperature=0.3, max_tokens=1024)
    print("\nInitial Response:")
    print(initial_response)
    modified_prompt = input(f"Please provide a more inclusive and unbiased version of the following response: {initial_response} (e.g. 'Describe the qualities of a doctor'): ").strip()
    if modified_prompt:
        modified_response = generate_response(modified_prompt, temperature=0.3, max_tokens=1024)
        print("\nModified Response:")
        print(modified_response)
    else:
        print("You did not provide a modified prompt. The activity will end here.")
def token_limit_activity():
    print("Welcome to the Token Limit Activity!")
    long_prompt = input("Enter a long prompt (e.g. 'Write a detailed story about a robot'): ").strip()
    if long_prompt:
        long_response = generate_response(long_prompt, temperature=0.3, max_tokens=1024)
        preview = (long_response[:500] + '...') if len(long_response) > 500 else long_response
        print(f"\nResponse to Long Prompt (Preview):\n{preview}")
    else:
        print("You did not enter a long prompt. Skipping long prompt.")
    short_prompt = input("Now, condense the long prompt to be more concise (e.g. 'Write a short, 1 paragraph story about a robot'): ").strip()
    if short_prompt:
        short_response = generate_response(short_prompt, temperature=0.3, max_tokens=1024)
        print(f"\nResponse to Short Prompt:\n{short_response}")
    else:
        print("You did not enter a short prompt. The activity will end here.")
def run_activity():
    print("\nSelect an activity:")
    print("1. Bias Mitigation Activity")
    print("2. Token Limit Activity")
    choice = input("Enter your choice (1-2): ").strip()
    if choice == "1":
        bias_mitigation_activity()
    elif choice == "2":
        token_limit_activity()
    else:
        print("Invalid choice. Please enter a number between 1 and 2.")
if __name__ == "__main__":
    run_activity()