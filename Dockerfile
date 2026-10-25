FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# Create non-root user for security compliance
RUN groupadd -r sre && useradd -r -g sre -u 10001 sre

COPY --from=builder /root/.local /home/sre/.local
COPY src/ /app/src/
COPY config/ /app/config/

# Ensure data directory exists and is owned by non-root user sre
RUN mkdir -p /app/data && chown -R sre:sre /app

ENV PATH=/home/sre/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PORT=8000

USER sre


EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]
