import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
from openai import OpenAI
from deepeval import evaluate
from deepeval.metrics import HallucinationMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from backend.retrieval import retrieve, format_results
from backend.reranker import rerank

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

test_questions = [
    # Multi-symptom combinations
    "I am experiencing a severe headache accompanied by nausea",
    "I have been experiencing abdominal pain and vomiting since last night",
    "I have a sore throat with fever and generalized body aches",
    "I am experiencing dizziness and a throbbing headache",
    "I have been feeling fatigued constantly even after sleeping",
    "I am experiencing chest tightness with persistent coughing",
    "I have stomach cramps with diarrhea and general weakness",
    "I have a headache behind my eyes with nasal congestion",

    # Moderate informal
    "my head is really hurting and I feel like throwing up",
    "my throat is very painful and I am having difficulty swallowing",
    "I feel dizzy every time I stand up",
    "I have been coughing continuously for several days",

    # Severity based
    "I have a mild headache that is slightly uncomfortable",
    "I have a moderate fever and am feeling generally unwell",
    "I am experiencing severe unbearable abdominal pain",

    # Single symptom baseline
    "I have a headache",
    "I am experiencing nausea",
    "I have a sore throat",
    "I feel dizzy",
    "I am experiencing fatigue"
]

def get_answer(question: str) -> tuple:
    results = retrieve(question, top_k=5)
    formatted = format_results(results)
    reranked = rerank(question, formatted, top_k=3)
    context_texts = [
        f"Condition: {r['possible_condition']}, Symptom: {r['symptom']}, Advice: {r.get('advice', '')}, When to See Doctor: {r.get('when_to_see_doctor', '')}"
        for r in reranked
    ]
    context_text = "\n\n".join(context_texts)
    prompt = f"""
You are a helpful medical assistant.
Only use the provided context. Do not provide a medical diagnosis.
If information is insufficient, recommend consulting a healthcare professional.

Context:
{context_text}

Question: {question}
Answer:
"""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    return answer, context_texts

if __name__ == "__main__":
    print("Building test cases...")
    test_cases = []
    for question in test_questions:
        print(f"Processing: {question[:50]}...")
        answer, contexts = get_answer(question)
        test_cases.append(LLMTestCase(
            input=question,
            actual_output=answer,
            context=contexts
        ))

    print("\nRunning DeepEval evaluation...")
    evaluate(
        test_cases=test_cases,
        metrics=[
            HallucinationMetric(threshold=0.5, model="gpt-4o-mini"),
            AnswerRelevancyMetric(threshold=0.5, model="gpt-4o-mini")
        ]
    )