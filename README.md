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
│   ├── webmd_scrapers.py
│   ├── combine_data.py
│   ├── clean_data.py
│   └── generate_data.py
├── backend/
│   ├── __init__.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retrieval.py
│   └── reranker.py
├── frontend/
│   └── app.py
├── tests/
│   ├── __init__.py
│   ├── test_ragas.py
│   └── test_deepeval.py
├── .env.example
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

## Setup

### Prerequisites
- Python 3.11
- Docker Desktop
- OpenAI API key
- HuggingFace account and token (for CrossEncoder model download)

### Environment Variables
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your-openai-api-key
HF_TOKEN=your-huggingface-token
```

### Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/B0nitoFlakes/symptom-sage.git
cd symptom-sage

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 4. Create .env file with your API keys

# 5. Start Qdrant
docker run -p 6333:6333 --name qdrant-sage qdrant/qdrant

# 6. Store embeddings in Qdrant
python backend/embeddings.py

# 7. Run the app
streamlit run frontend/app.py
```

Open `http://localhost:8501` in your browser.

### Docker Setup

```bash
# 1. Clone the repository
git clone https://github.com/B0nitoFlakes/symptom-sage.git
cd symptom-sage

# 2. Create .env file with your API keys

# 3. Build and start all services
docker-compose up --build

# 4. In a new terminal, store embeddings in Qdrant
docker-compose exec app python backend/embeddings.py
```

Open `http://localhost:8501` in your browser.

> **Note:** Step 4 is required every time you start fresh Docker containers unless you use a persistent Qdrant volume.

## Data Sources
- [NHS](https://www.nhs.uk)
- [WebMD](https://www.webmd.com)

## Evaluation

### RAGAS
Measures RAG pipeline quality across 20 test questions covering multi-symptom combinations, severity levels, and single symptom baselines.
- **Faithfulness: 0.74** — measures if answers are grounded in retrieved context
- **Answer Relevancy: 0.49** — measures if answers are relevant to the question

### DeepEval
Measures safety-critical metrics across 20 test questions using `gpt-4o-mini`.
- **Hallucination Pass Rate: 55%** — detects if answers contain information not supported by retrieved context
- **Answer Relevancy Pass Rate: 100%** — measures if answers directly address the user's symptoms

### Evaluation Limitations
- DeepEval hallucination failures are primarily due to GPT selecting the most relevant condition from multiple retrieved contexts rather than addressing all contexts — this is expected RAG behavior, not true hallucination
- ContextPrecision ground truth evaluation excluded as the project does not have access to verified medical expert annotations

## Known Limitations
- Knowledge base covers only 8 common symptoms from 2 sources (NHS, WebMD)
- Severity-aware retrieval not implemented — system retrieves same chunks regardless of symptom severity. The `when_to_see_doctor` field could be used in future to derive severity labels and filter retrieval accordingly
- Synthetic data generation via GPT may introduce subtle inaccuracies — all source content originates from NHS and WebMD
- Similar conditions from different sources (NHS and WebMD) may appear as duplicate results in the UI

## Future Improvements
- Expand knowledge base to cover more symptoms and sources
- Add severity classification at retrieval stage using `when_to_see_doctor` field
- Support follow-up questions for multi-turn conversations
- Replace Streamlit UI with HTML/CSS/JS + FastAPI for a more production-grade interface with separate Dockerfiles per service
- Integration with autonomous code review agent as semantic cache layer

## Disclaimer
This tool is not a substitute for professional medical advice. Always consult a doctor if symptoms persist or worsen.