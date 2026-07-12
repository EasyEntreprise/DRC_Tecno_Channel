"""
Ce fichier contiendra uniquement la mise en page (le layout) et les callbacks (la logique des boutons) liés aux insertions.
​Note : Pour que les callbacks fonctionnent dans un fichier séparé, on utilise @dash.callback au lieu de @app.callback.
"""
import dash
from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


# Importation de tes fonctions logiques depuis ton module de base de données
from database.export_to_sql import (
    insert_sd_fp_data, 
    insert_sd_sp_data, 
    insert_st_fp_data, 
    insert_st_sp_data
)

# =============================================================================
# MISE EN PAGE (LAYOUT)
# =============================================================================

show_button_layout = dmc.Container([
    dmc.Title("Data Entry", order=2, style={"textAlign": "center", "marginBottom": "20px"}),
    dmc.Divider(variant="solid", style={"marginBottom": "30px"}),
    html.Hr(),
    
    # Utilisation du système de grille de Mantine
    dmc.Grid([
        
        # ----------------- CARTE 1 : Sub-Dealer Feature Phone -----------------
        dmc.GridCol([
            dmc.Card([
                dmc.Text("Data Sub-Dealer Feature Phone", fw=500, size="lg", style={"marginBottom": "10px"}),
                dmc.Text("Insert the new data since Tecno_FP_SD_dataset.xlsx", size="sm", c="dimmed", style={"marginBottom": "15px"}),
                dmc.Button("Start the insertion", id="btn-insert-sd-fp", color="blue", fullWidth=True),
                html.Div(id="output-sd-fp", style={"marginTop": "15px"})
            ], withBorder=True, shadow="sm", radius="md", p="xl")
        ], span=4),
        
        # ------------------ CARTE 2 : Sub-Dealer Smart Phone ------------------
        dmc.GridCol([
            dmc.Card([
                dmc.Text("Data Sub-Dealer Smart Phone", fw=500, size="lg", style={"marginBottom": "10px"}),
                dmc.Text("Insert the new data since Tecno_SP_SD_dataset.xlsx", size="sm", c="dimmed", style={"marginBottom": "15px"}),
                dmc.Button("Start the insertion", id="btn-insert-sd-sp", color="blue", fullWidth=True),
                html.Div(id="output-sd-sp", style={"marginTop": "15px"})
            ], withBorder=True, shadow="sm", radius="md", p="xl")
        ], span=4),
        
        # ----------------- CARTE 3 : Sell Through Feature Phone -----------------
        dmc.GridCol([
            dmc.Card([
                dmc.Text("Sell Through data for Feature Phone", fw=500, size="lg", style={"marginBottom": "10px"}),
                dmc.Text("Insert the new data since Tecno_FP_ST_dataset.xlsx", size="sm", c="dimmed", style={"marginBottom": "15px"}),
                dmc.Button("Start the insertion", id="btn-insert-st-fp", color="blue", fullWidth=True),
                html.Div(id="output-st-fp", style={"marginTop": "15px"})
            ], withBorder=True, shadow="sm", radius="md", p="xl")
        ], span=4),
        
        # ------------------ CARTE 4 : Sell Through Smart Phone ------------------
        dmc.GridCol([
            dmc.Card([
                dmc.Text("Sell Through data for Smart Phone", fw=500, size="lg", style={"marginBottom": "10px"}),
                dmc.Text("Insert the new data since Tecno_SP_ST_dataset.xlsx", size="sm", c="dimmed", style={"marginBottom": "15px"}),
                dmc.Button("Start the insertion", id="btn-insert-st-sp", color="blue", fullWidth=True),
                html.Div(id="output-st-sp", style={"marginTop": "15px"})
            ], withBorder=True, shadow="sm", radius="md", p="xl")
        ], span=4)
        
    ], gutter="lg", className="g-4"),
    
], fluid=True)


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def generate_dmc_alert(message_result, color_alert, title_alert):
    """Fonction utilitaire pour générer une alerte dmc propre."""
    return dmc.Alert(
        message_result,
        title=title_alert,
        color=color_alert,
        variant="filled",
        withCloseButton=True
    )


# =============================================================================
# CALLBACKS DE LA PAGE
# =============================================================================

# 1. Callback pour Sub-Dealer Feature Phone
@callback(
    Output("output-sd-fp", "children"),
    Input("btn-insert-sd-fp", "n_clicks"),
    prevent_initial_call=True
)
def trigger_insertion_sd_fp(n_clicks):
    if n_clicks is None:
        return dash.no_update
    try:
        success = insert_sd_fp_data()
        if success:
            return generate_dmc_alert("Les données Sub-Dealer Feature Phone ont été insérées avec succès !", "green", "Succès !")
        return generate_dmc_alert("L'insertion a échoué. Veuillez vérifier les fichiers sources.", "red", "Erreur")
    except Exception as e:
        return generate_dmc_alert(f"Erreur technique : {str(e)}", "red", "Échec")


# 2. Callback pour Sub-Dealer Smart Phone
@callback(
    Output("output-sd-sp", "children"),
    Input("btn-insert-sd-sp", "n_clicks"),
    prevent_initial_call=True
)
def trigger_insertion_sd_sp(n_clicks):
    if n_clicks is None:
        return dash.no_update
    try:
        success = insert_sd_sp_data()
        if success:
            return generate_dmc_alert("Les données Sub-Dealer Smart Phone ont été insérées avec succès !", "green", "Succès !")
        return generate_dmc_alert("L'insertion a échoué. Veuillez vérifier les fichiers sources.", "red", "Erreur")
    except Exception as e:
        return generate_dmc_alert(f"Erreur technique : {str(e)}", "red", "Échec")


# 3. Callback pour Sell Through Feature Phone
@callback(
    Output("output-st-fp", "children"),
    Input("btn-insert-st-fp", "n_clicks"),
    prevent_initial_call=True
)
def trigger_insertion_st_fp(n_clicks):
    if n_clicks is None:
        return dash.no_update
    try:
        success = insert_st_fp_data()
        if success:
            return generate_dmc_alert("Les données Sell Through Feature Phone ont été insérées avec succès !", "green", "Succès !")
        return generate_dmc_alert("L'insertion a échoué. Veuillez vérifier les fichiers sources.", "red", "Erreur")
    except Exception as e:
        return generate_dmc_alert(f"Erreur technique : {str(e)}", "red", "Échec")


# 4. Callback pour Sell Through Smart Phone (Celui qui posait problème !)
@callback(
    Output("output-st-sp", "children"),
    Input("btn-insert-st-sp", "n_clicks"),
    prevent_initial_call=True
)
def trigger_insertion_st_sp(n_clicks):
    if n_clicks is None:
        return dash.no_update
    try:
        success = insert_st_sp_data()
        if success:
            return generate_dmc_alert("Les données Sell Through Smart Phone ont été insérées avec succès !", "green", "Succès !")
        return generate_dmc_alert("L'insertion a échoué. Veuillez vérifier les fichiers sources.", "red", "Erreur")
    except Exception as e:
        return generate_dmc_alert(f"Erreur technique : {str(e)}", "red", "Échec")