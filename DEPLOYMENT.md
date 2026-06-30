# Deployment (Coolify + Cloudflare)

This stack deploys to Coolify as a **Docker Compose** application behind Cloudflare.
The rules followed are in `COOLIFY_DEPLOY_RULES.md`.

## Topology

```
Cloudflare (TLS at edge, proxied)
        │
   Coolify / Traefik  ──Host()──►  frontend (nginx :80)  ── /api ─►  backend (uvicorn :8000)
                                                                          │
                                                                      postgres :5432 (internal)
```

Only **frontend** is public. nginx serves the built SPA and reverse-proxies `/api`
to `backend:8000`, so the browser only ever talks to one origin (no browser CORS to
the backend). `backend` and `postgres` are internal-only.

## What was changed for Coolify

- **`docker-compose.yml`**
  - Removed all `ports:` host mappings (rule B1 — Traefik handles host routing).
  - `postgres`: no `expose:` / `ports:` — internal only (B2).
  - `backend`: `expose: 8000` (matches uvicorn bind, A2).
  - `frontend`: `expose: 80` (matches nginx, A2) — this is the public service.
  - Removed the dead `REACT_APP_API_URL: http://localhost:8000/api` (Vite app, CRA
    var was ignored, and `localhost` is unreachable across containers — B3). The
    frontend now uses its default `/api`, proxied by nginx to `backend:8000`.
  - Removed the `./backend:/app/backend` dev bind-mount (production runs the built image).
  - Removed fixed `container_name`s (let Coolify name containers).
  - `CORS_ORIGINS` and `DEBUG` are now env-overridable; `DEBUG` defaults to `False`.
- **`frontend/Dockerfile`**: copy `/app/dist` (Vite output), not `/app/build`.
  *This was also a hard build failure before — the image could not build.*
- **`frontend/nginx.conf`**: `server_name _;` (accept any Host from Traefik) and
  `client_max_body_size 12M;` so PDF uploads up to the 10MB backend limit aren't
  rejected by nginx's 1MB default.

## Coolify configuration (UI — cannot be set in files)

1. Create an **application → Docker Compose**, point it at this repo, compose path `/docker-compose.yml`.
2. **Domains**: leave the top-level Domains field **empty**. After Coolify parses the
   compose, set **"Domains for frontend"** to your domain (e.g. `https://contracts.example.com`).
   Leave `backend` and `postgres` domains empty (C2, C3).
3. **No** `SERVICE_FQDN_*` / `SERVICE_URL_*` env vars (C4, C5).
4. Advanced tab: **Force HTTPS = OFF**, **Auto-generate SSL / Let's Encrypt = OFF**
   (Cloudflare terminates TLS — C6, C7).
5. Enable **Auto Deploy** only after the first successful manual deploy (C8).

### Environment variables to set in Coolify

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<set-a-real-password>
POSTGRES_DB=contract_db
DEBUG=False
NLP_MODEL_NAME=dslim/bert-base-NER
MAX_UPLOAD_SIZE=10485760
CORS_ORIGINS=https://<your-frontend-domain>
```

Notes:
- Set `CORS_ORIGINS` to your real public domain (the Origin the browser sends through
  the nginx `/api` proxy). Comma-separate multiple origins.
- `VITE_API_URL` is **not** needed — it is baked at build time and defaults to `/api`,
  which is what the nginx proxy expects. Only set it (as a build arg) if you change the
  API path.
- `PORT` / `APP_PORT` are unused by the compose routing; the bind ports are fixed at
  8000 (backend) and 80 (frontend).

## Cloudflare

- DNS: `A` record for the subdomain → Coolify server IP, **Proxied (orange cloud)** (D1).
- SSL/TLS mode: **Full** (not Flexible, not Off) (D2).
- "Always Use HTTPS": ON (D3); Minimum TLS 1.2 (D5).

## Pre-flight checklist

- [x] No `ports:` in compose
- [x] postgres has no `expose:`
- [x] backend `expose: 8000` == uvicorn bind; frontend `expose: 80` == nginx
- [x] Apps bind `0.0.0.0` (uvicorn `--host 0.0.0.0`; nginx `listen 80`)
- [x] Inter-service URLs use service names (`backend:8000`, `postgres:5432`)
- [ ] Coolify: Domain set on `frontend` only; top-level empty
- [ ] Coolify: no `SERVICE_FQDN_*` env vars
- [ ] Coolify: Force HTTPS OFF, Auto-LE OFF
- [ ] Cloudflare: A record proxied; SSL = Full
