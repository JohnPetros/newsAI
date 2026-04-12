# Arquitetura do Projeto NewsAI

## Visao Geral

O NewsAI e uma aplicacao backend para geracao automatizada de posts de blog sobre noticias. O projeto combina uma API HTTP em FastAPI, um workflow de IA com agentes especializados e um job agendado com Inngest para publicar conteudo de forma automatizada.

Em vez de uma arquitetura completa de Clean Architecture com repositorios, banco e multiplas camadas internas, o projeto atual segue uma arquitetura modular em camadas leves. O dominio central fica em `src/core`, a borda HTTP fica em `src/rest`, a orquestracao de IA fica em `src/ai` e a automacao assincrona fica em `src/pubsub`.

## Principios da Arquitetura

- **Core pequeno e estavel**: o dominio compartilha apenas entidades e erros de aplicacao.
- **Bordas finas**: controllers recebem a request, validam entrada e delegam o trabalho.
- **Workflow especializado**: a geracao de conteudo e orquestrada por um time de agentes com papeis definidos.
- **Integracoes isoladas**: chamadas ao blog externo, Gemini, Playwright e Inngest ficam fora do `core`.
- **Automacao por eventos e agenda**: a publicacao pode ser disparada via endpoint HTTP ou por job cron.
- **Falha centralizada**: erros de aplicacao sao transformados em JSON por um handler global.

## Camadas

- **Core (`src/core/`)**: entidades de dominio e erros da aplicacao.
- **REST (`src/rest/`)**: router, controllers, autenticacao por API key e service de integracao com a API do blog.
- **AI (`src/ai/`)**: workflow principal, agentes especializados e tools usadas pelos agentes.
- **PubSub (`src/pubsub/`)**: integracao com Inngest e job agendado para geracao automatica de posts.
- **Constants (`src/constants/`)**: configuracao da aplicacao carregada de variaveis de ambiente.
- **Bootstrap (`src/newsai/app.py`, `src/main.py`)**: composicao da aplicacao FastAPI, registro de CORS, exceptions, rotas e runtime local.

## Fluxo de Dados

Fluxo sincrono via API:

`HTTP Request` -> `Middleware.verify_api_key` -> `GeneratePostController` -> `Workflow.generate_post(...)` -> `AI Team + image agent` -> `Post` -> `BlogService.create_post(...)` -> `Blog API externa` -> `Response JSON`.

Fluxo assincrono agendado:

`Inngest cron` -> `GeneratePostJob` -> `BlogService.get_next_category()` -> `Workflow.generate_post(...)` -> `BlogService.create_post(...)`.

## Fluxos Implementados

Rotas HTTP atuais:

- `GET /health` -> `CheckApiHealthController` -> valida API key -> retorna `{"status": "healthy"}`.
- `POST /post` -> `GeneratePostController` -> `Workflow.generate_post(category)` -> `BlogService.create_post(post)` -> retorna `Post`.

Job atual:

- `generate.post.job` -> executado por `TriggerCron(cron="0 3 * * *")` -> consulta a proxima categoria no blog -> gera o post -> publica no blog externo.

## Pipeline de IA

O `Workflow` em `src/ai/workflow.py` centraliza a geracao de conteudo. Ele cria um `Team` do Agno com modelo Gemini e executa um pipeline em ordem fixa:

1. `Researcher Agent`: pesquisa noticias recentes sobre a categoria.
2. `Scrapper Agent`: extrai o conteudo da URL escolhida.
3. `Editor Agent`: escolhe o melhor angulo e define a estrutura editorial.
4. `Writer Agent`: escreve o post em HTML e PT-BR.
5. `Tagger Agent`: gera tags SEO.
6. `Image Generator Agent`: gera a imagem e devolve o `image_alt`.

O resultado final e convertido para a entidade `Post` do `core`.

## Padroes Principais

- **Arquitetura modular em camadas** para separar dominio, HTTP, IA e automacao.
- **Controller + Service** na borda REST.
- **Workflow orquestrador** como ponto central da logica de geracao.
- **Agent-based pipeline** para decompor a criacao do conteudo em etapas especializadas.
- **Error handling centralizado** via `ExceptionHandler`.
- **Configuracao por ambiente** encapsulada em `ENV`.

## Decisoes Arquiteturais

- O `core` concentra apenas tipos compartilhados do dominio (`Post`) e erros (`AppError`).
- A persistencia do conteudo nao e interna: os posts sao enviados para uma API externa de blog via `BlogService`.
- A imagem do post e gerada durante o workflow e salva temporariamente como `image.png` antes do upload.
- A autenticacao HTTP e simples e baseada em `X-Api-Key`.
- O Inngest e registrado dentro da app FastAPI e expoe o endpoint de eventos na mesma aplicacao.
- O workflow trata falhas de IA convertendo excecoes em `AppError` e aplica retry com `tenacity`.

## Armadilhas a Evitar

1. Colocar logica de geracao de conteudo diretamente nos controllers.
2. Acoplar `core` a FastAPI, requests, Inngest ou SDKs de IA.
3. Espalhar chamadas para a API do blog fora de `BlogService`.
4. Duplicar regras de autenticacao fora de `Middleware.verify_api_key`.
5. Alterar a ordem do pipeline de agentes sem revisar o contrato esperado do `Workflow`.
6. Retornar formatos livres dos agentes quando o `Workflow` espera JSON estruturado ao final.

## Stack Tecnologica

| Tecnologia | Pacote | Finalidade |
|------------|--------|------------|
| **Linguagem** | Python 3.13+ | Linguagem principal |
| **Framework** | FastAPI | API HTTP |
| **Servidor ASGI** | Uvicorn | Runtime da aplicacao |
| **IA Orquestrada** | Agno | Orquestracao de agentes |
| **LLM** | OpenAI | Geracao de texto e suporte aos agentes |
| **Geracao de Imagem** | Noop provider | Geracao desativada no momento |
| **Scraping** | Firecrawl | Extracao de conteudo de paginas |
| **Busca** | Exa | Pesquisa de noticias |
| **Eventos e Jobs** | Inngest | Agendamento e execucao assincrona |
| **Validacao** | Pydantic | Modelagem e validacao |
| **HTTP Client** | requests | Integracao com a API do blog |
| **Retry** | tenacity | Retentativas do workflow |
| **Ambiente** | python-dotenv | Carregamento de variaveis de ambiente |
| **Lint/Format** | Ruff | Qualidade de codigo |
| **Type Check** | Pyright | Checagem estatica |
| **Task Runner** | Poe the Poet | Automacao local |
| **Dependencias** | uv | Gerenciamento de pacotes |

## Infraestrutura de Execucao

O projeto depende principalmente de servicos externos configurados via ambiente:

| Componente | Origem | Observacao |
|---|---|---|
| **API HTTP** | FastAPI + Uvicorn | Expõe `/health`, `/post` e o endpoint do Inngest |
| **Blog API** | Servico externo | Recebe os posts gerados e informa a proxima categoria |
| **OpenAI** | OpenAI API | Gera texto e raciocinio dos agentes |
| **Inngest** | Inngest Cloud ou CLI local | Agenda o job `generate.post.job` |

## Estrutura de Diretorios

```text
src/
├── ai/
│   ├── agents/
│   ├── tools/
│   └── workflow.py
├── constants/
├── core/
│   ├── entities/
│   └── errors/
├── pubsub/
│   ├── jobs/
│   └── inngest_pubsub.py
├── rest/
│   ├── controllers/
│   ├── services/
│   ├── middleware.py
│   └── router.py
├── app.py
├── exception_handler.py
└── main.py
```

## Contrato da API

A API e HTTP/JSON e atualmente possui autenticacao por header `X-Api-Key`.

Contratos principais:

- `GET /health`: retorna status simples da API.
- `POST /post`: recebe `{"category": "..."}` e retorna um `Post` com `title`, `content`, `category`, `reading_time`, `image_alt` e `tags`.

## Variaveis de Ambiente Relevantes

- `HOST`
- `PORT`
- `BLOG_API_URL`
- `OPENAI_API_KEY`
- `EXA_API_KEY`
- `FIRECRAWL_API_KEY`
- `API_KEY`
- `INNGEST_SIGNING_KEY`
