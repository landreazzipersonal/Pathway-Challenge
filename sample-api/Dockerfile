# Basic Dockerfile for Sample API
# Candidates should optimize this similarly to the preprocessing service

# MULTI-STAGE BUILD - 1st Stage - Build Stage
# Changing to slim image for smaller size and faster builds, vulnerability scanning and better security.

FROM python:3.11-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv

COPY requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY app.py .

# MULTI-STAGE BUILD - 2nd Stage
FROM python:3.11-slim

WORKDIR /app

# MULTI-STAGE BUILD - Copy only the necessary files from the builder stage
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/app.py /app/app.py

# ADD NON-ROOT USER
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# ADD HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD /opt/venv/bin/python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["/opt/venv/bin/gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2", "--threads", "4", "--timeout", "60"]