FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1

# Install mkvmerge
RUN apt-get update && apt-get install -y --no-install-recommends \
    mkvtoolnix \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Production ---
FROM base AS prod
WORKDIR /anime_fixer
COPY . /anime_fixer

CMD ["python", "/anime_fixer/scheduler.py"]
