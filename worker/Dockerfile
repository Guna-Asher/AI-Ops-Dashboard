FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY worker/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copy backend app code so 'import app.core.config' works
COPY backend/app/ /app/app/

# Copy the worker source
COPY worker/src/ /app/src/

CMD ["python", "-m", "src.main"]