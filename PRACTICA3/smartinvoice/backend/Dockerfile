FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    poppler-utils \
    wget \
    curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m playwright install chromium
RUN python -m playwright install-deps chromium

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p uploads reports screenshots

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]