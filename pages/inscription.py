"""
Permet de gérer l'inscription des utilisateurs, en créant un compte avec un nom d'utilisateur et un mot de passe. 
Les mots de passe sont sécurisés en utilisant un hash avant d'être stockés dans la base de données. 

Cette page permet également de vérifier si le nom d'utilisateur est déjà pris et affiche des messages appropriés à l'utilisateur.
"""

from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash
from werkzeug.security import generate_password_hash
from database.connectDB import SessionLocal, engine
from database.models import Utilisateurs, Base
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


# 1. Connexion à la base de données
engine = create_engine("sqlite:///data/tecno_database.db", echo= True)

# On s'assure que les tables existent avant d'insérer
Base.metadata.create_all(engine)

def layout_register():
    return html.Div(
        [
            html.H2("Creat an account"),
            dcc.Input(id= "inscript-username", type="text", placeholder="Put your name"),
            dcc.Input(id= "inscript-password", type= "password", placeholder= "Put your password"),
            dcc.Input(id="inscript-role", type = "text", placeholder= "Put your role"),
            html.Button("Sign up", id="inscript-btn", className="btn-inscript"),
            html.Div(id= "inscript-message", style={"marginTop":"10px"}),
            html.A("return to login", href="/login")
        ]
    )


def register_inscription_callbacks(app):
    @app.callback(
        Output("inscript-message", "children"),
        Input("inscript-btn", "n_clicks"),
        State("inscript-username", "value"),
        State("inscript-password", "value"),
        State("inscript-role", "value"),
        prevent_initial_call=True
    )

    def register(n_clicks, username, password, role):
        db = SessionLocal()
        existing_user = db.query(Utilisateurs).filter(Utilisateurs.Username == username).first()

        if existing_user:
            return html.Div("⚠️ Username already taken. Please choose another one.", style={"color": "red"})

        # News
        # 1. Convertir le mot de passe en chaine d'octets (bytes)
        password_bytes = password.encode('utf-8')

        # 2. Generer un 'Salt' (sel) unique et hacher le mot de passe
        sel = bcrypt.gensalt()
        password_hache_bytes = bcrypt.hashpw(password_bytes, sel)

        # 3. Re-transformer en chaine de caracteres (string) pour le stocker dans le champ Mapped[str]
        password_securise = password_hache_bytes.decode('utf-8')

        new_user = Utilisateurs(
            Username= username,
            Password= password_securise, # Enregistrement de la version hachee
            Role= role
        )

        # Ajout et validation dans la base

        db.add(new_user)
        print(f"User '{username}' creat with succes (ID : {new_user.Id}) !")

        db.commit()
        db.close()

        

        # ✅ Message de confirmation + redirection
        return html.Div(
            [
                html.Div("✅ Account created successfully! You can now log in.", 
                         style={"color": "green", "fontWeight": "bold"}),
                dcc.Location(pathname="/login", id="redirect-login")
            ]
        )