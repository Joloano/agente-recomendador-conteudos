"""
Interface de linha de comando (CLI) para o Agente Recomendador de Conteúdos.

Uso:
    python -m src.cli.main

O CLI permite interagir com o agente de recomendação de forma interativa,
configurar interesses e receber recomendações personalizadas.
"""

import json
import os
import sys
from pathlib import Path
from typing import List

from src.engine.recommender import Recommender
from src.models.content import Content, ContentType
from src.models.history import History, InteractionType
from src.models.user import User

# Caminho para os dados de exemplo
DATA_PATH = Path(__file__).parent.parent.parent / "data" / "sample_contents.json"

# Cores ANSI para terminal
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"


def _print_header() -> None:
    """Exibe o cabeçalho do agente no terminal."""
    print(f"\n{BOLD}{CYAN}{'=' * 55}{RESET}")
    print(f"{BOLD}{CYAN}   🤖  Agente Recomendador de Conteúdos  🤖{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 55}{RESET}\n")


def _print_content(index: int, content: Content) -> None:
    """Exibe um conteúdo formatado no terminal."""
    type_icon = {
        "article": "📄",
        "video": "🎬",
        "course": "🎓",
        "podcast": "🎙️",
        "book": "📚",
    }.get(content.content_type.value, "📌")

    print(f"  {BOLD}{index}. {type_icon} {content.title}{RESET}")
    print(f"     {BLUE}Tipo:{RESET} {content.content_type.value.capitalize()}")
    print(f"     {BLUE}Autor:{RESET} {content.author or 'Desconhecido'}")
    print(f"     {BLUE}Avaliação:{RESET} {'⭐' * round(content.rating)} ({content.rating:.1f})")
    print(f"     {BLUE}Tags:{RESET} {', '.join(content.tags)}")
    print(f"     {BLUE}URL:{RESET} {content.url or 'N/A'}")
    print(f"     {BLUE}Descrição:{RESET} {content.description[:80]}...")
    print()


def _load_catalog() -> List[Content]:
    """Carrega o catálogo de conteúdos do arquivo JSON."""
    if not DATA_PATH.exists():
        print(f"{YELLOW}⚠️  Arquivo de dados não encontrado: {DATA_PATH}{RESET}")
        return []

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    catalog = []
    for item in raw:
        try:
            content = Content(
                content_id=item["content_id"],
                title=item["title"],
                description=item["description"],
                content_type=ContentType(item["content_type"]),
                tags=item.get("tags", []),
                url=item.get("url", ""),
                author=item.get("author", ""),
                rating=item.get("rating", 0.0),
            )
            catalog.append(content)
        except (KeyError, ValueError) as e:
            print(f"{RED}Erro ao carregar conteúdo: {e}{RESET}")

    return catalog


def _setup_user() -> User:
    """Coleta informações do usuário via input interativo."""
    print(f"{BOLD}📋 Configuração do Perfil{RESET}")
    print("-" * 40)

    name = input(f"  {CYAN}Seu nome:{RESET} ").strip() or "Usuário"
    user_id = name.lower().replace(" ", "_")

    print(f"\n  {CYAN}Informe seus interesses separados por vírgula{RESET}")
    print(f"  {YELLOW}Exemplo: python, machine learning, docker, apis{RESET}")
    interests_input = input(f"  Interesses: ").strip()

    interests = [i.strip().lower() for i in interests_input.split(",") if i.strip()]

    user = User(user_id=user_id, name=name, interests=interests)
    print(f"\n  {GREEN}✅ Perfil criado:{RESET} {name} | Interesses: {', '.join(interests) or 'nenhum'}")
    return user


def run_cli() -> None:
    """Ponto de entrada principal da interface CLI."""
    _print_header()

    # Carrega catálogo
    catalog = _load_catalog()
    if not catalog:
        print(f"{RED}❌ Sem conteúdos disponíveis. Encerrando.{RESET}")
        sys.exit(1)

    print(f"{GREEN}✅ {len(catalog)} conteúdo(s) carregado(s) no catálogo.{RESET}\n")

    # Configura usuário
    user = _setup_user()
    history = History(user_id=user.user_id)
    recommender = Recommender(catalog=catalog)

    while True:
        print(f"\n{BOLD}{'─' * 40}{RESET}")
        print(f"{BOLD}  Menu Principal{RESET}")
        print(f"{'─' * 40}{RESET}")
        print(f"  {CYAN}[1]{RESET} Ver recomendações personalizadas")
        print(f"  {CYAN}[2]{RESET} Filtrar por tipo de conteúdo")
        print(f"  {CYAN}[3]{RESET} Atualizar meus interesses")
        print(f"  {CYAN}[4]{RESET} Ver meu histórico")
        print(f"  {CYAN}[0]{RESET} Sair")
        print()

        choice = input(f"  {BOLD}Escolha:{RESET} ").strip()

        if choice == "1":
            print(f"\n{BOLD}🎯 Recomendações para {user.name}:{RESET}\n")
            recs = recommender.recommend(user=user, history=history, top_n=5)
            if not recs:
                print(f"  {YELLOW}Nenhuma recomendação encontrada. Tente adicionar mais interesses.{RESET}")
            for i, content in enumerate(recs, 1):
                _print_content(i, content)

            # Permite registrar interação
            feedback = input(
                f"  {CYAN}Quer registrar uma interação? (número do item ou Enter para pular):{RESET} "
            ).strip()
            if feedback.isdigit() and 1 <= int(feedback) <= len(recs):
                selected = recs[int(feedback) - 1]
                print(f"  {CYAN}[v] Visualizado  [l] Curtir  [d] Rejeitar  [s] Salvar{RESET}")
                action = input(f"  Ação: ").strip().lower()
                action_map = {
                    "v": InteractionType.VIEWED,
                    "l": InteractionType.LIKED,
                    "d": InteractionType.DISLIKED,
                    "s": InteractionType.SAVED,
                }
                if action in action_map:
                    history.add_interaction(selected.content_id, action_map[action])
                    print(f"  {GREEN}✅ Interação registrada!{RESET}")

        elif choice == "2":
            print(f"\n  Tipos disponíveis: {CYAN}article, video, course, podcast, book{RESET}")
            content_type = input(f"  Tipo desejado: ").strip().lower()
            recs = recommender.recommend_by_type(user=user, content_type=content_type, history=history)
            if not recs:
                print(f"  {YELLOW}Nenhum conteúdo do tipo '{content_type}' encontrado.{RESET}")
            else:
                print(f"\n{BOLD}🎯 Recomendações do tipo '{content_type}':{RESET}\n")
                for i, content in enumerate(recs, 1):
                    _print_content(i, content)

        elif choice == "3":
            print(f"  {YELLOW}Interesses atuais:{RESET} {', '.join(user.interests) or 'nenhum'}")
            new_interests = input(f"  {CYAN}Novos interesses (separados por vírgula):{RESET} ").strip()
            user.interests = [i.strip().lower() for i in new_interests.split(",") if i.strip()]
            print(f"  {GREEN}✅ Interesses atualizados!{RESET}")

        elif choice == "4":
            print(f"\n{BOLD}📊 Histórico de {user.name}:{RESET}")
            if not history.interactions:
                print(f"  {YELLOW}Nenhuma interação registrada ainda.{RESET}")
            else:
                for interaction in history.interactions:
                    print(
                        f"  • {interaction.content_id} | "
                        f"{interaction.interaction_type.value} | "
                        f"{interaction.timestamp.strftime('%d/%m/%Y %H:%M')}"
                    )

        elif choice == "0":
            print(f"\n{BOLD}{GREEN}👋 Até logo, {user.name}! Continue aprendendo!{RESET}\n")
            break

        else:
            print(f"  {RED}❌ Opção inválida. Tente novamente.{RESET}")


if __name__ == "__main__":
    run_cli()
