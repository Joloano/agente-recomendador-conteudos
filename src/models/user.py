"""
Modelo de dados para representar um usuário do sistema.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    """
    Representa um usuário do agente recomendador.

    Attributes:
        user_id (str): Identificador único do usuário.
        name (str): Nome do usuário.
        interests (List[str]): Lista de categorias de interesse do usuário.
        email (str): E-mail do usuário (opcional).
    """

    user_id: str
    name: str
    interests: List[str] = field(default_factory=list)
    email: str = ""

    def add_interest(self, interest: str) -> None:
        """Adiciona um interesse à lista do usuário, evitando duplicatas."""
        interest = interest.strip().lower()
        if interest and interest not in self.interests:
            self.interests.append(interest)

    def remove_interest(self, interest: str) -> bool:
        """
        Remove um interesse da lista do usuário.

        Returns:
            bool: True se removido com sucesso, False se não encontrado.
        """
        interest = interest.strip().lower()
        if interest in self.interests:
            self.interests.remove(interest)
            return True
        return False

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, name={self.name!r}, interests={self.interests})"
