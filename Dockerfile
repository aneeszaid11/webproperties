FROM python:3.12-slim


RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir httpx requests pandas openpyxl

WORKDIR /app
