# Plain Python base — this MCP needs no bashio/supervisor access.
FROM python:3.13-slim

ENV MCP_HOST=0.0.0.0 \
    MCP_PORT=8786 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY server.py /app/server.py
RUN pip install "mcp>=1.27.2" "ddgs>=9.0" "trafilatura>=1.12"

EXPOSE 8786
CMD ["python", "server.py"]
