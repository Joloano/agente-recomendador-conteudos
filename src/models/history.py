"""
Modelo de dados para representar o histórico de interações do usuário.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class InteractionType(Enum):
    """Tipos de interação do usuário com um conteúdo."""

    VIEWED = "viewed"
    LIKED = "liked"
    DISLIKED = "disliked"
    SAVED = "saved"
    SHARED = "shared"


@dataclass
class Interaction:
    """
    Representa uma interação específica entre usuário e conteúdo.

    Attributes:
        content_id (str): ID do conteúdo com o qual o usuário interagiu.
        interaction_type (InteractionType): Tipo de interação.
        timestamp (datetime): Momento da interação.
    """

    content_id: str
    interaction_type: InteractionType
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class History:
    """
    Mantém o histórico completo de interações de um usuário.

    Attributes:
        user_id (str): ID do usuário dono do histórico.
        interactions (List[Interaction]): Lista de interações registradas.
    """

    user_id: str
    interactions: List[Interaction] = field(default_factory=list)

    def add_interaction(
        self,
        content_id: str,
        interaction_type: InteractionType,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """
        Registra uma nova interação no histórico.

        Args:
            content_id: ID do conteúdo.
            interaction_type: Tipo de interação realizada.
            timestamp: Momento da interação (usa horário atual se não informado).
        """
        interaction = Interaction(
            content_id=content_id,
            interaction_type=interaction_type,
            timestamp=timestamp or datetime.now(),
        )
        self.interactions.append(interaction)

    def get_viewed_ids(self) -> List[str]:
        """Retorna IDs de todos os conteúdos já visualizados."""
        return [
            i.content_id
            for i in self.interactions
            if i.interaction_type == InteractionType.VIEWED
        ]

    def get_liked_ids(self) -> List[str]:
        """Retorna IDs de todos os conteúdos curtidos."""
        return [
            i.content_id
            for i in self.interactions
            if i.interaction_type == InteractionType.LIKED
        ]

    def get_disliked_ids(self) -> List[str]:
        """Retorna IDs de todos os conteúdos rejeitados."""
        return [
            i.content_id
            for i in self.interactions
            if i.interaction_type == InteractionType.DISLIKED
        ]

    def has_interacted(self, content_id: str) -> bool:
        """Verifica se o usuário já interagiu com o conteúdo."""
        return any(i.content_id == content_id for i in self.interactions)

    def __repr__(self) -> str:
        return f"History(user_id={self.user_id!r}, interactions={len(self.interactions)})"
