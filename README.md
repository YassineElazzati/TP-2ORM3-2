# TP 2 : CRUD Articles avec SQLAlchemy 2.0 & PostgreSQL

Ce projet implémente un système complet de gestion d'articles (CRUD) en utilisant les dernières normes de **SQLAlchemy 2.0** et une base de données **PostgreSQL** conteneurisée avec Docker.

## 🚀 Guide de démarrage rapide

### 1. Prérequis
- Docker et Docker Compose installés.
- Python 3.9+ installé.

### 2. Lancer la base de données
Démarrez le conteneur PostgreSQL en arrière-plan :
```bash
docker-compose up -d
```

### 3. Installation des dépendances
Il est recommandé d'utiliser un environnement virtuel :
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Exécuter le projet
Le script `test_crud.py` initialise la base de données, crée les tables, et exécute un scénario de test complet :
```bash
python3 test_crud.py
```

---

## 🏗️ Architecture du Projet

```text
TP-2/
├── app/
│   ├── crud/
│   │   └── article.py      # Logique métier (Create, Read, Update, Delete)
│   ├── models/
│   │   └── article.py      # Définition de la table Article (SQLAlchemy)
│   ├── database.py         # Configuration de la connexion et sessions
│   └── __init__.py         # Marqueur de package Python
├── docker-compose.yml      # Configuration PostgreSQL
├── requirements.txt        # Dépendances (SQLAlchemy, Psycopg2)
└── test_crud.py            # Script principal de démonstration
```

---

## 📖 Explications détaillées

### 1. Modèles (`app/models/article.py`)
Nous utilisons le nouveau système de mapping de **SQLAlchemy 2.0** :
- `Mapped[int]` : Définit de manière explicite le type Python et la colonne SQL.
- `mapped_column` : Remplace l'ancien `Column` pour une meilleure intégration avec les IDE et le typage statique.
- `DeclarativeBase` : La nouvelle classe de base pour tous les modèles.

### 2. Connexion (`app/database.py`)
- `create_engine` : Crée le moteur de connexion. L'URL pointe vers le conteneur Docker.
- `SessionLocal` : Une fabrique de sessions. Chaque interaction avec la BDD doit passer par une session.
- `get_db()` : Un générateur (yield) qui assure que la connexion est bien fermée après usage, évitant les fuites de mémoire.

### 3. Opérations CRUD (`app/crud/article.py`)
Chaque fonction est conçue pour être **atomique** et **typée** :
- **`scalar_one_or_none()`** : Utilisé pour récupérer un seul objet ou None si non trouvé. C'est la méthode recommandée en 2.0.
- **`scalars().all()`** : Convertit les lignes SQL brutes en objets Python `Article`.
- **`update()` & `delete()`** : Utilisent la syntaxe de "Statement" (déclarative) plutôt que l'ancienne méthode `query()`.
- **Incrémentation atomique** : `Article.view_count + 1` est exécuté directement par le serveur SQL, évitant les problèmes de concurrence si deux utilisateurs voient l'article en même temps.

### 4. Docker (`docker-compose.yml`)
- **`postgres:15-alpine`** : Image légère et sécurisée.
- **Volumes** : `postgres_data` permet de conserver vos données même si vous supprimez le conteneur.
- **Ports** : Mappe le port `5432` du conteneur sur votre machine locale pour permettre à Python d'y accéder via `localhost`.

---

## 🛠️ Pourquoi ces choix ?

1. **SQLAlchemy 2.0** : Offre une syntaxe plus proche du SQL standard, un meilleur support de l'asynchrone et un typage Python strict qui réduit drastiquement les bugs en production.
2. **PostgreSQL via Docker** : Garantit que l'environnement de base de données est identique pour tous les développeurs, sans avoir à installer Postgres "en dur" sur son système.
3. **Typage (Type Hints)** : L'utilisation de `Sequence`, `Optional`, et `List` permet une auto-complétion parfaite dans VS Code / PyCharm et facilite la maintenance à long terme.
