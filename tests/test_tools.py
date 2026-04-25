"""Tests for individual agent tools."""
import pytest
from unittest.mock import patch, MagicMock


class TestArxivTool:

    def test_search_returns_string(self):
        from src.tools.arxiv_tool import search_arxiv
        with patch("src.tools.arxiv_tool.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b"""<?xml version="1.0"?>
            <feed xmlns="http://www.w3.org/2005/Atom">
              <entry>
                <id>http://arxiv.org/abs/2305.10601v1</id>
                <title>Test Paper Title</title>
                <summary>This is a test abstract about machine learning.</summary>
                <published>2023-05-17T00:00:00Z</published>
                <author><name>Test Author</name></author>
              </entry>
            </feed>"""
            result = search_arxiv.invoke("machine learning")
            assert isinstance(result, str)
            assert "Test Paper Title" in result

    def test_search_handles_empty_results(self):
        from src.tools.arxiv_tool import search_arxiv
        with patch("src.tools.arxiv_tool.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = b"""<?xml version="1.0"?>
            <feed xmlns="http://www.w3.org/2005/Atom"></feed>"""
            result = search_arxiv.invoke("xyznonexistent123")
            assert "No papers found" in result

    def test_search_handles_network_error(self):
        from src.tools.arxiv_tool import search_arxiv
        import requests
        with patch("src.tools.arxiv_tool.requests.get", side_effect=requests.RequestException("timeout")):
            result = search_arxiv.invoke("test query")
            assert "No papers found" in result or isinstance(result, str)


class TestCalculateTool:

    def test_simple_addition(self):
        from src.tools.web_search_tool import calculate
        result = calculate.invoke("2 + 2")
        assert "4" in result

    def test_power(self):
        from src.tools.web_search_tool import calculate
        result = calculate.invoke("2 ** 10")
        assert "1024" in result

    def test_division(self):
        from src.tools.web_search_tool import calculate
        result = calculate.invoke("10 / 4")
        assert "2.5" in result

    def test_malicious_input_rejected(self):
        from src.tools.web_search_tool import calculate
        result = calculate.invoke("__import__('os').system('ls')")
        assert "error" in result.lower() or "Calculation error" in result
