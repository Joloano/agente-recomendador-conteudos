"""
Testes unitários para o motor de recomendação (Recommender).
"""

import pytest
from typing import List

from src.engine.recommender import Recommender
from src.models.content import Content, ContentType
from src.models.history import History, InteractionType
from src.models.user import User


# ─────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def python_user() -> User:
    """Usuário interessado em Python e Machine Learning."""
    return User(user_id="u001", name="Python Dev", interests=["python", "machine learning"])


@pytest.fixture
def devops_user() -> User:
    """Usuário interessado em DevOps e Docker."""
    return User(user_id="u002", name="DevOps Engineer", interests=["docker", "devops", "infraestrutura"])


@pytest.fixture
def sample_catalog() -> List[Content]:
    """Catálogo de conteúdos de exemplo para testes."""
    return [
        Content(
            content_id="c001",
            title="Machine Learning com Python",
            description="Curso de ML",
            content_type=ContentType.COURSE,
            tags=["python", "machine learning", "data science"],
            rating=4.8,
        ),
        Content(
            content_id="c002",
            title="Docker para Devs",
            description="Tutorial de Docker",
            content_type=ContentType.VIDEO,
            tags=["docker", "devops", "containers"],
            rating=4.6,
        ),
        Content(
            content_id="c003",
            title="APIs REST com FastAPI",
            description="Tutorial de FastAPI",
            content_type=ContentType.ARTICLE,
            tags=["python", "fastapi", "api", "backend"],
            rating=4.7,
        ),
        Content(
            content_id="c004",
            title="Inteligência Artificial no Futuro",
            description="Podcast sobre IA",
            content_type=ContentType.PODCAST,
            tags=["inteligência artificial", "ia", "futuro"],
            rating=4.5,
        ),
        Content(
            content_id="c005",
            title="Clean Code",
            description="Boas práticas de programação",
            content_type=ContentType.BOOK,
            tags=["clean code", "boas práticas", "software engineering"],
            rating=4.9,
        ),
    ]


@pytest.fixture
def recommender(sample_catalog: List[Content]) -> Recommender:
    """Motor de recomendação com catálogo de exemplo."""
    return Recommender(catalog=sample_catalog)


# ─────────────────────────────────────────────────────────────
# Testes: Inicialização
# ─────────────────────────────────────────────────────────────

class TestRecommenderInit:
    """Testes de inicialização do Recommender."""

    def test_empty_catalog(self) -> None:
        """Verifica que o recomendador pode ser criado sem catálogo."""
        r = Recommender()
        assert r.catalog == []

    def test_catalog_with_contents(self, sample_catalog: List[Content]) -> None:
        """Verifica que o catálogo é carregado corretamente."""
        r = Recommender(catalog=sample_catalog)
        assert len(r.catalog) == 5

    def test_add_content(self) -> None:
        """Verifica a adição dinâmica de conteúdos ao catálogo."""
        r = Recommender()
        content = Content(
            content_id="c099",
            title="Novo Conteúdo",
            description="Desc",
            content_type=ContentType.ARTICLE,
        )
        r.add_content(content)
        assert len(r.catalog) == 1
        assert r.catalog[0].content_id == "c099"


# ─────────────────────────────────────────────────────────────
# Testes: Recomendações
# ─────────────────────────────────────────────────────────────

class TestRecommend:
    """Testes do método recommend()."""

    def test_recommend_returns_correct_number(
        self, recommender: Recommender, python_user: User
    ) -> None:
        """Verifica que o número de recomendações respeita top_n."""
        recs = recommender.recommend(user=python_user, top_n=3)
        assert len(recs) <= 3

    def test_recommend_prioritizes_interest_match(
        self, recommender: Recommender, python_user: User
    ) -> None:
        """Verifica que conteúdos com tags de interesse aparecem primeiro."""
        recs = recommender.recommend(user=python_user, top_n=5)
        # c001 (python + ml) e c003 (python) devem aparecer antes dos demais
        rec_ids = [c.content_id for c in recs]
        assert "c001" in rec_ids[:2] or "c003" in rec_ids[:2]

    def test_recommend_for_devops_user(
        self, recommender: Recommender, devops_user: User
    ) -> None:
        """Verifica que recomendações são personalizadas por interesse."""
        recs = recommender.recommend(user=devops_user, top_n=3)
        rec_ids = [c.content_id for c in recs]
        # c002 (docker + devops) deve aparecer nas primeiras recomendações
        assert "c002" in rec_ids

    def test_recommend_empty_catalog(self, python_user: User) -> None:
        """Verifica que recomendações vazias são retornadas para catálogo vazio."""
        r = Recommender()
        recs = r.recommend(user=python_user)
        assert recs == []

    def test_recommend_excludes_disliked(
        self, recommender: Recommender, python_user: User
    ) -> None:
        """Verifica que conteúdos rejeitados são excluídos das recomendações."""
        history = History(user_id=python_user.user_id)
        history.add_interaction("c001", InteractionType.DISLIKED)

        recs = recommender.recommend(user=python_user, history=history, exclude_disliked=True)
        rec_ids = [c.content_id for c in recs]
        assert "c001" not in rec_ids

    def test_recommend_includes_disliked_when_flag_false(
        self, recommender: Recommender, python_user: User
    ) -> None:
        """Verifica que conteúdos rejeitados aparecem quando exclude_disliked=False."""
        history = History(user_id=python_user.user_id)
        history.add_interaction("c001", InteractionType.DISLIKED)

        recs = recommender.recommend(
            user=python_user, history=history, exclude_disliked=False, top_n=5
        )
        rec_ids = [c.content_id for c in recs]
        assert "c001" in rec_ids

    def test_recommend_with_no_interests(self, recommender: Recommender) -> None:
        """Verifica recomendações para usuário sem interesses declarados."""
        user = User(user_id="u999", name="No Interests", interests=[])
        recs = recommender.recommend(user=user, top_n=3)
        # Deve retornar conteúdos ordenados apenas pelo rating
        assert len(recs) <= 3


# ─────────────────────────────────────────────────────────────
# Testes: Scoring
# ─────────────────────────────────────────────────────────────

class TestScoring:
    """Testes do sistema de pontuação interno."""

    def test_liked_content_scores_higher(
        self, sample_catalog: List[Content], python_user: User
    ) -> None:
        """Verifica que conteúdos curtidos recebem pontuação maior."""
        r = Recommender(catalog=sample_catalog)
        history = History(user_id=python_user.user_id)

        score_without_like = r._score(sample_catalog[0], python_user, history)
        history.add_interaction("c001", InteractionType.LIKED)
        score_with_like = r._score(sample_catalog[0], python_user, history)

        assert score_with_like > score_without_like

    def test_viewed_content_scores_lower(
        self, sample_catalog: List[Content], python_user: User
    ) -> None:
        """Verifica que conteúdos visualizados recebem penalidade."""
        r = Recommender(catalog=sample_catalog)
        history = History(user_id=python_user.user_id)

        score_before = r._score(sample_catalog[0], python_user, history)
        history.add_interaction("c001", InteractionType.VIEWED)
        score_after = r._score(sample_catalog[0], python_user, history)

        assert score_after < score_before

    def test_disliked_content_scores_much_lower(
        self, sample_catalog: List[Content], python_user: User
    ) -> None:
        """Verifica que conteúdos rejeitados recebem penalidade forte."""
        r = Recommender(catalog=sample_catalog)
        history = History(user_id=python_user.user_id)

        history.add_interaction("c001", InteractionType.DISLIKED)
        score = r._score(sample_catalog[0], python_user, history)

        # Pontuação deve ser negativa após rejeição
        assert score < 0


# ─────────────────────────────────────────────────────────────
# Testes: recommend_by_type
# ─────────────────────────────────────────────────────────────

class TestRecommendByType:
    """Testes do método recommend_by_type()."""

    def test_recommend_by_type_returns_only_matching_type(
        self, recommender: Recommender, python_user: User
    ) -> None:
        """Verifica que apenas conteúdos do tipo solicitado são retornados."""
        recs = recommender.recommend_by_type(
            user=python_user, content_type="course", top_n=5
        )
        for content in recs:
            assert content.content_type == ContentType.COURSE

    def test_recommend_by_type_video(
        self, recommender: Recommender, devops_user: User
    ) -> None:
        """Verifica recomendações filtradas por vídeo."""
        recs = recommender.recommend_by_type(
            user=devops_user, content_type="video", top_n=5
        )
        assert all(c.content_type == ContentType.VIDEO for c in recs)

    def test_recommend_by_type_nonexistent_type(
        self, recommender: Recommender, python_user: User
    ) -> None:
        """Verifica que tipo inexistente retorna lista vazia."""
        recs = recommender.recommend_by_type(
            user=python_user, content_type="webinar", top_n=5
        )
        assert recs == []
