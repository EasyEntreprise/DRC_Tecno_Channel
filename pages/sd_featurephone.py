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
    df_sd_fp = pd.read_sql_table("SD_tecno_FP_data", con= engine)

    # df = pd.read_sql("SELECT * FROM SD_tecno_FP_data", con = session.bind)

    # Traitement des valeurs manquantes
    sd_data_fp = df_sd_fp.dropna(subset="Purchases_Qty")

finally:
    print("Data loaded successfully")


#########################################
### OTHERS CODE
###############

# Recuperation du Mois et l'annee en cours dans une date
annee = datetime.now().year
annee_str = str(annee)
mois  = datetime.now().month
mois_str = str(mois)

# Convertir en date
sd_data_fp["Date"] = pd.to_datetime(sd_data_fp["Date"], errors="coerce")

tableau  = sd_data_fp.groupby(["Cities", "Customers_Name"], as_index= False)["Purchases_Qty"].sum()
tableau2 = sd_data_fp.groupby(["Customers_Name", "Products"], as_index= False)["Purchases_Qty"].sum()


###########################
###### GRAPHIC ############
###########################
# 1. Graphic SD for FP
sd_fp_year = sd_data_fp.groupby("Years", as_index= False)["Purchases_Qty"].sum()
sd_fp_year_fig = px.line(sd_fp_year, x="Years", y="Purchases_Qty", text= "Purchases_Qty", title="SUB-DEALERS SITUATION BY YEARS FOR FP")
sd_fp_year_fig.update_traces(textposition = 'top center')
sd_fp_year_fig.update_layout(
    margin = dict(l=10, r=10, t=30, b=10),
    paper_bgcolor = '#F8F9FA', # Rend le fond du graphique transparent
    #plot_bgcolor = 'rgba(0,0,0,0)' # Rend le fond de la grille transarent 
    width = 570,
    height = 300   
    )

# 2. Create a DataFrame for sub-dealer evolution by years
sub_dealer_evolution = sd_data_fp.groupby("Years", as_index= False)["Customers_Name"].nunique()
fig_sd_evolution = px.line(sub_dealer_evolution, x="Years", y="Customers_Name", text="Customers_Name", title="Evolution of Sub-dealers by Years")
fig_sd_evolution.update_traces(textposition = 'top center')
fig_sd_evolution.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 570, height = 300)


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

              
        dmc.Title("SD FEATURE PHONE", order= 1, style={"marginTop": 20}), # order = 1, correspond a H1
        html.Hr(),

        # Un espaceur vertical pour aerer (optionnel mais tres propre avec Mantine)
        dmc.Space(h= "xl"),

        ############################################
        ## YEARLY SITUATION AND SD NUMBER BY YEARS
        ############################################

        dmc.Grid(
            gutter = "xs",
            children= [
                dmc.GridCol(
                    span= 6,
                    children= dmc.Paper(
                        children = [
                            dmc.Title("SD YEARLY SITUATION", order= 5, style={"marginBottom": 15}),
                            dcc.Graph(figure = sd_fp_year_fig)

                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                ),

                dmc.GridCol(
                    span = 6,
                    children= dmc.Paper(
                        children = [
                            dmc.Title("SD QUANTITY BY YEARS", order= 5, style={"marginBottom": 15}),
                            dcc.Graph(figure= fig_sd_evolution)

                        ], 
                        withBorder= True, p= "md", shadow= "xs"
                    )
                )
            ]
        ),

        html.Br(),
        html.Br(),

        # Selecteur des dates
        dmc.Title("Date Selector", order= 5, style={"marginBottom": 15}),
        dcc.DatePickerRange(
            id = "date-picker-sd_fp",
            start_date= sd_data_fp["Date"].min(),
            end_date= sd_data_fp["Date"].max(),
            display_format = "YYYY-MM-DD",
        ),

        html.Br(),

        # Metric et Autres
        dmc.Grid(
            gutter = "md",
            children= [
                # --- Colonne metric SD qty for KIN, Katanga, KC, BK et BE
                dmc.GridCol(
                    span = 3,
                    children= dmc.Paper(
                        children= dmc.Stack(
                            gap= "md",
                            children=[
                                # Grille pour aligner plusieurs cartes de manière responsive
                                # Quantite SD pour KIN
                                dmc.GridCol(
                                    span = 12,
                                    children= dmc.Paper(
                                        children= [
                                            dmc.Text("SD Qty for KINSHASA", c="dimmed", size= "sm"),
                                            dmc.Text(id = "metric-SD-KIN_fp", size="xl", fw=700),
                                        ], withBorder= True, p= "md", shadow= "xs",
                                    )
                                ),

                                dmc.GridCol(
                                    span = 12,
                                    children= dmc.Paper(
                                        children= [
                                            dmc.Text("SD Qty for KATANGA", c="dimmed", size= "sm"),
                                            dmc.Text(id = "metric-SD-KAT_fp", size="xl", fw=700),
                                        ], withBorder= True, p= "md", shadow= "xs",
                                    )
                                ),

                                dmc.GridCol(
                                    span = 12,
                                    children= dmc.Paper(
                                        children= [
                                            dmc.Text("SD Qty for KONGO-CENTRAL", c="dimmed", size= "sm"),
                                            dmc.Text(id = "metric-SD-KC_fp", size="xl", fw=700),
                                        ], withBorder= True, p= "md", shadow= "xs",
                                    )
                                ),

                                dmc.GridCol(
                                    span = 12,
                                    children= dmc.Paper(
                                        children= [
                                            dmc.Text("SD Qty for BIG-KASAI", c="dimmed", size= "sm"),
                                            dmc.Text(id = "metric-SD-BK_fp", size="xl", fw=700),
                                        ], withBorder= True, p= "md", shadow= "xs",
                                    )
                                ),

                                dmc.GridCol(
                                    span = 12,
                                    children= dmc.Paper(
                                        children= [
                                            dmc.Text("SD Qty for BIG-EQUATOR", c="dimmed", size= "sm"),
                                            dmc.Text(id = "metric-SD-BE_fp", size="xl", fw=700),
                                        ], withBorder= True, p= "md", shadow= "xs",
                                    )
                                ),
                            ]
                        )
                    )
                ),

                dmc.GridCol(
                    span = 9,
                    children = dmc.Grid(
                        gutter = "md",
                        children= [
                            dmc.GridCol(
                                span = 12,
                                children= dmc.Grid(
                                    gutter = "md",
                                    children = [
                                        dmc.GridCol(
                                            span = 4,
                                            children = dmc.Paper(
                                                #"Metric Total qty SD",
                                                children = [
                                                    dmc.Text("Total Sub-Dealer Quantity", c="dimmed", size= "sm"),
                                                    dmc.Text(id = "metric-SD-ALL_fp", size="xl", fw=700)
                                                ], 
                                                withBorder= True, p= "md", shadow= "xs"
                                            )
                                        ),

                                        dmc.GridCol(
                                            span = 4,
                                            children = dmc.Paper(
                                                #"Metric Total achat"
                                                children = [
                                                    dmc.Text("Total Purchases (Pcs)", c="dimmed", size= "sm"),
                                                    dmc.Text(id = "metric-ALL-Achat_fp", size="xl", fw=700)
                                                ], withBorder= True, p= "md", shadow= "xs"
                                            )
                                        ),

                                        dmc.GridCol(
                                            span = 4,
                                            children = dmc.Paper(
                                                #"Metric Total Invest"
                                                children= [
                                                    dmc.Text("Total Revenue ($)", c="dimmed", size= "sm"),
                                                    dmc.Text(id = "metric-ALL-Invest_fp", size="xl", fw=700)
                                                ], withBorder= True, p= "md", shadow= "xs"
                                            )
                                        ),
                                    ]
                                )
                            ),

                            dmc.Title("Purchases by Cities", order= 5, style={"marginBottom": 15}),

                            dmc.GridCol(
                                span = 12,
                                children= dmc.Grid(
                                    gutter = "md",
                                    children = [
                                        dmc.GridCol(
                                            span = 3,
                                            children = dmc.Paper(
                                                #"Metric Total achat Kin"
                                                children= [
                                                    dmc.Text("KINSHASA-Purchase", c="dimmed", size= "sm"),
                                                    dmc.Text(id= "metric-achat-Kin_fp", size="xl", fw=700)
                                                ], withBorder= True, p= "md", shadow= "xs"
                                            )
                                        ),

                                        dmc.GridCol(
                                            span = 3,
                                            children = dmc.Paper(
                                                #"Metric Total achat Kat"
                                                children =[
                                                    dmc.Text("KATANGA-Purchase", c="dimmed", size= "sm"),
                                                    dmc.Text(id= "metric-achat-Kat_fp", size="xl", fw=700)
                                                ], withBorder= True, p= "md", shadow= "xs")
                                        ),

                                        dmc.GridCol(
                                            span = 2,
                                            children = dmc.Paper(
                                                #"Metric Total achat KC"
                                                children=[
                                                    dmc.Text("K-CENTRAL", c="dimmed", size= "sm"),
                                                    dmc.Text(id= "metric-achat-KC_fp", size="xl", fw=700)
                                                ], withBorder= True, p= "md", shadow= "xs"
                                            )
                                        ),

                                        dmc.GridCol(
                                            span = 2,
                                            children = dmc.Paper(
                                                #"Metric Total achat BK"
                                                children= [
                                                    dmc.Text("BIG-KASAI", c="dimmed", size= "sm"),
                                                    dmc.Text(id= "metric-achat-BK_fp", size="xl", fw=700)
                                                ], withBorder= True, p= "md", shadow= "xs"
                                            )
                                        ),

                                        dmc.GridCol(
                                            span = 2,
                                            children = dmc.Paper(
                                                #"Metric Total achat BK"
                                                children= [
                                                    dmc.Text("BIG-EQUATOR", c="dimmed", size= "sm"),
                                                    dmc.Text(id= "metric-achat-BE_fp", size="xl", fw=700)
                                                ], withBorder= True, p= "md", shadow= "xs"
                                            )
                                        ),
                                    ]
                                )
                            ),

                            dmc.GridCol(
                                span= 12,
                                children = dmc.Grid(
                                    gutter = "md",
                                    children = [
                                        dmc.GridCol(
                                            span = 6,
                                            children = dmc.Paper(
                                                children= [
                                                    dcc.Graph(id="Graphic-Bar-City_fp"),
                                                ], 
                                                withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                                        ),

                                        dmc.GridCol(
                                            span = 6,
                                            children = dmc.Paper(dcc.Graph(id="Graphic-Pie-City_fp"), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                                        ),

                                    ]
                                )
                                
                            ),

                        ]
                    )
                )
            ]
        ),

        html.Br(),

        # Tableau qui affiche les resultats du dataset
        dmc.Title("Table Contents", order= 3, style={"textAlign": "left"}),
        dash_table.DataTable(
            id = 'tableau-datasets-Qty-fp',

            # Les colonnes sont définies une seule fois au chargement initial
            columns = [
                {"name": c, "id": c} for c in sd_data_fp.columns # tableau
            ], page_size = 10,

            # Style optionnel pour s'assurer qu'il s'adapte bien dans la carte
            style_table={
                'overflowX': 'auto',
                "minWidth" : "70px",
                "maxWidth": "120",
                "width" : "1210px",
                "fontZize" : "12px",
                "textAlign" : "center",
                },
            style_cell ={
                "textAlign": "center",
                "fontSize" : "20px",
                "padding" : "8px"
            },

            style_header= {
                "textAlign" :  "center",
                "fontWeight" : "bold"
            }
        ),

        html.Br(),

        # Tableau qui affiche les clients et leurs cities,market et achat total
        dmc.Title("Table Sub-Dealers Purchases", order= 3, style={"textAlign": "left"}),
        dash_table.DataTable(
            id = 'tableau-client-qty_fp',

            # Les colonnes sont définies une seule fois au chargement initial
            columns = [
                {"name": c, "id": c} for c in tableau.columns # tableau
            ], page_size = 10,

            # Style optionnel pour s'assurer qu'il s'adapte bien dans la carte
            style_table={
                'overflowX': 'auto',
                "minWidth" : "70px",
                "maxWidth": "120",
                "width" : "1210px",
                "fontZize" : "12px",
                "textAlign" : "center",
                },
            style_cell ={
                "textAlign": "center",
                "fontSize" : "20px",
                "padding" : "8px"
            },

            style_header= {
                "textAlign" :  "center",
                "fontWeight" : "bold"
            }
        ),

        html.Br(),

        # Monthly situation
        dmc.Title("Monthly situation", order= 5, style={"marginBottom": 15}),
        
        dmc.Grid(
            gutter= "md",
            children= [
                dmc.GridCol(
                    span= 12,
                    children= dmc.Paper(dcc.Graph(id="Graphic-line-month_fp"), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                )
            ]
        ),

        dmc.Grid(
            gutter= "md",
            children= [
                dmc.GridCol(
                    span= 3,
                    children= dmc.Paper(
                        children = dmc.Stack(
                            gap = "md",
                            children = [
                                #"Statistique"
                                # Grille pour aligner plusieurs cartes de manière responsive
                                # Moyenne-Median-Ecart Type
                                # Calcul de la moyenn
                                dmc.GridCol(
                                    span= 12,
                                    children= dmc.Paper(
                                        children=[
                                            dmc.Text("Average", c="dimmed", size= "sm"),
                                            dmc.Text(id= "metric-moyen_fp", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    ),
                                ),

                                dmc.GridCol(
                                    span= 12,
                                    children= dmc.Paper(
                                        children=[
                                            dmc.Text("Median", c="dimmed", size= "sm"),
                                            dmc.Text(id= "metric-medianx_fp", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    ),
                                ),

                                dmc.GridCol(
                                    span= 12,
                                    children= dmc.Paper(
                                        children=[
                                            dmc.Text("Standard Deviation", c="dimmed", size= "sm"),
                                            dmc.Text(id= "metric-ecarType_fp", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    ),
                                ),

                                dmc.GridCol(
                                    span= 12,
                                    children= dmc.Paper(
                                        children=[
                                            dmc.Text("Maximum Value", c="dimmed", size= "sm"),
                                            dmc.Text(id= "metric-max_fp", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    ),
                                ),

                                dmc.GridCol(
                                    span= 12,
                                    children= dmc.Paper(
                                        children=[
                                            dmc.Text("Minimum Value", c="dimmed", size= "sm"),
                                            dmc.Text(id= "metric-min_fp", size="xl", fw=700),
                                        ], 
                                        withBorder= True, p= "md", shadow= "xs",
                                    ),
                                ), 
                            ]
                        )
                    )
                ),

                dmc.GridCol(
                    span= 9,
                    children = dmc.Grid(
                        gutter= "md",
                        children = [
                            dmc.GridCol(
                                span = 12,
                                children = dmc.Paper(
                                    #"Graphic boite a moustache par city"
                                    children= [
                                        dcc.Graph(id= "moustache-graph_fpd"),
                                        dcc.Graph(id='graphic-histo_fpd'),
                                    ], withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            dmc.GridCol(
                                span = 12,
                                children = [
                                    dmc.Select(
                                        id= "nuage-points-sd_fp",
                                        label= "Select one model",
                                        placeholder= "Choose your model",
                                        data = [],
                                        clearable= True,
                                        searchable= True
                                    )
                                ]
                            ),

                            dmc.GridCol(
                                span = 12,
                                children = dmc.Paper(dcc.Graph(id= "graphic-scatter_fpd"), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),
                        ]
                    )
                ) 
            ]
        ),

        html.Br(),

        # Selection Multiple de Cities pour afficher les clients par city
        dmc.Title("Selecte your city", order= 5, style={"marginBottom": 15}),

        dmc.Select(
            id = "dropdown-city_sd_fp",
            label= "Select one city : ",
            placeholder= "Choose your city",
            data = [],
            clearable= True,
            searchable= True
        ),

        html.Br(),
        dmc.Grid(
            gutter = "md",
            children = [
                dmc.GridCol(
                    span = 6,
                    children = dmc.Paper(
                        children = [
                            #"Graphique en Bar qui afficher les clients du city choisi"
                            dcc.Graph(id = "sd-bar-by-city_fp")
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"}
                    )
                ),

                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children = [
                            #"Graphique en Pie qui afficher les clients du city choisi"
                            dcc.Graph(id = "sd-pie-by-city_fp")
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"}
                    )
                ),

                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children = [
                            #"Graphique en Pie qui affiche tout les clients du city"
                            dcc.Graph(id= "graphic-pie-all-sd_fp")
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"}
                    )
                ),
            ]
        ),

        html.Br(),
        dmc.Grid(
            gutter = "md",
            children = [
                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            #"Graphique en Bar qui affiche les models"
                            dcc.Graph(id="fig_bar_models_fp")
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"}
                    )
                ),
            ]
        ),


        html.Br(),

        # Graphic Models
        dmc.Title("Choose your models", order= 5, style={"marginBottom": 15}),

        ## --- Selecteur multipleselect pour models
        dmc.MultiSelect(
            id = "multiselect-models_fpD",
            label = "Select multiple models : ",
            placeholder = "Choose your models",
            data = [],
            clearable = True,
            searchable = True
        ),

        html.Br(),
        dmc.Grid(
            gutter = "md",
            children = [
                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            #"Graphique en Line qui affiche les models choisi par mois"
                            dcc.Graph(id="fig_line_modelMulti_fp")
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"}
                    )
                ),
            ]
        ),

        html.Br(),

        # Tableau qui affiche le nom des clients, modele choisi (un model) et sa qty
        dash_table.DataTable(
            id= "model-table-sd_fp",
            columns = [
                {"name": c, "id": c} for c in tableau2.columns
            ], page_size = 10,
            style_table={
                'overflowX': 'auto',
                "minWidth" : "70px",
                "maxWidth": "120",
                "width" : "1210px",
                "fontZize" : "12px",
                "textAlign" : "center",
                },
            style_cell ={
                "textAlign": "center",
                "fontSize" : "20px",
                "padding" : "8px"
            },

            style_header= {
                "textAlign" :  "center",
                "fontWeight" : "bold"
            }
        ),

        html.Br(),
        html.Hr(),

        # Profil de client
        dmc.Title("Sud-Dealers Profil", order= 2, style={"textAlign": "left"}),
        
        dmc.Select(
            id = "sub-dealer-profil-sd_fp",
            label= "Select one Sub-Dealer : ",
            placeholder= "Choose your Sub-Dealer",
            data = [],
            clearable= True,
            searchable= True
        ),
        html.Br(),
        dmc.Grid(
            gutter = "md",
            children = [
                dmc.GridCol(
                    span = 4,
                    children = dmc.Paper(
                        children = [
                            #"SD NAME"
                            dmc.Text("Sub-Dealer Name", c="dimmed", size= "sm"),
                            dmc.Text(id = "metric-SD-Name_fp", size="xl", fw=700),
                        ],
                        withBorder= True, p="md", shadow= "xs"
                    )
                ),

                dmc.GridCol(
                    span = 4,
                    children = dmc.Paper(
                        children = [
                            #"Total Achat"
                            dmc.Text("Sub-Dealer Purchase", c="dimmed", size= "sm"),
                            dmc.Text(id = "metric-SD-achat_fp", size="xl", fw=700),
                        ],
                        withBorder= True, p="md", shadow= "xs"
                    )
                ),

                dmc.GridCol(
                    span = 4,
                    children = dmc.Paper(
                        children = [
                            #"Total Invest"
                            dmc.Text("Sub-Dealer Revenue", c="dimmed", size= "sm"),
                            dmc.Text(id = "metric-SD-invest_fp", size="xl", fw=700),
                        ],
                        withBorder= True, p="md", shadow= "xs"
                    )
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

        dmc.Grid(
            gutter = "md",
            children = [
                dmc.GridCol(
                    span = 12,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [
                            dmc.GridCol(
                                span = 3,
                            ),

                            dmc.GridCol(
                                span = 6,
                                children= dmc.Paper(
                                    children = [
                                        #"Graphique en Radar"
                                        dcc.Graph(id= "sd-radar_fp")

                                    ],
                                    withBorder= True, p="md", style={**style_boite, "height": "300px"}
                                )
                            ),

                            #dmc.Text("", c="dimmed", size= "sm"),

                            dmc.GridCol(
                                span = 3,
                            ),
                        ]
                    )
                ),

                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            #"Graphique en Line qui afficher qty achat anne du client par mois"
                            dcc.Graph(id= "sd-line-annee_fp")
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"}
                    )
                ),

                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            #"Graphique en Line qui afficher qty achat du client par mois"
                            dcc.Graph(id= "sd-line-achat_fp")
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"}
                    )
                ),

                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            #"Graphique en Bar qui affiche tout les modeles acheter par le client"
                            dcc.Graph(id= "sd-bar-models_fp")
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"}
                    )
                ),
            ]
        ),
    ])

# ==========================================
# LE CALLBACK LISTE DEROULANTE 1
# ==========================================
@dash.callback(
        [Output('nuage-points-sd_fp', 'data'),
         Output('nuage-points-sd_fp', 'value'),
        ],
        [Input('date-picker-sd_fp', 'start_date'),
         Input('date-picker-sd_fp', 'end_date'),
        ]
)

def maj_liste_deroulanteOne_sp(debut, fin):
    if not debut or not fin :
        produits_uniques_sp = sd_data_fp["Products"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date       = pd.to_datetime(debut)
        end_date         = pd.to_datetime(fin)
        df_temp          = sd_data_fp[(sd_data_fp["Date"] >= start_date) & (sd_data_fp["Date"] <= end_date)]
        produits_uniques_sp = df_temp["Products"].unique()


    # Formater les options pour le dmc.Select de Mantine
    options_sp = [{"value": prod, "label": prod} for prod in produits_uniques_sp]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    valeur_par_defaut_sp = produits_uniques_sp[0] if len(produits_uniques_sp) > 0 else None

    return options_sp, valeur_par_defaut_sp


# ==========================================
# LE CALLBACK LISTE DEROULANTE 2
# ==========================================
@dash.callback(
        [Output('dropdown-city_sd_fp', 'data'),
         Output('dropdown-city_sd_fp', 'value'),
        ],
        [Input('date-picker-sd_fp', 'start_date'),
         Input('date-picker-sd_fp', 'end_date'),
        ]
)

def maj_liste_deroulanteTwo_sp(debut, fin):
    if not debut or not fin :
        city_uniques = sd_data_fp["Cities"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date       = pd.to_datetime(debut)
        end_date         = pd.to_datetime(fin)
        df_temp          = sd_data_fp[(sd_data_fp["Date"] >= start_date) & (sd_data_fp["Date"] <= end_date)]
        city_uniques = df_temp["Cities"].unique()


    # Formater les options pour le dmc.Select de Mantine
    options_city = [{"value": city, "label": city} for city in city_uniques]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    valeur_par_defaut_city = city_uniques[0] if len(city_uniques) > 0 else None

    return options_city, valeur_par_defaut_city


# ==========================================
# LE CALLBACK LISTE DEROULANTE 3
# ==========================================
@dash.callback(
        [Output('multiselect-models_fpD', 'data'),
         Output('multiselect-models_fpD', 'value'),
        ],
        [Input('date-picker-sd_fp', 'start_date'),
         Input('date-picker-sd_fp', 'end_date'),
        ]
)

def maj_liste_deroulanteThree_sp(debut, fin):
    if not debut or not fin :
        models_uniques = sd_data_fp["Products"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date     = pd.to_datetime(debut)
        end_date       = pd.to_datetime(fin) 
        df_temp        = sd_data_fp[(sd_data_fp["Date"] >= start_date) & (sd_data_fp["Date"] <= end_date)]
        models_uniques = df_temp["Products"].unique()

    # Formater les options pour le dmc.Select de Mantine
    options_models = [{"value": models, "label": models} for models in models_uniques]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    models_par_defaut = [models_uniques[0]] if len(models_uniques) > 0 else []

    return options_models, models_par_defaut

# ==========================================
# LE CALLBACK sub-dealer-profil-sd-sp
# ==========================================
@dash.callback(
        [Output('sub-dealer-profil-sd_fp', 'data'),
         Output('sub-dealer-profil-sd_fp', 'value'),
        ],
        [Input('date-picker-sd_fp', 'start_date'),
         Input('date-picker-sd_fp', 'end_date'),
        ]
)

def maj_liste_deroulanteFour_sp(debut, fin):
    if not debut or not fin :
        subDealers_uniques_sp = sd_data_fp["Customers_Name"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date       = pd.to_datetime(debut)
        end_date         = pd.to_datetime(fin)
        df_temp          = sd_data_fp[(sd_data_fp["Date"] >= start_date) & (sd_data_fp["Date"] <= end_date)]
        subDealers_uniques_sp = df_temp["Customers_Name"].unique()


    # Formater les options pour le dmc.Select de Mantine
    options_sp = [{"value": prod, "label": prod} for prod in subDealers_uniques_sp]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    valeur_par_defaut_sp = subDealers_uniques_sp[0] if len(subDealers_uniques_sp) > 0 else None

    return options_sp, valeur_par_defaut_sp


# ==========================================
# LE CALLBACK DE DISTRIBUTION
# ==========================================
@dash.callback(
    [
        # Metric
        Output('metric-SD-KIN_fp', 'children'),
        Output('metric-SD-KAT_fp', 'children'),
        Output('metric-SD-KC_fp', 'children'),
        Output('metric-SD-BK_fp', 'children'),
        Output('metric-SD-BE_fp', 'children'),
        Output('metric-SD-ALL_fp', 'children'),
        Output('metric-ALL-Achat_fp', 'children'),
        Output('metric-ALL-Invest_fp', 'children'),
        Output('metric-achat-Kin_fp', 'children'),
        Output('metric-achat-Kat_fp', 'children'),
        Output('metric-achat-KC_fp', 'children'),
        Output('metric-achat-BK_fp', 'children'),
        Output('metric-achat-BE_fp', 'children'),
        Output('metric-moyen_fp', 'children'),
        Output('metric-medianx_fp', 'children'),
        Output('metric-ecarType_fp', 'children'),
        Output('metric-max_fp', 'children'),
        Output('metric-min_fp', 'children'),
        Output('metric-SD-Name_fp', 'children'),
        Output('metric-SD-achat_fp', 'children'),
        Output('metric-SD-invest_fp', 'children'),

        # Graphic
        Output('Graphic-Bar-City_fp', 'figure'),
        Output('Graphic-Pie-City_fp', 'figure'),
        Output('Graphic-line-month_fp', 'figure'),
        Output('moustache-graph_fpd', 'figure'),
        Output('graphic-histo_fpd', 'figure'),
        Output('graphic-scatter_fpd', 'figure'), 
        Output('sd-bar-by-city_fp', 'figure'),
        Output('sd-pie-by-city_fp', 'figure'),
        Output('graphic-pie-all-sd_fp', 'figure'),
        Output('fig_bar_models_fp', 'figure'),
        Output('fig_line_modelMulti_fp', 'figure'),  # Apres ici
        Output('sd-radar_fp', 'figure'),
        Output('sd-line-annee_fp', 'figure'),
        Output('sd-line-achat_fp', 'figure'),
        Output('sd-bar-models_fp', 'figure'),

        # Tableau
        Output('tableau-client-qty_fp', 'data'),
        Output('model-table-sd_fp', 'data'),
        Output('tableau-datasets-Qty-fp', 'data'),
    ],
    [
        Input('date-picker-sd_fp', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-sd_fp', 'end_date'),
        Input('nuage-points-sd_fp', 'value'),
        Input('dropdown-city_sd_fp', 'value'),
        Input('multiselect-models_fpD', 'value'),
        Input('sub-dealer-profil-sd_fp', 'value'),
    ]
)

def filter_data(debut, fin, produit, city, models, clients):
    # 1. Sécurité : si une des deux dates est effacée par l'utilisateur
    if not debut or not fin:
        df_filtre = sd_data_fp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date = pd.to_datetime(debut)
        end_date = pd.to_datetime(fin)
        df_filtre = sd_data_fp[(sd_data_fp['Date'] >= start_date) & (sd_data_fp['Date'] <= end_date)]
    
    if produit :
        df_all_model = df_filtre[df_filtre["Products"] == produit]
    else :
        df_all_model = df_filtre.copy()

    if city :
        df_city_sd = df_filtre[df_filtre["Cities"] == city]
    else :
        df_city_sd = df_filtre.copy()

    if city :
        df_city_sd = df_filtre[df_filtre["Cities"] == city]
    else :
        df_city_sd = df_filtre.copy()

    if models :
        df_all_models_multi = df_filtre[df_filtre["Products"].isin(models)]
    else :
        df_all_models_multi = df_filtre.copy()

    if clients :
        df_clients = df_filtre[df_filtre["Customers_Name"] == clients]
    else :
        df_clients = df_filtre.copy()



    ####################
    ### METRIC
    ####################
    
    #-------------Recuperer Nbr client par region ----------
    kin_qty = df_filtre[df_filtre["Cities"]== "KINSHASA"] # Filtrer la dataset en Kinshasa comme Cities
    kat_qty = df_filtre[df_filtre["Cities"]== "BIG-KATANGA"]
    kc_qty  = df_filtre[df_filtre["Cities"]== "KONGO-CENTRAL"]
    bk_qty  = df_filtre[df_filtre["Cities"]== "BIG-KASAI"]
    be_qty  = df_filtre[df_filtre["Cities"]== "BIG-EQUATOR"]

    kinshasa = f"{kin_qty["Customers_Name"].nunique()} SD" # Recuperer le nombre des clients
    katanga  = f"{kat_qty["Customers_Name"].nunique()} SD"
    kcongo   = f"{kc_qty["Customers_Name"].nunique()} SD"
    bkasai   = f"{bk_qty["Customers_Name"].nunique()} SD"
    bequator = f"{be_qty["Customers_Name"].nunique()} SD"

    total_sd     = f"{df_filtre["Customers_Name"].nunique()} SD" # Recuperation du nombre des clients
    total_somme  = f"{df_filtre["Purchases_Qty"].sum()} Pcs"
    total_revenu = f"{df_filtre["Investments_usd"].sum()} $"
    

    kin = f"{kin_qty["Purchases_Qty"].sum()} Pcs"
    kat = f"{kat_qty["Purchases_Qty"].sum()} Pcs"
    kc  = f"{kc_qty["Purchases_Qty"].sum()} Pcs"
    bk  = f"{bk_qty["Purchases_Qty"].sum()} Pcs"
    be  = f"{be_qty["Purchases_Qty"].sum()} Pcs"

    ## Statistiques #####
    statis_group = df_filtre.groupby("Date", as_index= False)["Purchases_Qty"].sum()
    
    static_mean_spSD   = statis_group["Purchases_Qty"].mean()
    static_median_spSD = statis_group["Purchases_Qty"].median()
    static_ecartT      = statis_group["Purchases_Qty"].std()
    maximum            = statis_group["Purchases_Qty"].max()
    minimum            = statis_group["Purchases_Qty"].min()

    ## Client #####
    sd_name     = df_clients["Customers_Name"].unique()
    sd_purchase = f"{df_clients["Purchases_Qty"].sum()} Pcs"
    sd_revenu   = f"{df_clients["Investments_usd"].sum()} $"


    ###################
    ### GRAPHIC
    ###################

    # 1. Graphic en Bar par city
    bar_city = df_filtre.groupby("Cities", as_index= False)["Purchases_Qty"].sum()
    
    fig_bar_city = px.bar(bar_city, x="Cities", y="Purchases_Qty", color="Cities", text="Purchases_Qty", title="City situation for SD-FP")
    fig_bar_city.update_traces(textposition = 'outside')
    fig_bar_city.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', showlegend= False, width = 430, height = 290)

    # 2. Graphic en Pie par city
    fig_pie_city = go.Figure(data = [go.Pie(labels = bar_city["Cities"], values= bar_city["Purchases_Qty"], title = "City Proportions for SD-SP", opacity=0.5)])
    fig_pie_city.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
    fig_pie_city.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 430, height = 280)

    # 3. Graphic en Line pour purchase par mois
    monthly_all = df_filtre.groupby("Date", as_index= False)["Purchases_Qty"].sum()
    monthly_sd= px.line(monthly_all , x="Date", y="Purchases_Qty", text= "Purchases_Qty", title="Monthly purchase FOR SD-FP")
    monthly_sd.update_traces(textposition = 'top center')
    monthly_sd.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # 4. Graphic en Boite a moustache 
    prime = df_filtre.groupby(["Cities", "Date"], as_index= False)["Purchases_Qty"].sum()
    fig_boite_moust = px.box(prime, x="Cities", y="Purchases_Qty", color="Cities", title="Purchases breakdown by City", points= "outliers")
    fig_boite_moust.update_layout(showlegend= False, height= 290, width= 445, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor = '#F8F9FA')

    # 5. Graphic en Histogramme 
    prime_sd = df_filtre.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    fig_hist_spD = px.histogram(prime_sd, x= "Purchases_Qty", nbins= 30, title="Breakdown of Purchased Qty", labels= {"Purchased_Qty":"Purchasesd Quantity"})
    fig_hist_spD.update_layout(height= 290, width= 445, xaxis_title= "Purchases Qty", yaxis_title = "Frequency", margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA')

    # 6. Graphique en nuage au point pour comparer les prix par rappor a la vente
    df_model = (df_all_model.groupby(["Date", "Products"]).agg({"Prices_usd":"mean", "Purchases_Qty":"sum"}).reset_index())
    fig_scatter = px.scatter(
        df_model,
        x= "Prices_usd",
        y= "Purchases_Qty",
        text= "Date",
        hover_data= ["Products"],
        title= f"Price vs Purchase - {produit}"
    )
    fig_scatter.update_traces(textposition= "top center")
    fig_scatter.update_layout(height= 290, width= 890, xaxis_title= "Purchased Qty", yaxis_title = "Frequency", margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA')

    # 7. Graphique en Bar pour afficher les SD selon la city choisie
    city_choose = df_city_sd.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    fig_bar_citySelect = px.bar(city_choose, x="Customers_Name", y="Purchases_Qty", color="Customers_Name", text="Purchases_Qty", title="Sub-Dealers by City")
    fig_bar_citySelect.update_traces(textposition = 'outside')
    fig_bar_citySelect.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', showlegend= False, width = 590, height = 290)
    fig_bar_citySelect.update_xaxes(tickfont = dict(size= 8))


    # 8. Graphique en Pie pour afficher les SD selon la city choisie
    fig_pie_citySelect = go.Figure(data = [go.Pie(labels = city_choose["Customers_Name"], values= city_choose["Purchases_Qty"], hole = 0.4, textinfo= "none", hoverinfo="skip", title = "Proportions for SD by city", opacity=0.5)])
    fig_pie_citySelect.update_traces (
        textinfo = "none", # Ne rien afficher sur le graphic
        hovertemplate = "<b>%{label}</b><br>"
                        "Ventes : %{value}<br>"
                        "Pourcentage : %{percent}<extra></extra>" 
        )
    fig_pie_citySelect.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 8), font= dict(size= 8), width = 290, height = 280)

    # 9. Graphique en Pie pour all sub-dealer
    pie_all_sd = df_filtre.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    fig_pie_allSD = go.Figure(data = [go.Pie(labels = pie_all_sd["Customers_Name"], values= pie_all_sd["Purchases_Qty"], hole = 0.4, textinfo= "none", hoverinfo="skip", title = "Proportions for SD-SP", opacity=0.5)])
    fig_pie_allSD.update_traces (
        textinfo = "none", # Ne rien afficher sur le graphic
        hovertemplate = "<b>%{label}</b><br>"
                        "Ventes : %{value}<br>"
                        "Pourcentage : %{percent}<extra></extra>" 
        )
    fig_pie_allSD.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 8), font= dict(size= 8), width = 290, height = 280)

    # 10. Graphique en Bar pour all models
    bar_modeles = df_filtre.groupby("Products", as_index= False)["Purchases_Qty"].sum()
    fig_bar_models = px.bar(bar_modeles, x="Products", y="Purchases_Qty", color="Products", text="Purchases_Qty", title="Models Situation")
    fig_bar_models.update_traces(textposition = 'outside')
    fig_bar_models.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', showlegend= False, width = 1180, height = 290)


    # 11. Graphique en Line pour all plusieurs modeles par mois
    
    multi_model = df_all_models_multi.groupby(["Date", "Products"], as_index= False)["Purchases_Qty"].sum()
    fig_line_modelMulti = px.line(multi_model , x="Date", y="Purchases_Qty", text= "Purchases_Qty", color="Products", title="Monthly Purchase by Models")
    fig_line_modelMulti.update_traces(textposition = 'top center')
    fig_line_modelMulti.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # 12. Graphique en Line pour afficher les achats
    client_radar = df_clients.groupby(["Customers_Name", "Products"], as_index= False)["Purchases_Qty"].sum()
    fig_profil = go.Figure()
    fig_profil.add_trace(go.Scatterpolar(
        r= client_radar["Purchases_Qty"],
        theta= client_radar["Products"],
        fill= 'toself',
        name= clients
    ))

    fig_profil.update_layout(
        polar = dict(
            radialaxis= dict(visible=True, range= [0, 100])
        ),
        showlegend = False
    )

    # 13. Graphique en Line pour afficher les achats annuel
    df_clients_years = sd_data_fp[sd_data_fp["Customers_Name"] == clients]
    
    sd_years = df_clients_years.groupby("Years", as_index= False)["Purchases_Qty"].sum()
    sd_years_line = px.line(sd_years , x="Years", y="Purchases_Qty", text= "Purchases_Qty", title="Yearly Purchase")
    sd_years_line.update_traces(textposition = 'top center')
    sd_years_line.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)


    # 14. Graphique en Line pour afficher les achats mensuels
    client_model = df_clients.groupby("Date", as_index= False)["Purchases_Qty"].sum()
    client_line_model = px.line(client_model , x="Date", y="Purchases_Qty", text= "Purchases_Qty", title="Monthly Purchase")
    client_line_model.update_traces(textposition = 'top center')
    client_line_model.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # 15. Graphique en Bar pour afficher les modeles
    client_modeles = df_clients.groupby("Products", as_index= False)["Purchases_Qty"].sum()
    client_bar_models = px.bar(client_modeles, x="Products", y="Purchases_Qty", color="Products", text="Purchases_Qty", title="Models Situation")
    client_bar_models.update_traces(textposition = 'outside')
    client_bar_models.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', showlegend= False, width = 1180, height = 290)


    ####################################################
    # Préparation des données pour VOTRE DataTable
    ####################################################
    tableau = df_filtre.groupby(["Cities", "Customers_Name"], as_index= False)["Purchases_Qty"].sum()
    donnees_tableau = tableau.to_dict("records")
    
    tableau2 = df_all_models_multi.groupby(["Customers_Name", "Products"], as_index= False)["Purchases_Qty"].sum()
    donnees_tableau2 = tableau2.to_dict("records")

    donnees_tableau3 = df_filtre.to_dict("records")

    # 4. Envoi simultané aux composants graphiques et métriques
    return kinshasa, katanga, kcongo, bkasai, bequator, total_sd, total_somme, total_revenu, kin, kat, kc, bk, be, static_mean_spSD, static_median_spSD, static_ecartT, maximum, minimum, sd_name, sd_purchase, sd_revenu, fig_bar_city, fig_pie_city, monthly_sd, fig_boite_moust, fig_hist_spD, fig_scatter, fig_bar_citySelect, fig_pie_citySelect, fig_pie_allSD, fig_bar_models, fig_line_modelMulti, fig_profil, sd_years_line, client_line_model, client_bar_models, donnees_tableau, donnees_tableau2, donnees_tableau3
                                                                                                                                                                                              


