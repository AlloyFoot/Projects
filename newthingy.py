import streamlit as st
import random

st.set_page_config(
    page_title="Math Mastermind",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Math Mastermind")
st.caption("Your friendly AI math coach for practice, hints, and step-by-step learning.")

st.markdown("""
<style>
.box {
    padding: 1rem;
    border-radius: 12px;
    background: linear-gradient(135deg, #e0f7fa, #f1f8e9);
    border: 2px solid #7e57c2;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

def generate_response(problem, difficulty):
    system_prompt = """
    You are a Math Wizard built by Ved, trained to help students master math.
    Explain solutions clearly, step by step, in a friendly and encouraging way.
    Adapt your explanation based on the student's difficulty level:
    - Beginner: simple and very guided
    - Regular: balanced explanation
    - Challenging: concise but deeper reasoning
    """

    if difficulty == "Beginner":
        return f"""
Let's solve this step by step:

Problem: {problem}

1. First, identify what the question is asking.
2. Write down the important numbers or expressions.
3. Apply the correct math rule or formula.
4. Simplify carefully.
5. Check the final answer.

Final thought: Try solving it slowly and verify each step.
"""
    elif difficulty == "Regular":
        return f"""
Here is a clear solution approach for:

{problem}

- Identify the math concept involved.
- Set up the equation or expression properly.
- Solve step by step.
- Simplify your answer.
- Double-check for mistakes.

This level gives a balanced explanation without too much hand-holding.
"""
    else:
        return f"""
Challenge mode solution for:

{problem}

- Determine the core concept quickly.
- Use the most efficient method.
- Show the logic behind each transformation.
- Verify whether the result is mathematically valid.

This version focuses on deeper reasoning and efficiency.
"""

st.sidebar.title("Options")
difficulty = st.sidebar.selectbox(
    "Choose difficulty",
    ["Beginner", "Regular", "Challenging"]
)

st.markdown('<div class="box">Enter a math problem below and get a guided solution.</div>', unsafe_allow_html=True)

problem = st.text_area("Type your math problem here")

with st.expander("🧩 Example Problems I Can Solve"):
    st.write("1. Solve: 3x + 5 = 20")
    st.write("2. Find the area of a triangle with base 8 and height 5")
    st.write("3. What is the probability of rolling a 4 on a fair die?")
    st.write("4. Solve: x² - 9 = 0")
    st.write("5. A rectangle has length 10 and width 4. Find its perimeter.")

if st.button("Solve Problem"):
    if problem.strip():
        response = generate_response(problem, difficulty)
        st.markdown('<div class="box"><b>Solution:</b><br><br>' + response.replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a math problem first.")

st.markdown('<div class="box">Tip: Test this app with algebra, geometry, and probability problems.</div>', unsafe_allow_html=True)
