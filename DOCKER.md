# Docker para NewsAI

Este documento descreve como usar Docker com a aplicação NewsAI.

## 🏗️ Arquitetura da Imagem

Esta aplicação usa um **multi-stage build** otimizado com as seguintes
características:

- **Base**: Python 3.11-slim (Debian)
- **Gerenciador de pacotes**: uv (mais rápido que pip)
- **Multi-stage**: Separação entre dependências e código
- **Segurança**: Usuário não-root (appuser)
- **Otimização**: Cache de dependências e build incremental

## 📋 Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+ (opcional)
- 2GB+ de RAM disponível

## 🚀 Build da Imagem

### Usando o script de build (Recomendado)

```bash
# Build padrão
./build.sh

# Build com tag específica
./build.sh -t v1.0.0

# Build para desenvolvimento (apenas dependências)
./build.sh -d

# Limpar imagens antigas
./build.sh -c

# Ver ajuda
./build.sh -h
```

### Usando Docker diretamente

```bash
# Build padrão
docker build -t newsai:latest .

# Build para plataforma específica
docker build --platform linux/amd64 -t newsai:latest .

# Build com cache
docker build --build-arg BUILDKIT_INLINE_CACHE=1 -t newsai:latest .
```

## 🏃‍♂️ Execução

### Modo Produção

```bash
# Usando Docker
docker run -d \
  --name newsai \
  -p 8000:8000 \
  -e BLOG_API_URL=your_blog_api_url \
  -e GOOGLE_API_KEY=your_google_api_key \
  newsai:latest

# Usando Docker Compose
docker-compose up -d
```

### Modo Desenvolvimento

```bash
# Com hot reload
docker-compose --profile dev up newsai-dev

# Com volume montado para desenvolvimento
docker run -it \
  -p 8000:8000 \
  -v $(pwd)/src:/app/src \
  -e BLOG_API_URL=your_blog_api_url \
  -e GOOGLE_API_KEY=your_google_api_key \
  newsai:latest
```

## 🔧 Variáveis de Ambiente

| Variável         | Descrição              | Padrão    | Obrigatória |
| ---------------- | ---------------------- | --------- | ----------- |
| `HOST`           | Host da aplicação      | `0.0.0.0` | Não         |
| `PORT`           | Porta da aplicação     | `8000`    | Não         |
| `BLOG_API_URL`   | URL da API do blog     | -         | Sim         |
| `GOOGLE_API_KEY` | Chave da API do Google | -         | Sim         |

### Exemplo de arquivo .env

```env
BLOG_API_URL=https://api.blog.com
GOOGLE_API_KEY=your_google_api_key_here
HOST=0.0.0.0
PORT=8000
```

## 🏥 Health Check

A aplicação expõe um endpoint de health check em `/health` que retorna:

```json
"healthy"
```

O Dockerfile inclui um health check configurado para:

- **Intervalo**: 30 segundos
- **Timeout**: 30 segundos
- **Retry**: 3 tentativas
- **Start period**: 5 segundos

## 📊 Monitoramento

### Logs

```bash
# Docker
docker logs newsai
docker logs -f newsai  # Follow

# Docker Compose
docker-compose logs newsai
docker-compose logs -f newsai
```

### Status do container

```bash
# Verificar status
docker ps

# Verificar health check
docker inspect newsai | grep -A 10 "Health"

# Verificar recursos
docker stats newsai
```

## 🔍 Troubleshooting

### Problemas comuns

1. **Porta já em uso**
   ```bash
   # Verificar se a porta está em uso
   lsof -i :8000

   # Usar porta diferente
   docker run -p 8001:8000 newsai:latest
   ```

2. **Variáveis de ambiente não definidas**
   ```bash
   # Verificar variáveis no container
   docker exec newsai env | grep -E "(BLOG_API_URL|GOOGLE_API_KEY)"
   ```

3. **Problemas de permissão**
   ```bash
   # Verificar logs do container
   docker logs newsai

   # Executar como root temporariamente
   docker run --user root newsai:latest
   ```

### Debug

```bash
# Entrar no container
docker exec -it newsai /bin/bash

# Verificar estrutura de arquivos
docker exec newsai ls -la /app

# Verificar processo Python
docker exec newsai ps aux
```

## 📈 Performance

### Otimizações implementadas

1. **Multi-stage build**: Reduz tamanho da imagem final
2. **Cache de dependências**: uv cache para builds mais rápidos
3. **Imagem base otimizada**: python:3.11-slim
4. **Usuário não-root**: Segurança aprimorada
5. **Health check**: Monitoramento automático

### Comparação de tamanhos

| Componente          | Tamanho Aproximado |
| ------------------- | ------------------ |
| Imagem base         | ~40MB              |
| Dependências Python | ~150MB             |
| Código da aplicação | ~5MB               |
| **Total**           | **~195MB**         |

## 🔒 Segurança

### Medidas implementadas

- ✅ Usuário não-root (appuser)
- ✅ Imagem base oficial Python
- ✅ Sem dependências desnecessárias
- ✅ Health check para monitoramento
- ✅ Variáveis de ambiente para configuração

### Boas práticas

1. **Nunca** execute como root em produção
2. **Sempre** use variáveis de ambiente para secrets
3. **Monitore** logs regularmente
4. **Atualize** a imagem base periodicamente

## 🧪 Testes

### Testar a aplicação

```bash
# Testar health check
curl http://localhost:8000/health

# Testar API
curl http://localhost:8000/docs

# Testar com dados
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "content": "Test content"}'
```

### Testar a imagem

```bash
# Build e teste rápido
./build.sh && docker run --rm -p 8000:8000 newsai:latest

# Teste de integração
docker-compose up -d && sleep 10 && curl http://localhost:8000/health
```

## 📚 Comandos Úteis

```bash
# Build rápido
./build.sh

# Executar em background
docker run -d --name newsai -p 8000:8000 newsai:latest

# Parar e remover
docker stop newsai && docker rm newsai

# Limpar tudo
docker system prune -a

# Ver informações da imagem
docker images newsai
docker history newsai:latest
```
