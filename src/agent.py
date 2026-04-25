"""
Agentic AI Research Assistant.

Uses LangChain's ReAct (Reasoning + Acting) agent with:
- ArXiv search (academic papers)
- Web search via DuckDuckGo (no API key)
- Calculator tool
- Persistent conversation memory

The agent autonomously decides which tools to use based on the query,
can chain multiple tool calls, and synthesizes results into a coherent answer.
"""
import logging
from typing import List, Optional, Generator
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage

from src.tools import ALL_TOOLS
from src.config import get_llm

logger = logging.getLogger(__name__)


# ── System Prompt ─────────────────────────────────────────────────────────────

AGENT_SYSTEM_PROMPT = """You are ResearchAgent, an advanced AI research assistant with access to \
real-time academic databases and the web.

You have the following tools:
{tools}

Tool names: {tool_names}

Use the following format STRICTLY:

Question: the input question you must answer
Thought: think about what to do step by step
Action: the action to take — must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat up to 5 times)
Thought: I now have enough information to give a comprehensive answer
Final Answer: [your detailed, well-structured answer with citations]

Guidelines:
- For academic questions, ALWAYS search ArXiv first
- Cross-reference with web search for recent developments (2024-2025)
- Cite specific papers with ArXiv IDs when available
- Structure answers with headers and bullet points for readability
- For quantitative questions, use the calculator tool
- If a tool fails, try an alternative approach
- Be honest when information is limited or uncertain

Chat History (for context):
{chat_history}

Begin!

Question: {input}
Thought: {agent_scratchpad}"""


# ── Agent Factory ─────────────────────────────────────────────────────────────

class ResearchAgent:
    """
    Autonomous research agent that can:
    - Search academic papers (ArXiv)
    - Browse the web (DuckDuckGo, no API key)
    - Perform calculations
    - Maintain conversation history
    - Chain multiple tool calls per query
    """

    def __init__(self, llm: Optional[BaseChatModel] = None, memory_window: int = 10):
        self.llm = llm or get_llm()
        self.tools = ALL_TOOLS
        self.memory = ConversationBufferWindowMemory(
            k=memory_window,
            memory_key="chat_history",
            return_messages=False,
        )
        self._build_agent()
        logger.info(f"ResearchAgent initialized with {len(self.tools)} tools")

    def _build_agent(self) -> None:
        """Build the ReAct agent executor."""
        prompt = PromptTemplate.from_template(AGENT_SYSTEM_PROMPT)

        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )

        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=6,
            max_execution_time=60,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )

    def run(self, query: str) -> dict:
        """
        Execute a research query with autonomous tool use.

        Args:
            query: Natural language research question.
        Returns:
            Dict with 'output', 'steps', and 'tool_calls'.
        """
        try:
            result = self.executor.invoke({"input": query})
            steps = result.get("intermediate_steps", [])
            tool_calls = [
                {
                    "tool": step[0].tool,
                    "input": step[0].tool_input,
                    "output": str(step[1])[:300] + "…" if len(str(step[1])) > 300 else str(step[1]),
                }
                for step in steps
            ]
            return {
                "output": result["output"],
                "tool_calls": tool_calls,
                "steps_taken": len(steps),
            }
        except Exception as e:
            logger.error(f"Agent execution error: {e}")
            return {
                "output": f"I encountered an error: {str(e)}. Please try rephrasing your question.",
                "tool_calls": [],
                "steps_taken": 0,
            }

    def clear_memory(self) -> None:
        """Reset conversation memory."""
        self.memory.clear()
        logger.info("Agent memory cleared")

    def get_tool_descriptions(self) -> List[dict]:
        """Return descriptions of available tools."""
        return [
            {"name": t.name, "description": t.description[:100]}
            for t in self.tools
        ]
