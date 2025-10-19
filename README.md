# Advance Containers Assignment
This repo contains a containerized FastAPI service + PostgreSQL DB, orchestrated by Docker Compose, with Nginx as a reverse proxy for optional scaling/load balancing.
## Run

```powershell
docker compose build
docker compose up -d
docker compose ps


## Test API

- GET http://localhost:8081/healthz

### Create a user
```powershell
$body = @{ first_name = "Ada"; last_name = "Lovelace" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8081/user -Body $body -ContentType "application/json"

Fetch the user
Invoke-RestMethod -Method Get -Uri http://localhost:8081/user/1
View logs
docker compose exec web sh -c "tail -n 50 /app/logs/app.log"

## Persistence

- Database data is stored in the Docker named volume **pgdata**.
- App file logs are stored in the volume **app-logs** at `/app/logs/app.log`.
- `docker compose down` keeps data; `docker compose down -v` wipes it.

### Quick check
1) Create a user at http://localhost:8081 (temporary port):
   - POST /user with { "first_name": "Ada", "last_name": "Lovelace" }
2) Stop and start:
docker compose down
docker compose up -d
3) Fetch the same user:
- GET /user/1 (or the ID you got)
- The record is still there 

