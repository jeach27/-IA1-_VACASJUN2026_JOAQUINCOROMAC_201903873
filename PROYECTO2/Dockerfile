FROM python:3.11-slim

# Instalar SWI-Prolog desde los repositorios de Debian
RUN apt-get update && \
    apt-get install -y --no-install-recommends swi-prolog && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias Python (cacheado antes de copiar el codigo)
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copiar codigo fuente
COPY backend/ ./backend/
COPY prolog/  ./prolog/
COPY frontend/ ./frontend/

WORKDIR /app/backend

EXPOSE 5000

ENV FLASK_ENV=production

CMD ["python", "app.py"]
