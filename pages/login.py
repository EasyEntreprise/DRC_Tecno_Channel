import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from flask import session, redirect
from werkzeug.security import check_password_hash
from database.connectDB import SessionLocal
from database.models import Utilisateurs
import bcrypt



def layout_login(id = "login", style= {"border" : "5px"}):
    return html.Div(
        [
            
            html.H2("Login"),
            html.Br(),
            dcc.Input(id= "username", type= "text", placeholder= "Put your name"),
            dcc.Input(id= "password", type= "password", placeholder= "Put your password"),
            html.Br(),
            html.Button(
                "Login", 
                id="login-btn",
                className= "btn-login", 
                style = {
                    "backgroundColor" : "#B3D1FD",
                    "border"          : "none",
                    "width"           : "120px",
                    "height"          : "40px",
                    "borderRadius"    : "8px",
                    "padding"         : "12px 24px",
                    "cursor"          : "pointer",
                    "fontWeight"      : "bold",
                    "boxShadow"       : "0 2px 5px rgba(0, 0, 0, 0.2)",
                    "transition"      : "all 0.3s ease"
                }),
            html.Div(id="login-message"),
            html.Br(),
            html.A("Create an account", href="/inscription") # 🔗 lien vers inscription

        ]
    )

def register_auth_callbacks(app):
    @app.callback(
        #Output("login-message", "children"),  # On modifiera cette sortie
        Output("url", "pathname"),            # Modifie l'url pour declencher le changement de page
        Output("login-message", "children"),   
        Input("login-btn", "n_clicks"),       # Le callback sera executer lorsqu'on clique sur le bouton
        State("username", "value"),           # Recupere le nom de l'utilisateur
        State("password", "value"),           # Recupere mot de passe de l'utilisateur
        prevent_imitial_call = True           # Empeche l'execution automatique du callback au demarrage de l'application
    )

    def login(n_clicks, username, password): # Fonction executer lors du clic, n_clicks nombre des clics
        
        #db = SessionLocal()                                              # Cree une session SQLAlchemy, cette session permettra d'interroger la base des donnees
        #user = db.query(User).filter(User.username == username).first()  # SQLAlchemy genere une requete equivalente a celle de sql "SELECT * FROM table WHERE username = ? LIMIT 1"
        
        if not username or not password :
            return dash.no_update                                        # Veuillez remplir tous les champs.
        db = SessionLocal()

        try:
            user = db.query(Utilisateurs).filter(Utilisateurs.Username == username).first()  # SQLAlchemy genere une requete equivalente a celle de sql "SELECT * FROM table WHERE username = ? LIMIT 1" 
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user.Password.encode('utf-8')):        # Verification du mot de passe
                session["logged_in"] = True                                  # On enregistre dans la session Flask que l'utilisateur est connecter
                session["user_role"] = user.Role
                
                # SUUCES : On dirige vers /dashboard, et on ne touche pas au message d'erreur
                return "/dashboard", dash.no_update  

            # ECHEC : On ne change pas l'URL (dash.no_update), mais on affiche l'erreur
            return dash.no_update,  "Identifiant invalides"                       



        finally :
            db.close()                                                   # Tres important pour liberer la connexion a la base de donnees                                   
        
        if user and check_password_hash(user.password, password):        # Verification du mot de passe
            session["logged_in"] = True                                  # On enregistre dans la session Flask que l'utilisateur est connecter
            #return dcc.Location(pathname="/dashboard", id="redirect")    # La redirection si l'authentification reussit
        return "⚠️ Identifiants invalides"                               # Message d'erreur si l'utilisateur n'existe pas

    # ✅ Correction de la route logout
    @app.server.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")  # redirection propre vers login
