"""Websearch — a tiny MCP server that does DuckDuckGo web search (no API key).

Two tools: `web_search` (DuckDuckGo, title/url/snippet) and `fetch_page` (read a page —
trafilatura → markdown with links + images, so the model can actually "look at" a site
and grab real image URLs). Speaks **streamable-HTTP**; runs as its own container / HA
add-on. Open-source + self-contained — no external API/service.

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


@mcp.tool()
async def fetch_page(url: str) -> dict:
    """Lees de inhoud van een webpagina. Gebruik dit ná web_search om een gevonden URL
    echt te bekijken (de snippets zijn te kort). Geeft de hoofdinhoud als markdown terug,
    met links [tekst](url) en afbeeldingen ![alt](src) — zo kun je ook een echte
    afbeeldings-URL pakken om met screen.show_image te tonen."""

    def _run() -> dict:
        import trafilatura

        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return {"url": url, "error": "kon pagina niet ophalen"}
        md = trafilatura.extract(
            downloaded, output_format="markdown",
            include_links=True, include_images=True, favor_recall=True,
        )
        return {"url": url, "content": (md or "geen leesbare inhoud gevonden")[:6000]}

    try:
        return await asyncio.to_thread(_run)
    except Exception as err:  # noqa: BLE001 - surface as a tool result, not a crash
        return {"url": url, "error": str(err)[:200]}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
