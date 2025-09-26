# --- Base image with Python + mkvmerge ---
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1

# Install mkvmerge and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    mkvtoolnix \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Production image ---
FROM base AS prod
WORKDIR /anime_fixer

# Copy project code
COPY . /anime_fixer

# Run scheduler (handles daily execution at midnight)
CMD ["python", "/anime_fixer/scheduler.py"]
