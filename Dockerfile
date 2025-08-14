FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  UV_CACHE_DIR=/tmp/uv-cache

RUN apt-get update && apt-get install -y \
  curl \
  build-essential \
  wget \
  gnupg \
  ca-certificates \
  fonts-liberation \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libatspi2.0-0 \
  libcups2 \
  libdbus-1-3 \
  libdrm2 \
  libgtk-3-0 \
  libnspr4 \
  libnss3 \
  libxcomposite1 \
  libxdamage1 \
  libxrandr2 \
  libxss1 \
  xdg-utils \
  libxkbcommon0 \
  libx11-xcb1 \
  libxcb-dri3-0 \
  libxcb1 \
  libxrandr2 \
  libgbm1 \
  libasound2 \
  libatspi2.0-0 \
  libxss1 \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

FROM base AS deps

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

RUN uv run playwright install --with-deps chromium

FROM deps AS builder

COPY src/ ./src/

FROM python:3.11-slim AS production

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  HOST=0.0.0.0 \
  PORT=8000 \
  UV_CACHE_DIR=/tmp/uv-cache

RUN apt-get update && apt-get install -y \
  curl \
  fonts-liberation \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libatspi2.0-0 \
  libcups2 \
  libdbus-1-3 \
  libdrm2 \
  libgtk-3-0 \
  libnspr4 \
  libnss3 \
  libxcomposite1 \
  libxdamage1 \
  libxrandr2 \
  libxss1 \
  xdg-utils \
  libxkbcommon0 \
  libx11-xcb1 \
  libxcb-dri3-0 \
  libxcb1 \
  libgbm1 \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean

RUN pip install --no-cache-dir uv

RUN groupadd -r appuser && useradd -r -g appuser appuser

RUN mkdir -p /tmp/uv-cache && chown -R appuser:appuser /tmp/uv-cache

WORKDIR /app

COPY --from=deps /app/.venv /app/.venv

COPY --from=deps /root/.cache/ms-playwright /home/appuser/.cache/ms-playwright

COPY --from=builder /app/src ./src

COPY .env ./

ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /home/appuser/.cache && \
  chown -R appuser:appuser /home/appuser && \
  chown -R appuser:appuser /app

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uv", "run", "python", "src/main.py"]
