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




