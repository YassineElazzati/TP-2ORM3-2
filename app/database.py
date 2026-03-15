import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# URL de connexion Postgres (par défaut vers le conteneur Docker)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://user_tp2:password_tp2@localhost:5432/db_articles"
)

# Création de l'engine avec SQLAlchemy 2.0
engine = create_engine(DATABASE_URL, echo=True)

# Fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Générateur de session pour utilisation avec 'with' ou dans une API."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
