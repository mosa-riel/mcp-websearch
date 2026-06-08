# mcp-websearch

DuckDuckGo web-search MCP server for the [reSpeaker agent](https://gitlab.zzapps.nl/development/respeaker-agent).
No API key. Speaks **streamable-HTTP** so it runs as its own container / Home Assistant
add-on; the agent connects by `url`.

## Tools

`web_search(query, max_results=5)` → `[{title, url, snippet}]`

## Run

```bash
MCP_PORT=8786 uv run python server.py        # → http://127.0.0.1:8786/mcp
docker build -t mcp-websearch . && docker run -p 8786:8786 mcp-websearch
```

## Home Assistant add-on

Copy this folder into the HA host's `/addons` dir (SSH/Samba add-on) → Install.
Bridged; agent reaches it at `http://local-mcp_websearch:8786/mcp`.

## Env

| var        | default   | meaning   |
|------------|-----------|-----------|
| `MCP_HOST` | `0.0.0.0` | bind host |
| `MCP_PORT` | `8786`    | bind port |
