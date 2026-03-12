FROM python:3.12-slim

workdir /app

copy . .

run pip install --no-cache-dir -r requirements.txt

cmd ["uvicorn", "main:app", "--host", "0.0.0.0" "--port", "8000"]