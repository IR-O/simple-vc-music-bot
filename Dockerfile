FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install system deps + NodeJS (required for PyTgCalls)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
 && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
 && apt-get install -y nodejs \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
