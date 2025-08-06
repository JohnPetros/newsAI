# NewsAI

<h1 align="center">🚧 Working in Progress 🚧</h1>

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do servidor
HOST=0.0.0.0
PORT=8000

# APIs externas
BLOG_API_URL=https://api.blog.com
GOOGLE_API_KEY=your_google_api_key_here
```

### Variáveis Obrigatórias

- `BLOG_API_URL`: URL da API do blog
- `GOOGLE_API_KEY`: Chave da API do Google
- `AGENTQL_API_KEY`: Chave da API do AgentQL (necessária para o AgentQLTools)

### Variáveis Opcionais

- `HOST`: Host da aplicação (padrão: 0.0.0.0)
- `PORT`: Porta da aplicação (padrão: 8000)

## Docker

Para executar com Docker, o arquivo `.env` será automaticamente incluído na
imagem. Veja [DOCKER.md](DOCKER.md) para mais detalhes.
