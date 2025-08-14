<h1 align="center">
  NewsAI 🤖📰
</h1>

<div align="center">
   <a href="https://github.com/JohnPetros">
      <img alt="Made by JohnPetros" src="https://img.shields.io/badge/made%20by-JohnPetros-blueviolet">
   </a>
   <img alt="GitHub Language Count" src="https://img.shields.io/github/languages/count/JohnPetros/newsAI">
   <a href="https://github.com/JohnPetros/newsAI/commits/main">
      <img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/JohnPetros/newsAI">
   </a>
   <a href="https://github.com/JohnPetros/newsAI/blob/main/LICENSE.md">
      <img alt="GitHub License" src="https://img.shields.io/github/license/JohnPetros/newsAI">
   </a>
   <img alt="Stargazers" src="https://img.shields.io/github/stars/JohnPetros/newsAI?style=social">
</div>
<br>

## 🖥️ About the Project

NewsAI is an intelligent automated content generation application for blogs that
uses artificial intelligence to create complete posts about news and specific
topics.

The system works through a team of specialized AI agents that work together to
research, analyze, write, and optimize journalistic content in Brazilian
Portuguese, offering an automated solution for quality content creation.

---

## ✨ Features

### ✅ Functional Requirements

#### Automated Post Generation

- [x] Must be possible to generate complete posts about specific topics
- [x] Each post must contain:
  - SEO-optimized title
  - Content in HTML format
  - Relevant tags for categorization
  - Estimated reading time
  - Original news URL
  - Alternative description for generated image
- [x] Content must be generated in Brazilian Portuguese
- [x] Must be possible to specify the post category

#### AI Agents System

- [x] **Researcher Agent**: Searches for the most relevant news about the topic
- [x] **Editor Agent**: Optimizes and makes content more engaging
- [x] **Scrapper Agent**: Extracts complete content from the news
- [x] **Writer Agent**: Creates the blog post based on the news
- [x] **Tagger Agent**: Generates relevant tags for categorization
- [x] **Image Generator Agent**: Creates alternative descriptions for images

#### External APIs Integration

- [x] Must be possible to integrate with existing blog APIs
- [x] Must be possible to use search APIs for news research
- [x] Must be possible to use AI APIs for content generation
- [x] Must be possible to use image generation APIs

#### REST API

- [x] Must provide endpoint for post generation
- [x] Must include API key authentication system
- [x] Must return responses in JSON format
- [x] Must include adequate error handling

### ☑️ Non-Functional Requirements

#### Performance and Scalability

- [x] Must be possible to run multiple generations simultaneously
- [x] Must implement automatic retry in case of failures
- [x] Must be optimized for production use

#### Security

- [x] Must validate all data inputs
- [x] Must implement API key authentication
- [x] Must protect against common attacks

#### Monitoring

- [x] Must include detailed logs for debugging
- [x] Must provide information about API status
- [x] Must include performance metrics

---

## ⚙️ Architecture

### 🛠️ Technologies, tools and external services

This project was developed using the following technologies:

✔️ **[FastAPI](https://fastapi.tiangolo.com/)** for high-performance REST API
development

✔️ **[Python 3.10+](https://www.python.org/)** as the main programming language

✔️ **[Agno](https://github.com/agno-ai/agno)** for AI agents team orchestration

✔️ **[Google Gemini](https://ai.google.dev/)** as the main language model

✔️ **[AgentQL](https://agentql.com/)** for advanced AI tools

✔️ **[Pydantic](https://docs.pydantic.dev/)** for data validation and
serialization

✔️ **[Uvicorn](https://www.uvicorn.org/)** as high-performance ASGI server

✔️ **[Playwright](https://playwright.dev/)** for advanced web scraping

✔️ **[DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)** for news
research

✔️ **[Google Search](https://pypi.org/project/googlesearch-python/)** for
advanced search

✔️ **[UV](https://github.com/astral-sh/uv)** as optimized Python package manager

✔️ **[Docker](https://www.docker.com/)** for containerization and deployment

> For more details about project dependencies, such as specific versions, see
> the
> [pyproject.toml](https://github.com/JohnPetros/newsAI/blob/main/pyproject.toml)
> file

---

## 🚀 How to run the application?

### 🔧 Prerequisites

Before downloading the project, you will need to have the following tools
installed on your machine:

- [Git](https://git-scm.com/)
- [Python 3.10+](https://www.python.org/downloads/)
- [UV](https://github.com/astral-sh/uv) (Python package manager)
- [Docker](https://www.docker.com/) (optional, for containerization)

> It's also good to have an editor to work with the code, such as
> [VSCode](https://code.visualstudio.com/)

> It's crucial to configure environment variables in a file called `.env` before
> running the application. See the configuration section below to see which
> variables should be configured

### 📟 Running the application

#### Using UV (Recommended)

```bash
# Clone this repository
$ git clone https://github.com/JohnPetros/newsAI.git

# Access the project folder
$ cd newsAI

# Install dependencies
$ uv sync

# Run the application in development mode
$ uv run python src/main.py
```

#### Using Docker

```bash
# Clone this repository
$ git clone https://github.com/JohnPetros/newsAI.git

# Access the project folder
$ cd newsAI

# Run with Docker
$ docker-compose up -d
```

> See the [Docker documentation](DOCKER.md) for more details on how to use
> Docker with this project

### 🔑 Environment Variables Configuration

Create a `.env` file in the project root with the following variables:

```env
# Server configuration
HOST=0.0.0.0
PORT=8000

# External APIs (REQUIRED)
BLOG_API_URL=https://api.blog.com
GOOGLE_API_KEY=your_google_api_key_here
AGENTQL_API_KEY=your_agentql_api_key_here

# Optional APIs
TAVILY_API_KEY=your_tavily_api_key_here
```

#### Required Variables

- `BLOG_API_URL`: Blog API URL for integration
- `GOOGLE_API_KEY`: Google API key for Gemini
- `AGENTQL_API_KEY`: AgentQL API key for advanced tools

#### Optional Variables

- `HOST`: Application host (default: 0.0.0.0)
- `PORT`: Application port (default: 8000)

### 🧪 Running tests

```bash
# Run tests
$ uv run pytest

# Run with coverage
$ uv run pytest --cov=src
```

### 🎮 Playground and Experimentation

```bash
# Run playground for interactive testing
$ uv run python src/playground.py

# Run Google GenAI tests
$ uv run python src/genai.py
```

---

## 💪 How to contribute

```bash
# Fork this repository
$ git clone https://github.com/JohnPetros/newsAI.git

# Create a branch with your feature
$ git checkout -b my-feature

# Commit your changes:
$ git commit -m 'feat: My feature'

# Push your branch:
$ git push origin my-feature
```

> You should replace 'my-feature' with the name of the feature you are adding

> See my
> [emoji list for each commit type](https://gist.github.com/JohnPetros/1f63f8cf07c719c5d2c5e011e2eac770)
> that I'm using to maintain consistency between commit messages

> You can also open a [new issue](https://github.com/JohnPetros/newsAI/issues)
> regarding any problem, question or suggestion for the project. I'll be happy
> to help, as well as improve this project

---

## 🎨 Layout

The project was developed following software architecture best practices, with a
modular and well-organized structure:

```
src/
├── ai/                    # AI agents and workflows
│   ├── agents/           # Specialized agents
│   └── tools/            # AI tools
├── entities/              # Data models
├── rest/                  # REST API
│   ├── controllers/       # API controllers
│   └── services/          # Business services
├── errors/                # Error handling
└── constants/             # Application constants
```

---

## 📝 License

This application is under MIT license. See the [License file](LICENSE) for more
details.

---

<p align="center">
  Made with 💜 by John Petros 👋🏻
</p>
