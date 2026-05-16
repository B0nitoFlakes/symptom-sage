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
- Python
- OpenAI API (`text-embedding-3-small`)
- Qdrant (vector store)
- LangChain
- Sentence Transformers (CrossEncoder reranker)
- RAGAS + DeepEval (evaluation)
- Streamlit (UI)
- Docker

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
2. **Data Generation** — use GPT to generate structured condition/advice pairs
3. **Chunking** — structure data into consistent chunks
4. **Embedding** — embed chunks using `text-embedding-3-small`
5. **Vector Store** — store embeddings in Qdrant
6. **Retrieval** — embed user query and search Qdrant for top-k similar chunks
7. **Reranking** — rerank results using CrossEncoder for better precision
8. **Evaluation** — evaluate pipeline using RAGAS and DeepEval

## Data Sources
- [NHS](https://www.nhs.uk)
- [WebMD](https://www.webmd.com)

## Evaluation
- **RAGAS** — measures faithfulness, answer relevancy, and context precision
- **DeepEval** — measures hallucination detection, critical for medical content

## Future Improvements
- Expand knowledge base to cover more symptoms
- Add severity classification (mild / serious / see a doctor)
- Support follow-up questions for multi-turn conversations
- Integration with autonomous code review agent as semantic cache layer

## Disclaimer
This tool is not a substitute for professional medical advice. Always consult a doctor if symptoms persist or worsen.