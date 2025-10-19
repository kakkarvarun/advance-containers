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



> If you used a different port earlier, change **8081** to your port.

### 4) Save the file
- Press **Ctrl + S**.

### 5) Make the commit (two easy options)

**Option A — Using VS Code GUI**
1. Click the **Source Control** icon (left sidebar, looks like a branch).
2. In the message box at the top, type:  
   `docs: add API test steps and log tail command`
3. Click **Commit** (the ✓ button).

**Option B — Using the terminal**
```powershell
git add README.md
git commit -m "docs: add API test steps and log tail command"
