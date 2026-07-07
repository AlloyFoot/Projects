# main.py
# Switch provider by changing the import line:
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
    border: 1px solid #e6e6e6;
    background: #ffffff;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 10px 0;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.q {
    font-weight: 700; 
    color: #2b2b2b; 
    margin-bottom: 8px;
}
.a {
    white-space: pre-wrap; 
    color: #333333; 
    line-height: 1.5;
}
</style>
"""

def export_bytes(history):
    text = "".join([f"Q: {h['question']}\nA: {h['answer']}\n\n" for h in history])
    return io.BytesIO(text.encode("utf-8"))

def setup_ui():
    st.set_page_config(page_title="AI Powered Assistant", layout="centered")
    st.title("AI Powered Assistant")
    
    st.session_state.setdefault("history", [])

    col_clear, col_export = st.columns([1, 1])
    
    with col_clear:
        if st.button("Clear the conversation", use_container_width=True):
            st.session_state.history = []
            st.rerun()
            
    with col_export:
        if st.session_state.history:
            st.download_button(
                label="Export the chat history",
                data=export_bytes(st.session_state.history),
                file_name="chat_history.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.button("Export the chat history", disabled=True, use_container_width=True)

    st.write("---")

    user_input = st.text_input("Enter your message:", placeholder="Type something here...")
    
    if st.button("Ask a question"):
        q = user_input.strip()
        if q:
            with st.spinner("Generating response..."):
                a = generate_response(q)
            
            st.session_state.history.append({"question": q, "answer": a})
            st.rerun()
        else:
            st.warning("Please enter a question before clicking 'Ask a question'.")

    st.markdown("### Chat History")
    st.markdown(CSS, unsafe_allow_html=True)

    if st.session_state.history:
        cards = []
        for h in st.session_state.history:
            cards.append(
                f'<div class="qa-card">'
                f'<div class="q"><b>You:</b> {h["question"]}</div>'
                f'<div class="a"><b>AI:</b> {h["answer"]}</div>'
                f'</div>'
            )
        st.markdown('<div class="history-wrap">' + "".join(cards) + "</div>", unsafe_allow_html=True)
    else:
        st.info("No conversation history yet. Ask a question above to get started!")

def main():
    setup_ui()

if __name__ == "__main__":
    main()