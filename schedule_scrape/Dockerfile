FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x schedule_scrape.py

CMD ["python", "schedule_scrape.py"]
