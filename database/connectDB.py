from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#DATABASE_URL = "sqlite:///data/tecno_database.db"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "tecno_database.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"
# Exemple MySQL : "mysql+pymysql://user:password@localhost/dbname"
# DATABASE_URL = "mysql+pymysql://user:password@host/database"  # Pour MySQL, remplacez 'user', 'password', 'host' et 'database' par vos informations de connexion.
# DATABASE_URL = "postgresql+psycopg2://user:password@host/database"  # Pour PostgreSQL, remplacez 'user', 'password', 'host' et 'database' par vos informations de connexion.

# Creation du moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Affiche les requêtes SQL générées
    connect_args={"check_same_thread": False}  # Nécessaire pour SQLite avec SQLAlchemy
)

# Creation de la session
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush= False,
    bind=engine
    )

# Classe de base pour tous les modeles 
Base = declarative_base()

print("Database connection established successfully !")

#########################################
### COMMENT LANCER 
######################################
"""
1. Lancer le fichier 'create_tables.py'
2. Lancer le fichier 'models.py'
3. Creer un utilisateur administrateur en lancant 'insert_user.py'
"""