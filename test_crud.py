from app.database import engine, SessionLocal
from app.models.article import Base, Article
from app.crud.article import (
    create_article, 
    publish_article, 
    list_articles, 
    update_article, 
    search_articles, 
    delete_article, 
    count_articles
)

def run_tests():
    # 1. Création des tables
    Base.metadata.create_all(engine)
    
    with SessionLocal() as session:
        print("--- Étape 1 : Création de 5 articles ---")
        articles_data = [
            ("Introduction à Python", "python-intro", "Apprendre les bases de Python."),
            ("SQLAlchemy pour les Pro", "sqla-pro", "Maîtriser SQLAlchemy 2.0."),
            ("Python Avancé", "python-adv", "Décorateurs et générateurs en Python."),
            ("Le guide de Flask", "flask-guide", "Créer des API web avec Flask."),
            ("Développement Web Moderne", "web-modern", "React, Vue et les frameworks modernes.")
        ]
        
        created_articles = []
        for title, slug, content in articles_data:
            art = create_article(session, title, slug, content)
            created_articles.append(art)
            print(f"Créé : {art.title} (ID: {art.id})")

        print("\n--- Étape 2 : Publication des 3 premiers articles ---")
        for i in range(3):
            publish_article(session, created_articles[i].id)
            print(f"Publié : {created_articles[i].title}")

        print("\n--- Étape 3 : Affichage d'une page de résultats (limit=2) ---")
        page = list_articles(session, limit=2, offset=0)
        for art in page:
            print(f"Page Item : {art.title}")

        print("\n--- Étape 4 : Mise à jour du titre de l'article ID 1 ---")
        updated = update_article(session, 1, {"title": "Python : Guide Complet pour Débutants"})
        if updated:
            print(f"Nouveau titre ID 1 : {updated.title}")

        print("\n--- Étape 5 : Recherche du mot 'Python' ---")
        results = search_articles(session, "Python")
        print(f"Résultats de recherche ({len(results)}) :")
        for art in results:
            print(f"- {art.title}")

        print("\n--- Étape 6 : Suppression du dernier article et vérification ---")
        last_id = created_articles[-1].id
        deleted = delete_article(session, last_id)
        total_count = count_articles(session)
        print(f"Article ID {last_id} supprimé : {deleted}")
        print(f"Nombre total d'articles restant : {total_count}")

if __name__ == "__main__":
    run_tests()
