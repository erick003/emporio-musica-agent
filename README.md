# Empório da Música - AI Customer Support Agent

This repository contains the technical challenge implementation for the AI Engineer / Data Engineering internship role at **Artefact**.

The project implements an intelligent, context-aware conversational agent designed to support the customer service team of **Empório da Música**, a fictional musical instrument store located in Campo Grande/MS.

---

## 1. System Architecture & Decisions

The architecture follows a **Hybrid Agent Tool-Use Pattern** combining structured relational querying and semantic unstructured document search (RAG).

```text
                  +-----------------------------+
                  |       User Interface        |
                  |        (CLI Engine)         |
                  +--------------+--------------+
                                 |
                                 v
                  +-----------------------------+
                  |   OpenAI Tool-Calling Agent |
                  |       (GPT-4o-mini)         |
                  +--------------+--------------+
                                 |
          +----------------------+----------------------+
          |                                             |
          v                                             v
+---------------------------+                 +---------------------------+
| Tool 1: SQLite DB Search  |                 |  Tool 2: Policy RAG Search|
|   (Data from CSV files)   |                 | (Chroma Vector Store DB)  |
+---------------------------+                 +---------------------------+
```
Technical Rationale:
LLM & Provider: OpenAI gpt-4o-mini was selected for its cost-efficiency, low latency, and robust function/tool calling performance.

Structured Data Approach (CSVs): CSV files (products, orders, customers, categories, order_items, promotions) are ingested on startup into a local SQLite database (sqlite3). A dedicated SQL tool allows the LLM to write precise queries without risking hallucination on prices or inventory counts.

Unstructured Data Approach (PDF Policy): Store policies (politicas_da_loja.pdf) are embedded using text-embedding-3-small and stored in a ChromaDB vector store. The agent uses RAG to retrieve policy context dynamically.

CLI Interface: Built using standard Python input/output loops, supporting conversation memory per session.

---

## 2. Installation and Setup Instructions
### Prerequisites
- Python 3.10+
- OpenAI API Key with available API credits
- `pip` and `venv` installed

### Steps
Clone the repository:

```bash
git clone [https://github.com/erick003/emporio-musica-agent.git](https://github.com/erick003/emporio-musica-agent.git)
cd emporio-musica-agent
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

If this project environment previously used LangChain 0.x, recreate it before
installing the current requirements:

```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The current dependency set includes LangChain 1.x packages and the
`langchain-classic` compatibility package required by the agent executor and
`create_openai_tools_agent`.

Configure environment variables:
Copy the example file and add your API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=sua-chave-real
```

The API key must have available OpenAI API credits. A ChatGPT subscription is
separate from API usage credits. Without credits, OpenAI may return
`credit_balance_exhausted` and the agent cannot process questions.

Run the agent:

```bash
python main.py
```

---

## 3. Known Limitations & Future Improvements
Multi-turn Memory Persistence: Current conversational history is maintained in memory per CLI session. In a production environment, history would be persisted via Redis or PostgreSQL.

Complex SQL Injection Prevention: The SQL tool executes agent-generated queries. Production deployment would enforce strict read-only user privileges and parameter validation.

Automated Evaluation: Future iterations could implement evaluation suites (e.g., Ragas, DeepEval) to measure answer accuracy, groundedness, and latency.

---

## 4. Use of AI Coding Assistants
During the development of this challenge, GitHub Copilot / ChatGPT were utilized as productivity tools for:

Accelerating boilerplate code generation for pandas-to-sqlite ingestion scripts.

Drafting Markdown templates for project documentation.

Formatting sample evaluation transcripts.

All architectural choices, prompt designs, and tool integrations were manually designed, evaluated, and validated.