# mcp-websearch

DuckDuckGo web-search MCP server for the [reSpeaker agent](https://github.com/mosa-riel/respeaker-agent).
No API key. Speaks **streamable-HTTP** so it runs as its own container / Home Assistant
add-on; the agent connects by `url`.

## Tools

| tool | what |
|---|---|
| `web_search(query, max_results=5)` | DuckDuckGo (`ddgs` library) → `[{title, url, snippet}]` |
| `fetch_page(url)` | the page as markdown with links and images (trafilatura) |

[mcp-staan](https://github.com/mosa-riel/mcp-staan) also searches DuckDuckGo (next to staan.ai),
so with that one installed this server is optional.

## Run

```bash
MCP_PORT=8786 uv run python server.py        # → http://127.0.0.1:8786/mcp
docker build -t mcp-websearch . && docker run -p 8786:8786 mcp-websearch
```

## Home Assistant add-on

Add this repository to the add-on store, install "MCP Websearch". Bridged, internal only; the
agent reaches it at `http://<repo-hash>-mcp-websearch:8786/mcp`.

## Env

| var        | default   | meaning   |
|------------|-----------|-----------|
| `MCP_HOST` | `0.0.0.0` | bind host |
| `MCP_PORT` | `8786`    | bind port |
