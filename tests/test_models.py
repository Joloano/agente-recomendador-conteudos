"""
Testes unitários para os modelos de dados: User, Content e History.
"""

import pytest
from datetime import datetime

from src.models.content import Content, ContentType
from src.models.history import History, InteractionType
from src.models.user import User


# ─────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def sample_user() -> User:
    """Usuário de exemplo para os testes."""
    return User(
        user_id="u001",
        name="Test User",
        interests=["python", "machine learning"],
        email="test@example.com",
    )


@pytest.fixture
def sample_content() -> Content:
    """Conteúdo de exemplo para os testes."""
    return Content(
        content_id="c001",
        title="Intro ao ML",
        description="Curso introdutório de Machine Learning",
        content_type=ContentType.COURSE,
        tags=["python", "machine learning", "data science"],
        url="https://example.com/ml",
        author="Ana Silva",
        rating=4.8,
    )


@pytest.fixture
def sample_history() -> History:
    """Histórico de exemplo para os testes."""
    return History(user_id="u001")


# ─────────────────────────────────────────────────────────────
# Testes: User
# ─────────────────────────────────────────────────────────────

class TestUser:
    """Testes para o modelo User."""

    def test_create_user(self, sample_user: User) -> None:
        """Verifica a criação correta de um usuário."""
        assert sample_user.user_id == "u001"
        assert sample_user.name == "Test User"
        assert "python" in sample_user.interests

    def test_add_interest(self, sample_user: User) -> None:
        """Verifica a adição de novos interesses."""
        sample_user.add_interest("Docker")
        assert "docker" in sample_user.interests

    def test_add_duplicate_interest(self, sample_user: User) -> None:
        """Verifica que interesses duplicados não são adicionados."""
        original_count = len(sample_user.interests)
        sample_user.add_interest("Python")  # já existe como 'python'
        assert len(sample_user.interests) == original_count

    def test_remove_interest(self, sample_user: User) -> None:
        """Verifica a remoção de um interesse existente."""
        result = sample_user.remove_interest("python")
        assert result is True
        assert "python" not in sample_user.interests

    def test_remove_nonexistent_interest(self, sample_user: User) -> None:
        """Verifica que remover interesse inexistente retorna False."""
        result = sample_user.remove_interest("java")
        assert result is False

    def test_add_empty_interest(self, sample_user: User) -> None:
        """Verifica que interesses vazios são ignorados."""
        original_count = len(sample_user.interests)
        sample_user.add_interest("   ")
        assert len(sample_user.interests) == original_count

    def test_user_repr(self, sample_user: User) -> None:
        """Verifica a representação em string do usuário."""
        repr_str = repr(sample_user)
        assert "u001" in repr_str
        assert "Test User" in repr_str


# ─────────────────────────────────────────────────────────────
# Testes: Content
# ─────────────────────────────────────────────────────────────

class TestContent:
    """Testes para o modelo Content."""

    def test_create_content(self, sample_content: Content) -> None:
        """Verifica a criação correta de um conteúdo."""
        assert sample_content.content_id == "c001"
        assert sample_content.content_type == ContentType.COURSE
        assert sample_content.rating == 4.8

    def test_tags_normalized_to_lowercase(self) -> None:
        """Verifica que as tags são normalizadas para minúsculas."""
        content = Content(
            content_id="c002",
            title="Test",
            description="Test",
            content_type=ContentType.ARTICLE,
            tags=["Python", "DOCKER", "FastAPI"],
        )
        assert "python" in content.tags
        assert "docker" in content.tags
        assert "fastapi" in content.tags

    def test_invalid_rating_raises_error(self) -> None:
        """Verifica que rating inválido levanta ValueError."""
        with pytest.raises(ValueError, match="Rating deve estar entre"):
            Content(
                content_id="c003",
                title="Test",
                description="Test",
                content_type=ContentType.VIDEO,
                rating=6.0,  # inválido
            )

    def test_matches_interests_true(self, sample_content: Content) -> None:
        """Verifica que matches_interests retorna True quando há interseção."""
        assert sample_content.matches_interests(["python", "devops"]) is True

    def test_matches_interests_false(self, sample_content: Content) -> None:
        """Verifica que matches_interests retorna False sem interseção."""
        assert sample_content.matches_interests(["javascript", "react"]) is False

    def test_matches_interests_empty_list(self, sample_content: Content) -> None:
        """Verifica que matches_interests retorna False com lista vazia."""
        assert sample_content.matches_interests([]) is False

    def test_content_type_enum_values(self) -> None:
        """Verifica os valores do enum ContentType."""
        assert ContentType.ARTICLE.value == "article"
        assert ContentType.VIDEO.value == "video"
        assert ContentType.COURSE.value == "course"
        assert ContentType.PODCAST.value == "podcast"
        assert ContentType.BOOK.value == "book"


# ─────────────────────────────────────────────────────────────
# Testes: History
# ─────────────────────────────────────────────────────────────

class TestHistory:
    """Testes para o modelo History."""

    def test_create_history(self, sample_history: History) -> None:
        """Verifica a criação de um histórico vazio."""
        assert sample_history.user_id == "u001"
        assert len(sample_history.interactions) == 0

    def test_add_interaction(self, sample_history: History) -> None:
        """Verifica o registro de uma interação."""
        sample_history.add_interaction("c001", InteractionType.VIEWED)
        assert len(sample_history.interactions) == 1

    def test_get_viewed_ids(self, sample_history: History) -> None:
        """Verifica a recuperação de IDs de conteúdos visualizados."""
        sample_history.add_interaction("c001", InteractionType.VIEWED)
        sample_history.add_interaction("c002", InteractionType.LIKED)
        assert "c001" in sample_history.get_viewed_ids()
        assert "c002" not in sample_history.get_viewed_ids()

    def test_get_liked_ids(self, sample_history: History) -> None:
        """Verifica a recuperação de IDs de conteúdos curtidos."""
        sample_history.add_interaction("c001", InteractionType.LIKED)
        assert "c001" in sample_history.get_liked_ids()

    def test_get_disliked_ids(self, sample_history: History) -> None:
        """Verifica a recuperação de IDs de conteúdos rejeitados."""
        sample_history.add_interaction("c001", InteractionType.DISLIKED)
        assert "c001" in sample_history.get_disliked_ids()

    def test_has_interacted_true(self, sample_history: History) -> None:
        """Verifica que has_interacted retorna True para interações registradas."""
        sample_history.add_interaction("c001", InteractionType.VIEWED)
        assert sample_history.has_interacted("c001") is True

    def test_has_interacted_false(self, sample_history: History) -> None:
        """Verifica que has_interacted retorna False para novos conteúdos."""
        assert sample_history.has_interacted("c999") is False

    def test_add_interaction_with_timestamp(self, sample_history: History) -> None:
        """Verifica o registro de interação com timestamp personalizado."""
        custom_time = datetime(2024, 1, 15, 10, 30)
        sample_history.add_interaction("c001", InteractionType.SAVED, timestamp=custom_time)
        assert sample_history.interactions[0].timestamp == custom_time
