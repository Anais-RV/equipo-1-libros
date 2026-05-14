FROM python:3.13-slim

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.7.0
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY data ./data
COPY archive ./archive

WORKDIR /app/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
