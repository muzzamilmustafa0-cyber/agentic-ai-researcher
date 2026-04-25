"""
Web search tool using DuckDuckGo (no API key required).
"""
import logging
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults

logger = logging.getLogger(__name__)

_ddg_run = DuckDuckGoSearchRun()
_ddg_results = DuckDuckGoSearchResults(num_results=5)


@tool
def web_search(query: str) -> str:
    """
    Search the web for current information using DuckDuckGo.
    No API key required. Use for recent news, non-academic content, or verifying facts.

    Args:
        query: Web search query (e.g., "latest LLM benchmarks 2025")

    Returns:
        Top search results as formatted text with snippets.
    """
    try:
        results = _ddg_results.run(query)
        return f"🌐 Web search results for '{query}':\n\n{results}"
    except Exception as e:
        logger.warning(f"DuckDuckGo search failed: {e}")
        try:
            result = _ddg_run.run(query)
            return f"🌐 Web search for '{query}':\n\n{result}"
        except Exception as e2:
            return f"Search failed: {e2}. Try a different query."


@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.

    Args:
        expression: Math expression (e.g., "2**10", "sum([1,2,3,4,5])", "0.75 * 100")

    Returns:
        Computed result as a string.
    """
    import ast
    import operator

    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.Mod: operator.mod,
    }

    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            op = allowed_ops.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op)}")
            return op(_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            op = allowed_ops.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operator")
            return op(_eval(node.operand))
        else:
            raise ValueError(f"Unsupported expression type: {type(node)}")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval(tree.body)
        return f"🔢 {expression} = {result}"
    except Exception as e:
        return f"Calculation error: {e}"
