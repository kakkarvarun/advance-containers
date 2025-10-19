# Advance Containers Assignment
This repo contains a containerized FastAPI service + PostgreSQL DB, orchestrated by Docker Compose, with Nginx as a reverse proxy for optional scaling/load balancing.
## How to Run

1) Copy `.env.example` to `.env` and set your own password.
2) Start:
docker compose up -d
docker compose ps
3) Base URL (via Nginx): http://localhost:8088
4) Health: http://localhost:8088/healthz
## Persistence (Volumes)

- Database data persists in the named volume `pgdata`.
- App file logs persist in `app-logs` at `/app/logs/app.log`.

### Quick check
1) Create a user (POST /user).
2) Restart containers:
docker compose down
docker compose up -d

3) Fetch the same user (GET /user/{id}) — data is still there 

## Test the API

- Health: http://localhost:8080/healthz

### Create a user
```powershell
$body = @{ first_name = "Ada"; last_name = "Lovelace" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8088/user -Body $body -ContentType "application/json"
Fetch the user
Invoke-RestMethod -Method Get -Uri http://localhost:8088/user/1
View logs
docker compose exec web sh -lc "tail -n 50 /app/logs/app.log"

## Scaling (Bonus)

- Scale to 3 replicas:
docker compose up -d --scale web=3 --no-recreate
docker compose ps

- Keep using http://localhost:8088 — Nginx routes to the `web` service across replicas.
- Return to 1 replica:

docker compose up -d --scale web=1 --no-recreate

## Security Measures

- App runs as non-root (UID/GID 10001)
- Minimal base images (python:3.12-slim, postgres:16-alpine, nginx:alpine)
- Least privilege for app: dropped capabilities, no-new-privileges
- App filesystem read-only; writable volume only for logs
- Secrets via `.env` (sample provided as `.env.example`, real `.env` not committed)
- Health checks on DB and App
- Isolated network `app-net`


## Submission Checklist

- [x] `app/Dockerfile`
- [x] `docker-compose.yml`
- [x] App: `app/main.py`, `app/requirements.txt`, `app/gunicorn_conf.py`
- [x] DB init: `db/init.sql`
- [x] Reverse proxy: `nginx/default.conf`
- [x] `.env.example` (no real secrets committed)
- [x] README with build/run/test/persistence/security/scaling
- [x] Test script: `test/invoke-tests.ps1`

## Required Screenshots
1) Docker Desktop: `db`, `web`, `nginx` running
2) Terminal: `docker compose ps`
3) Browser: `http://localhost:8088/healthz`
4) PowerShell: POST `/user` response
5) PowerShell: GET `/user/{id}` response
6) Terminal: `docker compose exec web sh -lc "tail -n 50 /app/logs/app.log"`
7) Terminal: after scaling (`--scale web=3`), show `docker compose ps`

### Quick Tunnel (no domain)
1) docker rm -f cftunnel
2) docker run -d --name cftunnel --restart unless-stopped cloudflare/cloudflared:latest tunnel --no-autoupdate --url http://host.docker.internal:8088
3) docker logs -f cftunnel → copy the https://<random>.trycloudflare.com URL
4) Test: https://<random>.trycloudflare.com/healthz




