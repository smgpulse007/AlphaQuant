# Agentic Alpha Engine (AlphaQuant)

A local-first, Docker-first research stack for building structured market and macro intelligence from public data, agent workflows, and lightweight model inference.

## Why this project exists

AlphaQuant is designed to help researchers and developers prototype an end-to-end alpha workflow without depending on cloud-only tooling:

- ingest and normalize macro, cross-asset, options, and politician-trade signals;
- run agentic analysis over those signals with a clear orchestration layer;
- export structured “Fusion” reports that can be reviewed, tested, and iterated locally.

This repo is intentionally local-first: the core path is reproducible on a developer laptop, and the compose stack makes it easy to run the API and supporting services together.

## Demo assets

![Terminal setup preview](artifacts/terminal-demo.gif)

![UI demo GIF](artifacts/ui-demo.gif)

![UI screenshot](artifacts/ui-screenshot.png)

The terminal preview above shows the setup flow in sequence. The raw VHS source files are also available in [artifacts/quick-setup.tape](artifacts/quick-setup.tape) and [artifacts/setup-demo.tape](artifacts/setup-demo.tape).

## What is included

- FastAPI API and worker entry points under [src/api](src/api)
- Agent orchestration and state logic under [src/agents](src/agents) and [src/orchestrator](src/orchestrator)
- Storage and retrieval helpers under [src/storage](src/storage)
- Small-world demo runner under [scripts/run_small_world.py](scripts/run_small_world.py)
- Frontend integration notes under [frontend](frontend)

## Quick start

1. Copy the environment template and add your local values.
   - `cp .env.example .env`
2. Start the local stack.
   - `docker compose up -d --build`
3. Pull the required local models once.
   - `docker exec -it ollama ollama pull llama3.1:8b mxbai-embed-large deepseek-r1:7b`
4. Run the API and try the sample payloads in [samples](samples).
   - `POST http://localhost:8000/run`

## Local development

### Python

- `python -m pip install -r requirements.api.txt`
- `python -m pip install -r requirements.worker.txt`

### Frontend

- `cd frontend`
- `npm install`
- `npm run dev -- --host 127.0.0.1 --port 5173`

### Small-world test

- `python scripts/run_small_world.py`

## Architecture at a glance

- API layer: FastAPI routes and worker entry points
- Orchestration: LangGraph-style state and graph planning helpers
- Agents: discovery, crawler, normalization, entities, macro, cross-asset, sectors, technicals, flows, politicians, synthesis, verification
- Storage: Postgres, Redis, Qdrant, MinIO, OpenSearch
- Local models: Ollama + embeddings for offline-friendly experimentation

## Notes for contributors

- All timestamps are recorded in PT.
- The verifier includes a double-source rule and warnings for missing corroboration.
- The workflow is intentionally modular so each agent/tool can be upgraded incrementally.

## Contributing

Contributions are welcome. Please open an issue first for larger changes, then submit a pull request with a clear summary and test evidence.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
