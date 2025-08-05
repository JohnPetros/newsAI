# Estágio 1: Base com dependências do sistema
FROM python:3.11-slim AS base

# Definir variáveis de ambiente para otimização
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  UV_CACHE_DIR=/tmp/uv-cache

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
  curl \
  build-essential \
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

# =============================================================================
# Estágio 3: Build da aplicação
# =============================================================================
FROM deps AS builder

# Copiar código da aplicação
COPY src/ ./src/
COPY main.py ./

# Verificar se há erros de sintaxe
RUN python -m py_compile src/main.py

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

# Instalar dependências mínimas do sistema
RUN apt-get update && apt-get install -y \
  curl \
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

# Copiar código da aplicação
COPY --from=builder /app/src ./src
COPY --from=builder /app/main.py ./

# Copiar arquivo .env se existir (inclui .env, .env.local, .env.production, etc.)
COPY .env ./

# Definir PATH para incluir o ambiente virtual
ENV PATH="/app/.venv/bin:$PATH"

# Alterar propriedade dos arquivos para o usuário appuser
RUN chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 8080

# Comando para executar a aplicação
CMD ["uv", "run", "python", "src/main.py"]
