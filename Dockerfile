FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt || true
RUN pip install --no-cache-dir uvicorn fastapi || true

EXPOSE 8000

CMD ["python", "web_server.py"]
