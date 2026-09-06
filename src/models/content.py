"""
Modelo de dados para representar um conteúdo recomendável.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class ContentType(Enum):
    """Tipos de conteúdo suportados pelo sistema."""

    ARTICLE = "article"
    VIDEO = "video"
    COURSE = "course"
    PODCAST = "podcast"
    BOOK = "book"


@dataclass
class Content:
    """
    Representa um conteúdo disponível para recomendação.

    Attributes:
        content_id (str): Identificador único do conteúdo.
        title (str): Título do conteúdo.
        description (str): Descrição ou resumo do conteúdo.
        content_type (ContentType): Tipo do conteúdo (artigo, vídeo, curso, etc.).
        tags (List[str]): Tags/categorias associadas ao conteúdo.
        url (str): URL de acesso ao conteúdo.
        author (str): Autor ou criador do conteúdo.
        rating (float): Avaliação média do conteúdo (0.0 a 5.0).
    """

    content_id: str
    title: str
    description: str
    content_type: ContentType
    tags: List[str] = field(default_factory=list)
    url: str = ""
    author: str = ""
    rating: float = 0.0

    def __post_init__(self) -> None:
        """Normaliza as tags para letras minúsculas."""
        self.tags = [tag.strip().lower() for tag in self.tags]
        if not (0.0 <= self.rating <= 5.0):
            raise ValueError(f"Rating deve estar entre 0.0 e 5.0, recebido: {self.rating}")

    def matches_interests(self, interests: List[str]) -> bool:
        """
        Verifica se o conteúdo corresponde a pelo menos um interesse do usuário.

        Args:
            interests: Lista de interesses do usuário.

        Returns:
            bool: True se houver interseção entre tags e interesses.
        """
        normalized = [i.strip().lower() for i in interests]
        return bool(set(self.tags) & set(normalized))

    def __repr__(self) -> str:
        return f"Content(id={self.content_id!r}, title={self.title!r}, type={self.content_type.value})"
