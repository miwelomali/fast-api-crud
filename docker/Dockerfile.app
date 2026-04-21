# Stage 1: MUST match the Distroless Python version (3.13)
FROM python:3.13-slim-trixie AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir fastapi uvicorn[standard]

COPY . .

# Stage 2: Distroless (Debian 13 comes with Python 3.13)
FROM gcr.io/distroless/python3-debian13:latest

WORKDIR /app

# Copy from builder (Note the 3.13 in the path)
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

ENV PYTHONPATH=/usr/local/lib/python3.13/site-packages

EXPOSE 8080

CMD ["-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

