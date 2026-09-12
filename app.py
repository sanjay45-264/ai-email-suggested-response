import json
import streamlit as st
from src.generator import generate_reply
from src.evaluator import evaluate

st.set_page_config(page_title="AI Email Suggested Response", page_icon="✉️")
st.title("✉️ AI Email Suggested Response System")
st.caption("RAG-grounded generation with multi-dimensional response evaluation.")

email=st.text_area("Incoming email",height=180,placeholder="Paste an incoming email here...")

if st.button("Generate suggested reply",type="primary") and email.strip():
    reply,mode=generate_reply(email)
    st.subheader("Suggested response")
    st.write(reply)
    st.caption(f"Generation mode: {mode}")
    st.info("For a real evaluation score, compare this response with the reply that was actually sent.")

with st.expander("Evaluate a generated response"):
    incoming=st.text_area("Incoming email",key="eval_in")
    reference=st.text_area("Actual/reference reply",key="eval_ref")
    generated=st.text_area("Generated reply",key="eval_gen")
    if st.button("Evaluate"):
        if incoming and reference and generated:
            r=evaluate(incoming,reference,generated)
            st.metric("Overall quality",f"{r['overall_score']}/100")
            st.json(r)
        else:
            st.warning("Fill in all three fields.")
