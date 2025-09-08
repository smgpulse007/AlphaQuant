Agentic Alpha Engine (AlphaQuant)

Local-first, Docker-first agentic research stack that ingests macro, cross-asset, options, and politician/government trades, then outputs Rev-4 “Fusion” reports with double-sourced facts, timestamps (PT), POP scores, roll/repair logic, and trade tables.

Quick start
- Copy env: `cp .env.example .env` and fill keys (or use SCRAPE_ONLY=true semantics later).
- Build: `docker compose up -d --build`
- Pull models (first run): `docker exec -it ollama ollama pull llama3.1:8b mxbai-embed-large deepseek-r1:7b`
- Call API: `POST http://localhost:8000/run` with sample payloads in `samples/`.

Structure
- FastAPI orchestrator with LangGraph-style flow (stubbed here).
- Agents for discovery → crawl → normalize → entities → macro → cross-asset → sectors → technicals → flows → politicians → synthesis → verify.
- Storage: Postgres, Redis, Qdrant, MinIO, OpenSearch (compose includes services).
- Local models: Ollama (compose service) and embeddings (to be pulled at runtime).

Small-world test
- Run `python scripts/run_small_world.py` to exercise a minimal pipeline (no paid APIs), and print a Rev-4 style JSON.

Frontend integration (separate repo)
- Repo example: `https://github.com/smgpulse007/AlphaQuantFrontEnd.git`
- Option A (fastest dev): run the frontend locally and point it at the API
  - Set `VITE_API_BASE_URL=http://localhost:8000` (or `NEXT_PUBLIC_API_BASE_URL` for Next.js)
  - Start your dev server (`npm run dev` or equivalent)
- Option B (Compose, static SPA)
  - Clone the frontend into `frontend/` at repo root: `git clone <your-frontend-repo> frontend`
  - Or add as submodule: `git submodule add <your-frontend-repo> frontend`
  - Build both: `docker compose -f docker-compose.yml -f docker-compose.ui.yml up -d --build`
  - Open UI at `http://localhost:8080` (UI calls API at `http://api:8000` on the compose network)
  - Adjust Dockerfile if the frontend is SSR (Next.js) instead of SPA; provided Dockerfile targets Vite/React SPA by default.

Notes for UI Dockerfile
- `docker/ui.Dockerfile` expects the frontend to produce `dist/` via `npm run build`.
- If your UI is Next.js SSR, use a Node runtime instead of Nginx and run `npm run start` after `npm run build`.

Notes
- All timestamps in PT. Double-source rule enforced in verifier stub (warnings for missing corroboration).
- Replace stubs incrementally; see TODOs in each agent/tool.
