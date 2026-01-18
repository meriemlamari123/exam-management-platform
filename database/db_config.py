import os
import sqlite3
from sqlalchemy import create_engine

# Détection automatique : PostgreSQL (production) ou SQLite (local)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_path():
    """Retourne le chemin de la base de données SQLite"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(BASE_DIR, "database", "university.db")

def get_engine():
    """Retourne l'engine SQLAlchemy approprié"""
    if DATABASE_URL:
        # Production : PostgreSQL
        # Fix pour Render (remplace postgres:// par postgresql://)
        db_url = DATABASE_URL
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return create_engine(db_url)
    else:
        # Local : SQLite
        db_path = get_db_path()
        return create_engine(f"sqlite:///{db_path}")

def get_connection():
    """Retourne une connexion à la base de données"""
    if DATABASE_URL:
        # PostgreSQL
        engine = get_engine()
        return engine.connect()
    else:
        # SQLite
        db_path = get_db_path()
        return sqlite3.connect(db_path)

def database_exists():
    """Vérifie si la base de données existe et contient des données"""
    try:
        conn = get_connection()
        if DATABASE_URL:
            # PostgreSQL
            cursor = conn.execute("SELECT COUNT(*) FROM students")
        else:
            # SQLite
            cursor = conn.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except:
        return False
