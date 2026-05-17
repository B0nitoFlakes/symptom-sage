import os
try:
    from backend.retrieval import retrieve, format_results
except ImportError:
    from retrieval import retrieve, format_results
from sentence_transformers import CrossEncoder
from huggingface_hub import login

login(token=os.getenv("HF_TOKEN"))

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, results: list, top_k: int=3):
    pairs = [[query, result["possible_condition"] + " " + result["symptom"]] for result in results]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(scores, results),
        key=lambda x: x[0],
        reverse=True
    )

    return [result for score, result in ranked[:top_k]]

if __name__ == "__main__":
    query = "its so painful to swallow anything my throat feels like sandpaper"
    print(f"Query: {query}\n")
    
    results = retrieve(query, top_k=5)
    formatted = format_results(results)
    
    print("Before reranking:")
    for r in formatted:
        print(f"  {r['score']} - {r['possible_condition']}")
    
    reranked = rerank(query, formatted, top_k=3)
    
    print("\nAfter reranking:")
    for r in reranked:
        print(f"  {r['possible_condition']} ({r['symptom']}) - {r['source']}")