"""
C'est dans ce fichier que nous lancerons notre programme professionnel
Dash plotly
"""
###############################
## IMPORTATION LIBRAIRIES
###############################
import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages.login import layout_login, register_auth_callbacks
from pages.inscription import layout_register, register_inscription_callbacks
import pages.dashboard as dashboard
import pages.profil as profil
import pages.report as report
import pages.st_smartphone as smartphoneST
import pages.st_featurephone as featurephoneST
import pages.sd_smartphone as smartphoneSD
import pages.sd_featurephone as featurephoneSD
from pages.show_button import show_button_layout
from flask import session
import os
import dash_mantine_components as dmc
from dash_iconify import DashIconify

### Import callback
from callbacks import report_sd_fp, report_sd_sp, report_st_fp, report_st_sp

# pip install dash dash-mantine-components dash-iconify

# Creation application Dash
app = Dash(__name__, title="Channel Tecno Phone", use_pages= False, suppress_callback_exceptions=True) # Ou True, si tu utilises dash.register_page
server = app.server

# Style pour les liens de navigation
link_style = {
    "display"        : "flex",
    "alignItems"     : "center",
    "gap"            : "10px",
    "padding"        : "10px",
    "borderRadius"   : "6px",
    "textDecoration" : "none",
    "color"          : "#495057",
}

server = app.server
# 🔑 Clé secrète obligatoire pour les sessions
#server.secret_key = "une_cle_ultra_secrete_a_changer"

# Exemple avec variable d’environnement :
server.secret_key = os.environ.get("SECRET_KEY", "dev_key") # Puis tu définis SECRET_KEY dans ton système ou ton hébergeur.

# Structure de la barre de navigation avec Sidebar
sidebar = html.Nav(
    children= 
    [
        # Le composant dcc.Location permet de suivre l'URL actuelle
        dcc.Location(id = "url", refresh= False),

        dmc.NavLink(
            id      = "nav-login",
            label   = "LOGIN",
            href    = "/",
            variant = "light"
        ),

        dmc.NavLink(
            id      = "nav-dashboard",
            label   = "DASHBOARD",
            href    = "/dashboard",
            variant = "light"
        ),

        dmc.NavLink(
            id      = "nav-st-sp",
            label   ="ST SMART PHONE",
            href    = "/st_smartphone",
            variant = "light"
        ),

        dmc.NavLink(
            id      = "nav-st-fp",
            label   = "ST FEATURE PHONE",
            href    = "/st_featurephone",
            variant = "light"
        ),

        dmc.NavLink(
            id      = "nav-sd-sp",
            label   = "SD SMART PHONE",
            href    = "/sd_smartphone",
            variant = "light"
        ),

        dmc.NavLink(
            id      = "nav-sd-fp",
            label   = "SD FEATURE PHONE",
            href    = "/sd_featurephone",
            variant = "light"
        ),

        dmc.NavLink(
            id      = "nav-ex-database",
            label   = "EXPORT DATABASE",
            href    = "/show_button",
            variant = "light"
        ),

        dmc.NavLink(
            id = "nav-report",
            label = "REPORT",
            href= "/report",
            variant ="light"
        ),

        dmc.NavLink(
            id = "nav-aboutMe",
            label = "ABOUT ME",
            href= "/profil",
            variant ="light"
        ),

        dmc.NavLink(
            id = "nav-inscription",
            label = "INSCRIPTION",
            href= "/inscription",
            variant ="light"
        ),

        dmc.NavLink(
            id = "nav-logout",
            label = "LOGOUT",
            href= "/logout",
            variant = "light"
        ),
    ], className= "sidebar"

)


# Layout principal
app.layout = dmc.MantineProvider(
    children=html.Div(
        [
            
            html.Div(
                id = "sidebar-container",
                children = sidebar
            ),

            html.Div(
                id="page-content",
                style={
                    "flex": 1,
                    "padding": "20px"
                }
            )
        ],
        style={
            "display": "flex"
        }
    )
)
# ==================================================
# CALLBACK 0 : Gestion de l'affichage du menu Admin
# ==================================================
@app.callback(
    Output("nav-login", "active"),
    Output("nav-dashboard", "active"),
    Output("nav-st-sp", "active"),
    Output("nav-st-fp", "active"),
    Output("nav-sd-sp", "active"),
    Output("nav-sd-fp", "active"),
    Output("nav-ex-database", "active"),
    Output("nav-report", "active"),
    Output("nav-aboutMe", "active"),
    Output("nav-inscription", "active"),
    Output("nav-logout", "active"),
    Input("url", "pathname")
)

def activate_nav(pathname):
    return (
        pathname == "/",
        pathname == "/dashboard",
        pathname == "/st_smartphone",
        pathname == "/st_featurephone",
        pathname == "/sd_smartphone",
        pathname == "/sd_featurephone",
        pathname == "/show_button",
        pathname == "/report",
        pathname == "/profil",
        pathname == "/inscription",
        pathname == "/logout"
    )


# ===================================================================
# CALLBACK 1 : Ajouter un callback pour afficher/masquer la sidebar
# ===================================================================

@app.callback(
    Output("sidebar-container", "style"),
    Input("url", "pathname")
)
def toggle_sidebar(_):

    if not session.get("logged_in"):
        return {
            "display": "none"
        }

    return {
        "display": "block",
        "width": "240px"
    }

# ===================================================================
# CALLBACK 2 : Routage principal des pages (Le moteur de votre app)
# ===================================================================
@app.callback(
    dash.Output("page-content", "children"),
    dash.Input("url", "pathname")
)

def display_page(pathname):
    # 1. Verifier si l'utilisateur est connecte
    if not session.get("logged_in"):
        if pathname == "/inscription":
            return layout_register()
        return layout_login()
    
    if pathname == "/":
        return dcc.Location(
            pathname="/dashboard",
            id="redirect-home"
            )
    
    
    # 2. Recuperer le role de l'utilisateur
    user_role = session.get("user_role", "user")

    # Definir les acces aux pages
    
    # 3. Pages accessibles par TOUT LE MONDE (Admin et User standard) 
    if pathname == "/dashboard":
        return dashboard.layout()
    
    elif pathname == "/profil":
        return profil.layout()
    
    elif pathname == "/logout":
        session.clear()
        return layout_login()
    
    # 4. Pages STRICTEMENT RESERVE A L'ADMIN
    # Vous listez ici les chemins d'URL que vous voulez bloquer pour les simples utilisateurs

    elif pathname in ["/st_smartphone", "/st_featurephone", "/sd_smartphone", "/sd_featurephone", "/show_button", "/report", "/inscription", "/logout"] :
        # Seul l'admin peut voir ces pages
        if user_role == "admin": # 
            if pathname == "/st_smartphone":
                return smartphoneST.layout()
            
            elif pathname == "/st_featurephone":
                return featurephoneST.layout()
            
            elif pathname == "/sd_smartphone":
                return smartphoneSD.layout()
            
            elif pathname == "/sd_featurephone":
                return featurephoneSD.layout()
            
            elif pathname == "/inscription":
                return layout_register()
            
            elif pathname == "/show_button":
                return show_button_layout # on retourne le layout defini dans show_button.py
            
            elif pathname == "/report":
                return report.layout()
            
            elif pathname == "/logout":
                session.clear()
                return layout_login()
        
        else :
            # Si un simple utilisateur tente d'y acceder  --> Redirection forcee ou message d'erreur
            return dmc.Center(
                style = {"height": "70vh"},
                children= dmc.Stack(
                    align= "center",
                    spacing = "md",
                    children= [
                        dmc.Alert(
                            title= "Acces denied",
                            color= "red",
                            variant = "filled",
                            withCloseButton= False,
                            children= "Sorry, you aren't administrator for consulting this page."
                        ),

                        dmc.Button(
                            "Return to Dashboard",
                            id = "back-to-dashboard-btn",
                            component = "a", # Permet au bouton de se comporter comme un lien hypertexte
                            href= "/dashboard",
                            color= "blue",
                            variant= "light",
                            size= "md",
                        )
                    ]
                )
            )
        


register_auth_callbacks(app)
register_inscription_callbacks(app)


if __name__ == "__main__":
    app.run(debug= True)
    #app.run(
        #host="0.0.0.0",
        #port=int(os.environ.get("PORT", 8050)),
        #debug=False
    #)



# http://127.0.0.1:8050/