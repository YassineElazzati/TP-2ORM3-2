from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, engine
from app.models.article import Base
from app.crud import article as crud_article

# Création des tables au démarrage (si elles n'existent pas)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion d'Articles API")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion d'articles !"}

@app.get("/articles", response_model=List[dict])
def list_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = crud_article.list_articles(session=db, offset=skip, limit=limit)
    return [
        {
            "id": a.id,
            "title": a.title,
            "slug": a.slug,
            "content": a.content,
            "is_published": a.is_published,
            "view_count": a.view_count
        } for a in articles
    ]

@app.get("/articles/{article_id}")
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud_article.get_article_by_id(session=db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return db_article

@app.post("/articles")
def create_article(title: str, content: str, slug: str, db: Session = Depends(get_db)):
    return crud_article.create_article(session=db, title=title, content=content, slug=slug)

@app.put("/articles/{article_id}/publish")
def publish_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud_article.publish_article(session=db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return db_article
