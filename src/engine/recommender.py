"""
Motor de recomendação baseado em correspondência de interesses e histórico do usuário.
"""

from typing import List, Optional

from src.models.content import Content
from src.models.history import History, InteractionType
from src.models.user import User


class Recommender:
    """
    Motor de recomendação de conteúdos.

    Utiliza um sistema de pontuação baseado em:
    - Correspondência entre tags do conteúdo e interesses do usuário.
    - Avaliação (rating) do conteúdo.
    - Penalidade para conteúdos já visualizados ou rejeitados.
    - Bônus para conteúdos curtidos pelo usuário (reforço positivo).

    Attributes:
        catalog (List[Content]): Catálogo completo de conteúdos disponíveis.
    """

    # Pesos usados no cálculo da pontuação
    WEIGHT_INTEREST_MATCH = 3.0
    WEIGHT_RATING = 1.0
    BONUS_LIKED = 2.0
    PENALTY_VIEWED = 1.5
    PENALTY_DISLIKED = 10.0

    def __init__(self, catalog: Optional[List[Content]] = None) -> None:
        """
        Inicializa o motor de recomendação.

        Args:
            catalog: Lista de conteúdos disponíveis para recomendação.
        """
        self.catalog: List[Content] = catalog or []

    def add_content(self, content: Content) -> None:
        """Adiciona um conteúdo ao catálogo."""
        self.catalog.append(content)

    def _score(self, content: Content, user: User, history: Optional[History] = None) -> float:
        """
        Calcula a pontuação de relevância de um conteúdo para um usuário.

        Args:
            content: Conteúdo a ser avaliado.
            user: Usuário para o qual calcular a relevância.
            history: Histórico de interações do usuário (opcional).

        Returns:
            float: Pontuação de relevância (maior = mais relevante).
        """
        score = 0.0

        # Pontuação por correspondência de interesse
        matched_tags = set(content.tags) & set(
            [i.strip().lower() for i in user.interests]
        )
        score += len(matched_tags) * self.WEIGHT_INTEREST_MATCH

        # Pontuação pela avaliação do conteúdo
        score += content.rating * self.WEIGHT_RATING

        if history:
            # Bônus por conteúdo similar a curtidos
            liked_ids = set(history.get_liked_ids())
            if content.content_id in liked_ids:
                score += self.BONUS_LIKED

            # Penalidade para já visualizados
            viewed_ids = set(history.get_viewed_ids())
            if content.content_id in viewed_ids:
                score -= self.PENALTY_VIEWED

            # Penalidade forte para rejeitados
            disliked_ids = set(history.get_disliked_ids())
            if content.content_id in disliked_ids:
                score -= self.PENALTY_DISLIKED

        return score

    def recommend(
        self,
        user: User,
        history: Optional[History] = None,
        top_n: int = 5,
        exclude_disliked: bool = True,
    ) -> List[Content]:
        """
        Retorna os top-N conteúdos recomendados para o usuário.

        Args:
            user: Usuário que receberá as recomendações.
            history: Histórico de interações do usuário.
            top_n: Número máximo de recomendações a retornar.
            exclude_disliked: Se True, exclui conteúdos rejeitados das recomendações.

        Returns:
            List[Content]: Lista de conteúdos ordenados por relevância decrescente.
        """
        disliked_ids: set = set()
        if history and exclude_disliked:
            disliked_ids = set(history.get_disliked_ids())

        scored = [
            (content, self._score(content, user, history))
            for content in self.catalog
            if content.content_id not in disliked_ids
        ]

        # Ordena por pontuação decrescente
        scored.sort(key=lambda x: x[1], reverse=True)

        return [content for content, _ in scored[:top_n]]

    def recommend_by_type(
        self,
        user: User,
        content_type: str,
        history: Optional[History] = None,
        top_n: int = 3,
    ) -> List[Content]:
        """
        Retorna recomendações filtradas por tipo de conteúdo.

        Args:
            user: Usuário que receberá as recomendações.
            content_type: Tipo de conteúdo desejado (ex: 'video', 'article').
            history: Histórico de interações do usuário.
            top_n: Número máximo de recomendações a retornar.

        Returns:
            List[Content]: Lista de conteúdos do tipo solicitado ordenados por relevância.
        """
        filtered_catalog = [
            c for c in self.catalog if c.content_type.value == content_type.lower()
        ]
        temp_recommender = Recommender(catalog=filtered_catalog)
        return temp_recommender.recommend(user=user, history=history, top_n=top_n)
