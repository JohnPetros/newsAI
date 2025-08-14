# Estágio 1: Base com dependências do sistema
FROM python:3.11-slim AS base

# Definir variáveis de ambiente para otimização
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  UV_CACHE_DIR=/tmp/uv-cache

# Instalar dependências do sistema necessárias (incluindo Playwright)
RUN apt-get update && apt-get install -y \
  curl \
  build-essential \
  wget \
  gnupg \
  ca-certificates \
  fonts-liberation \
  fonts-dejavu \
  fonts-freefont-ttf \
  fonts-unifont \
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

# Instalar uv
RUN pip install --no-cache-dir uv

# =============================================================================
# Estágio 2: Dependências
# =============================================================================
FROM base AS deps

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências com uv (apenas produção)
RUN uv sync --frozen --no-dev

# Instalar Playwright e navegadores (sem dependências do sistema)
RUN uv run playwright install chromium

# =============================================================================
# Estágio 3: Build da aplicação
# =============================================================================
FROM deps AS builder

# Copiar código da aplicação
COPY src/ ./src/


# =============================================================================
# Estágio 4: Imagem final
# =============================================================================
FROM python:3.11-slim AS production

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  HOST=0.0.0.0 \
  PORT=8000 \
  UV_CACHE_DIR=/tmp/uv-cache

# Instalar dependências mínimas do sistema (incluindo Playwright)
RUN apt-get update && apt-get install -y \
  curl \
  fonts-liberation \
  fonts-dejavu \
  fonts-freefont-ttf \
  fonts-unifont \
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

# Instalar uv
RUN pip install --no-cache-dir uv

# Criar usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Criar diretório de cache do uv com permissões corretas
RUN mkdir -p /tmp/uv-cache && chown -R appuser:appuser /tmp/uv-cache

# Definir diretório de trabalho
WORKDIR /app

# Copiar ambiente virtual do estágio de dependências
COPY --from=deps /app/.venv /app/.venv

# Copiar navegadores do Playwright do estágio de dependências
COPY --from=deps /root/.cache/ms-playwright /home/appuser/.cache/ms-playwright

# Ajustar permissões dos navegadores do Playwright
RUN chown -R appuser:appuser /home/appuser/.cache/ms-playwright

# Copiar código da aplicação
COPY --from=builder /app/src ./src


# Copiar arquivo .env se existir (inclui .env, .env.local, .env.production, etc.)
COPY .env ./

# Definir PATH para incluir o ambiente virtual
ENV PATH="/app/.venv/bin:$PATH"

# Ajustar permissões dos navegadores do Playwright
RUN mkdir -p /home/appuser/.cache && \
  chown -R appuser:appuser /home/appuser && \
  chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uv", "run", "python", "src/main.py"]