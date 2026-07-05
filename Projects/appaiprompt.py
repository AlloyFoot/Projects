from groq import generate_response
import re
import streamlit as st
def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) < 10:
        return True
    t = text.strip()
    if t.endswith(("**", "*", "-", "_", "(", "[", "{", ":", ";", ",")):
        return True
    if re.search(r"\d+\.\s*\*\*$", t):
        return True
    if re.search(r"[.!?]\s*$", t):
        return True
    return False
def complete_answer(question: str, max_rounds: int = 2) -> str:
    base_prompt = (
        "Answer clearly in numbered points. "
        "Do not cut sentences. Finish each point fully."
        f"Question: {question}"
    )
    ans = generate_response(base_prompt, temperature=0.3, max_tokens=1024)
    rounds = 0
    while rounds < max_rounds and looks_incomplete(ans):
        cont_prompt = (
            "Continue EXACTLY from where you left off. "
            "Do NOT repeat any previous content. "
            "Finish the incomplete point and complete the answer. "
            f"Question: {question} "
            f"Previous answer: {ans}"
        )
        more = generate_response(cont_prompt, temperature=0.3, max_tokens=1024)
        if not more or more.strip() in ans:
            break
        ans = (ans.rstrip() + " " + more.lstrip()).strip()
        rounds += 1
    return ans
def main():
    st.title("AI Writing Assistant")
    st.write("Welcome to the AI Writing Assistant! Please provide the details for your essay.")
    user_input = st.text_input("Enter your question here:")
    if user_input:
        st.write(f"**Your Question:** {user_input}")
        answer = complete_answer(user_input)
        st.write(f"**AI Response:** {answer}")
        st.markdown(answer)
    else:
        st.info("Please enter a question to get started.")
if __name__ == "__main__":
    main()