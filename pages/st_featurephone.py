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

    # df = pd.read_sql("SELECT * FROM SD_tecno_FP_data", con = session.bind)

    # Traitement des valeurs manquantes
    st_data_fp = df_st_fp.dropna(subset="Purchased_Qty")

finally:
    #session.close()
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
st_data_fp["Date"] = pd.to_datetime(st_data_fp["Date"])


###########################
###### GRAPHIC ############
###########################
#######################
# A. Annual Situation
##############
# 1. Graphic ST for SP
st_fp_year = st_data_fp.groupby("Years", as_index= False)["Purchased_Qty"].sum()
st_fp_year_fig = px.line(st_fp_year, x="Years", y="Purchased_Qty", text= "Purchased_Qty", title="SELL THROUGH FOR FP")
st_fp_year_fig.update_traces(textposition = 'top center')
st_fp_year_fig.update_layout(
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

              
        dmc.Title("ST FEATURE PHONE", order= 1, style={"marginTop": 20}), # order = 1, correspond a H1
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
                    children= dmc.Paper(dcc.Graph(figure= st_fp_year_fig), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                )
            ]
        ),

        html.Br(),
        html.Br(),

        # Selecteur des dates
        dmc.Title("Date Selector", order= 5, style={"marginBottom": 15}),
        dcc.DatePickerRange(
            id = "date-picker-st-fp",
            start_date= st_data_fp["Date"].min(),
            end_date= st_data_fp["Date"].max(),
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
                            dmc.Text(id="metric-achat_fp", size= "xl", fw=700),
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

                            dmc.Text(id="metric-revenu_fp", size="xl", fw=700),
                        ], withBorder= True, p= "md", shadow= "xs"
                    ),
                ),

                dmc.GridCol(
                    span = 3,
                    children= dmc.Paper(
                        children= [
                            dmc.Text("Best Week", c="dimmed", size= "sm"),
                            dmc.Text(id= "metric-bestWeek_fp", size="xl", fw=700),
                        ], withBorder= True, p= "md", shadow= "xs",
                    ),
                ),

                dmc.GridCol(
                    span = 3, 
                    children= dmc.Paper(
                        children= [
                            dmc.Text("Worst Week", c="dimmed", size= "sm"),
                            dmc.Text(id="metric-badWeek_fp", size="xl", fw=700),
                        ], withBorder= True, p= "md", shadow= "xs",
                    ),
                ),
            ]

        ),

        html.Br(),

        # Conteneurs pour les resultats filtres
        dmc.Title("Table Contents", order= 3, style={"textAlign": "left"}),
        dash_table.DataTable(
            id = 'mon-tableau_fp',

            # Les colonnes sont définies une seule fois au chargement initial
            columns = [
                {"name": c, "id": c} for c in st_data_fp.columns
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
                                        dmc.Text(id= "metric-average_fp", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs",
                                ),
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    children=[
                                        dmc.Text("Median", c="dimmed", size= "sm"),
                                        dmc.Text(id= "metric-median_fp", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs",
                                ),
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    children=[
                                        dmc.Text("Standard Deviation", c="dimmed", size= "sm"),
                                        dmc.Text(id= "metric-ecarTyp_fp", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs"
                                ),
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    children=[
                                        dmc.Text("Maximum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "metric-max-fp", size="xl", fw=700),
                                    ], withBorder= True, p= "md", shadow= "xs",
                                ),
                            ),

                            dmc.GridCol(
                                span= 12,
                                children= dmc.Paper(
                                    children=[
                                        dmc.Text("Minimum Value", c="dimmed", size= "sm"),
                                        dmc.Text(id= "metric-min-fp", size="xl", fw=700),
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
                                        dcc.Graph(id='bar-channel_fp'),
                                    ],
                                    withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            # Graphic channel Pie
                            dmc.GridCol(
                                span = 4,
                                children= dmc.Paper(
                                    # "Graphic Pie Channel"
                                    children = [
                                        dcc.Graph(id='pie-channel_fp'),
                                    ],
                                    withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            # --- Graphic Boite a moustapha
                            dmc.GridCol(
                                span = 12,
                                children= dmc.Paper(
                                    #"Graphic Boite a Moustache",
                                    children = [
                                        dcc.Graph(id= "moustache-graph_fp"),
                                        dcc.Graph(id='box-channel_fp'),

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
                            id = "dropdown-product_fp",
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
                            dcc.Graph(id='scatter-price_fp')
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
                            dcc.Graph(id= "line-monthly_fp"),
                        ], 
                        withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                ),

                # --- Weekly Situation
                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            dcc.Graph(id= "line-weekly_fp"),
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
            id = "multiselect-models_fp",
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
                            dcc.Graph(id = "model_months_fp"),
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"})
                ),

                # -- Graphic Bar models par Channel
                dmc.GridCol(
                    span = 5,
                    children = dmc.Paper(
                        children = [
                            #"Graphic Bar models par Channel",
                            dcc.Graph(id = "models_channel_fp"), 
                        ],
                        withBorder= True, p="md", style={**style_boite, "height": "300px"})
                ),

                # -- Graphic Line models par week
                dmc.GridCol(
                    span = 12,
                    children = dmc.Paper(
                        children = [
                            #"Graphic Line models par week",
                            dcc.Graph(id = "models_weeks_fp"), 
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
                            dcc.Graph(id = "all_models_bar_fp"),
                        ],
                        withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                ),

                # -- Colonne droite graphic Pie all models
                dmc.GridCol(
                    span = 4, 
                    children= dmc.Paper(
                        children = [
                            #"Graphic Pie all models",
                            dcc.Graph(id = "all_models_pie_fp"),
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
        [Output('dropdown-product_fp', 'data'),
         Output('dropdown-product_fp', 'value'),
        ],
        [Input('date-picker-st-fp', 'start_date'),
         Input('date-picker-st-fp', 'end_date'),
        ]
)

def maj_liste_deroulanteOne_fp(debut, fin):
    if not debut or not fin :
        produits_uniques = st_data_fp["Products"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date       = pd.to_datetime(debut)
        end_date         = pd.to_datetime(fin)
        df_temp          = st_data_fp[(st_data_fp["Date"] >= start_date) & (st_data_fp["Date"] <= end_date)]
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
        [Output('multiselect-models_fp', 'data'),
         Output('multiselect-models_fp', 'value'),
        ],
        [Input('date-picker-st-fp', 'start_date'),
         Input('date-picker-st-fp', 'end_date'),
        ]
)

def maj_liste_deroulanteTwo_fp(debut, fin):
    if not debut or not fin :
        models_uniques = st_data_fp["Products"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date = pd.to_datetime(debut)
        end_date   = pd.to_datetime(fin) 
        df_temp          = st_data_fp[(st_data_fp["Date"] >= start_date) & (st_data_fp["Date"] <= end_date)]
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
        Output('metric-achat_fp', 'children'),
        Output('metric-revenu_fp', 'children'),
        Output('metric-bestWeek_fp', 'children'),
        Output('metric-badWeek_fp', 'children'),
        Output('metric-average_fp', 'children'),
        Output('metric-median_fp', 'children'),
        Output('metric-ecarTyp_fp', 'children'),
        Output('metric-max-fp', 'children'),
        Output('metric-min-fp', 'children'),

        # Graphic
        Output('bar-channel_fp', 'figure'),
        Output('pie-channel_fp', 'figure'),
        Output('moustache-graph_fp', 'figure'),
        Output('box-channel_fp', 'figure'),
        Output('scatter-price_fp', 'figure'),
        Output('line-monthly_fp', 'figure'),
        Output('line-weekly_fp', 'figure'),
        Output('model_months_fp', 'figure'),
        Output('models_channel_fp', 'figure'),
        Output('models_weeks_fp', 'figure'),
        Output('all_models_bar_fp', 'figure'),
        Output('all_models_pie_fp', 'figure'),

        # Tableua
        Output('mon-tableau_fp', 'data')
    ],
    [
        Input('date-picker-st-fp', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-st-fp', 'end_date'),     # Input 2 : Date de fin
        Input('dropdown-product_fp', 'value'),
        Input('multiselect-models_fp', 'value'),
    ]    
)
def filtrer_et_analyser_donnees(debut, fin, produit, models):
    # 1. Sécurité : si une des deux dates est effacée par l'utilisateur
    if not debut or not fin:
        df_filtre = st_data_fp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date = pd.to_datetime(debut)
        end_date = pd.to_datetime(fin)
        df_filtre = st_data_fp[(st_data_fp['Date'] >= start_date) & (st_data_fp['Date'] <= end_date)]

    if produit :
        df_all_model = df_filtre[df_filtre["Products"] == produit]
    else :
        df_all_model = df_filtre.copy()

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

    best_st_fp  = df_filtre.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    best_week    = best_st_fp["Purchased_Qty"].max()
    bad_week     = best_st_fp["Purchased_Qty"].min()
    
    txt_achat    = f"{total_achat:,.2f} Pcs"
    txt_invest   = f"{total_invest} $"
    txt_bestWeek = f"{best_week :,.2f} Pcs"
    txt_badWeek  = f"{bad_week:,.2f} Pcs"

    ## Statistiques #####
    statis_group = df_filtre.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    
    static_mean        = statis_group["Purchased_Qty"].mean()
    static_median      = statis_group["Purchased_Qty"].median()
    static_ecartType   = statis_group["Purchased_Qty"].std()
    maximum            = statis_group["Purchased_Qty"].max()
    minimum            = statis_group["Purchased_Qty"].min()

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
        title="Channel-City situation for ST-FP"
    )
    fig_bar_channel.update_traces(textposition = 'outside')
    fig_bar_channel.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.2. Graphique en Pie pour channel Kin et Lushi
    fig_pie_chan = go.Figure(data = [go.Pie(labels = channel["City"], values= channel["Purchased_Qty"], title = "Channel-City Proportions for ST-FP", opacity=0.5)])
    fig_pie_chan.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
    fig_pie_chan.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 280, height = 280)

    # B.3. Graphique en boite a moustache
    prime = df_filtre.groupby(["City", "Date"], as_index= False)["Purchased_Qty"].sum()
    fig_box_chan = px.box(prime, x="City", y="Purchased_Qty", color="City", title="Purchases breakdown by City", points= "outliers")
    fig_box_chan.update_layout(showlegend= False, height= 360, width= 400, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor = '#F8F9FA')

    # B.4. Graphique en Histogram pour channel
    prime_city = df_filtre.groupby("Date", as_index= False)["Purchased_Qty"].sum()
    fig_hist = px.histogram(prime_city, x= "Purchased_Qty", nbins= 30, title="Breakdown of Purchased Qty", labels= {"Purchased_Qty":"Purchasesd Quantity"})
    fig_hist.update_layout(height= 360, width= 470, xaxis_title= "Purchased Qty", yaxis_title = "Frequency", margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA')

    # B.5. Graphique en nuage au point pour comparer les prix par rappor a la vente
    
    #df_model = df_all_model.groupby(["Products", "Prices_usd"], as_index= False)["Purchased_Qty"].sum()
    df_model = (df_all_model.groupby(["Months", "Products"]).agg({"Prices_usd":"mean", "Purchased_Qty":"sum"}).reset_index())
    fig_scatter = px.scatter(
        df_model,
        x= "Prices_usd",
        y= "Purchased_Qty",
        text= "Months",
        hover_data= ["Products"],
        title= f"Price vs Purchase - {produit}"
    )
    fig_scatter.update_traces(textposition= "top center")
    fig_scatter.update_layout(height= 300, width= 1180, xaxis_title= "Purchased Qty", yaxis_title = "Frequency", margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA')

    # B.6. Graphique en Line sur la situation mensuelle
    monthly = df_filtre.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    monthly_fig = px.line(monthly , x="Months", y="Purchased_Qty", text= "Purchased_Qty", title="Monthly Purchase FOR ST-FP")
    monthly_fig.update_traces(textposition = 'top center')
    monthly_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # B.7. Graphique en Line sur la situation semestriel
    weekly = df_filtre.groupby("Date", as_index= False)["Purchased_Qty"].sum()
    weekly_fig = px.line(weekly , x="Date", y="Purchased_Qty", text= "Purchased_Qty", title="Weekly Sell FOR ST-FP")
    weekly_fig.update_traces(textposition = 'top center')
    weekly_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # B.8. Graphique en Line par models par mois
    model_line = df_all_models.groupby(["Products", "Months"], as_index= False)["Purchased_Qty"].sum()
    model_line_fig = px.line(model_line , x="Months", y="Purchased_Qty", color = "Products", text= "Purchased_Qty", title="Monthly Purchases by models")
    model_line_fig.update_traces(textposition = 'top center')
    model_line_fig.update_layout(margin = dict(l=20, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 670, height = 300)


    # B.9. Graphique en Bar sur la series par channel
    models_sp_chan = df_all_models.groupby(["Products", "City"], as_index= False)["Purchased_Qty"].sum()
    fig_bar_modelx_chan = px.bar(models_sp_chan, x="City", y="Purchased_Qty", color="Products", text="Purchased_Qty", title="Channel-Models situation for ST-FP",)
    fig_bar_modelx_chan.update_traces(textposition = 'outside')
    fig_bar_modelx_chan.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 480, height = 290)

    # B.10. Graphique en Line par models par weeks
    model_weeks = df_all_models.groupby(["Products", "Date"], as_index= False)["Purchased_Qty"].sum()
    model_weeks_fig = px.line(model_weeks , x="Date", y="Purchased_Qty", color = "Products", text= "Purchased_Qty", title="Weekly Purchases by models")
    model_weeks_fig.update_traces(textposition = 'top center')
    model_weeks_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)
  
    # B.11. Graphique en Bar sur all models
    all_model_chan = df_filtre.groupby("Products", as_index= False)["Purchased_Qty"].sum()
    all_model_bar = px.bar(all_model_chan, x="Products", y="Purchased_Qty", color="Products", text="Purchased_Qty", title="All models situation for ST-FP",)
    all_model_bar.update_traces(textposition = 'outside')
    all_model_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', showlegend= False, width = 790, height = 290)

    # B.12. Graphique en Pie sur all models
    all_model_pie = go.Figure(data = [go.Pie(labels = all_model_chan["Products"], values= all_model_chan["Purchased_Qty"], title = "All models Proportions for ST-FP", opacity=0.5)])
    all_model_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
    all_model_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 380, height = 280)


    ####################################################
    # C. Préparation des données pour VOTRE DataTable
    ####################################################
    # On transforme simplement le dataframe filtré en dictionnaire 'records'
    donnees_tableau = df_filtre.to_dict("records")

    # 4. Envoi simultané aux composants graphiques et métriques
    return txt_achat, txt_invest, txt_bestWeek, txt_badWeek, static_mean, static_median, static_ecartType, maximum, minimum, fig_bar_channel, fig_pie_chan, fig_box_chan, fig_hist, fig_scatter, monthly_fig, weekly_fig, model_line_fig, fig_bar_modelx_chan, model_weeks_fig, all_model_bar, all_model_pie, donnees_tableau


