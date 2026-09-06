# 🤖 Agente Recomendador de Conteúdos

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](#-testes)

> Sistema de agente inteligente que recomenda conteúdos personalizados (artigos, vídeos, cursos, podcasts e livros) com base nos interesses e no histórico de interações do usuário.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Motor de Recomendação](#-motor-de-recomendação)
- [Testes](#-testes)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Visão Geral

O **Agente Recomendador de Conteúdos** é um sistema Python que analisa os interesses declarados do usuário e seu histórico de interações para sugerir os conteúdos mais relevantes de um catálogo.

O sistema utiliza um **algoritmo de pontuação próprio** que combina:

| Fator | Peso |
|---|---|
| Correspondência de tags com interesses | `+3.0` por tag |
| Avaliação do conteúdo (rating) | `+1.0 × rating` |
| Bônus para conteúdos curtidos | `+2.0` |
| Penalidade para já visualizados | `-1.5` |
| Penalidade para rejeitados | `-10.0` |

---

## ✨ Funcionalidades

- 🎯 **Recomendação personalizada** baseada em interesses e histórico
- 🔍 **Filtro por tipo** de conteúdo (artigo, vídeo, curso, podcast, livro)
- 📊 **Histórico de interações** (visualizou, curtiu, rejeitou, salvou)
- 🖥️ **Interface CLI interativa** com cores e navegação por menu
- 📁 **Catálogo extensível** via arquivo JSON
- ✅ **Cobertura de testes** com pytest

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│              CLI Interface               │
│          (src/cli/main.py)              │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          Recommendation Engine           │
│       (src/engine/recommender.py)       │
└──────────┬───────────────────┬──────────┘
           │                   │
┌──────────▼──────┐  ┌─────────▼────────┐
│   Data Models   │  │  Content Catalog  │
│  User / Content │  │  (data/*.json)    │
│  History        │  │                   │
└─────────────────┘  └───────────────────┘
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- pip

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/Joloano/agente-recomendador-conteudos.git
cd agente-recomendador-conteudos

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## 💻 Como Usar

### Executar o agente via CLI

```bash
python -m src.cli.main
```

O agente irá:
1. Solicitar seu **nome** e **interesses**
2. Exibir um menu com opções de recomendação
3. Permitir registrar interações com os conteúdos

### Usar o motor de recomendação via código

```python
from src.models.user import User
from src.models.content import Content, ContentType
from src.engine.recommender import Recommender

# Cria um usuário
user = User(user_id="u001", name="João", interests=["python", "machine learning"])

# Cria o catálogo
catalog = [
    Content(
        content_id="c001",
        title="Intro ao ML com Python",
        description="Curso completo de Machine Learning",
        content_type=ContentType.COURSE,
        tags=["python", "machine learning"],
        rating=4.8,
    )
]

# Cria o recomendador e obtém recomendações
recommender = Recommender(catalog=catalog)
recommendations = recommender.recommend(user=user, top_n=3)

for content in recommendations:
    print(f"- {content.title} ({content.content_type.value})")
```

---

## 📁 Estrutura do Projeto

```
agente-recomendador-conteudos/
├── README.md               # Este arquivo
├── CONTRIBUTING.md         # Guia de contribuição
├── requirements.txt        # Dependências Python
├── pyproject.toml          # Configuração do pytest
├── .gitignore              # Arquivos ignorados pelo git
├── src/
│   ├── __init__.py
│   ├── models/             # Modelos de dados
│   │   ├── user.py         # Modelo de usuário
│   │   ├── content.py      # Modelo de conteúdo
│   │   └── history.py      # Modelo de histórico
│   ├── engine/             # Motor de recomendação
│   │   └── recommender.py  # Algoritmo de scoring
│   └── cli/                # Interface de linha de comando
│       └── main.py         # CLI interativa
├── data/
│   └── sample_contents.json  # Dados de exemplo
└── tests/
    ├── test_models.py      # Testes dos modelos
    └── test_recommender.py # Testes do motor
```

---

## ⚙️ Motor de Recomendação

O método `recommend()` aceita os seguintes parâmetros:

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `user` | `User` | obrigatório | Usuário para recomendação |
| `history` | `History` | `None` | Histórico de interações |
| `top_n` | `int` | `5` | Número de recomendações |
| `exclude_disliked` | `bool` | `True` | Exclui rejeitados |

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com relatório de cobertura
pytest --cov=src --cov-report=term-missing

# Rodar testes específicos
pytest tests/test_recommender.py -v
```

---

## 🤝 Contribuindo

Veja o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como contribuir com este projeto.

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">
  Feito com ❤️ por <a href="https://github.com/Joloano">Joloano</a>
</div>
