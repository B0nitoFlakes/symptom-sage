import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from ragas import evaluate
from ragas.llms import llm_factory
from ragas.metrics.collections import Faithfulness, AnswerRelevancy, ContextPrecision
from datasets import Dataset

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.retrieval import retrieve, format_results
from backend.reranker import rerank

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
llm = llm_factory("gpt-4o-mini", client=openai_client)

test_questions = [
    "I have a terrible headache and feel nauseous",
    "I feel very hot and my body temperature is high",
    "my stomach hurts and I keep vomiting",
    "everytime I stand up I feel like I'm going to pass out",
    "my throat is painful and scratchy when I swallow"
]

def generate_answer(question: str, contexts: list) -> str:
    context_text = "\n\n".join([
        f"Condition: {r['possible_condition']}\nAdvice: {r.get('advice', 'See a doctor')}"
        for r in contexts
    ])
    
    prompt = f"""Based on the following medical information, answer the question.
    
Context:
{context_text}

Question: {question}

Provide a helpful, grounded answer based only on the context above."""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def build_dataset():
    questions = []
    answers = []
    contexts_list = []
    
    for question in test_questions:
        print(f"Processing: {question[:50]}...")
        
        results = retrieve(question, top_k=5)
        formatted = format_results(results)
        reranked = rerank(question, formatted, top_k=3)
        
        context_texts = [
            f"Condition: {r['possible_condition']}, Symptom: {r['symptom']}"
            for r in reranked
        ]
        
        answer = generate_answer(question, reranked)
        
        questions.append(question)
        answers.append(answer)
        contexts_list.append(context_texts)
    
    return Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts_list
    })

if __name__ == "__main__":
    print("Building evaluation dataset...")
    dataset = build_dataset()
    
    print("\nRunning RAGAS evaluation...")
    results = evaluate(
        dataset,
        metrics=[
            Faithfulness(llm=llm),
            AnswerRelevancy(llm=llm),
            ContextPrecision(llm=llm)
        ]
    )
    
    print("\nRAGAS Evaluation Results:")
    print(results)