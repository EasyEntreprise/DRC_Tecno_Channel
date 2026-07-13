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
    df_st_sp = pd.read_sql_table("ST_tecno_SP_data", con= engine)

    # df = pd.read_sql("SELECT * FROM SD_tecno_FP_data", con = session.bind)

    # Traitement des valeurs manquantes
    st_data_sp = df_st_sp.dropna(subset="Purchased_Qty")


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
st_data_sp["Date"] = pd.to_datetime(st_data_sp["Date"])




###########################
###### GRAPHIC ############
###########################

#######################
# A. Annual Situation
##############
# 1. Graphic ST for SP
st_sp_year = st_data_sp.groupby("Years", as_index= False)["Purchased_Qty"].sum()
st_sp_year_fig = px.line(st_sp_year, x="Years", y="Purchased_Qty", text= "Purchased_Qty", title="SELL THROUGH FOR SP")
st_sp_year_fig.update_traces(textposition = 'top center')
st_sp_year_fig.update_layout(
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

              
        dmc.Title("ST SMART PHONE", order= 1, style={"marginTop": 20}), # order = 1, correspond a H1
        html.Hr(),

        # Un espaceur vertical pour aerer (optionnel mais tres propre avec Mantine)
        dmc.Space(h= "xl"),
        

        ###############################
        ## YEARLY SITUATION
        ###############################
        dmc.Title("I. YEARLY SITUATION", order= 3, style={"marginBottom": 15}),

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

        html.Br(),
        html.Br(),

        # Selecteur des dates
        dmc.Title("Date Selector", order= 5, style={"marginBottom": 15}),
        dcc.DatePickerRange(
            id = "date-picker-st-sp",
            start_date= st_data_sp["Date"].min(),
            end_date= st_data_sp["Date"].max(),
            display_format = "YYYY-MM-DD",
        ),
        

        html.Br(),
        
        dmc.Grid(
            gutter = "xs",
            children = [
                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children= [
                            dmc.Text("Total Purchase (Pcs)", c= "dimmed", size="sm"),
                            dmc.Text(id="metric-achat", size= "xl", fw=700),
                        ], withBorder= True,
                        p= "md",
                        shadow= "xs",
                    )
                ),

                dmc.GridCol(
                    span = 3,
                    children= dmc.Paper(
                        children=[
                            dmc.Text(
                                "Revenue ($)",
                                c= "dimmed",
                                size= "sm"
                            ),

                            dmc.Text(id="metric-revenu", size="xl", fw=700),
                        ], withBorder= True, p= "md", shadow= "xs"
                    ),
                ),

                dmc.GridCol(
                    span = 3,
                    children= dmc.Paper(
                        children= [
                            dmc.Text("Best Week", c="dimmed", size= "sm"),
                            dmc.Text(id= "metric-bestWeek", size="xl", fw=700),
                        ], withBorder= True, p= "md", shadow= "xs",
                    ),
                ),

                dmc.GridCol(
                    span = 3, 
                    children= dmc.Paper(
                        children= [
                            dmc.Text("Worst Week", c="dimmed", size= "sm"),
                            dmc.Text(id="metric-badWeek", size="xl", fw=700),
                        ], withBorder= True, p= "md", shadow= "xs",
                    ),
                ),
            ]

        ),

        html.Br(),

        # Conteneurs pour les resultats filtres
        dmc.Title("Table Contents", order= 3, style={"textAlign": "left"}),
        dash_table.DataTable(
            id = 'mon-tableau',

            # Les colonnes sont définies une seule fois au chargement initial
            columns = [
                {"name": c, "id": c} for c in st_data_sp.columns
            ], page_size = 10,

            # Style optionnel pour s'assurer qu'il s'adapte bien dans la carte
            style_table={'overflowX': 'auto'}
        ),

        

        html.Br(),

        # Graphic Channel Bar et Pie
        dmc.Title("Channel Proportion", order= 5, style={"marginBottom": 15}),

        # -----Channel proportion ---
        dmc.Grid(

            gutter= "md",
            children= [
                # --- Colonne de gauche (Metric)--
                dmc.GridCol(
                    span = 3,
                    children= dmc.Grid(
                        gutter= "md",
                        children= [
                            # Calcul de la moyenn
                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    children=[
                                        dmc.Text("Average", c="dimmed", size= "sm"),
                                        dmc.Text(id= "metric-average", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs",
                                ),
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    children=[
                                        dmc.Text("Median", c="dimmed", size= "sm"),
                                        dmc.Text(id= "metric-median", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs",
                                ),
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation", c="dimmed", size= "sm"),
                                        dmc.Text(id= "metric-mode", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs",
                                ),
                            ),
                        ]
                    )
                    
                ),

                # -- Colonne de droite (Graphic)
                dmc.GridCol(
                    span= 9,
                    children= dmc.Grid(
                        gutter = "md",
                        children = [
                            # Graphic bar de Channel
                            dmc.GridCol(
                                span = 8,
                                # "Graphic Bar Channel
                                children= dmc.Paper(
                                    children = [
                                        dcc.Graph(id='bar-channel'),
                                    ],
                                    withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            # Graphic channel Pie
                            dmc.GridCol(
                                span = 4,
                                children= dmc.Paper(
                                    # "Graphic Pie Channel"
                                    children = [
                                        dcc.Graph(id='pie-channel'),
                                    ],
                                    withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            # --- Graphic Boite a moustapha
                            dmc.GridCol(
                                span = 12,
                                children= dmc.Paper(
                                    #"Graphic Boite a Moustache",
                                    children = [
                                        dcc.Graph(id= "moustache-graph"),
                                        dcc.Graph(id='box-channel'),

                                    ],
                                    withBorder= True, p= "md", style={**style_boite, "height": "370px"})
                            ),
                        ]
                    )
                )
            ]
        ),

        html.Br(),

        # Selecteur du modele et graphique nuage a points
        dmc.Grid(
            gutter = "xs",
            children= [
                dmc.GridCol(
                    span= 12,
                    children= [
                        dmc.Select(
                            id = "dropdown-product",
                            label= "Select one model : ",
                            placeholder= "Choose your model",
                            data = [],
                            clearable= True,
                            searchable= True
                        )
                    ]
                ),

                dmc.GridCol(
                    span = 12,
                    children= dmc.Paper(
                        children= [
                            dcc.Graph(id='scatter-price')
                        ]
                    )
                )
            ]

        ),

        html.Br(),

        # Graphic Monthly and Weekly Situation
        dmc.Title("Monthly and Weekly Situation", order= 5, style={"marginBottom": 15}),

        dmc.Grid(
            gutter = "md",
            children = [
                
                # --- Monthly Situation
                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            dcc.Graph(id= "line-monthly"),
                        ], 
                        withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                ),

                # --- Weekly Situation
                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            dcc.Graph(id= "line-weekly"),
                        ],
                        withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                )
            ]
        ),

        html.Br(),

        # Graphic Series
        dmc.Title("Choose your series", order= 5, style={"marginBottom": 15}),

        ## --- Selecteur multipleselect pour series
        dmc.MultiSelect(
            id = "multiselect-series",
            label = "Select multiple series : ",
            placeholder = "Choose your series",
            data = [],
            clearable = True,
            searchable = True
        ),
        html.Br(),

        ## --- Graphic Bar de series, Pie de series et Bar de channel par serie
        dmc.Grid(
            gutter= "xs", # Remplace className = "g-1"
            styles= {
                "backgroundColor" : "#F8F9FA",
                "borderRadius" : "8px",
                "padding" : "10px",
                "boxShadow": "0px 1px 3px rgba(0, 0, 0, 0.05)" # Optionnel pour embellir
            },

            children= [
                dmc.GridCol(
                    span= 4,
                    children = dmc.Paper(
                        children= [
                            #"Graphic Bar pour series",
                            dcc.Graph(id = "bar_series"),
                        ],
                        withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                ),

                dmc.GridCol(
                    span= 4,
                    children = dmc.Paper(
                        children = [
                            #"Graphic Pie pour Series",
                            dcc.Graph(id = "pie_series"),
                        ],
                        withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                ),

                dmc.GridCol(
                    span= 4,
                    children = dmc.Paper(
                        children = [
                            #"Graphic Bar qui affiche le channel par series"
                            dcc.Graph(id = "channel_series"),
                        ],
                        withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                )
            ]
        ),

        html.Br(),

        # Graphic Models
        dmc.Title("Choose your models", order= 5, style={"marginBottom": 15}),

        ## --- Selecteur multipleselect pour models
        dmc.MultiSelect(
            id = "multiselect-models",
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
                # -- Graphic Line models par mois
                dmc.GridCol(
                    span = 7,
                    children = dmc.Paper(
                        children = [
                            #"Graphic Line models par mois",
                            dcc.Graph(id = "model_months"),
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"})
                ),

                # -- Graphic Bar models par Channel
                dmc.GridCol(
                    span = 5,
                    children = dmc.Paper(
                        children = [
                            #"Graphic Bar models par Channel",
                            dcc.Graph(id = "models_channel"), 
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"})
                ),

                # -- Graphic Line models par week
                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            #"Graphic Line models par week",
                            dcc.Graph(id = "models_weeks"), 
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"})
                ),
            ]
        ),

        html.Br(),


        ## All Models graphic Bar et Pie
        dmc.Grid(
            gutter = "md",
            children= [
                # -- Colonne gauche graphic Bar all models
                dmc.GridCol(
                    span = 8, 
                    children= dmc.Paper(
                        children = [
                            #"Graphic Bar All models",
                            dcc.Graph(id = "all_models_bar"),
                        ],
                        withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                ),

                # -- Colonne droite graphic Pie all models
                dmc.GridCol(
                    span = 4, 
                    children= dmc.Paper(
                        children = [
                            #"Graphic Pie all models",
                            dcc.Graph(id = "all_models_pie"),
                        ],
                        withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                ),
            ]
        )
    
    ])

# ==========================================
# LE CALLBACK LISTE DEROULANTE 1
# ==========================================
@dash.callback(
        [Output('dropdown-product', 'data'),
         Output('dropdown-product', 'value'),
        ],
        [Input('date-picker-st-sp', 'start_date'),
         Input('date-picker-st-sp', 'end_date'),
        ]
)

def maj_liste_deroulanteOne(debut, fin):
    if not debut or not fin :
        produits_uniques = st_data_sp["Products"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date       = pd.to_datetime(debut)
        end_date         = pd.to_datetime(fin)
        df_temp          = st_data_sp[(st_data_sp["Date"] >= start_date) & (st_data_sp["Date"] <= end_date)]
        produits_uniques = df_temp["Products"].unique()


    # Formater les options pour le dmc.Select de Mantine
    options = [{"value": prod, "label": prod} for prod in produits_uniques]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    valeur_par_defaut = produits_uniques[0] if len(produits_uniques) > 0 else None

    return options, valeur_par_defaut


# ==========================================
# LE CALLBACK LISTE DEROULANTE 2
# ==========================================
@dash.callback(
        [Output('multiselect-series', 'data'),
         Output('multiselect-series', 'value'),
        ],
        [Input('date-picker-st-sp', 'start_date'),
         Input('date-picker-st-sp', 'end_date'),
        ]
)

def maj_liste_deroulanteTwo(debut, fin):
    if not debut or not fin :
        series_uniques = st_data_sp["SERIES"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date     = pd.to_datetime(debut)
        end_date       = pd.to_datetime(fin)
        df_temp        = st_data_sp[(st_data_sp["Date"] >= start_date) & (st_data_sp["Date"] <= end_date)]
        series_uniques = df_temp["SERIES"].unique()


    # Formater les options pour le dmc.Select de Mantine
    options_series = [{"value": serie, "label": serie} for serie in series_uniques]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    series_par_defaut = [series_uniques[0]] if len(series_uniques) > 0 else[]

    return options_series, series_par_defaut


# ==========================================
# LE CALLBACK LISTE DEROULANTE 3
# ==========================================
@dash.callback(
        [Output('multiselect-models', 'data'),
         Output('multiselect-models', 'value'),
        ],
        [Input('date-picker-st-sp', 'start_date'),
         Input('date-picker-st-sp', 'end_date'),
        ]
)

def maj_liste_deroulanteThree(debut, fin):
    if not debut or not fin :
        models_uniques = st_data_sp["Products"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date = pd.to_datetime(debut)
        end_date   = pd.to_datetime(fin) 
        df_temp          = st_data_sp[(st_data_sp["Date"] >= start_date) & (st_data_sp["Date"] <= end_date)]
        models_uniques = df_temp["Products"].unique()

    # Formater les options pour le dmc.Select de Mantine
    options_models = [{"value": models, "label": models} for models in models_uniques]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    models_par_defaut = [models_uniques[0]] if len(models_uniques) > 0 else []

    return options_models, models_par_defaut


# ==========================================
# LE CALLBACK DE DISTRIBUTION
# ==========================================
@dash.callback(
    [
        # Metric
        Output('metric-achat', 'children'),
        Output('metric-revenu', 'children'),
        Output('metric-bestWeek', 'children'),
        Output('metric-badWeek', 'children'),
        Output('metric-average', 'children'),
        Output('metric-median', 'children'),
        Output('metric-mode', 'children'),

        # Graphic
        Output('bar-channel', 'figure'),
        Output('pie-channel', 'figure'),
        Output('moustache-graph', 'figure'),
        Output('box-channel', 'figure'),
        Output('scatter-price', 'figure'),
        Output('line-monthly', 'figure'),
        Output('line-weekly', 'figure'),
        Output('bar_series', 'figure'),
        Output('pie_series', 'figure'),
        Output('channel_series', 'figure'),
        Output('model_months', 'figure'),
        Output('models_channel', 'figure'),
        Output('models_weeks', 'figure'),
        Output('all_models_bar', 'figure'),
        Output('all_models_pie', 'figure'),

        # Tableua
        Output('mon-tableau', 'data')
    ],
    [
        Input('date-picker-st-sp', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-st-sp', 'end_date'),     # Input 2 : Date de fin
        Input('dropdown-product', 'value'),
        Input('multiselect-series', 'value'),
        Input('multiselect-models', 'value'),
    ]    
)
def filtrer_et_analyser_donnees(debut, fin, produit, series, models):
    # 1. Sécurité : si une des deux dates est effacée par l'utilisateur
    if not debut or not fin:
        df_filtre = st_data_sp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date = pd.to_datetime(debut)
        end_date = pd.to_datetime(fin)
        df_filtre = st_data_sp[(st_data_sp['Date'] >= start_date) & (st_data_sp['Date'] <= end_date)]

    if produit :
        df_all_model = df_filtre[df_filtre["Products"] == produit]
    else :
        df_all_model = df_filtre.copy()


    if series :
        df_all_series = df_filtre[df_filtre["SERIES"].isin(series)]
    else :
        df_all_series = df_filtre.copy()

    if models :
        df_all_models = df_filtre[df_filtre["Products"].isin(models)]
    else :
        df_all_models = df_filtre.copy()
        

    # --- 3. Utilisation du résultat filtré (df_filtre) dans le reste du programme ---
    #############################
    # A. Calcul des Métriques
    ###############################
    total_achat = df_filtre["Purchased_Qty"].sum()
    df_filtre["Investisment"] = df_filtre["Purchased_Qty"] * df_filtre["Prices_usd"]
    total_invest = df_filtre['Investisment'].sum()

    best_st_sp  = df_filtre.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    best_week    = best_st_sp["Purchased_Qty"].max()
    bad_week     = best_st_sp["Purchased_Qty"].min()
    
    txt_achat    = f"{total_achat:,.2f} Pcs"
    txt_invest   = f"{total_invest} $"
    txt_bestWeek = f"{best_week :,.2f} Pcs"
    txt_badWeek  = f"{bad_week:,.2f} Pcs"

    ## Statistiques #####
    statis_group = df_filtre.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    
    static_mean   = statis_group["Purchased_Qty"].mean()
    static_median = statis_group["Purchased_Qty"].median()
    static_ecartType   = statis_group["Purchased_Qty"].std()

    ###################################
    # B. Graphique Bar pour Channel
    ##################################
    
    # B.1. Graphique en Bar pour channel Kin et Lushi
    channel = df_filtre.groupby("City", as_index= False)["Purchased_Qty"].sum()

    fig_bar_channel = px.bar(
        channel, 
        x="City", 
        y="Purchased_Qty", 
        color="City",
        text="Purchased_Qty",
        title="Channel-City situation for ST-SP"
    )
    fig_bar_channel.update_traces(textposition = 'outside')
    fig_bar_channel.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.2. Graphique en Pie pour channel Kin et Lushi
    fig_pie_chan = go.Figure(data = [go.Pie(labels = channel["City"], values= channel["Purchased_Qty"], title = "Channel-City Proportions for ST-SP", opacity=0.5)])
    fig_pie_chan.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
    fig_pie_chan.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 280, height = 280)

    # B.3. Graphique en boite a moustache
    fig_box_chan = px.box(df_filtre, x="City", y="Purchased_Qty", color="City", title="Sales breakdown by City", points= "outliers")
    fig_box_chan.update_layout(height= 360, width= 400, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor = '#F8F9FA')

    # B.4. Graphique en Histogram pour channel
    fig_hist = px.histogram(df_filtre, x= "Purchased_Qty", color="City", nbins= 10, title="Breakdown of Purchased Qty", barmode= "overlay")
    fig_hist.update_layout(height= 360, width= 470, xaxis_title= "Purchased Qty", yaxis_title = "Frequency", margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA')

    # B.5. Graphique en nuage au point pour comparer les prix par rappor a la vente
    
    df_model = (df_all_model.groupby(["Weeks", "Products"]).agg({"Prices_usd":"mean", "Purchased_Qty":"sum"}).reset_index())
    fig_scatter = px.scatter(
        df_model,
        x= "Prices_usd",
        y= "Purchased_Qty",
        text= "Weeks",
        hover_data= ["Products"],
        title= f"Price vs Purchase - {produit}"
    )
    fig_scatter.update_traces(textposition= "top center")
    fig_scatter.update_layout(height= 300, width= 1180, xaxis_title= "Purchased Qty", yaxis_title = "Frequency", margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA')

    # B.6. Graphique en Line sur la situation mensuelle
    monthly = df_filtre.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    monthly_fig = px.line(monthly , x="Months", y="Purchased_Qty", text= "Purchased_Qty", title="Monthly Sell FOR ST-SP")
    monthly_fig.update_traces(textposition = 'top center')
    monthly_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # B.7. Graphique en Line sur la situation semestriel
    weekly = df_filtre.groupby("Date", as_index= False)["Purchased_Qty"].sum()
    weekly_fig = px.line(weekly , x="Date", y="Purchased_Qty", text= "Purchased_Qty", title="Weekly Sell FOR ST-SP")
    weekly_fig.update_traces(textposition = 'top center')
    weekly_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # B.8. Graphique en Bar sur la series
    series_sp = df_all_series.groupby("SERIES", as_index= False)["Purchased_Qty"].sum()
    fig_bar_series = px.bar(series_sp, x="SERIES", y="Purchased_Qty", color="SERIES", text="Purchased_Qty", title="Channel-Series situation for ST-SP",)
    fig_bar_series.update_traces(textposition = 'outside')
    fig_bar_series.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.9. Graphique en Pie sur la series
    fig_pie_series = go.Figure(data = [go.Pie(labels = series_sp["SERIES"], values= series_sp["Purchased_Qty"], title = "Channel-series Proportions for ST-SP", opacity=0.5)])
    fig_pie_series.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
    fig_pie_series.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 380, height = 280)

    # B.10. Graphique en Bar sur la series par channel
    series_sp_chan = df_all_series.groupby(["SERIES", "City"], as_index= False)["Purchased_Qty"].sum()
    fig_bar_series_chan = px.bar(series_sp_chan, x="City", y="Purchased_Qty", color="SERIES", text="Purchased_Qty", title="Channel-Series situation for ST-SP",)
    fig_bar_series_chan.update_traces(textposition = 'outside')
    fig_bar_series_chan.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.11. Graphique en Line par models par mois
    model_line = df_all_models.groupby(["Products", "Months"], as_index= False)["Purchased_Qty"].sum()
    model_line_fig = px.line(model_line , x="Months", y="Purchased_Qty", color = "Products", text= "Purchased_Qty", title="Monthly Purchases by models")
    model_line_fig.update_traces(textposition = 'top center')
    model_line_fig.update_layout(margin = dict(l=20, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 670, height = 300)


    # B.12. Graphique en Bar sur la series par channel
    models_sp_chan = df_all_models.groupby(["Products", "City"], as_index= False)["Purchased_Qty"].sum()
    fig_bar_modelx_chan = px.bar(models_sp_chan, x="City", y="Purchased_Qty", color="Products", text="Purchased_Qty", title="Channel-Models situation for ST-SP",)
    fig_bar_modelx_chan.update_traces(textposition = 'outside')
    fig_bar_modelx_chan.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 480, height = 290)

    # B.13. Graphique en Line par models par weeks
    model_weeks = df_all_models.groupby(["Products", "Date"], as_index= False)["Purchased_Qty"].sum()
    model_weeks_fig = px.line(model_weeks , x="Date", y="Purchased_Qty", color = "Products", text= "Purchased_Qty", title="Weekly Purchases by models")
    model_weeks_fig.update_traces(textposition = 'top center')
    model_weeks_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)
  
    # B.14. Graphique en Bar sur all models
    all_model_chan = df_filtre.groupby("Products", as_index= False)["Purchased_Qty"].sum()
    all_model_bar = px.bar(all_model_chan, x="Products", y="Purchased_Qty", color="Products", text="Purchased_Qty", title="All models situation for ST-SP",)
    all_model_bar.update_traces(textposition = 'outside')
    all_model_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', showlegend= False, width = 790, height = 290)

    # B.15. Graphique en Pie sur all models
    all_model_pie = go.Figure(data = [go.Pie(labels = all_model_chan["Products"], values= all_model_chan["Purchased_Qty"], title = "All models Proportions for ST-SP", opacity=0.5)])
    all_model_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
    all_model_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 380, height = 280)


    ####################################################
    # C. Préparation des données pour VOTRE DataTable
    ####################################################
    # On transforme simplement le dataframe filtré en dictionnaire 'records'
    donnees_tableau = df_filtre.to_dict("records")

    # 4. Envoi simultané aux composants graphiques et métriques
    return txt_achat, txt_invest, txt_bestWeek, txt_badWeek, static_mean, static_median, static_ecartType, fig_bar_channel, fig_pie_chan, fig_box_chan, fig_hist, fig_scatter, monthly_fig, weekly_fig, fig_bar_series, fig_pie_series, fig_bar_series_chan, model_line_fig, fig_bar_modelx_chan, model_weeks_fig, all_model_bar, all_model_pie, donnees_tableau



