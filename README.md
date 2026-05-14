# Symptom Sage

A medical symptom checker powered by Retrieval-Augmented Generation (RAG). Users input their symptoms and the system retrieves relevant information from trusted medical sources (NHS and WebMD) to provide possible conditions, advice, and cited sources.

## Features
- Symptom-based medical information retrieval
- Answers grounded in trusted sources (NHS, WebMD)
- Every answer includes source citations
- Covers 8 common symptoms: headache, fever, cough, fatigue, nausea, stomach pain, sore throat, dizziness
- Simple and clean Streamlit UI

## Project Structure
```
symptom-sage/
├── data/
├── scrapers/
├── requirements.txt
└── README.md
```

## Data Sources
- [NHS](https://www.nhs.uk)
- [WebMD](https://www.webmd.com)

## Disclaimer
This tool is not a substitute for professional medical advice. Always consult a doctor if symptoms persist or worsen.