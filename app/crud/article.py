from typing import List, Optional, Sequence
from sqlalchemy import select, update, delete, func, or_
from sqlalchemy.orm import Session
from app.models.article import Article


def create_article(session: Session, title: str, slug: str, content: str) -> Article:
    """Crée un nouvel article et le rafraîchit pour récupérer l'ID généré."""
    new_article = Article(title=title, slug=slug, content=content)
    session.add(new_article)
    session.commit()
    session.refresh(new_article)
    return new_article


def get_article_by_id(session: Session, article_id: int) -> Optional[Article]:
    """Récupère un article par son ID en utilisant scalar_one_or_none()."""
    # .execute() renvoie un itérateur de lignes ; .scalar_one_or_none() extrait le premier élément ou None.
    statement = select(Article).where(Article.id == article_id)
    return session.execute(statement).scalar_one_or_none()


def get_article_by_slug(session: Session, slug: str) -> Optional[Article]:
    """Récupère un article par son slug unique."""
    statement = select(Article).where(Article.slug == slug)
    return session.execute(statement).scalar_one_or_none()


def list_articles(
    session: Session, 
    limit: int = 10, 
    offset: int = 0, 
    is_published: Optional[bool] = None
) -> Sequence[Article]:
    """Liste les articles avec pagination et filtre optionnel sur le statut de publication."""
    statement = select(Article).offset(offset).limit(limit)
    if is_published is not None:
        statement = statement.where(Article.is_published == is_published)
    
    # .scalars() convertit les lignes de résultat (tuples à 1 élément) en objets Article directement.
    return session.execute(statement).scalars().all()


def update_article(session: Session, article_id: int, update_data: dict) -> Optional[Article]:
    """Mise à jour partielle d'un article en utilisant setattr()."""
    article = get_article_by_id(session, article_id)
    if article:
        for key, value in update_data.items():
            if hasattr(article, key):
                setattr(article, key, value)
        session.commit()
        session.refresh(article)
    return article


def publish_article(session: Session, article_id: int) -> Optional[Article]:
    """Passe l'état is_published à True pour un article spécifique."""
    return update_article(session, article_id, {"is_published": True})


def increment_view_count(session: Session, article_id: int) -> None:
    """Incrémente le compteur de vues de manière atomique via une expression SQL."""
    # Utilisation d'une expression SQL (Article.view_count + 1) pour éviter les race conditions.
    statement = (
        update(Article)
        .where(Article.id == article_id)
        .values(view_count=Article.view_count + 1)
    )
    session.execute(statement)
    session.commit()


def delete_article(session: Session, article_id: int) -> bool:
    """Suppression physique d'un article. Retourne True si l'article existait."""
    statement = delete(Article).where(Article.id == article_id)
    result = session.execute(statement)
    session.commit()
    # .rowcount indique le nombre de lignes affectées par l'opération DELETE.
    return result.rowcount > 0


def count_articles(session: Session) -> int:
    """Compte le nombre total d'articles en utilisant func.count()."""
    statement = select(func.count()).select_from(Article)
    return session.execute(statement).scalar() or 0


def search_articles(session: Session, query: str) -> Sequence[Article]:
    """Recherche les articles par titre ou contenu (insensible à la casse via .ilike())."""
    search_filter = f"%{query}%"
    statement = select(Article).where(
        or_(
            Article.title.ilike(search_filter),
            Article.content.ilike(search_filter)
        )
    )
    return session.execute(statement).scalars().all()
