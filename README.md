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
