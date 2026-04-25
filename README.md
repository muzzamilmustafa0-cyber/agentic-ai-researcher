<div align="center">

# 🤖 Agentic AI Research Assistant
### *Autonomous AI that searches, reasons, and synthesizes research — on its own.*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-ReAct_Agent-1C3C3C?style=for-the-badge)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-Free_Tier-F55036?style=for-the-badge)](https://console.groq.com)
[![ArXiv](https://img.shields.io/badge/ArXiv-API-B31B1B?style=for-the-badge)](https://arxiv.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![CI](https://img.shields.io/github/actions/workflow/status/muzzamilmustafa0-cyber/agentic-ai-researcher/ci.yml?style=for-the-badge&label=CI)](https://github.com/muzzamilmustafa0-cyber/agentic-ai-researcher/actions)

**Ask any research question → Agent autonomously plans, searches ArXiv + Web, chains tool calls, and delivers cited answers — no hand-holding.**

[🚀 Quick Start](#-quick-start) • [🧠 How It Works](#-how-it-works) • [🛠️ Tools](#-tools) • [💬 Examples](#-example-queries)

</div>

---

## 🧠 How It Works

This project implements the **ReAct (Reasoning + Acting)** paradigm — the agent alternates between:
1. **Reasoning** about the question and what it knows
2. **Acting** by calling appropriate tools
3. **Observing** the results
4. Repeating until it has enough information for a comprehensive answer

```
User Question
     ↓
┌────────────────────────────────────────────────────┐
│                ReAct Agent Loop                     │
│                                                     │
│  Thought: "Need to find papers on RAG..."          │
│  Action: search_arxiv("RAG retrieval 2024")        │
│  Observation: [5 papers returned]                  │
│       ↓                                            │
│  Thought: "Let me get details on the top paper..." │
│  Action: get_arxiv_paper("2312.10997")             │
│  Observation: [full abstract + metadata]           │
│       ↓                                            │
│  Thought: "Check latest industry news too..."      │
│  Action: web_search("RAG production 2025")         │
│  Observation: [web snippets]                       │
│       ↓                                            │
│  Final Answer: Comprehensive cited summary         │
└────────────────────────────────────────────────────┘
```

---

## 🛠️ Tools

| Tool | Source | API Key? | Description |
|---|---|---|---|
| `search_arxiv` | arxiv.org API | ❌ Free | Search academic papers by keyword |
| `get_arxiv_paper` | arxiv.org API | ❌ Free | Fetch full metadata by paper ID |
| `web_search` | DuckDuckGo | ❌ Free | Real-time web search |
| `calculate` | Python AST | ❌ None | Safe math expression evaluator |

> **Zero-cost setup** — all tools work without API keys. Only the LLM needs a key (Groq is free).

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/muzzamilmustafa0-cyber/agentic-ai-researcher.git
cd agentic-ai-researcher

# Install
pip install -r requirements.txt

# Configure (free Groq key: https://console.groq.com)
cp .env.example .env
# Set GROQ_API_KEY in .env

# Launch Streamlit UI
streamlit run ui/app.py
```

Or use it directly in Python:
```python
from src.agent import ResearchAgent

agent = ResearchAgent()

result = agent.run("What are the key differences between RAG and fine-tuning for LLMs?")
print(result["output"])
print(f"Tool calls made: {result['steps_taken']}")
```

---

## 💬 Example Queries

```
📚 "Summarize the latest advances in multimodal LLMs from 2024"
🔬 "Find papers by Yann LeCun on self-supervised learning and explain the main contributions"
🤔 "What is the attention mechanism and which paper introduced it?"
📊 "Compare BERT vs GPT architectures — search ArXiv and web for a comprehensive answer"
🧮 "What is 2^32, and which papers use this as a vocabulary size?"
🏥 "Find recent papers on ML for medical diagnosis — focus on transformer-based approaches"
```

---

## 📁 Structure

```
agentic-ai-researcher/
├── src/
│   ├── agent.py              # ReAct agent with LangChain AgentExecutor
│   ├── config.py             # LLM factory (Groq/OpenAI/Gemini)
│   └── tools/
│       ├── arxiv_tool.py     # ArXiv search + paper fetcher
│       └── web_search_tool.py # DuckDuckGo + calculator
├── ui/
│   └── app.py                # Streamlit chat UI with tool call inspector
├── tests/
│   └── test_tools.py         # Unit tests for all tools
└── .github/workflows/ci.yml  # GitHub Actions CI
```

---

## 🔧 Extending

- Add **code execution** tool (Python REPL via LangChain)
- Add **PDF reader** tool to fetch and read ArXiv PDFs
- Add **citation manager** that exports BibTeX
- Replace DuckDuckGo with **Tavily** for richer web results
- Add **multi-agent** setup: orchestrator agent + specialist agents

---

## 👨‍💻 Author

**Muzzamil Mustafa** — AI Researcher & ML Engineer

[![Google Scholar](https://img.shields.io/badge/Scholar-4285F4?style=flat&logo=google-scholar&logoColor=white)](https://scholar.google.com/citations?user=v2bGrp0AAAAJ)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github)](https://github.com/muzzamilmustafa0-cyber)
[![ORCID](https://img.shields.io/badge/ORCID-A6CE39?style=flat&logo=orcid&logoColor=white)](https://orcid.org/0000-0002-4896-0305)

---
MIT License
</div>
