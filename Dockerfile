FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt update && apt install -y ffmpeg \
 && pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
