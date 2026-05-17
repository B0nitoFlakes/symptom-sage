# Symptom Sage

A medical symptom checker powered by Retrieval-Augmented Generation (RAG). Users input their symptoms and the system retrieves relevant information from trusted medical sources (NHS and WebMD) to provide possible conditions, advice, and cited sources.

## Features
- Symptom-based medical information retrieval
- Answers grounded in trusted sources (NHS, WebMD)
- Every answer includes source citations
- Covers 8 common symptoms: headache, fever, cough, fatigue, nausea, stomach pain, sore throat, dizziness
- Reranking using CrossEncoder for more accurate results
- Evaluated using RAGAS and DeepEval for RAG quality and hallucination detection
- Simple and clean Streamlit UI

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| OpenAI GPT-4o-mini | Answer generation and data generation |
| OpenAI text-embedding-3-small | Embedding chunks and queries |
| Qdrant | Vector store for storing and retrieving embeddings |
| Sentence Transformers CrossEncoder | Reranking retrieved results |
| RAGAS | RAG evaluation (faithfulness, answer relevancy) |
| DeepEval | Safety evaluation (hallucination, answer relevancy) |
| Streamlit | Frontend UI |
| Docker | Containerization |

## Project Structure
```
symptom-sage/
├── data/
├── scrapers/
│   ├── nhs_scrapers.py
│   ├── mayo_scrapers.py
│   ├── combine_data.py
│   ├── clean_data.py
│   └── generate_data.py
├── backend/
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retrieval.py
│   └── reranker.py
├── frontend/
│   └── app.py
├── tests/
│   ├── test_ragas.py
│   └── test_deepeval.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Pipeline
1. **Data Collection** — scrape NHS and WebMD for 8 common symptoms
2. **Data Generation** — use GPT to generate structured condition/advice pairs (synthetic data generation)
3. **Chunking** — structure data into consistent chunks with metadata (symptom, condition, advice, when to see doctor, source, url)
4. **Embedding** — embed chunks using `text-embedding-3-small`
5. **Vector Store** — store embeddings in Qdrant
6. **Retrieval** — embed user query and search Qdrant for top-k similar chunks using cosine similarity
7. **Reranking** — rerank results using CrossEncoder for better precision
8. **Evaluation** — evaluate pipeline using RAGAS and DeepEval

## Data Sources
- [NHS](https://www.nhs.uk)
- [WebMD](https://www.webmd.com)

## Evaluation

### RAGAS
Measures RAG pipeline quality across 20 test questions covering multi-symptom combinations, informal language, severity levels, and single symptom baselines.
- **Faithfulness** — measures if answers are grounded in retrieved context
- **Answer Relevancy** — measures if answers are relevant to the question

### DeepEval
Measures safety-critical metrics across 20 test questions using `gpt-4o-mini`.
- **Hallucination** — detects if answers contain information not supported by retrieved context
- **Answer Relevancy** — measures if answers directly address the user's symptoms

### Evaluation Limitations
- RAGAS answer relevancy scores are affected by informal language test questions — RAGAS penalizes semantic mismatch between casual queries and clinical answers
- DeepEval hallucination failures are primarily due to GPT selecting the most relevant condition from multiple retrieved contexts rather than addressing all contexts — this is expected RAG behavior, not true hallucination
- ContextPrecision ground truth evaluation excluded as the project does not have access to verified medical expert annotations

## Known Limitations
- Knowledge base covers only 8 common symptoms from 2 sources (NHS, WebMD)
- Severity-aware retrieval not implemented — system retrieves same chunks regardless of symptom severity. The `when_to_see_doctor` field could be used in future to derive severity labels and filter retrieval accordingly
- Synthetic data generation via GPT may introduce subtle inaccuracies — all source content originates from NHS and WebMD

## Future Improvements
- Expand knowledge base to cover more symptoms and sources
- Add severity classification at retrieval stage using `when_to_see_doctor` field
- Support follow-up questions for multi-turn conversations
- Replace Streamlit UI with HTML/CSS/JS + FastAPI for a more production-grade interface
- Integration with autonomous code review agent as semantic cache layer

## Disclaimer
This tool is not a substitute for professional medical advice. Always consult a doctor if symptoms persist or worsen.