FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app
COPY src /app/src

# Minimal tool shim; real scraping runs via MCP server later
CMD ["python", "-c", "print('Playwright container ready')"]

