# AI Technical Recruiter - Structured Evaluation Pipeline

## Project Overview

This project is an **AI-powered technical recruiter** that evaluates candidates against job descriptions using **structured LLM extraction and semantic similarity analysis**. It creates an auditable pipeline for candidate assessment that produces evidence-based, explainable results without relying on external knowledge.

The system extracts structured information from CVs and job descriptions, computes semantic similarity between relevant sections, and generates comprehensive evaluation reports with LLM-powered explanations.

---

## Key Features

- **Document Ingestion**: Load CVs and job descriptions from PDF, DOCX, and TXT formats
- **Intelligent Text Cleaning**: Remove noise, special characters, and formatting artifacts
- **Structured LLM Extraction**: Parse documents into semantic sections (education, skills, experience, etc.)
- **Semantic Similarity Analysis**: Compare CV sections against job requirements using embeddings
- **LLM-Powered Evaluation**: Generate human-readable explanations and final hiring decisions
- **Structured JSON Output**: Auditable results with scores, evidence, and reasoning

---

## Pipeline Architecture

### 1. **Document Retrieval**
   - Load CVs and job descriptions from multiple file formats (PDF, DOCX, TXT)
   - Extract raw text content using LangChain document loaders

### 2. **Text Cleaning**
   - Remove headers, footers, and special characters
   - Normalize whitespace and line breaks
   - Eliminate repeated patterns and artifacts

### 3. **Structured Extraction** (Semantic "Chunking")
   - **CV Extraction**: Education, Skills, Experience, Certifications, Projects
   - **Job Description Extraction**: Requirements, Responsibilities, Qualifications
   - Uses LLM (deepseek-r1) with structured output to parse documents into Pydantic models
   - Each section serves as a semantically meaningful "chunk" aligned to evaluation criteria

### 4. **Semantic Similarity Scoring**
   - Generate embeddings for CV and JD sections using Ollama (snowflake-arctic-embed2)
   - Compute cosine similarity between aligned sections:
     - **Requirements** ↔ Education + Projects
     - **Responsibilities** ↔ Experience + Projects
     - **Qualifications** ↔ Skills + Certifications
   - Calculate overall weighted score (Requirements 50%, Responsibilities 30%, Qualifications 20%)

### 5. **Hybrid Evaluation & Decision Engine**
   - **Blind LLM Analysis**: LLM analyzes text context *without* seeing scores to form an unbiased opinion
   - **Score Verification**: Embedding scores act as a "veto" or "verification" layer
   - **Hybrid Logic**:
     - LLM **REJECT** → Final **REJECT**
     - LLM **PASS** + Low Score → Downgrade to **REVIEW**
     - LLM **REVIEW** + Very Low Score → Downgrade to **REJECT**
   - Output structured JSON with evidence, reasoning, and final decision

---

## Tech Stack

- **Python 3.12+**
- **LangChain** (document loading, LLM orchestration)
- **Ollama** (local LLM inference - llama3:latest, snowflake-arctic-embed2)
- **Pydantic** (structured data validation and schemas)
- **NumPy** (embedding similarity calculations)
- **PyPDF, Docx2txt** (document parsing)

---

## Why This Architecture?

- **No Vector Database Needed**: Embeddings are computed on-the-fly; no persistent storage required
- **Semantic Chunking via LLM**: Structured extraction creates meaningful sections instead of arbitrary text splits
- **Aligned Evaluation**: CV sections naturally map to JD sections for targeted comparison
- **Explainable Results**: LLM generates human-readable explanations grounded in similarity scores
- **Deterministic & Auditable**: Structured pipeline with logging at every stage
