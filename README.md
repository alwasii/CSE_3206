# CSE_3206 — Production-Based RAG System for University Websites

Conversational RAG prototype to answer university questions in natural language using grounded, source-backed responses from official websites, PDFs and notices.

## Team

| Name | Roll |
|------|------|
| Fahim | 24524203101 |
| Wasit | 24524203105 |
| Shanto | 24524203177 |
| Nayeem | 23524202127 |

## Contents

- `Ashik.txt` — 1. Introduction
- `24524203101.txt` — 2. Overall Description
- `Wasit.txt` — 3.1 Functional Requirements (FR-01 to FR-25)
- `Shanto.txt` — 3.2 Non-Functional Requirements (NFR-01 to NFR-22)
- `class_diagram_fahim_24524203101.png` / `.pdf` / `.puml` — Class diagram (Fahim)
- `classdigram_wasit.png` — Class diagram (Wasit)
- `seq_diagran_shanto.jpeg` — Sequence diagram (Shanto)

## Tech Stack

Frontend: HTML, CSS, JavaScript | Backend: Python, FastAPI | Retrieval: Dense Vector + BM25 + RRF + Cross-Encoder Rerank | Store: Qdrant | Ingestion: PyMuPDF, BeautifulSoup | Env: Linux/Ubuntu, Git, VS Code

## Notes

- Prototype scope: limited university sites/docs, English QA only.
- See SRS `.txt` files for full requirements and diagrams for design.