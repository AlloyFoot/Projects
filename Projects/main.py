from hf import generate_response
def get_essay_details():
    print("\nAI writing assistant\n")
    topic = input("Enter the topic for your essay: ").strip()
    essay_type = input("Enter the type of essay (e.g., argumentative, descriptive, narrative): ").strip()
    lengths = ["300 words", "900 words", "1200 words", "2000 words"]
    print("\nSelect the desired length of the essay:")
    for i, length in enumerate(lengths, start=1):
        print(f"{i}. {length}")
    try:
        idx = int(input("> ").strip())
        length = lengths[idx - 1] if 1 <= idx <= len(lengths) else lengths[0]
    except ValueError:
        length = lengths[0]
    target_audience = input("Enter the target audience for your essay: ").strip()
    return {"topic": topic, "essay_type": essay_type, "length": length, "target_audience": target_audience}
def generate_essay_content(details):
    try:
        temp = float(input("Enter the temperature for the essay generation (0.0 to 1.0, default is 0.7): ").strip())
        if not (0.0 <= temp <= 1.0):
            raise ValueError
    except ValueError:
        print("Invalid input. Using default temperature of 0.3.")
        temp = 0.3
    intro_p = f"Write an introduction for an {details['essay_type']} essay on the topic '{details['topic']}' for a {details['target_audience']} audience in {details['length']}."
    intro = generate_response(intro_p, temperature=temp, max_tokens=1024)
    print("\nGenerated Introduction:\n")
    print(intro)
    print("\nWould you like the body writeen as a full draft or in sections? (Enter 'full' or 'sections')")
    choice = input("> ").strip().lower()
    if choice == 'full':
        body_p = f"Write the full body of an {details['essay_type']} essay on the topic '{details['topic']}' for a {details['target_audience']} audience in {details['length']}."
        body = generate_response(body_p, temperature=temp, max_tokens=1024)
        print("\nGenerated Body:\n")
        print(body)
    elif choice == 'sections':
        step_p = f"Write step-by-step sections for an {details['essay_type']} essay on the topic '{details['topic']}' for a {details['target_audience']} audience in {details['length']}."
        body_step = generate_response(step_p, temperature=temp, max_tokens=1024)
        print("\nGenerated Body Sections:\n")
        print(body_step)

    concl_p = f"Write a conclusion for an {details['essay_type']} essay on the topic '{details['topic']}' for a {details['target_audience']} audience in {details['length']}."
    concl = generate_response(concl_p, temperature=temp, max_tokens=1024)
    print("\nGenerated Conclusion:\n")
    print(concl)
def feedback_and_refinement():
    print("\nWould you like to provide feedback for refinement? (yes/no)")
    feedback_choice = input("> ").strip().lower()
    if feedback_choice == 'yes':
        try:
            rating = int(input("Please rate the essay on a scale of 1 to 5: ").strip())
            if not (1 <= rating <= 5):
                raise ValueError("Invalid rating. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid rating. Using 3.")
            rating = 3
        if rating != 5:
            feedback = input("Please provide your feedback: ").strip()
            print("\nRefining the essay based on your feedback...\n")
            refined_essay = generate_response(f"Refine the essay based on the following feedback: {feedback}", temperature=0.3, max_tokens=1024)
            print("\nRefined Essay:\n")
            print(refined_essay)
        else:
            print("Thank you for your feedback! No refinement needed.")
def run_activity():
    print("Welcome to the AI Writing Assistant!")
    details = get_essay_details()
    if not details['topic'] or not details['essay_type'] or not details['target_audience']:
        print("Error: All fields are required. Please try again.")
        return
    generate_essay_content(details)
    feedback_and_refinement()
if __name__ == "__main__":
    run_activity()
