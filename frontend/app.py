import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from backend.retrieval import retrieve, format_results
from backend.reranker import rerank

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Symptom Sage",
    page_icon="🌿",
    layout="centered"
)

st.title("Symptom Sage")
st.subheader("A medical symptom checker powered by RAG")
st.markdown("---")

def generate_answer(question: str, contexts:list) -> str:
    context_text = "\n\n".join([
        f"Condition: {r['possible_condition']}, Symptom: {r['symptom']}, Advice: {r.get('advice', '')}, When to See Doctor: {r.get('when_to_see_doctor', '')}"
        for r in contexts
    ])

    prompt = f"""
You are a helpful medical assistant.

Based on the context below, directly address the user's symptoms and provide helpful guidance.
Only use information from the provided context.
Do not provide a medical diagnosis.
If information is insufficient, recommend consulting a healthcare professional.

Context:
{context_text}

Question: {question}

Provide a clear, specific answer that directly addresses the symptoms mentioned.
Answer:
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content": prompt}]
    )
    return response.choices[0].message.content

query = st.text_area(
    "Describe your symptoms",
    placeholder="e.g. I have a terrible headache and feel nauseous...",
    height=100
)

if st.button("Check Symptoms", type="primary"):
    if not query:
        st.warning("Please describe your symptoms first!")
    else:
        with st.spinner("Analysing your symptoms..."):
            results = retrieve(query, top_k=5)
            formatted = format_results(results)
            reranked = rerank(query, formatted, top_k=3)
            answer = generate_answer(query, reranked)
        
        st.markdown("### Assessment")
        st.write(answer)
        st.markdown("---")

        st.markdown("### Posible Conditions")
        for r in reranked:
            with st.expander(f"**{r['possible_condition']}** — {r['symptom']}"):
                st.write(f"**Advice:** {r.get('advice', 'N/A')}")
                st.write(f"**When to see a doctor:** {r.get('when_to_see_doctor', 'N/A')}")
                st.write(f"**Source:** [{r['source']}]({r['url']})")

        st.markdown("---")
        st.caption("⚠️ This tool is not a substitute for professional medical advice. Always consult a doctor if symptoms persist or worsen.")