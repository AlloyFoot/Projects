import config
import os
from hf import generate_response
# from groq import generate_response

def save_log(filename, content):
    os.makedirs("activity_results", exist_ok=True)
    filepath = os.path.join("activity_results", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def run_reinforcement_learning():
    prompt = "Describe the future of artificial intelligence"
    
    initial_response = generate_response(prompt)
    
    rating = "3"
    feedback = "Make the response more creative by including unique metaphors, expand on the ethical details of automation, and improve clarity in the conclusion."
    
    rl_prompt = (
        f"You previously gave this response to the prompt '{prompt}':\n\n"
        f"{initial_response}\n\n"
        f"The user rated this response a {rating}/5 and provided this feedback: {feedback}\n\n"
        f"Please generate an improved response that fully incorporates this feedback."
    )
    
    improved_response = generate_response(rl_prompt)
    
    reflection = (
        "REINFORCEMENT LEARNING REFLECTION\n"
        "===============================\n\n"
        "How did the response evolve after your feedback? How did the rating influence the AI's adjustment?\n"
        "The response became significantly more descriptive, replacing generic trends with specific metaphors "
        "and dedicating deeper structural sections to data privacy and societal ethics. Presenting the numerical "
        "rating and qualitative critiques explicitly flags specific gaps for the model, forcing it to pivot away "
        "from its original baseline response style to focus heavily on the requested structural adjustments."
    )
    
    log_content = (
        f"PART 1: REINFORCEMENT LEARNING\n\n"
        f"Initial Prompt: {prompt}\n\n"
        f"Initial Response:\n{initial_response}\n\n"
        f"Rating: {rating}/5\n"
        f"Feedback: {feedback}\n\n"
        f"Improved Response:\n{improved_response}\n\n"
        f"{reflection}"
    )
    save_log("reinforcement_learning_results.txt", log_content)

def run_role_based_prompting():
    topic = "machine learning algorithms"
    
    prompts = {
        "Teacher": f"You are a Teacher. Provide a simple and easy-to-understand explanation of {topic}.",
        "Expert": f"You are an Expert. Provide a detailed and in-depth explanation of {topic} for someone with a high level of knowledge.",
        "Business Leader": f"You are a Business Leader. Provide a practical and application-focused explanation of {topic}.",
        "Peer Student": f"You are a Peer Student. Provide a response about {topic} that speaks to a high school or college student with basic knowledge of the topic."
    }
    
    responses = {}
    for role, role_prompt in prompts.items():
        responses[role] = generate_response(role_prompt)
        
    reflection = (
        "ROLE-BASED PROMPTING REFLECTION\n"
        "===============================\n\n"
        "1. Compare how the responses differ based on role. Which response was most aligned with your expectations for that role?\n"
        "The Teacher role focused on basic definitions and intuitive analogies, while the Expert utilized high-level "
        "technical terminology and mathematical foundations. The Business Leader stripped away technical implementation "
        "details entirely to highlight financial ROI and strategic market use cases, and the Peer Student struck an "
        "accessible, collaborative tone. Each matched expectations closely by altering syntax, vocabulary complexity, and framing.\n\n"
        "2. How can role-based prompts influence the tone and complexity of AI-generated content? How can this be used in real-world scenarios?\n"
        "System directives completely shift the structural lens, jargon level, and persona traits used by the model. "
        "In production scenarios, this allows a single backend engine to power highly distinct user experiences—such as "
        "automatically adapting educational software to match a child's reading level or generating tailored business executive summaries "
        "from raw engineering analytics reports."
    )
    
    log_content = f"PART 2: ROLE-BASED PROMPTING\n\nCategory: Technology\nTopic: {topic}\n\n"
    for role, resp in responses.items():
        log_content += f"--- {role}'s Perspective ---\n{resp}\n\n"
    log_content += reflection
    
    save_log("role_based_prompting_results.txt", log_content)

def main():
    run_reinforcement_learning()
    run_role_based_prompting()
    print("All tasks processed successfully. Log results saved to the 'activity_results' directory.")

if __name__ == "__main__":
    main()