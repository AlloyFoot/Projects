from hf import generate_response
# from groq import generate_response

import io
import streamlit as st

CSS = """
<style>
.history-wrap {
    max-height: 400px; 
    overflow-y: auto; 
    padding-right: 6px;
}
.qa-card {
    border: 1px solid #dcdcdc;
    background: #fdfdfd;
    border-radius: 8px;
    padding: 15px;
    margin: 12px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.difficulty-badge {
    display: inline-block;
    padding: 3px 8px;
    font-size: 0.7rem;
    font-weight: 700;
    border-radius: 5px;
    background-color: #e3f2fd;
    color: #0d47a1;
    margin-bottom: 8px;
    text-transform: uppercase;
}
.q {
    font-weight: 700; 
    color: #1e3a8a; 
    margin-bottom: 8px;
}
.a {
    white-space: pre-wrap; 
    color: #2d3748; 
    line-height: 1.6;
}
</style>
"""

def export_bytes(history):
    text = "".join([f"Difficulty: {h['difficulty']}\nProblem: {h['question']}\nSolution:\n{h['answer']}\n\n" for h in history])
    return io.BytesIO(text.encode("utf-8"))

def setup_ui():
    st.set_page_config(page_title="Math Mastermind", layout="centered")
    st.title("🧮 Math Mastermind")
    st.write("Submit any math problem to receive an explicit, step-by-step solution.")
    
    st.session_state.setdefault("history", [])

    difficulty = st.select_slider(
        "Select Problem Difficulty Level:",
        options=["Easy", "Medium", "Hard"]
    )

    col_clear, col_export = st.columns([1, 1])
    with col_clear:
        if st.button("🧹 Clear Session", use_container_width=True):
            st.session_state.history = []
            st.rerun()
            
    with col_export:
        if st.session_state.history:
            st.download_button(
                label="📤 Export Session Logs",
                data=export_bytes(st.session_state.history),
                file_name="math_mastermind_session.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.button("📤 Export Session Logs", disabled=True, use_container_width=True)

    st.write("---")

    user_input = st.text_area("Enter your math problem here:", placeholder="e.g., Solve for x: 3x + 7 = 22 or Find the derivative of f(x) = sin(x)*e^x")
    
    if st.button("Generate Step-by-Step Solution", use_container_width=True):
        q = user_input.strip()
        if q:
            modified_prompt = (
                f"You are Math Mastermind, an expert mathematics tutor. "
                f"Provide a clear, detailed, step-by-step mathematical solution suited for a {difficulty} level context "
                f"for the following problem: {q}"
            )
            
            try:
                with st.spinner("Calculating solution and structural breakdown..."):
                    a = generate_response(modified_prompt)
                
                st.session_state.history.append({
                    "difficulty": difficulty,
                    "question": q,
                    "answer": a
                })
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ An error occurred while communicating with the API: {e}")
        else:
            st.warning("⚠️ Please enter a math problem before requesting a solution.")

    st.markdown("### Solved Problems History")
    st.markdown(CSS, unsafe_allow_html=True)

    if st.session_state.history:
        cards = []
        for h in st.session_state.history:
            cards.append(
                f'<div class="qa-card">'
                f'<div class="difficulty-badge">📊 Level: {h["difficulty"]}</div>'
                f'<div class="q"><b>Problem:</b> {h["question"]}</div>'
                f'<div class="a"><b>Step-by-Step Solution:</b>\n{h["answer"]}</div>'
                f'</div>'
            )
        st.markdown('<div class="history-wrap">' + "".join(cards) + "</div>", unsafe_allow_html=True)
    else:
        st.info("No problems solved in this session yet. Input a math problem above to begin!")

def main():
    setup_ui()

if __name__ == "__main__":
    main()