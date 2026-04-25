"""
Streamlit UI for the Agentic AI Research Assistant.
Shows real-time tool calls, reasoning steps, and final cited answers.
"""
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.agent import ResearchAgent
from src.config import get_llm

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchAgent — Agentic AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .agent-header {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .tool-call {
        background: #1a1a2e; color: #e0e0e0; border-radius: 8px;
        padding: 0.6rem 1rem; margin: 0.3rem 0;
        font-family: monospace; font-size: 0.85rem;
        border-left: 3px solid #f093fb;
    }
    .step-card {
        background: #0f3460; color: white;
        padding: 0.5rem 0.8rem; border-radius: 6px; margin: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tool_calls" not in st.session_state:
    st.session_state.total_tool_calls = 0

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 ResearchAgent")
    st.caption("Autonomous AI powered by LangChain ReAct")
    st.divider()

    st.markdown("### 🔧 LLM Provider")
    provider = st.selectbox("Backend", ["groq (free)", "openai", "gemini"], index=0)
    provider_key = provider.split(" ")[0]

    if st.button("🚀 Initialize Agent", use_container_width=True, type="primary"):
        with st.spinner("Loading agent…"):
            try:
                llm = get_llm(provider_key)
                st.session_state.agent = ResearchAgent(llm=llm)
                st.success("Agent ready!")
            except Exception as e:
                st.error(f"Failed: {e}. Check your API key in .env")

    st.divider()

    # Available tools display
    st.markdown("### 🛠️ Available Tools")
    tool_descriptions = [
        ("🔬", "search_arxiv", "Search academic papers on ArXiv"),
        ("📄", "get_arxiv_paper", "Fetch a specific paper by ID"),
        ("🌐", "web_search", "Search the web (DuckDuckGo)"),
        ("🔢", "calculate", "Evaluate math expressions"),
    ]
    for icon, name, desc in tool_descriptions:
        st.markdown(f"{icon} **{name}**  \n_{desc}_")

    st.divider()

    st.markdown("### 💡 Example Queries")
    examples = [
        "What are the latest transformer models for NLP in 2024?",
        "Find papers on RAG (Retrieval-Augmented Generation) and summarize the key approaches",
        "What is the difference between BERT and GPT architectures?",
        "Search for recent papers on LLM hallucination reduction",
        "What is 2 to the power of 10, and which paper introduced the attention mechanism?",
    ]
    for ex in examples:
        if st.button(f"💬 {ex[:45]}…" if len(ex) > 45 else f"💬 {ex}", use_container_width=True):
            st.session_state.pending_query = ex

    st.divider()

    stats_col1, stats_col2 = st.columns(2)
    stats_col1.metric("Messages", len(st.session_state.messages))
    stats_col2.metric("Tool Calls", st.session_state.total_tool_calls)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.agent:
            st.session_state.agent.clear_memory()
        st.session_state.total_tool_calls = 0
        st.rerun()


# ── Main Interface ────────────────────────────────────────────────────────────
st.markdown('<h1 class="agent-header">🤖 ResearchAgent</h1>', unsafe_allow_html=True)
st.caption("Autonomous AI researcher — searches ArXiv, browses the web, and synthesizes answers.")

if not st.session_state.agent:
    st.info("👈 **Initialize the agent** in the sidebar to start.")
    st.markdown("""
    ### How it works:
    1. You ask a research question
    2. The agent **autonomously decides** which tools to use
    3. It can chain multiple tool calls (e.g., search ArXiv → get paper details → web search for latest news)
    4. You see every reasoning step and tool call transparently
    5. Final answer is synthesized with citations

    ```
    User: "What are the best RAG techniques in 2024?"
    Agent: Thought → search_arxiv("RAG 2024") → Thought → web_search("RAG improvements 2024")
         → Thought → Final Answer with citations
    ```
    """)
else:
    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])
            if msg.get("tool_calls"):
                with st.expander(f"🔍 {len(msg['tool_calls'])} tool call(s) made"):
                    for tc in msg["tool_calls"]:
                        st.markdown(
                            f'<div class="tool-call">'
                            f'<b>🛠 {tc["tool"]}</b><br>'
                            f'Input: <code>{tc["input"]}</code><br>'
                            f'Output: {tc["output"][:200]}</div>',
                            unsafe_allow_html=True,
                        )

    # Handle example query click
    pending = st.session_state.pop("pending_query", None)

    if query := (pending or st.chat_input("Ask anything — I'll search ArXiv, the web, and synthesize an answer…")):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user", avatar="👤"):
            st.markdown(query)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Agent reasoning and searching…"):
                result = st.session_state.agent.run(query)

            answer = result["output"]
            tool_calls = result["tool_calls"]
            st.session_state.total_tool_calls += len(tool_calls)

            st.markdown(answer)

            if tool_calls:
                with st.expander(f"🔍 {len(tool_calls)} tool call(s) — click to inspect"):
                    for i, tc in enumerate(tool_calls, 1):
                        st.markdown(
                            f'<div class="tool-call">'
                            f'<b>Step {i}: 🛠 {tc["tool"]}</b><br>'
                            f'Input: <code>{tc["input"]}</code><br>'
                            f'Result: {tc["output"]}</div>',
                            unsafe_allow_html=True,
                        )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "tool_calls": tool_calls,
            })
