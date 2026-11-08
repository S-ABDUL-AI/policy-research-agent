"""
Tool executor — runs the actual side-effects for each tool call.
"""

import time
import urllib.request
import urllib.parse
import json
import re
from html.parser import HTMLParser


# ------------------------------------------------------------------ #
# Minimal HTML text extractor (no external deps)                      #
# ------------------------------------------------------------------ #

class _TextExtractor(HTMLParser):
    SKIP_TAGS = {"script", "style", "nav", "footer", "header", "aside"}

    def __init__(self):
        super().__init__()
        self.chunks: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self._skip > 0:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip == 0:
            stripped = data.strip()
            if stripped:
                self.chunks.append(stripped)

    def get_text(self) -> str:
        return " ".join(self.chunks)


def _extract_text_from_html(html: str, max_chars: int = 4000) -> str:
    extractor = _TextExtractor()
    try:
        extractor.feed(html)
        text = extractor.get_text()
    except Exception:
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


# ------------------------------------------------------------------ #
# DuckDuckGo search (no API key required)                             #
# ------------------------------------------------------------------ #

def _ddg_search(query: str, max_results: int = 5) -> list[dict]:
    try:
        from ddgs import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")[:300],
                })
        return results
    except ImportError:
        return _ddg_html_search(query, max_results)
    except Exception:
        return _ddg_html_search(query, max_results)


def _ddg_html_search(query: str, max_results: int = 5) -> list[dict]:
    encoded = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"
    headers = {"User-Agent": "Mozilla/5.0 policy-research-agent/1.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return [{"title": "Search error", "url": "", "snippet": str(e)}]

    results = []
    matches = list(re.finditer(
        r'class="result__title"[^>]*>.*?href="([^"]+)"[^>]*>(.*?)</a>.*?'
        r'class="result__snippet"[^>]*>(.*?)</span>',
        html, re.DOTALL
    ))
    for m in matches[:max_results]:
        results.append({
            "title": re.sub(r"<[^>]+>", "", m.group(2)).strip(),
            "url": m.group(1),
            "snippet": re.sub(r"<[^>]+>", "", m.group(3)).strip()[:300],
        })

    if not results:
        results.append({
            "title": "Search returned results",
            "url": f"https://duckduckgo.com/?q={encoded}",
            "snippet": "Could not parse results. Try fetch_url with specific URLs.",
        })
    return results


# ------------------------------------------------------------------ #
# URL fetcher                                                          #
# ------------------------------------------------------------------ #

def _fetch_url(url: str, max_chars: int = 4000) -> str:
    headers = {"User-Agent": "Mozilla/5.0 policy-research-agent/1.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"[fetch error: {e}]"

    if "html" in content_type.lower():
        return _extract_text_from_html(raw, max_chars)
    return raw[:max_chars]


# ------------------------------------------------------------------ #
# Public executor                                                      #
# ------------------------------------------------------------------ #

class ToolExecutor:
    def __init__(self):
        self._notes: list[str] = []
        self._brief: str | None = None

    @property
    def notes(self):
        return list(self._notes)

    @property
    def brief(self):
        return self._brief

    @property
    def done(self):
        return self._brief is not None

    def run(self, tool_name: str, tool_input: dict) -> tuple[str, float]:
        t0 = time.perf_counter()

        if tool_name == "web_search":
            results = _ddg_search(tool_input["query"])
            if results:
                lines = [
                    f"{i+1}. [{r['title']}]({r['url']})\n   {r['snippet']}"
                    for i, r in enumerate(results)
                ]
                result = "\n\n".join(lines)
            else:
                result = "No results found."

        elif tool_name == "fetch_url":
            result = _fetch_url(tool_input["url"])

        elif tool_name == "take_note":
            note = (
                tool_input.get("note")
                or tool_input.get("text")
                or tool_input.get("content")
                or str(tool_input)
            )
            self._notes.append(note)
            result = f"Note saved ({len(self._notes)} total)."

        elif tool_name == "get_notes":
            if not self._notes:
                result = "No notes yet."
            else:
                result = "\n\n".join(
                    f"[{i+1}] {n}" for i, n in enumerate(self._notes)
                )

        elif tool_name == "write_brief":
            self._brief = (
                tool_input.get("brief")
                or tool_input.get("content")
                or tool_input.get("text")
                or tool_input.get("output")
                or tool_input.get("policy_brief")
                or tool_input.get("summary")
                or (str(tool_input) if tool_input else None)
            )
            result = "Brief written. Research complete."

        else:
            result = f"Unknown tool: {tool_name}"

        duration_ms = (time.perf_counter() - t0) * 1000
        return result, duration_ms
