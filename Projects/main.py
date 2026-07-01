from groq import generate_response
def reinforcement_learning_activity():
    print("\nWelcome to the Reinforcement Learning Activity!\n")
    prompt = input("Enter a prompt for the AI Model (e.g. 'What is reinforcement learning?'): ").lower().strip()
    if not prompt:
        print("No prompt provided. Exiting the activity.")
        return
    
    rating = 0
    while rating < 4:
        initial_response = generate_response(prompt, temperature=0.3, max_tokens=1028)
        print("\nInitial Response from the AI Model:\n")
        print(initial_response)
        try:
            rating = int(input("\nPlease rate the response on a scale of 1 to 5 (1 being poor, 5 being excellent): "))
            if rating < 1 or rating > 5:
                print("Invalid rating. Please enter a number between 1 and 5.")
                return
        except ValueError:
            print("Invalid input. Using 3.")
            rating = 3
        feedback = input("Please provide feedback for the AI Model : ").strip()
        improved_response = f"{initial_response}\n\nUser Feedback: {feedback}\n\nPlease improve the response based on the feedback."
        print(f"\nImproved Response from the AI Model:{improved_response}\n")
        prompt = improved_response


    print("Reflection:")
    print("1. How did the AI model's response change after receiving feedback?")
    print("2. What aspects of the response were improved or remained the same?")
def role_based_prompt_activity():
    print("\nWelcome to the Role-Based Prompt Activity!\n")
    category = input("Enter a category (e.g. science, history, math): ").lower().strip()
    item = input(f"Enter a specific item in the category of {category}: ").lower().strip()
    if not category or not item:
        print("Category or item not provided. Exiting the activity.")
        return
    teacher_prompt = f"Imagine you are a teacher explaining {item} in the context of {category}. Provide a detailed explanation suitable for students."
    expert_prompt = f"Imagine you are an expert in {category}. Provide an in-depth analysis of {item}, including its significance and applications."
    teacher_response = generate_response(teacher_prompt, temperature=0.3, max_tokens=1028)
    expert_response = generate_response(expert_prompt, temperature=0.3, max_tokens=1028)
    print("\nTeacher's Response:\n")
    print(teacher_response)
    print("\nExpert's Response:\n")
    print(expert_response)
    print("\nReflection:")
    print("1. How did the responses differ based on the role of the AI model?")
    print("2. What insights did you gain from comparing the two responses?")
def run_activity():
    print("Welcome to the AI Model Interaction Activities!")
    print("Please choose an activity:")
    print("1. Reinforcement Learning Activity")
    print("2. Role-Based Prompt Activity")
    choice = input("Enter the number of the activity you want to participate in (1 or 2): ").strip()
    if choice == '1':
        reinforcement_learning_activity()
    elif choice == '2':
        role_based_prompt_activity()
    else:
        print("Invalid choice. Please enter 1 or 2.")
if __name__ == "__main__":
    run_activity()