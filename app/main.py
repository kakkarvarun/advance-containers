import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import psycopg2
import psycopg2.pool

LOG_DIR = "/app/logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
os.makedirs(LOG_DIR, exist_ok=True)

log_level = os.getenv("APP_LOG_LEVEL", "INFO").upper()
logger = logging.getLogger("app")
logger.setLevel(getattr(logging, log_level, logging.INFO))

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(stream_handler)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
  raise RuntimeError("DATABASE_URL is not set. Check compose environment block.")

db_pool: Optional[psycopg2.pool.SimpleConnectionPool] = None
app = FastAPI(title="Advance Containers Assignment API", version="1.0.0")

class UserIn(BaseModel):
  first_name: str = Field(..., min_length=1, max_length=100)
  last_name:  str = Field(..., min_length=1, max_length=100)

class UserOut(BaseModel):
  id: int
  first_name: str
  last_name:  str

@app.on_event("startup")
def startup_event():
  global db_pool
  logger.info("Starting up application... creating DB pool")
  db_pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=10, dsn=DATABASE_URL)
  conn = db_pool.getconn()
  try:
    with conn.cursor() as cur:
      cur.execute("SELECT 1;")
      conn.commit()
    logger.info("DB pool OK.")
  finally:
    db_pool.putconn(conn)

@app.on_event("shutdown")
def shutdown_event():
  global db_pool
  if db_pool:
    logger.info("Closing DB pool")
    db_pool.closeall()

@app.get("/healthz")
def healthz():
  return {"status": "ok"}

@app.post("/user", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
  logger.info(f"POST /user payload={user.model_dump()}")
  conn = db_pool.getconn()
  try:
    with conn.cursor() as cur:
      cur.execute(
        "INSERT INTO users (first_name, last_name) VALUES (%s, %s) RETURNING id, first_name, last_name;",
        (user.first_name, user.last_name)
      )
      row = cur.fetchone()
      conn.commit()
    return {"id": row[0], "first_name": row[1], "last_name": row[2]}
  except Exception as e:
    logger.exception("Error creating user")
    raise HTTPException(status_code=500, detail=str(e))
  finally:
    db_pool.putconn(conn)

@app.get("/user/{user_id}", response_model=UserOut)
def get_user(user_id: int):
  logger.info(f"GET /user/{user_id}")
  conn = db_pool.getconn()
  try:
    with conn.cursor() as cur:
      cur.execute("SELECT id, first_name, last_name FROM users WHERE id = %s;", (user_id,))
      row = cur.fetchone()
    if not row:
      raise HTTPException(status_code=404, detail="User not found")
    return {"id": row[0], "first_name": row[1], "last_name": row[2]}
  except HTTPException:
    raise
  except Exception as e:
    logger.exception("Error fetching user")
    raise HTTPException(status_code=500, detail=str(e))
  finally:
    db_pool.putconn(conn)
