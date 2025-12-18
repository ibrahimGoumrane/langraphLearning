# AI Technical Recruiter - LangChain Pipeline

## Project Overview

This project is an **AI-powered technical recruiter** that evaluates candidates against job descriptions in an **evidence-based and explainable way**. It leverages **LangChain** to create a structured pipeline for candidate assessment using CVs and job descriptions, without relying on external knowledge.

The system is designed to produce **auditable, structured outputs** for each candidate, including skill matching, experience evaluation, and overall suitability scoring.

---

## Key Features

- **Document Ingestion**: Parse and chunk CVs and job descriptions.
- **Retrieval-Augmented Evaluation (RAG)**: Retrieve only relevant chunks from CVs and job descriptions to ground LLM reasoning.
- **Skill & Experience Evaluation**: Score candidate skills and experience against job requirements.
- **Evidence-Based Scoring**: All outputs reference specific CV or job description sections.
- **Structured JSON Output**: Provides a clear, machine-readable summary of evaluation results.

---

## Pipeline Overview

1. **Data Preparation**

   - CVs and job descriptions are ingested and chunked.
   - Text embeddings are created and stored in a vector database (FAISS/Chroma).

2. **Retrieval**

   - Relevant CV chunks are retrieved for each job requirement.
   - Retrieval ensures the LLM sees only task-specific evidence.

3. **Evaluation Chains**

   - Skill evaluation chain scores each skill requirement.
   - Experience evaluation chain assesses years and relevance.
   - Optional red-flag detection identifies gaps or inconsistencies.

4. **Scoring & Decision**

   - Aggregates scores from all evaluation chains.
   - Produces a final structured JSON output per candidate.

5. **Output**
   - JSON includes scores, evidence, and overall decision (Pass/Review/Reject).
   - Designed for explainability and auditability.

---

## Tech Stack

- **Python**
- **LangChain**
- **FAISS / Chroma** (vector store)
- **OpenAI API / other LLMs**
- **Pydantic** (for structured outputs)

---

## Notes

- The project focuses on **task-specific RAG** over candidate CVs and job descriptions, not general knowledge retrieval.
- Designed to be **pipeline-first**, using LangChain only; upgrade to LangGraph is optional for complex workflows later.
- Aims to create **deterministic, traceable, and auditable AI evaluation results**.
