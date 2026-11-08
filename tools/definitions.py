"""
Tool definitions for the Anthropic tool-use API.
"""

TOOLS = [
    {
        "name": "web_search",
        "description": (
            "Search the web for information on a topic. "
            "Returns a list of result titles, URLs, and snippets."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string.",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "fetch_url",
        "description": (
            "Fetch and extract the main text content from a URL. "
            "Use this to read a source after finding it via web_search."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch.",
                }
            },
            "required": ["url"],
        },
    },
    {
        "name": "take_note",
        "description": (
            "Save a research finding to your notes. "
            "Include the source URL. Notes persist for the entire run."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "note": {
                    "type": "string",
                    "description": "The finding to record. Include source URL.",
                }
            },
            "required": ["note"],
        },
    },
    {
        "name": "get_notes",
        "description": "Retrieve all notes taken so far in this research session.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]
