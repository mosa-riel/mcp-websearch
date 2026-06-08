"""Websearch — a tiny MCP server that does DuckDuckGo web search (no API key).

A tool source for the reSpeaker agent: finding places, looking up current info, etc.
Returns title/url/snippet the agent uses to answer. Speaks **streamable-HTTP** so it
runs as its own container / Home Assistant add-on; the agent connects by url.

Env:
  MCP_HOST  bind host (default 0.0.0.0)
  MCP_PORT  bind port (default 8786)
URL the agent points at:  http://<host>:<MCP_PORT>/mcp
"""

from __future__ import annotations

import asyncio
import os

from ddgs import DDGS
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# Server↔server MCP on a trusted internal add-on network — disable the browser-oriented
# DNS-rebinding guard (localhost-only, no glob) so non-localhost Host headers don't 421.
mcp = FastMCP(
    "websearch",
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8786")),
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


@mcp.tool()
async def web_search(query: str, max_results: int = 5) -> list[dict]:
    """Zoek op het web (DuckDuckGo) naar actuele informatie, plekken, feiten, enz.
    Geeft een lijst met {title, url, snippet} terug om je antwoord op te baseren."""

    def _run() -> list[dict]:
        n = max(1, min(max_results, 8))
        with DDGS() as ddgs:
            return [
                {"title": r.get("title"), "url": r.get("href"), "snippet": (r.get("body") or "")[:300]}
                for r in ddgs.text(query, max_results=n)
            ]

    try:
        return await asyncio.to_thread(_run)
    except Exception as err:  # noqa: BLE001 - surface as a tool result, not a crash
        return [{"error": str(err)[:200]}]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
