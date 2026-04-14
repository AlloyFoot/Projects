import requests
import html
import random

EDUCATION_CATEGORY_ID = 9
URL = f"https://opentdb.com/api.php?amount=10&category={EDUCATION_CATEGORY_ID}&type=multiple"

def load_questions():
    response = requests.get(URL)
    data = response.json()
    
    if data["response_code"] == 0 and data["results"]:
        return data["results"]
    return None
    
def run_quiz():
    questions = load_questions()
    if not questions:
        print("Failed to fetch educational questions.")
        return
    score = 0

    print("Welcome to the educational quiz!")

    for i, q in enumerate(questions, start=1):
        a = html.unescape(q['question'])
        b = html.unescape(q['correct_answer'])
        c = [html.unescape(ans) for ans in q['incorrect_answers']]  
        
        print(f"\nQuestion {i}: {a}")

        options = c + [b]  
        random.shuffle(options)  

        for idx, choice in enumerate(options, start=1):
            print(f"{idx}. {choice}")

        try:
            user_choice = int(input("Your Answer: "))
            selected = options[user_choice - 1]
        except:
            print("Invalid Input")
            continue

        if selected == b:
            print("correct!")
            score += 1
        else:
            print(f"incorrect. the correct answer was {b}")
    
    print(f"Final Score: {score}/{len(questions)}")
    print(f"Percent: {(score/len(questions))*100:.1f}%")

if __name__ == "__main__":
    run_quiz()
