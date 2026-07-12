import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from connectDB import engine, SessionLocal
from models import Utilisateurs, Base
from werkzeug.security import generate_password_hash


#########################
### Nouveau Code
#########################

# 1. Connexion à la base de données
engine = create_engine("sqlite:///data/tecno_database.db", echo= True)

# On s'assure que les tables existent avant d'insérer
Base.metadata.create_all(engine)

# 2. Fonction pour insérer des données dans la Users

def insertionData(username: str, password: str, role: str):
    # Hacher le mot de passe et insere de l'utilisateur de maniere securisee en base de donnees

    # --ETAPE DE SECURITE : Hachage du mot de passe ---
    # 1. Convertir le mot de passe en chaine d'octets (bytes)

    password_bytes = password.encode('utf-8')

    # 2. Generer un 'Salt' (sel) unique et hacher le mot de passe
    sel = bcrypt.gensalt()
    password_hache_bytes = bcrypt.hashpw(password_bytes, sel)

    # 3. Re-transformer en chaine de caracteres (string) pour le stocker dans le champ Mapped[str]
    password_securise = password_hache_bytes.decode('utf-8')

    # --ETAPE SQLALCHEMY : Insertion en Base de donnees --
    with Session(engine) as session :
        # Creation de l'objet utilisateur avec le mot de passe securise
        new_users = Utilisateurs(
            Username = username,
            Password = password_securise, # Enregistrement de la version hachee
            Role = role
        )

        # Ajout et validation dans la base
        session.add(new_users)
        session.commit()

        print(f"User '{username}' creat with succes (ID : {new_users.Id}) !")


def verifier_connexion(username_saisi : str, password_saisi : str) :
    with Session(engine) as session :
        # 1. Rechercher l'utilisateur par son nom
        utilisateur = session.query(Utilisateurs).filter_by(Username = username_saisi).first()

        if not utilisateur :
            print("Utilisateur introuvable")
            return False
        
        # 2. Verifier si le mot de passe saisi correspond au hachage stocke
        # On doit re-encoder les chaines en 'bytes' pour bcrypt
        match = bcrypt.checkpw(
            password_saisi.encode('utf-8'),
            utilisateur.Password.encode('utf-8')
        )

        if match :
            print("Connexion reussie ! Bienvenue {utilisateur.Username} ({utilisateur.Role})")
            return True
        
        else :
            print("Mot de passe incorrect")
            return False
        

insertionData("Rodrigue", "Mayanza@3", "admin")