FROM python:3.14.4-alpine3.23

# Install pip dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /app

# Copy the requirements from pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

#Running command for the application
CMD ["uvicorn", main:app, "--host", "0.0.0.0", "--port", "8000"]
