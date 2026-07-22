# IMPORTATION LIBRAIRIES
import dash
from dash import html, callback
from dash import dcc, dash_table
import pandas as pd
from database.connectDB import engine, SessionLocal
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import dash_mantine_components as dmc
from dash.dependencies import Input, Output
from dash_iconify import DashIconify
from pages.fonctionDef import create_metric_card, create_metric_card2, create_metric_card3, create_metric_card4

#session = SessionLocal()

try:
    df_st_fp = pd.read_sql_table("ST_tecno_FP_data", con= engine)
    df_st_sp = pd.read_sql_table("ST_tecno_SP_data", con= engine)
    df_sd_fp = pd.read_sql_table("SD_tecno_FP_data", con= engine)
    df_sd_sp = pd.read_sql_table("SD_tecno_SP_data", con= engine)

    # df = pd.read_sql("SELECT * FROM SD_tecno_FP_data", con = session.bind)

    # Traitement des valeurs manquantes
    st_data_sp = df_st_sp.dropna(subset="Purchased_Qty")
    st_data_fp = df_st_fp.dropna(subset="Purchased_Qty")
    sd_data_sp = df_sd_sp.dropna(subset="Purchases_Qty")
    sd_data_fp = df_sd_fp.dropna(subset="Purchases_Qty")

finally:
    print("Data loaded successfully")


##########################################
### OTHERS CODE
###############

# Recuperation du Mois et l'annee en cours dans une date
annee = datetime.now().year
annee_str = str(annee)
mois  = datetime.now().month
mois_str = str(mois)

# Convertir en date
st_data_sp["Date"] = pd.to_datetime(st_data_sp["Date"], errors="coerce")
st_data_fp["Date"] = pd.to_datetime(st_data_fp["Date"], errors="coerce")
sd_data_sp["Date"] = pd.to_datetime(sd_data_sp["Date"], errors="coerce")
sd_data_fp["Date"] = pd.to_datetime(sd_data_fp["Date"], errors="coerce")


# Considerons seulement les donnees pour l'annee en cours pour nos ST et SD
year_st_sp = st_data_sp[st_data_sp["Years"] == annee_str]
year_st_fp = st_data_fp[st_data_fp["Years"] == annee_str]
year_sd_sp = sd_data_sp[sd_data_sp["Years"] == annee_str]
year_sd_fp = sd_data_fp[sd_data_fp["Years"] == annee_str]

# Considerons seulement les donnees pour l'annee en cours pour nos ST et SD
month_st_sp = st_data_sp[st_data_sp["Months"] == mois_str]
month_st_fp = st_data_fp[st_data_fp["Months"] == mois_str]
month_sd_sp = sd_data_sp[sd_data_sp["Months"] == mois_str]
month_sd_fp = sd_data_fp[sd_data_fp["Months"] == mois_str]




###########################
###### GRAPHIC ############
###########################

# 1. Graphic ST for SP
st_sp_year = st_data_sp.groupby("Years", as_index= False)["Purchased_Qty"].sum()
st_sp_year_fig = px.line(st_sp_year, x="Years", y="Purchased_Qty", text= "Purchased_Qty", title="ST SMART PHONE YEARLY SITUATION")
st_sp_year_fig.update_traces(textposition = 'top center')
st_sp_year_fig.update_layout(
    margin = dict(l=10, r=10, t=30, b=10),
    paper_bgcolor = '#F8F9FA', # Rend le fond du graphique transparent
    #plot_bgcolor = 'rgba(0,0,0,0)' # Rend le fond de la grille transarent 
    width = 1180,
    height = 300   
    )

# 2. Graphic ST for SP
st_fp_year = st_data_fp.groupby("Years", as_index= False)["Purchased_Qty"].sum()
st_fp_year_fig = px.line(st_fp_year, x="Years", y="Purchased_Qty", text= "Purchased_Qty", title="ST FEATURE PHONE YEARLY SITUATION")
st_fp_year_fig.update_traces(textposition = 'top center')
st_fp_year_fig.update_layout(
    margin = dict(l=10, r=10, t=30, b=10),
    paper_bgcolor = '#F8F9FA', # Rend le fond du graphique transparent
    #plot_bgcolor = 'rgba(0,0,0,0)' # Rend le fond de la grille transarent 
    width = 1180,
    height = 300   
    )

# 3. Graphic SD for SP
sd_sp_year = sd_data_sp.groupby("Years", as_index= False)["Purchases_Qty"].sum()
sd_sp_year_fig = px.line(sd_sp_year, x="Years", y="Purchases_Qty", text= "Purchases_Qty", title="SUB-DEALERS SITUATION BY YEARS FOR SP")
sd_sp_year_fig.update_traces(textposition = 'top center')
sd_sp_year_fig.update_layout(
    margin = dict(l=10, r=10, t=30, b=10),
    paper_bgcolor = '#F8F9FA', # Rend le fond du graphique transparent
    #plot_bgcolor = 'rgba(0,0,0,0)' # Rend le fond de la grille transarent 
    width = 1180,
    height = 300   
    )

# 4. Graphic SD for FP
sd_fp_year = sd_data_fp.groupby("Years", as_index= False)["Purchases_Qty"].sum()
sd_fp_year_fig = px.line(sd_fp_year, x="Years", y="Purchases_Qty", text= "Purchases_Qty", title="SUB-DEALERS SITUATION BY YEARS FOR FP")
sd_fp_year_fig.update_traces(textposition = 'top center')
sd_fp_year_fig.update_layout(
    margin = dict(l=10, r=10, t=30, b=10),
    paper_bgcolor = '#F8F9FA', # Rend le fond du graphique transparent
    #plot_bgcolor = 'rgba(0,0,0,0)' # Rend le fond de la grille transarent 
    width = 1180,
    height = 300   
    )

#############################################################
#############################################
# Style commun pour vos "boites" (Paper)
style_boite = {
    "height": "100%", 
    "width": "100%", 
    "display": "flex", 
    "alignItems": "center", 
    "justifyContent": "center",
    "borderRadius": "16px"
}

################################
#### CORPS DU PROGRAMME

def layout():
    return dmc.Container(
        fluid= True, 
        children=[

              
        dmc.Title("REPORTING", order= 1, style={"marginTop": 20}), # order = 1, correspond a H1
        html.Hr(),

        # Un espaceur vertical pour aerer (optionnel mais tres propre avec Mantine)
        dmc.Space(h= "xl"),

        ######################
        ## Date Selector
        dmc.Title("DATA SELECTOR", order= 5, style={"marginBottom": 15}),
        dmc.Grid(
            gutter = "md",
            children = [
                dmc.GridCol(
                    # Annee anterieure
                    span = 6,
                    children= dmc.Grid(
                        gutter = "md",
                        children= [
                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    children = [
                                        dmc.Title("Date Selector", order= 5, style={"marginBottom": 15}),
                                        dcc.DatePickerRange(
                                            id = "date-picker-rep-date1",
                                            start_date= sd_data_sp["Date"].min(),
                                            end_date= sd_data_sp["Date"].max(),
                                            display_format = "YYYY-MM-DD",
                                        ),
                                    ]
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),
                        ]
                    )
                ),
        
                #########################
                #########################
                dmc.GridCol(
                    # Annee recente
                    span = 6,
                    children= dmc.Grid(
                        gutter = "md",
                        children= [
                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    children = [
                                        dmc.Title("Date Selector", order= 5, style={"marginBottom": 15}),
                                        dcc.DatePickerRange(
                                            id = "date-picker-rep-date2",
                                            start_date= sd_data_sp["Date"].min(),
                                            end_date= sd_data_sp["Date"].max(),
                                            display_format = "YYYY-MM-DD",
                                        ),
                                    ]
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),
                        ]
                    ) 
                ),
            ]
        ),

        html.Br(),
        html.Br(),
        html.Br(),


        #############################################
        ############## A. SELL THROUGH ##############
        #############################################
        dmc.Title("A. SELL THROUGH", order= 3, style={"marginBottom": 15}),
        dmc.Divider(my="sm", size= "sm", color="black"),

        dmc.Title("A.1. SELL THROUGH SMART PHONE", order= 5, style={"marginBottom": 15}),

        # ST SMART PHONE
        ###################################
        ## ST SMART PHONE YEARLY SITUATION
        ####################################

        dmc.Grid(
            gutter= "md", # Remplace className = "g-1"
            styles= {
                "backgroundColor" : "#F8F9FA",
                "borderRadius" : "8px",
                "padding" : "10px",
                "boxShadow": "0px 1px 3px rgba(0, 0, 0, 0.05)" # Optionnel pour embellir
            },

            children = [
                dmc.GridCol(
                    span = 12,
                    children= dmc.Paper(dcc.Graph(figure= st_sp_year_fig), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                )
            ]
        ),

        dmc.Grid(
            gutter = "md",
            children = [
                dmc.GridCol(
                    # Annee anterieure
                    span = 6,
                    children= dmc.Grid(
                        gutter = "md",
                        children= [
                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Total Purchase"
                                    children = [
                                        dmc.Text("Total Purchase Qty", c="dimmed", size= "sm"),
                                        dmc.Text(id = "total-purchaseST-old", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Best Week"
                                    children = [
                                        dmc.Text("Best Week", c="dimmed", size= "sm"),
                                        dmc.Text(id = "best-ST-SP-old", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Bad Week"
                                    children = [
                                        dmc.Text("Bad Week", c="dimmed", size= "sm"),
                                        dmc.Text(id = "bad-ST-SP-old", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    #"Monthly Situation graphic Line"
                                    children= [
                                        dcc.Graph(id = "monthly_ST_SP_Line_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    #"Weekly Situation graphic Line"
                                    children = [
                                        dcc.Graph(id = "weekly_ST_SP_Line_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Channel Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "Channel_ST_SP_Bar_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Channel Situation graphic Pie"
                                    children= [
                                        dcc.Graph(id = "Channel_ST_SP_Pie_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Series Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "series_ST_SP_Bar_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Series Situation graphic Pie"
                                    children = [
                                        dcc.Graph(id = "series_ST_SP_Pie_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Models Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "models_ST_SP_Bar_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Models Situation graphic Pie"
                                    children = [
                                        dcc.Graph(id = "models_ST_SP_Pie_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                        ]
                    )
                ),
        
                #########################
                #########################
                dmc.GridCol(
                    # Annee recente
                    span = 6,
                    children= dmc.Grid(
                        gutter = "md",
                        children= [
                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Total Purchase"
                                    children = [
                                        dmc.Text("Total Purchase Qty", c="dimmed", size= "sm"),
                                        dmc.Text(id = "total-purchaseST-new", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Best Week"
                                    children = [
                                        dmc.Text("Best Week", c="dimmed", size= "sm"),
                                        dmc.Text(id = "best-ST-SP-new", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Bad Week"
                                    children = [
                                        dmc.Text("Bad Week", c="dimmed", size= "sm"),
                                        dmc.Text(id = "bad-ST-SP-new", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    #"Monthly Situation graphic Line"
                                    children= [
                                        dcc.Graph(id = "monthly_ST_SP_Line_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    #"Weekly Situation graphic Line"
                                    children = [
                                        dcc.Graph(id = "weekly_ST_SP_Line_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Channel Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "Channel_ST_SP_Bar_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Channel Situation graphic Pie"
                                    children= [
                                        dcc.Graph(id = "Channel_ST_SP_Pie_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Series Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "series_ST_SP_Bar_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Series Situation graphic Pie"
                                    children = [
                                        dcc.Graph(id = "series_ST_SP_Pie_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Models Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "models_ST_SP_Bar_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Models Situation graphic Pie"
                                    children = [
                                        dcc.Graph(id = "models_ST_SP_Pie_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, 
                            ),
                        ]
                    )
                    
                ),

            ]
        ),

        html.Br(),
        dmc.Title("STATISTIQUE SELL THROUGH SMART PHONE", order= 6, style={"marginBottom": 15}),

        dmc.Grid(
            gutter= "md",
            children= [
                dmc.GridCol(
                    span= 6,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [ 
                            dmc.GridCol(
                                span = 6,
                                children = dmc.Paper(
                                    children = [
                                        dmc.Text("Average", c="dimmed", size= "sm"),
                                        dmc.Text(id= "average-st-sp-one", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Median", c="dimmed", size= "sm"),
                                        dmc.Text(id= "median-st-sp-one", size="xl", fw=700),

                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation", c="dimmed", size= "sm"),
                                        dmc.Text(id= "ecartT-st-sp-one", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Maximum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "maxim-st-sp-one", size="xl", fw=700),
                                    ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 12,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Manimum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "minim-st-sp-one", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                ),

                ####

                dmc.GridCol(
                    span= 6,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [  
                            #
                            dmc.GridCol(
                                span = 6,
                                children = dmc.Paper(
                                    children = [
                                        dmc.Text("Average", c="dimmed", size= "sm"),
                                        dmc.Text(id= "average-st-sp-two", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Median", c="dimmed", size= "sm"),
                                        dmc.Text(id= "median-st-sp-two", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation", c="dimmed", size= "sm"),
                                        dmc.Text(id= "ecartT-st-sp-two", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Maximum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "maxim-st-sp-two", size="xl", fw=700),
                                    ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 12,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Manimum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "minim-st-sp-two", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                )
            ]
        ),

        html.Br(),

        dmc.Title("Choose your models", order= 5, style={"marginBottom": 15}),

        ## --- Selecteur multipleselect pour models
        dmc.MultiSelect(
            id = "multiselect-modelST_Smart",
            label = "Select multiple models : ",
            placeholder = "Choose your models",
            data = [],
            clearable = True,
            searchable = True
        ),

        html.Br(),
        dmc.Grid(
            gutter= "md",
            children= [
                dmc.GridCol(
                    span= 12,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [ 
                            dmc.GridCol(
                                span = 8,
                                children = dmc.Paper(
                                    children = [
                                        dcc.Graph(id= "modelSelectBar-st-sp-old")
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 4,
                                children = dmc.Paper(
                                    children=[
                                        dcc.Graph(id= "modelSelectPie-st-sp-old")

                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                ),

            ]
        ),

        html.Br(),
        
        
        #############################################
        # A.2. SELL THROUGH FEATURE PHONE
        #############################################
        html.Hr(),
        html.Br(),
        dmc.Title("A.2. SELL THROUGH FEATURE PHONE", order= 5, style={"marginBottom": 15}),
        
        ######################################
        ## ST FEATURE PHONE YEARLY SITUATION
        ######################################
        
        dmc.Grid(
            gutter= "md", # Remplace className = "g-1"
            styles= {
                "backgroundColor" : "#F8F9FA",
                "borderRadius" : "8px",
                "padding" : "10px",
                "boxShadow": "0px 1px 3px rgba(0, 0, 0, 0.05)" # Optionnel pour embellir
            },

            children = [
                dmc.GridCol(
                    span = 12,
                    children= dmc.Paper(dcc.Graph(figure= st_fp_year_fig), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                )
            ]
        ),
        html.Br(),

        dmc.Grid(
            gutter = "md",
            children = [
                dmc.GridCol(
                    # Annee anterieure
                    span = 6,
                    children= dmc.Grid(
                        gutter = "md",
                        children= [
                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Total Purchase"
                                    children = [
                                        dmc.Text("Total Purchase Qty", c="dimmed", size= "sm"),
                                        dmc.Text(id = "total-purchaseST-FP-old", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Best Week"
                                    children = [
                                        dmc.Text("Best Week", c="dimmed", size= "sm"),
                                        dmc.Text(id = "best-ST-FP-old", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Bad Week"
                                    children = [
                                        dmc.Text("Bad Week", c="dimmed", size= "sm"),
                                        dmc.Text(id = "bad-ST-FP-old", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    #"Monthly Situation graphic Line"
                                    children= [
                                        dcc.Graph(id = "monthly_ST_FP_Line_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    #"Weekly Situation graphic Line"
                                    children = [
                                        dcc.Graph(id = "weekly_ST_FP_Line_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Channel Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "Channel_ST_FP_Bar_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Channel Situation graphic Pie"
                                    children= [
                                        dcc.Graph(id = "Channel_ST_FP_Pie_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Models Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "models_ST_FP_Bar_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Models Situation graphic Pie"
                                    children = [
                                        dcc.Graph(id = "models_ST_FP_Pie_old")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                        ]
                    )
                ),
        
                #########################
                #########################
                dmc.GridCol(
                    # Annee recente
                    span = 6,
                    children= dmc.Grid(
                        gutter = "md",
                        children= [
                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Total Purchase"
                                    children = [
                                        dmc.Text("Total Purchase Qty", c="dimmed", size= "sm"),
                                        dmc.Text(id = "total-purchaseST-FP-new", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Best Week"
                                    children = [
                                        dmc.Text("Best Week", c="dimmed", size= "sm"),
                                        dmc.Text(id = "best-ST-FP-new", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Metric Bad Week"
                                    children = [
                                        dmc.Text("Bad Week", c="dimmed", size= "sm"),
                                        dmc.Text(id = "bad-ST-FP-new", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    #"Monthly Situation graphic Line"
                                    children= [
                                        dcc.Graph(id = "monthly_ST_FP_Line_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    #"Weekly Situation graphic Line"
                                    children = [
                                        dcc.Graph(id = "weekly_ST_FP_Line_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Channel Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "Channel_ST_FP_Bar_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Channel Situation graphic Pie"
                                    children= [
                                        dcc.Graph(id = "Channel_ST_FP_Pie_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 8,
                                children= dmc.Paper(
                                    #"Models Situation graphic Bar"
                                    children = [
                                        dcc.Graph(id = "models_ST_FP_Bar_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                            ),

                            dmc.GridCol(
                                span= 4,
                                children= dmc.Paper(
                                    #"Models Situation graphic Pie"
                                    children = [
                                        dcc.Graph(id = "models_ST_FP_Pie_new")
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"}
                                )#, 
                            ),
                        ]
                    )
                    
                ),

            ]
        ),

        html.Br(),
        dmc.Title("STATISTIQUE SELL THROUGH FEATURE PHONE", order= 6, style={"marginBottom": 15}),

        dmc.Grid(
            gutter= "md",
            children= [
                dmc.GridCol(
                    span= 6,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [ 
                            dmc.GridCol(
                                span = 6,
                                children = dmc.Paper(
                                    children = [
                                        dmc.Text("Average", c="dimmed", size= "sm"),
                                        dmc.Text(id= "average-st-fp-one", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Median", c="dimmed", size= "sm"),
                                        dmc.Text(id= "median-st-fp-one", size="xl", fw=700),

                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation", c="dimmed", size= "sm"),
                                        dmc.Text(id= "ecartT-st-fp-one", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Maximum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "maxim-st-fp-one", size="xl", fw=700),
                                    ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 12,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Manimum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "minim-st-fp-one", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                ),

                ####

                dmc.GridCol(
                    span= 6,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [  
                            #
                            dmc.GridCol(
                                span = 6,
                                children = dmc.Paper(
                                    children = [
                                        dmc.Text("Average", c="dimmed", size= "sm"),
                                        dmc.Text(id= "average-st-fp-two", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Median", c="dimmed", size= "sm"),
                                        dmc.Text(id= "median-st-fp-two", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation", c="dimmed", size= "sm"),
                                        dmc.Text(id= "ecartT-st-fp-two", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Maximum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "maxim-st-fp-two", size="xl", fw=700),
                                    ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 12,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Manimum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "minim-st-fp-two", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                )
            ]
        ),

        html.Br(),

        dmc.Title("Choose your models", order= 5, style={"marginBottom": 15}),

        ## --- Selecteur multipleselect pour models
        dmc.MultiSelect(
            id = "multiselect-modelST_Feature",
            label = "Select multiple models : ",
            placeholder = "Choose your models",
            data = [],
            clearable = True,
            searchable = True
        ),

        html.Br(),
        dmc.Grid(
            gutter= "md",
            children= [
                dmc.GridCol(
                    span= 12,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [ 
                            dmc.GridCol(
                                span = 8,
                                children = dmc.Paper(
                                    children = [
                                        dcc.Graph(id= "modelSelectBar-st-fp-old")
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 4,
                                children = dmc.Paper(
                                    children=[
                                        dcc.Graph(id= "modelSelectPie-st-fp-old")

                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                ),

            ]
        ),

        html.Br(),


        #############################################
        ############# SUB-DEALERS ###################
        #############################################
        html.Hr(),
        # B. SUB-DEALERS
        dmc.Title("B. SUB-DEALERS", order= 3, style={"marginBottom": 15}),
        dmc.Divider(my="sm", size= "sm", color="black"),

        #####################################################
        # B.1. SUB-DEALERS SMART PHONE
        #####################################################
        dmc.Title("B.1. SUB-DEALERS SMART PHONE", order= 5, style={"marginBottom": 15}),
        
        #######################################
        ## SD SMART PHONE YEARLY SITUATION
        #######################################
        
        dmc.Grid(
            gutter = "xs",
            children= [
                dmc.GridCol(
                    span= 12,
                    children= dmc.Paper(
                        children = [
                            dcc.Graph(figure = sd_sp_year_fig)

                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                )
            ]
        ),

       ## Corps du Programme
       dmc.Grid(
           gutter = "md",
           children = [
               # Annee anterieure
               dmc.GridCol(
                   span= 6,
                   children= dmc.Grid(
                       gutter= "md",
                       children = [
                           dmc.GridCol(
                               span= 6,
                               children= dmc.Paper(
                                   children= [
                                        # La Quantite total de SD
                                        dmc.Text("Sud-Dealers Quantity SP", c="dimmed", size= "sm"),
                                        dmc.Text(id = "sd-qty_sd_sp_old", size="xl", fw=700),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                           dmc.GridCol(
                               span= 6,
                               children= dmc.Paper(
                                   children= [
                                        # Les Achats Total des Clients
                                        dmc.Text("Sud-Dealers Total Purchase SP", c="dimmed", size= "sm"),
                                        dmc.Text(id = "total-purchase_sd_sp_old", size="xl", fw=700),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                           dmc.GridCol(
                               span= 12,
                               children= dmc.Paper(
                                   children= [
                                       # Situation Mensuel general des SD
                                        dmc.Text("SD Monthly Purchase SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "monthly-purchase_sd_sp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par regions Graphic Bar
                                        dmc.Text("Situation by Regions SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "regions_bar_sd_sp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par regions Graphic Pie
                                        dmc.Text("Situation by Regions SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "regions_pie_sd_sp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par series Graphic Bar
                                        dmc.Text("Situation by series SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "series_bar_sd_sp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par series Graphic Pie
                                        dmc.Text("Situation by series SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "series_pie_sd_sp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par models Graphic Bar
                                        dmc.Text("Situation by models SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "models_bar_sd_sp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par models Graphic Pie
                                        dmc.Text("Situation by models SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "models_pie_sd_sp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par clients Graphic Bar
                                        dmc.Text("Situation by SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "SD_bar_sd_sp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par clients Graphic Pie
                                        dmc.Text("Situation by SD-SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "SD_pie_sd_sp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ), 
                       ]
                   )
               ),

               # Annee Recente
               dmc.GridCol(
                   span= 6,
                   children= dmc.Grid(
                       gutter= "md",
                       children = [
                           dmc.GridCol(
                               span= 6,
                               children= dmc.Paper(
                                   children= [
                                        # La Quantite total de SD
                                        dmc.Text("Sud-Dealers Quantity SP", c="dimmed", size= "sm"),
                                        dmc.Text(id = "sd-qty_sd_sp_new", size="xl", fw=700),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                           dmc.GridCol(
                               span= 6,
                               children= dmc.Paper(
                                   children= [
                                        # Les Achats Total des Clients
                                        dmc.Text("Sud-Dealers Total Purchase SP", c="dimmed", size= "sm"),
                                        dmc.Text(id = "total-purchase_sd_sp_new", size="xl", fw=700),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                           dmc.GridCol(
                               span= 12,
                               children= dmc.Paper(
                                   children= [
                                       # Situation Mensuel general des SD
                                        dmc.Text("SD Monthly Purchase SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "monthly-purchase_sd_sp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par regions Graphic Bar
                                        dmc.Text("Situation by Regions SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "regions_bar_sd_sp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par regions Graphic Pie
                                        dmc.Text("Situation by Regions SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "regions_pie_sd_sp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par series Graphic Bar
                                        dmc.Text("Situation by series SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "series_bar_sd_sp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par series Graphic Pie
                                        dmc.Text("Situation by series SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "series_pie_sd_sp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par models Graphic Bar
                                        dmc.Text("Situation by models SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "models_bar_sd_sp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par models Graphic Pie
                                        dmc.Text("Situation by models SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "models_pie_sd_sp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par clients Graphic Bar
                                        dmc.Text("Situation by SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "SD_bar_sd_sp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par clients Graphic Pie
                                        dmc.Text("Situation by SP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "SD_pie_sd_sp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ), 
                       ]
                   )
               ),
           ]
           
       ),

        ################################
        ### STATISTIQUE SD SMART PHONE
        ############
        html.Br(),
        dmc.Title("STATISTIQUE SUB-DEALERS SMART PHONE", order= 6, style={"marginBottom": 15}),

        dmc.Grid(
            gutter= "md",
            children= [
                dmc.GridCol(
                    span= 6,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [ 
                            dmc.GridCol(
                                span = 6,
                                children = dmc.Paper(
                                    children = [
                                        dmc.Text("Average SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "average-sd-sp-old", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Median SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "median-sd-sp-old", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "ecartT-sd-sp-old", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Maximum Value SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "maxim-sd-sp-old", size="xl", fw=700),
                                    ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 12,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Minimum Value SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "minim-sd-sp-old", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                ),

                ####

                dmc.GridCol(
                    span= 6,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [  
                            #
                            dmc.GridCol(
                                span = 6,
                                children = dmc.Paper(
                                    children = [
                                        dmc.Text("Average SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "average-sd-sp-new", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Median SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "median-sd-sp-new", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "ecartT-sd-sp-new", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Maximum Value SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "maxim-sd-sp-new", size="xl", fw=700),
                                    ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 12,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Minimum Value SD-SP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "minim-sd-sp-new", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                )
            ]
        ),

        html.Br(),

        # Selection de SD pour afficher les clients
        dmc.Title("Select your Sub-Dealer-SP", order= 5, style={"marginBottom": 15}),

        dmc.Select(
            id = "dropdown_sd_sp_old",
            placeholder= "Choose your Sub-Dealer",
            data = [],
            clearable= True,
            searchable= True
        ),

        html.Br(),

        dmc.Grid(
            gutter = "xs",
            children= [
                dmc.GridCol(
                    span= 12,
                    children= dmc.Paper(
                        children = [
                            dmc.Title("YEARLY SITUATION FOR SP", order= 5, style={"marginBottom": 15}),
                            dcc.Graph(id = "sd_sp_year_fig")
                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                ),

                dmc.GridCol(
                    span = 12,
                    children= dmc.Paper(
                        children = [
                            dmc.Title("MONTHLY SITUATION FOR SP", order= 5, style={"marginBottom": 15}),
                            dcc.Graph(id = "sd_sp_month_fig")
                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                ),

                dmc.GridCol(
                    span = 12,
                    children= dmc.Paper(
                        children = [
                            dmc.Title("MODELS SITUATION FOR SP BY YEARS", order= 5, style={"marginBottom": 15}),
                            dcc.Graph(id = "sd_sp_model_years_fig")
                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                ),
            ]
        ),


        #############################################
        # B.2. SUB-DEALERS FEATURE PHONE
        #############################################
        html.Hr(),
        html.Br(),
        dmc.Title("B.2. SUB-DEALERS FEATURE PHONE", order= 5, style={"marginBottom": 15}),

        #######################################
        ## SD FEATURE PHONE YEARLY SITUATION
        #######################################
        
        dmc.Grid(
            gutter = "xs",
            children= [
                dmc.GridCol(
                    span= 12,
                    children= dmc.Paper(
                        children = [
                            dcc.Graph(figure = sd_fp_year_fig)

                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                )
            ]
        ),

       ## Corps du Programme
       dmc.Grid(
           gutter = "md",
           children = [
               # Annee anterieure
               dmc.GridCol(
                   span= 6,
                   children= dmc.Grid(
                       gutter= "md",
                       children = [
                           dmc.GridCol(
                               span= 6,
                               children= dmc.Paper(
                                   children= [
                                        # La Quantite total de SD
                                        dmc.Text("Sud-Dealers Quantity FP", c="dimmed", size= "sm"),
                                        dmc.Text(id = "sd-qty_sd_fp_old", size="xl", fw=700),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                           dmc.GridCol(
                               span= 6,
                               children= dmc.Paper(
                                   children= [
                                        # Les Achats Total des Clients
                                        dmc.Text("Sud-Dealers Total Purchase FP", c="dimmed", size= "sm"),
                                        dmc.Text(id = "total-purchase_sd_fp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                           dmc.GridCol(
                               span= 12,
                               children= dmc.Paper(
                                   children= [
                                       # Situation Mensuel general des SD
                                        dmc.Text("SD Monthly Purchase FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "monthly-purchase_sd_fp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par regions Graphic Bar
                                        dmc.Text("Situation by Regions FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "regions_bar_sd_fp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par regions Graphic Pie
                                        dmc.Text("Situation by Regions FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "regions_pie_sd_fp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par models Graphic Bar
                                        dmc.Text("Situation by models FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "models_bar_sd_fp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par models Graphic Pie
                                        dmc.Text("Situation by models FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "models_pie_sd_fp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par clients Graphic Bar
                                        dmc.Text("Situation by FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "SD_bar_sd_fp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par clients Graphic Pie
                                        dmc.Text("Situation by SD FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "SD_pie_sd_fp_old"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ), 
                       ]
                   )
               ),

               # Annee Recente
               dmc.GridCol(
                   span= 6,
                   children= dmc.Grid(
                       gutter= "md",
                       children = [
                           dmc.GridCol(
                               span= 6,
                               children= dmc.Paper(
                                   children= [
                                        # La Quantite total de SD
                                        dmc.Text("Sud-Dealers Quantity FP", c="dimmed", size= "sm"),
                                        dmc.Text(id = "sd-qty_sd_fp_new", size="xl", fw=700),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                           dmc.GridCol(
                               span= 6,
                               children= dmc.Paper(
                                   children= [
                                        # Les Achats Total des Clients
                                        dmc.Text("Sud-Dealers Total Purchase Qty FP", c="dimmed", size= "sm"),
                                        dmc.Text(id = "total-purchase_sd_fp_new", size="xl", fw=700),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                           dmc.GridCol(
                               span= 12,
                               children= dmc.Paper(
                                   children= [
                                       # Situation Mensuel general des SD
                                        dmc.Text("SD Monthly Purchase FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "monthly-purchase_sd_fp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par regions Graphic Bar
                                        dmc.Text("Situation by Regions FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "regions_bar_sd_fp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par regions Graphic Pie
                                        dmc.Text("Situation by Regions FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "regions_pie_sd_fp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par models Graphic Bar
                                        dmc.Text("Situation by models FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "models_bar_sd_fp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par models Graphic Pie
                                        dmc.Text("Situation by models FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "models_pie_sd_fp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 8,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par clients Graphic Bar
                                        dmc.Text("Situation by FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "SD_bar_sd_fp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ),

                            dmc.GridCol(
                               span= 4,
                               children= dmc.Paper(
                                   children= [
                                       # Situation par clients Graphic Pie
                                        dmc.Text("Situation by FP", c="dimmed", size= "sm"),
                                        dcc.Graph(id = "SD_pie_sd_fp_new"),
                                   ], withBorder= True, p= "md", shadow= "xs"
                               )
                            ), 
                       ]
                   )
               ),
           ]
           
       ),

        ################################
        ### STATISTIQUE SD FEATURE PHONE
        ############
        html.Br(),
        dmc.Title("STATISTIQUE SUB-DEALERS FEATURE PHONE", order= 6, style={"marginBottom": 15}),

        dmc.Grid(
            gutter= "md",
            children= [
                dmc.GridCol(
                    span= 6,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [ 
                            dmc.GridCol(
                                span = 6,
                                children = dmc.Paper(
                                    children = [
                                        dmc.Text("Average SD-FP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "average-sd-fp-old", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Median SD-FP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "median-sd-fp-old", size="xl", fw=700),

                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation SD-FP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "ecartT-sd-fp-old", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Maximum Value SD-FP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "maxim-sd-fp-old", size="xl", fw=700),
                                    ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 12,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Minimum Value SD-FP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "minim-sd-fp-old", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                ),

                ####

                dmc.GridCol(
                    span= 6,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [  
                            #
                            dmc.GridCol(
                                span = 6,
                                children = dmc.Paper(
                                    children = [
                                        dmc.Text("Average SD-FP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "average-sd-fp-new", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ), 

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Median SD-Fp", c="dimmed", size= "sm"),
                                        dmc.Text(id= "median-sd-fp-new", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation SD-Fp", c="dimmed", size= "sm"),
                                        dmc.Text(id= "ecartT-sd-fp-new", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    )
                            ),

                            dmc.GridCol(
                                span= 6,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Maximum Value SD-FP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "maxim-sd-fp-new", size="xl", fw=700),
                                    ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                )
                            ),

                            dmc.GridCol(
                                span= 12,
                                children = dmc.Paper(
                                    children=[
                                        dmc.Text("Minimum Value SD-FP", c="dimmed", size= "sm"),
                                        dmc.Text(id= "minim-sd-fp-new", size="xl", fw=700),
                                    ], 
                                    withBorder= True, p= "md", shadow= "xs",
                                )
                            ),
                        ]
                    )
                )
            ]
        ),

        html.Br(),

        # Selection clients 
        dmc.Title("Select your Sub-Dealer FP", order= 5, style={"marginBottom": 15}),

        dmc.Select(
            id = "dropdown_sd_fp_old",
            placeholder= "Choose your Sub-dealer",
            data = [],
            clearable= True,
            searchable= True
        ),

        html.Br(),

        dmc.Grid(
            gutter = "xs",
            children= [
                dmc.GridCol(
                    span= 12,
                    children= dmc.Paper(
                        children = [
                            dmc.Title("YEARLY SITUATION SD-FP", order= 5, style={"marginBottom": 15}),
                            dcc.Graph(id = "sd_fp_year_fig")
                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                ),

                dmc.GridCol(
                    span = 12,
                    children= dmc.Paper(
                        children = [
                            dmc.Title("MONTHLY SITUATION SD-FP", order= 5, style={"marginBottom": 15}),
                            dcc.Graph(id = "sd_fp_month_fig")
                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                ),

                dmc.GridCol(
                    span = 12,
                    children= dmc.Paper(
                        children = [
                            dmc.Title("MODELS SITUATION SD-FP BY YEARS", order= 5, style={"marginBottom": 15}),
                            dcc.Graph(id = "sd_fp_model_years_fig")
                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                ),
            ]
        ),

        html.Hr(),
    ])