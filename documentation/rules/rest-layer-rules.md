# REST Layer — Guia de Padrões e Convenções

Este documento descreve a arquitetura, padrões e convenções utilizados na camada REST (`src/rest`) do projeto. Siga estas diretrizes ao criar novos endpoints ou modificar os existentes.

---

## Visão Geral da Arquitetura

A camada REST segue uma arquitetura em camadas com separação clara de responsabilidades:

```
src/rest/
├── router.py              # Registro centralizado de rotas
├── middleware.py           # Middlewares compartilhados (autenticação, etc.)
├── controllers/            # Handlers de rotas HTTP
│   ├── __init__.py
│   ├── check_api_health_controller.py
│   └── generate_post_controller.py
└── services/               # Integração com APIs externas
    ├── __init__.py
    └── blog_service.py
```

**Fluxo da requisição:**

```
Request → Middleware (auth) → Controller → Service / Domain → Response
```

---

## Router (`router.py`)

O `Router` é o ponto central de registro de todas as rotas da aplicação. Ele expõe um único método estático `register()` que retorna um `APIRouter` do FastAPI.

### Convenções

- Cada controller é registrado via chamada a `Controller.handle(router)`.
- Novos controllers devem ser adicionados seguindo o mesmo padrão.

```python
from fastapi import APIRouter
from rest.controllers import CheckApiHealthController, GeneratePostController

class Router:
    @staticmethod
    def register() -> APIRouter:
        router = APIRouter()
        CheckApiHealthController.handle(router)
        GeneratePostController.handle(router)
        return router
```

### Integração com a aplicação

O router é integrado na aplicação principal em `app.py` via `app.include_router(Router.register())`.

---

## Controllers (`controllers/`)

Controllers são responsáveis por receber requisições HTTP, validar dados de entrada e orquestrar a resposta.

### Padrão de Implementação

Cada controller é uma **classe com um método estático `handle`** que recebe um `APIRouter` e registra o endpoint internamente:

```python
from fastapi import APIRouter, Depends
from rest.middleware import Middleware

class MeuNovoController:
    @staticmethod
    def handle(router: APIRouter) -> None:
        @router.post("/minha-rota", dependencies=[Depends(Middleware.verify_api_key)])
        def _(body: MeuBody) -> MeuResponse:
            # lógica aqui
            ...
```

### Convenções

| Convenção | Regra |
|---|---|
| **Nomenclatura do arquivo** | `snake_case` descrevendo a ação — ex: `generate_post_controller.py` |
| **Nomenclatura da classe** | `PascalCase` com sufixo `Controller` — ex: `GeneratePostController` |
| **Método de registro** | Sempre `handle(router: APIRouter) -> None` como `@staticmethod` |
| **Nome do handler interno** | Função anônima nomeada como `_` (underscore) |
| **Autenticação** | Aplicada via `dependencies=[Depends(Middleware.verify_api_key)]` |
| **Request body** | Definido como classe Pydantic `BaseModel` no próprio arquivo do controller |
| **Tipo de retorno** | Sempre com type hint explícito (ex: `-> Post`, `-> dict[str, str]`) |

### Exemplo: Criando um novo Controller

1. Crie o arquivo `src/rest/controllers/meu_novo_controller.py`:

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from rest.middleware import Middleware

class Body(BaseModel):
    campo: str

class MeuNovoController:
    @staticmethod
    def handle(router: APIRouter) -> None:
        @router.post("/minha-rota", dependencies=[Depends(Middleware.verify_api_key)])
        def _(body: Body) -> dict[str, str]:
            return {"resultado": body.campo}
```

2. Exporte em `src/rest/controllers/__init__.py`:

```python
from .meu_novo_controller import MeuNovoController

__all__ = [..., "MeuNovoController"]
```

3. Registre no `src/rest/router.py`:

```python
MeuNovoController.handle(router)
```

---

## Request Bodies (DTOs de entrada)

Os modelos de requisição são definidos **no próprio arquivo do controller** usando Pydantic `BaseModel`:

```python
from pydantic import BaseModel

class Body(BaseModel):
    category: str
```

### Convenções

- A classe é nomeada como `Body` (nome genérico por arquivo).
- Definida no escopo do módulo do controller, **antes** da classe do controller.
- Aproveite os recursos de validação do Pydantic (validators, constraints, etc.) quando necessário.

---

## Respostas

### Formato de sucesso

- Retorne diretamente a entidade de domínio ou um `dict` com type hint.
- O FastAPI se encarrega da serialização automática (dataclasses e Pydantic são serializados para JSON).

```python
# Retornando entidade de domínio
def _(body: Body) -> Post:
    ...
    return post

# Retornando dict simples
async def _() -> dict[str, str]:
    return {"status": "healthy"}
```

### Formato de erro

Erros são tratados de forma **centralizada** pelo `ExceptionHandler` registrado em `app.py`. O formato padrão de erro é:

```json
{
  "title": "Título do erro",
  "message": "Descrição detalhada do erro"
}
```

**Não use `try/except` nos controllers.** Lance `AppError` nas camadas inferiores (services, workflow, etc.) e o handler global cuidará da resposta:

```python
from errors import AppError

# Em um service ou camada de domínio:
raise AppError("Título do Erro", "Mensagem descritiva")
```

O `ExceptionHandler` retorna status `500` para todos os erros, diferenciando `AppError` de exceções genéricas:

```python
# AppError → {"title": exception.title, "message": exception.message}
# Exception genérica → {"title": "Error", "message": str(exception)}
```

---

## Middleware (`middleware.py`)

Middlewares são implementados como **métodos estáticos** na classe `Middleware`.

### Autenticação via API Key

Todas as rotas são protegidas por autenticação via header `X-Api-Key`. A validação é feita comparando o valor recebido com `ENV.api_key`:

```python
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from constants import ENV

class Middleware:
    @staticmethod
    def verify_api_key(
        api_key: str = Depends(APIKeyHeader(name="X-Api-Key", auto_error=False)),
    ) -> str:
        if api_key != ENV.api_key:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return api_key
```

### Convenções

- Middlewares são aplicados via `dependencies=[Depends(Middleware.metodo)]` no decorator da rota.
- Novos middlewares devem ser adicionados como `@staticmethod` na classe `Middleware`.
- Para autenticação: use `HTTPException(status_code=401)`.

---

## Services (`services/`)

Services encapsulam a **integração com APIs externas** e lógica que não pertence ao domínio da aplicação.

### Convenções

| Convenção | Regra |
|---|---|
| **Nomenclatura do arquivo** | `snake_case` com sufixo `_service.py` — ex: `blog_service.py` |
| **Nomenclatura da classe** | `PascalCase` com sufixo `Service` — ex: `BlogService` |
| **Instanciação** | Feita diretamente no controller (`service = BlogService()`) |
| **HTTP client** | Usar a biblioteca `requests` (importada como `rest_client`) |
| **Timeout** | Sempre definir `timeout=30` (ou valor adequado) nas chamadas HTTP |
| **Stateless** | Services não mantêm estado; cada instância é independente |

### Exemplo

```python
import requests as rest_client
from entities import Post
from constants import ENV

class BlogService:
    def create_post(self, post: Post) -> None:
        rest_client.post(
            f"{ENV.blog_api_url}/posts/create",
            data=form_data,
            timeout=30,
        )

    def get_next_category(self) -> str:
        response = rest_client.get(f"{ENV.blog_api_url}/posts/next", timeout=30)
        data = response.json()
        return data["category"]
```

---

## Padrão de Imports

A camada REST segue um padrão consistente de imports:

```python
# 1. Bibliotecas do framework (FastAPI, Pydantic)
from fastapi import APIRouter, Depends
from pydantic import BaseModel

# 2. Módulos internos do projeto
from ai import Workflow
from entities import Post
from constants import ENV

# 3. Módulos da camada REST
from rest.middleware import Middleware
from rest.services import BlogService
```

### Regras

- **Imports absolutos** para todos os módulos (sem imports relativos, exceto nos `__init__.py`).
- Nos `__init__.py`: usar **imports relativos** com `from .modulo import Classe`.
- Todo `__init__.py` deve definir `__all__` listando as exportações públicas.

---

## Checklist para Novos Endpoints

- [ ] Criar arquivo do controller em `src/rest/controllers/` seguindo a convenção de nome
- [ ] Implementar classe com método estático `handle(router: APIRouter) -> None`
- [ ] Definir `Body` (Pydantic `BaseModel`) se o endpoint aceita request body
- [ ] Aplicar middleware de autenticação via `dependencies=[Depends(Middleware.verify_api_key)]`
- [ ] Definir type hint de retorno explícito no handler
- [ ] Exportar controller no `__init__.py` do diretório `controllers/`
- [ ] Registrar controller no `Router.register()` em `router.py`
- [ ] Se necessário, criar service em `src/rest/services/` para integrações externas
- [ ] Exportar service no `__init__.py` do diretório `services/`
- [ ] Lançar `AppError` para erros de negócio (não usar `try/except` no controller)
