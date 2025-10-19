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
