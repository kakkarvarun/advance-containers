FROM python:3.12-slim

# Make Python behave well in containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user/group with stable IDs
RUN addgroup --system --gid 10001 appgroup \
    && adduser --system --uid 10001 --ingroup appgroup appuser

WORKDIR /app

# Install deps first for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY main.py gunicorn_conf.py ./

# Make a writable logs dir (we'll mount a volume here)
RUN mkdir -p /app/logs && chown -R appuser:appgroup /app

USER 10001:10001
EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn_conf.py", "main:app"]
