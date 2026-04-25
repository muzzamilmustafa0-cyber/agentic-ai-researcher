"""
ArXiv tool for the research agent.
Fetches and summarizes papers from arxiv.org by keyword or paper ID.
"""
import re
import logging
from typing import Optional
import requests
import xml.etree.ElementTree as ET

from langchain.tools import tool

logger = logging.getLogger(__name__)

ARXIV_API = "http://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def _search_arxiv(query: str, max_results: int = 5) -> list:
    """Search ArXiv and return structured paper metadata."""
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    try:
        resp = requests.get(ARXIV_API, params=params, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"ArXiv API error: {e}")
        return []

    root = ET.fromstring(resp.content)
    papers = []

    for entry in root.findall("atom:entry", NS):
        paper_id = entry.findtext("atom:id", "", NS).split("/abs/")[-1]
        title = entry.findtext("atom:title", "", NS).strip().replace("\n", " ")
        summary = entry.findtext("atom:summary", "", NS).strip().replace("\n", " ")
        published = entry.findtext("atom:published", "", NS)[:10]
        authors = [
            a.findtext("atom:name", "", NS)
            for a in entry.findall("atom:author", NS)
        ]

        categories = [
            c.get("term", "")
            for c in entry.findall("arxiv:primary_category", NS)
        ]

        papers.append({
            "id": paper_id,
            "title": title,
            "authors": authors[:5],  # Cap at 5 authors
            "published": published,
            "summary": summary[:500] + "…" if len(summary) > 500 else summary,
            "url": f"https://arxiv.org/abs/{paper_id}",
            "pdf_url": f"https://arxiv.org/pdf/{paper_id}",
            "categories": categories,
        })

    return papers


@tool
def search_arxiv(query: str) -> str:
    """
    Search ArXiv for research papers on a topic.

    Args:
        query: Search query (e.g., "transformer attention mechanism NLP 2024")

    Returns:
        Formatted list of top-5 relevant papers with title, authors, year, abstract, and URL.
    """
    papers = _search_arxiv(query, max_results=5)
    if not papers:
        return f"No papers found for query: '{query}'"

    lines = [f"📚 Top {len(papers)} ArXiv results for '{query}':\n"]
    for i, p in enumerate(papers, 1):
        authors_str = ", ".join(p["authors"][:3])
        if len(p["authors"]) > 3:
            authors_str += " et al."
        lines.append(
            f"[{i}] **{p['title']}**\n"
            f"    Authors: {authors_str} ({p['published'][:4]})\n"
            f"    Abstract: {p['summary']}\n"
            f"    🔗 {p['url']}\n"
        )
    return "\n".join(lines)


@tool
def get_arxiv_paper(paper_id: str) -> str:
    """
    Fetch details of a specific ArXiv paper by its ID.

    Args:
        paper_id: ArXiv paper ID (e.g., "2305.10601" or "https://arxiv.org/abs/2305.10601")

    Returns:
        Full paper metadata including title, authors, abstract, and links.
    """
    # Extract ID from URL if full URL provided
    paper_id = paper_id.strip()
    if "arxiv.org" in paper_id:
        paper_id = paper_id.split("/abs/")[-1].split("v")[0]

    params = {"id_list": paper_id, "max_results": 1}
    try:
        resp = requests.get(ARXIV_API, params=params, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        return f"Error fetching paper {paper_id}: {e}"

    root = ET.fromstring(resp.content)
    entries = root.findall("atom:entry", NS)

    if not entries:
        return f"Paper not found: {paper_id}"

    entry = entries[0]
    title = entry.findtext("atom:title", "", NS).strip().replace("\n", " ")
    summary = entry.findtext("atom:summary", "", NS).strip().replace("\n", " ")
    authors = [a.findtext("atom:name", "", NS) for a in entry.findall("atom:author", NS)]
    published = entry.findtext("atom:published", "", NS)[:10]

    return (
        f"📄 **{title}**\n\n"
        f"**Authors:** {', '.join(authors)}\n"
        f"**Published:** {published}\n"
        f"**ArXiv ID:** {paper_id}\n"
        f"**URL:** https://arxiv.org/abs/{paper_id}\n"
        f"**PDF:** https://arxiv.org/pdf/{paper_id}\n\n"
        f"**Abstract:**\n{summary}"
    )
