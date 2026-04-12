# Core Layer — Guia de Padrões e Convenções

Este documento descreve a arquitetura, padrões e convenções utilizados na camada Core (`src/core`) do projeto. A camada Core representa o **núcleo do domínio** da aplicação — é a camada mais interna e não deve depender de nenhuma outra camada (REST, AI, PubSub, etc.).

---

## Visão Geral da Arquitetura

A camada Core contém as definições fundamentais do domínio: entidades de dados e erros da aplicação.

```
src/core/
├── entities/            # Entidades de domínio (modelos de dados)
│   ├── __init__.py
│   └── post.py
└── errors/              # Erros customizados da aplicação
    ├── __init__.py
    └── app_error.py
```

### Princípio Fundamental

A camada Core é **independente de framework e infraestrutura**. Ela não importa FastAPI, requests, ou qualquer biblioteca de infraestrutura. Apenas bibliotecas utilitárias de tipagem/validação (como Pydantic) são permitidas.

```
                  ┌─────────────┐
                  │    Core     │  ← Não depende de nada externo
                  │ (entities,  │
                  │   errors)   │
                  └──────▲──────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────┴─────┐  ┌────┴────┐  ┌─────┴─────┐
    │   REST    │  │   AI    │  │  PubSub   │
    │  (camada  │  │ (camada │  │  (camada  │
    │  externa) │  │  de IA) │  │  eventos) │
    └───────────┘  └─────────┘  └───────────┘
```

---

## Entidades (`entities/`)

Entidades representam os **objetos de dados centrais** do domínio. São estruturas imutáveis que definem o formato dos dados que transitam entre as camadas da aplicação.

### Padrão de Implementação

Entidades são implementadas usando **Pydantic dataclasses** (`pydantic.dataclasses.dataclass`), o que garante validação automática de tipos em tempo de execução:

```python
from pydantic.dataclasses import dataclass


@dataclass
class Post:
    title: str
    content: str
    category: str
    reading_time: int
    image_alt: str
    tags: list[str]
```

### Convenções

| Convenção | Regra |
|---|---|
| **Decorator** | `@dataclass` importado de `pydantic.dataclasses` (não de `dataclasses` stdlib) |
| **Nomenclatura do arquivo** | `snake_case` com o nome da entidade — ex: `post.py` |
| **Nomenclatura da classe** | `PascalCase` representando o substantivo do domínio — ex: `Post` |
| **Atributos** | `snake_case` com type hints explícitos em todos os campos |
| **Tipos compostos** | Usar generics nativos do Python — ex: `list[str]`, `dict[str, int]` |
| **Sem lógica** | Entidades são **objetos de dados puros** — não contêm métodos de negócio |
| **Sem dependências** | Não importam módulos de outras camadas (REST, AI, etc.) |

### Por que Pydantic Dataclasses?

Diferente das `dataclasses` padrão do Python, Pydantic dataclasses oferecem:

- **Validação automática** de tipos em tempo de execução (ex: passar `"abc"` para um campo `int` lança erro)
- **Serialização nativa** com FastAPI — entidades retornadas por controllers são automaticamente convertidas para JSON
- **Compatibilidade** com o ecossistema Pydantic (schemas OpenAPI, validators, etc.)

### Exemplo: Criando uma Nova Entidade

1. Crie o arquivo `src/core/entities/minha_entidade.py`:

```python
from pydantic.dataclasses import dataclass


@dataclass
class MinhaEntidade:
    nome: str
    descricao: str
    ativo: bool
    itens: list[str]
```

2. Exporte no `src/core/entities/__init__.py`:

```python
from .minha_entidade import MinhaEntidade

__all__ = [..., "MinhaEntidade"]
```

---

## Erros (`errors/`)

Erros customizados definem as **exceções de domínio** da aplicação. São lançados por qualquer camada quando uma regra de negócio é violada ou um erro esperado ocorre.

### Padrão de Implementação

Erros estendem `Exception` e possuem campos estruturados:

```python
class AppError(Exception):
    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
```

### Convenções

| Convenção | Regra |
|---|---|
| **Nomenclatura do arquivo** | `snake_case` com sufixo `_error.py` — ex: `app_error.py` |
| **Nomenclatura da classe** | `PascalCase` com sufixo `Error` — ex: `AppError` |
| **Herança** | Estender `Exception` (ou outro erro customizado do Core) |
| **Campos** | `title` (título curto) e `message` (descrição detalhada) |
| **Type hints** | Todos os parâmetros do `__init__` devem ter type hints |
| **Retorno do init** | Sempre anotar com `-> None` |

### Estrutura do Erro

Todos os erros seguem o contrato com dois campos:

| Campo | Tipo | Descrição |
|---|---|---|
| `title` | `str` | Identificador curto do tipo de erro (ex: `"AI Error"`, `"Validation Error"`) |
| `message` | `str` | Descrição detalhada do que aconteceu |

Esse contrato é consumido pelo `ExceptionHandler` global, que serializa os erros para a resposta HTTP:

```json
{
  "title": "AI Error",
  "message": "No response from the news writing team"
}
```

### Como Lançar Erros

Erros do Core devem ser **lançados nas camadas que executam lógica** (AI, Services, etc.), nunca nos controllers:

```python
from core.errors import AppError

# Em um service ou workflow:
raise AppError("AI Error", str(exception))

# Encadeando a exceção original (preserva o traceback):
raise AppError("AI Error", str(exception)) from exception
```

### Exemplo: Criando um Novo Tipo de Erro

Se necessário especializar tipos de erro, crie uma subclasse:

1. Crie o arquivo `src/core/errors/validation_error.py`:

```python
class ValidationError(Exception):
    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
```

2. Exporte no `src/core/errors/__init__.py`:

```python
from .validation_error import ValidationError

__all__ = [..., "ValidationError"]
```

3. Registre o handler em `app.py` se necessário tratamento HTTP diferenciado.

---

## Padrão de Imports

### Importando a camada Core de outras camadas

Todas as camadas externas devem importar a partir do **pacote público** (via `__init__.py`), nunca diretamente do módulo interno:

```python
# Correto — importar pelo pacote
from core.entities import Post
from core.errors import AppError

# Incorreto — importar diretamente do módulo interno
from core.entities.post import Post
from core.errors.app_error import AppError
```

### Imports internos (dentro da camada Core)

Dentro dos arquivos `__init__.py`, usar **imports relativos**:

```python
# Em core/entities/__init__.py
from .post import Post

__all__ = ["Post"]
```

### Regra de `__all__`

Todo `__init__.py` na camada Core **deve** definir `__all__` listando explicitamente todos os símbolos públicos exportados. Isso garante controle explícito sobre a API pública do módulo.

---

## Regras de Dependência

A camada Core obedece à **regra de dependência invertida**: camadas externas dependem do Core, mas o Core nunca depende de camadas externas.

### Permitido no Core

- `pydantic` — para validação e dataclasses
- Módulos da stdlib do Python (`typing`, `dataclasses`, `enum`, etc.)
- Outros módulos dentro do próprio `core/`

### Proibido no Core

- `fastapi`, `requests`, ou qualquer framework web
- Módulos de outras camadas (`rest`, `ai`, `pubsub`, `constants`)
- Bibliotecas de infraestrutura (banco de dados, mensageria, etc.)

---

## Checklist para Novos Artefatos no Core

### Nova Entidade

- [ ] Criar arquivo em `src/core/entities/` com nomenclatura `snake_case.py`
- [ ] Usar `@dataclass` de `pydantic.dataclasses` (não da stdlib)
- [ ] Definir todos os campos com type hints explícitos
- [ ] Não incluir lógica de negócio ou dependências externas
- [ ] Exportar no `__init__.py` com import relativo
- [ ] Adicionar ao `__all__`

### Novo Erro

- [ ] Criar arquivo em `src/core/errors/` com sufixo `_error.py`
- [ ] Estender `Exception` com campos `title: str` e `message: str`
- [ ] Anotar `__init__` com type hints e `-> None`
- [ ] Exportar no `__init__.py` com import relativo
- [ ] Adicionar ao `__all__`
- [ ] Registrar handler em `app.py` se necessário tratamento HTTP especial
