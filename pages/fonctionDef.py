# IMPORTATION LIBRAIRIES
from dash import html
import pandas as pd
from datetime import datetime
import dash_mantine_components as dmc
from dash_iconify import DashIconify

####################
## 1. Def One
def create_metric_card(title, value, percentage, is_positive = True, icon_name = "fluent:commerce-revenu-24-regular"):
    # Generer une carte metrique stylisee et reutilisable
    # Configuration semantique delon la tendance (positive ou negative)
    trend_color = "green" if is_positive else "red"
    trend_icon = "fluent: arrow-trending-24-filled" if is_positive else "fluent:arrow-trending-down-24-filled"

    return dmc.Card(
        children= [
            # Ligne 1 : Titre et Icon principale
            dmc.Group(
                children= [
                    dmc.Text(title, size = "sm", c= "dimmed", fw=600, lts= "0.5px"),
                    dmc.ThemeIcon(
                        DashIconify(icon = icon_name, width = 20),
                        variant = "light",
                        color = "indigo",
                        radius = "md",
                        size = "lg"
                    )
                ],
                justify = "space-between",
                align = "center"
            ),

            # Ligne 2 : Valeur principale et Evolution
            dmc.Group(
                children= [
                    dmc.Text(value, size= "xl", fw=700, style={"fontSize": "1.8rem"}),
                    
                    # Badge d'evolution (Tendance)
                    dmc.Badge(
                        children= [
                            dmc.Group(
                                [
                                    DashIconify(icon = trend_icon, width= 14),
                                    dmc.Text(f"{'' if is_positive else ''}{percentage}%", size= "xs", fw=700)
                                ],
                                gap= 4,
                                align= "center"
                            )
                        ],
                        color = trend_color,
                        variant = "light",
                        size= "md",
                        radius= "sm"
                    )
                ], 
                justify= "space-between",
                align= "flex-end",
                mt= "xl"
            )
        ],
        withBorder= True,
        shadow= "sm",
        radius= "md",
        p= "xl",
        style= {"width":280, "backgroundColor": "#ffffff"}
    )
# ----------------------------------------

def create_metric_card2(title, value, is_positive = True, icon_name = "fluent:commerce-revenu-24-regular"):
    # Generer une carte metrique stylisee et reutilisable
    # Configuration semantique delon la tendance (positive ou negative)
    trend_color = "green" if is_positive else "red"
    trend_icon = "fluent: arrow-trending-24-filled" if is_positive else "fluent:arrow-trending-down-24-filled"

    return dmc.Card(
        children= [
            # Ligne 1 : Titre et Icon principale
            dmc.Group(
                children= [
                    dmc.Text(title, size = "sm", c= "dimmed", fw=600, lts= "0.5px"),
                    dmc.ThemeIcon(
                        DashIconify(icon = icon_name, width = 20),
                        variant = "light",
                        color = "indigo",
                        radius = "md",
                        size = "lg"
                    )
                ],
                justify = "space-between",
                align = "center"
            ),

            # Ligne 2 : Valeur principale et Evolution
            dmc.Group(
                children= [
                    dmc.Text(value, size= "xl", fw=700, style={"fontSize": "1.8rem"}),
                    
                    # Badge d'evolution (Tendance)
                    dmc.Badge(
                        children= [
                            dmc.Group(
                                [
                                    DashIconify(icon = trend_icon, width= 14)
                                ],
                                gap= 4,
                                align= "center"
                            )
                        ],
                        color = trend_color,
                        variant = "light",
                        size= "md",
                        radius= "sm"
                    )
                ], 
                justify= "space-between",
                align= "flex-end",
                mt= "xl"
            )
        ],
        withBorder= True,
        shadow= "sm",
        radius= "md",
        p= "xl",
        style= {"width":280, "backgroundColor": "#ffffff"}
    )


####################################################
####################################################
## 3. Def three
def create_metric_card3(title, value, percentage, is_positive = True, icon_name = "fluent:commerce-revenu-24-regular"):
    # Generer une carte metrique stylisee et reutilisable
    # Configuration semantique delon la tendance (positive ou negative)
    trend_color = "green" if is_positive else "red"
    trend_icon = "fluent: arrow-trending-24-filled" if is_positive else "fluent:arrow-trending-down-24-filled"

    return dmc.Card(
        children= [
            # Ligne 1 : Titre et Icon principale
            dmc.Group(
                children= [
                    dmc.Text(title, size = "sm", c= "dimmed", fw=600, lts= "0.5px"),
                    dmc.ThemeIcon(
                        DashIconify(icon = icon_name, width = 20),
                        variant = "light",
                        color = "indigo",
                        radius = "md",
                        size = "lg"
                    )
                ],
                justify = "space-between",
                align = "center"
            ),

            # Ligne 2 : Valeur principale et Evolution
            dmc.Group(
                children= [
                    dmc.Text(value, size= "xl", fw=700, style={"fontSize": "1.8rem"}),
                    
                    # Badge d'evolution (Tendance)
                    dmc.Badge(
                        children= [
                            dmc.Group(
                                [
                                    DashIconify(icon = trend_icon, width= 14),
                                    dmc.Text(f"{'' if is_positive else ''}{percentage}%", size= "xs", fw=700)
                                ],
                                gap= 4,
                                align= "center"
                            )
                        ],
                        color = trend_color,
                        variant = "light",
                        size= "md",
                        radius= "sm"
                    )
                ], 
                justify= "space-between",
                align= "flex-end",
                mt= "xl"
            )
        ],
        withBorder= True,
        shadow= "sm",
        radius= "md",
        p= "xl",
        style= {"width":280, "backgroundColor": "#ffffff"}
    )
# ----------------------------------------

def create_metric_card4(title, value, is_positive = True, icon_name = "fluent:commerce-revenu-24-regular"):
    # Generer une carte metrique stylisee et reutilisable
    # Configuration semantique delon la tendance (positive ou negative)
    trend_color = "green" if is_positive else "red"
    trend_icon = "fluent: arrow-trending-24-filled" if is_positive else "fluent:arrow-trending-down-24-filled"

    return dmc.Card(
        children= [
            # Ligne 1 : Titre et Icon principale
            dmc.Group(
                children= [
                    dmc.Text(title, c= "dimmed", fw=700, lts= "0.5px", style={"fontSize": "12"}),
                    dmc.ThemeIcon(
                        DashIconify(icon = icon_name, width = 20),
                        variant = "light",
                        color = "indigo",
                        radius = "md",
                        size = "lg"
                    )
                ],
                justify = "space-between",
                align = "center"
            ),

            # Ligne 2 : Valeur principale et Evolution
            dmc.Group(
                children= [
                    dmc.Text(value, fw=700, style={"fontSize": "55"}),
                    
                    # Badge d'evolution (Tendance)
                    dmc.Badge(
                        children= [
                            dmc.Group(
                                [
                                    DashIconify(icon = trend_icon, width= 14)
                                ],
                                gap= 4,
                                align= "center"
                            )
                        ],
                        color = trend_color,
                        variant = "light",
                        size= "md",
                        radius= "sm"
                    )
                ], 
                justify= "space-between",
                align= "flex-end",
                mt= "xs"
            )
        ],
        withBorder= True,
        shadow= "sm",
        radius= "md",
        p= "sm",
        style= {"width":270, "height": 100, "backgroundColor": "#ffffff"}
    )