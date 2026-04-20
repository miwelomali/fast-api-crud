# Stage 1: Build with python-alpine
FROM python:3.14.4-alpine3.23 AS builder

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /app

# Copy requirements and install into a separate folder
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy application code
COPY . .

# Stage 2: Run distroless python app
FROM gcr.io/distroless/python3-debian13:latest

WORKDIR /app

# Copy installed packages and app from builder
COPY --from=builder /install /usr/local
COPY --from=builder /app /app

# Expose port
EXPOSE 8080

# Run the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]