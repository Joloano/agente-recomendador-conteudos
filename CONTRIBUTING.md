# 🤝 Guia de Contribuição

Obrigado pelo interesse em contribuir com o **Agente Recomendador de Conteúdos**! Este documento descreve o processo para contribuir de forma eficiente e organizada.

---

## 📋 Índice

- [Como Reportar um Bug](#-como-reportar-um-bug)
- [Como Sugerir uma Melhoria](#-como-sugerir-uma-melhoria)
- [Fluxo de Trabalho com Git](#-fluxo-de-trabalho-com-git)
- [Padrões de Código](#-padrões-de-código)
- [Convenções de Commits](#-convenções-de-commits)
- [Testes](#-testes)
- [Pull Requests](#-pull-requests)

---

## 🐛 Como Reportar um Bug

1. Verifique se o bug **já não foi reportado** nas [Issues abertas](https://github.com/Joloano/agente-recomendador-conteudos/issues).
2. Abra uma **nova Issue** com:
   - Título claro e descritivo
   - Passos para reproduzir o bug
   - Comportamento esperado vs. comportamento atual
   - Versão do Python e do sistema operacional

---

## 💡 Como Sugerir uma Melhoria

1. Abra uma **Issue** com o label `enhancement`.
2. Descreva claramente a funcionalidade desejada.
3. Explique o caso de uso e o benefício esperado.

---

## 🌿 Fluxo de Trabalho com Git

Usamos o **GitHub Flow** simplificado:

```
main (produção estável)
└── feature/<nome>     (nova funcionalidade)
└── fix/<nome>         (correção de bug)
└── docs/<nome>        (documentação)
└── test/<nome>        (testes)
└── refactor/<nome>    (refatoração)
```

### Passo a passo

```bash
# 1. Crie uma branch a partir de main
git checkout main
git pull origin main
git checkout -b feature/minha-feature

# 2. Faça suas alterações e commits
git add .
git commit -m "feat: adiciona nova funcionalidade X"

# 3. Push e abra um Pull Request
git push origin feature/minha-feature
```

---

## 🧹 Padrões de Código

- **PEP 8**: Seguimos o guia de estilo PEP 8 para Python.
- **Docstrings**: Toda função e classe pública deve ter docstring no formato Google Style.
- **Type hints**: Use type hints em todas as funções.
- **Nomes em inglês**: Variáveis, funções e classes devem ser nomeadas em inglês.

### Exemplo de função bem documentada

```python
def recommend(
    self,
    user: User,
    history: Optional[History] = None,
    top_n: int = 5,
) -> List[Content]:
    """
    Retorna os top-N conteúdos recomendados para o usuário.

    Args:
        user: Usuário que receberá as recomendações.
        history: Histórico de interações do usuário.
        top_n: Número máximo de recomendações a retornar.

    Returns:
        List[Content]: Lista de conteúdos ordenados por relevância decrescente.
    """
```

---

## 📝 Convenções de Commits

Seguimos o padrão **Conventional Commits**:

```
<tipo>(<escopo opcional>): <descrição curta>

[corpo opcional com mais detalhes]

[rodapé: Closes #<número da issue>]
```

### Tipos de commit

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `test` | Testes |
| `refactor` | Refatoração sem mudança de comportamento |
| `chore` | Configuração, build, CI |
| `style` | Formatação (sem mudança de lógica) |

### Exemplos

```bash
git commit -m "feat: add recommendation by content type"
git commit -m "fix: prevent duplicate interests in User model"
git commit -m "docs: update README with API usage examples"
git commit -m "test: add unit tests for scoring algorithm"
```

---

## 🧪 Testes

- Todo novo código deve vir acompanhado de **testes unitários**.
- Os testes ficam na pasta `tests/`.
- Use `pytest` para rodar os testes:

```bash
pytest --cov=src --cov-report=term-missing
```

- A cobertura mínima aceitável é **80%**.

---

## 🔍 Pull Requests

1. Certifique-se de que os **testes passam** antes de abrir o PR.
2. Preencha o **template de PR** com:
   - Descrição das mudanças
   - Issue relacionada (`Closes #<número>`)
   - Screenshots (se aplicável)
3. Aguarde a revisão de ao menos **1 aprovação** antes do merge.
4. Use **Squash and Merge** para manter o histórico limpo.

---

Agradecemos sua contribuição! 🚀
