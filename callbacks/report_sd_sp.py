# IMPORTATION
from dash import callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_mantine_components as dmc
from datetime import datetime
from database.connectDB import engine
from database.data import sd_data_sp

# Convertir en date
sd_data_sp["Date"] = pd.to_datetime(sd_data_sp["Date"])


# ==========================================
# LE CALLBACK LISTE DEROULANTE 3
# ==========================================
@callback(
    [
        Output('dropdown_sd_sp_old', 'data'),
        Output('dropdown_sd_sp_old', 'value'),
    ],

    [
        Input('date-picker-rep-date1', 'start_date'),
        Input('date-picker-rep-date2', 'end_date'),
    ]
)

def maj_liste_deroulanteThree(debut, fin):
    if not debut or not fin :
        subD_uniques = sd_data_sp["Customers_Name"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date_one = pd.to_datetime(debut)
        end_date_two   = pd.to_datetime(fin)
        df_temp        = sd_data_sp[(sd_data_sp["Date"] >= start_date_one) & (sd_data_sp["Date"] <= end_date_two)]
        subD_uniques = df_temp["Customers_Name"].unique()


    # Formater les options pour le dmc.Select de Mantine
    options_subD = [{"value": prod, "label": prod} for prod in subD_uniques]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    subD_par_defaut = subD_uniques[0] if len(subD_uniques) > 0 else None

    return options_subD, subD_par_defaut

################################################
### CallBack General SD-SP
################################################
@callback(
    [
        ################
        ##### Metric ###
        ################
        # SD-SMART PHONE 1
        Output('sd-qty_sd_sp_old', 'children'),
        Output('total-purchase_sd_sp_old', 'children'),
        Output('average-sd-sp-old', 'children'),
        Output('median-sd-sp-old', 'children'),
        Output('ecartT-sd-sp-old', 'children'),
        Output('maxim-sd-sp-old', 'children'),
        Output('minim-sd-sp-old', 'children'),
        

        # SD-SMART PHONE 2
        Output('sd-qty_sd_sp_new', 'children'),
        Output('total-purchase_sd_sp_new', 'children'),
        Output('average-sd-sp-new', 'children'),
        Output('median-sd-sp-new', 'children'),
        Output('ecartT-sd-sp-new', 'children'),
        Output('maxim-sd-sp-new', 'children'),
        Output('minim-sd-sp-new', 'children'),

        ########################    
        ###### Graphic #########
        ########################
        # SD-SMART 1
        Output('monthly-purchase_sd_sp_old', 'figure'),
        Output('regions_bar_sd_sp_old', 'figure'),
        Output('regions_pie_sd_sp_old', 'figure'),
        Output('series_bar_sd_sp_old', 'figure'),
        Output('series_pie_sd_sp_old', 'figure'),
        Output('models_bar_sd_sp_old', 'figure'),
        Output('models_pie_sd_sp_old', 'figure'),
        Output('SD_bar_sd_sp_old', 'figure'),
        Output('SD_pie_sd_sp_old', 'figure'),

        # SD-SMART 2
        Output('monthly-purchase_sd_sp_new', 'figure'),
        Output('regions_bar_sd_sp_new', 'figure'),
        Output('regions_pie_sd_sp_new', 'figure'),
        Output('series_bar_sd_sp_new', 'figure'),
        Output('series_pie_sd_sp_new', 'figure'),
        Output('models_bar_sd_sp_new', 'figure'),
        Output('models_pie_sd_sp_new', 'figure'),
        Output('SD_bar_sd_sp_new', 'figure'),
        Output('SD_pie_sd_sp_new', 'figure'),
        Output('sd_sp_year_fig', 'figure'),
        Output('sd_sp_month_fig', 'figure'),
        Output('sd_sp_model_years_fig', 'figure'),

    ],

    [
        Input('date-picker-rep-date1', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-rep-date1', 'end_date'),
        Input('date-picker-rep-date2', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-rep-date2', 'end_date'),
        Input('dropdown_sd_sp_old', 'value'),
    ]
)

def filter_data_sd_sp(debut_one, fin_one, debut_two, fin_two, clients_1):

    # 1. Sécurité : si une des deux dates est effacée par l'utilisateur

    #######################
    #### SD SMART 

    if not debut_one or not fin_one:
        df_sd_sp_one = sd_data_sp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date_one = pd.to_datetime(debut_one)
        end_date_one = pd.to_datetime(fin_one)
        df_sd_sp_one = sd_data_sp[(sd_data_sp['Date'] >= start_date_one) & (sd_data_sp['Date'] <= end_date_one)]


    if not debut_two or not fin_two:
        df_sd_sp_two = sd_data_sp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date_two = pd.to_datetime(debut_two)
        end_date_two = pd.to_datetime(fin_two)
        df_sd_sp_two = sd_data_sp[(sd_data_sp['Date'] >= start_date_two) & (sd_data_sp['Date'] <= end_date_two)]


    if not debut_one or not fin_two:
        df_sd_sp_three = sd_data_sp.copy()

    else:
        start_date_one = pd.to_datetime(debut_one)
        end_date_two = pd.to_datetime(fin_two)
        df_sd_sp_three = sd_data_sp[(sd_data_sp['Date'] >= start_date_one) & (sd_data_sp['Date'] <= end_date_two)]


    #############################
    #########
    # SD-SP
    if clients_1 :
        df_clients_1 = df_sd_sp_three[df_sd_sp_three["Customers_Name"] == clients_1]
    else :
        df_clients_1 = df_sd_sp_three.copy()

    if clients_1 :
        df_clients_1_full = sd_data_sp[sd_data_sp["Customers_Name"] == clients_1]
    else :
        df_clients_1_full = sd_data_sp.copy()



    ####################
    ### METRIC
    ####################
    #########################
    ### A. SD SMART PHONE

    # Partie One
    qty_sd_sp_one   = df_sd_sp_one["Customers_Name"].nunique()
    achat_sd_sp_one = df_sd_sp_one["Purchases_Qty"].sum()
    
    txt_qty_sd_sp_one    = f"{qty_sd_sp_one} A Sub-Dealers"
    txt_achat_sd_sp_one  = f"{achat_sd_sp_one:,.2f} Pcs"

    ## Statistiques #####
    statis_sd_sp_one    = df_sd_sp_one.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    
    moyenne_sd_sp_one   = statis_sd_sp_one["Purchases_Qty"].mean()
    mediane_sd_sp_one   = statis_sd_sp_one["Purchases_Qty"].median()
    ecarT_dt_sp_one     = statis_sd_sp_one["Purchases_Qty"].std()
    maximum_sd_sp_one   = statis_sd_sp_one["Purchases_Qty"].max()
    minimum_sd_sp_one   = statis_sd_sp_one["Purchases_Qty"].min()

    # Partie Two
    qty_sd_sp_two   = df_sd_sp_two["Customers_Name"].nunique()
    achat_sd_sp_two = df_sd_sp_two["Purchases_Qty"].sum()
    
    txt_qty_sd_sp_two    = f"{qty_sd_sp_two} A Sub-Dealers"
    txt_achat_sd_sp_two  = f"{achat_sd_sp_two:,.2f} Pcs"

    ## Statistiques #####
    statis_sd_sp_two    = df_sd_sp_two.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    
    moyenne_sd_sp_two   = statis_sd_sp_two["Purchases_Qty"].mean()
    mediane_sd_sp_two   = statis_sd_sp_two["Purchases_Qty"].median()
    ecarT_dt_sp_two     = statis_sd_sp_two["Purchases_Qty"].std()
    maximum_sd_sp_two   = statis_sd_sp_two["Purchases_Qty"].max()
    minimum_sd_sp_two   = statis_sd_sp_two["Purchases_Qty"].min()

    #####################################################################
    #####################################################################
    ########################### GRAPHIC #################################
    #####################################################################
    ########################
    ## B. SD SMART PHONE
    ##########
    # Partie One

    # B.1. Vente mensuelle de SD
    sd_sp_monthly_one = df_sd_sp_one.groupby("Date", as_index= False)["Purchases_Qty"].sum()
    sd_sp_monthly_fig_one = px.line(sd_sp_monthly_one , x="Date", y="Purchases_Qty", text= "Purchases_Qty")
    sd_sp_monthly_fig_one.update_traces(textposition = 'top center')
    sd_sp_monthly_fig_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.2. Vente par regions de SD
    regions_sd_sd_one = df_sd_sp_one.groupby("Cities", as_index= False)["Purchases_Qty"].sum()
    bar_regions_sd_sp_one = px.bar(regions_sd_sd_one, x="Cities", y="Purchases_Qty", color="Cities", text="Purchases_Qty")
    bar_regions_sd_sp_one.update_traces(textposition = 'outside')
    bar_regions_sd_sp_one.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # B.3. Graphique en Pie pour regions 
    pie_region_sd_sp_one = go.Figure(data = [go.Pie(labels = regions_sd_sd_one["Cities"], values= regions_sd_sd_one["Purchases_Qty"], opacity=0.5)])
    pie_region_sd_sp_one.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_region_sd_sp_one.update_layout(showlegend= False, margin = dict(l=5, r=5, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # B.4. Vente par series de SD
    series_sd_sp_one = df_sd_sp_one.groupby("SERIES", as_index= False)["Purchases_Qty"].sum()
    bar_series_sd_sp_one = px.bar(series_sd_sp_one, x="SERIES", y="Purchases_Qty", color="SERIES", text="Purchases_Qty")
    bar_series_sd_sp_one.update_traces(textposition = 'outside')
    bar_series_sd_sp_one.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # B.5. Graphique en Pie pour series 
    pie_series_sd_sp_one = go.Figure(data = [go.Pie(labels = series_sd_sp_one["SERIES"], values= series_sd_sp_one["Purchases_Qty"], opacity=0.5)])
    pie_series_sd_sp_one.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_series_sd_sp_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # B.6. Vente par models de SD
    models_sd_sp_one = df_sd_sp_one.groupby("Products", as_index= False)["Purchases_Qty"].sum()
    bar_models_sd_sp_one = px.bar(models_sd_sp_one, x="Products", y="Purchases_Qty", color="Products", text="Purchases_Qty")
    bar_models_sd_sp_one.update_traces(textposition = 'outside')
    bar_models_sd_sp_one.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # B.7. Graphique en Pie pour models 
    pie_models_sd_sp_one = go.Figure(data = [go.Pie(labels = models_sd_sp_one["Products"], values= models_sd_sp_one["Purchases_Qty"], opacity=0.5)])
    pie_models_sd_sp_one.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_models_sd_sp_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # B.8. Vente par clients de SD
    clients_sd_sp_one = df_sd_sp_one.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    bar_clients_sd_sp_one = px.bar(clients_sd_sp_one, x="Customers_Name", y="Purchases_Qty", color="Customers_Name", text="Purchases_Qty")
    bar_clients_sd_sp_one.update_traces(textposition = 'outside')
    bar_clients_sd_sp_one.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # B.9. Graphique en Pie pour clients 
    pie_clients_sd_sp_one = go.Figure(data = [go.Pie(labels = clients_sd_sp_one["Customers_Name"], values= clients_sd_sp_one["Purchases_Qty"], opacity=0.5)])
    pie_clients_sd_sp_one.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_clients_sd_sp_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # Partie Two

    # B.10. Vente mensuelle de SD
    sd_sp_monthly_two = df_sd_sp_two.groupby("Date", as_index= False)["Purchases_Qty"].sum()
    sd_sp_monthly_fig_two = px.line(sd_sp_monthly_two , x="Date", y="Purchases_Qty", text= "Purchases_Qty")
    sd_sp_monthly_fig_two.update_traces(textposition = 'top center')
    sd_sp_monthly_fig_two.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.11. Vente par regions de SD
    regions_sd_sd_two = df_sd_sp_two.groupby("Cities", as_index= False)["Purchases_Qty"].sum()
    bar_regions_sd_sp_two = px.bar(regions_sd_sd_two, x="Cities", y="Purchases_Qty", color="Cities", text="Purchases_Qty")
    bar_regions_sd_sp_two.update_traces(textposition = 'outside')
    bar_regions_sd_sp_two.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 290)
    
    # B.12. Graphique en Pie pour regions 
    pie_region_sd_sp_two = go.Figure(data = [go.Pie(labels = regions_sd_sd_two["Cities"], values= regions_sd_sd_two["Purchases_Qty"], opacity=0.5)])
    pie_region_sd_sp_two.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_region_sd_sp_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # B.13. Vente par series de SD
    series_sd_sp_two = df_sd_sp_two.groupby("SERIES", as_index= False)["Purchases_Qty"].sum()
    bar_series_sd_sp_two = px.bar(series_sd_sp_two, x="SERIES", y="Purchases_Qty", color="SERIES", text="Purchases_Qty")
    bar_series_sd_sp_two.update_traces(textposition = 'outside')
    bar_series_sd_sp_two.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # B.14. Graphique en Pie pour series 
    pie_series_sd_sp_two = go.Figure(data = [go.Pie(labels = series_sd_sp_two["SERIES"], values= series_sd_sp_two["Purchases_Qty"], opacity=0.5)])
    pie_series_sd_sp_two.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_series_sd_sp_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # B.15. Vente par models de SD
    models_sd_sp_two = df_sd_sp_two.groupby("Products", as_index= False)["Purchases_Qty"].sum()
    bar_models_sd_sp_two = px.bar(models_sd_sp_two, x="Products", y="Purchases_Qty", color="Products", text="Purchases_Qty")
    bar_models_sd_sp_two.update_traces(textposition = 'outside')
    bar_models_sd_sp_two.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # B.16. Graphique en Pie pour models 
    pie_models_sd_sp_two = go.Figure(data = [go.Pie(labels = models_sd_sp_two["Products"], values= models_sd_sp_two["Purchases_Qty"], opacity=0.5)])
    pie_models_sd_sp_two.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_models_sd_sp_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # B.17. Vente par clients de SD
    clients_sd_sp_two = df_sd_sp_two.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    bar_clients_sd_sp_two = px.bar(clients_sd_sp_two, x="Customers_Name", y="Purchases_Qty", color="Customers_Name", text="Purchases_Qty")
    bar_clients_sd_sp_two.update_traces(textposition = 'outside')
    bar_clients_sd_sp_two.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # B.18. Graphique en Pie pour clients 
    pie_clients_sd_sp_two = go.Figure(data = [go.Pie(labels = clients_sd_sp_two["Customers_Name"], values= clients_sd_sp_two["Purchases_Qty"], opacity=0.5)])
    pie_clients_sd_sp_two.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_clients_sd_sp_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # B.19. Graphique en Line qui affiche les achats annuel du client choisi 
    yearlySD_clients_sp = df_clients_1_full.groupby("Years", as_index= False)["Purchases_Qty"].sum()
    yearly_fig_sp_one = px.line(yearlySD_clients_sp , x="Years", y="Purchases_Qty", text= "Purchases_Qty")
    yearly_fig_sp_one.update_traces(textposition = 'top center')
    yearly_fig_sp_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # B.20. Graphique en Line qui affiche les achats mensuel du clients chois
    monthlySD_clients_sp = df_clients_1.groupby("Date", as_index= False)["Purchases_Qty"].sum()
    monthly_fig_sp_one = px.line(monthlySD_clients_sp , x="Date", y="Purchases_Qty", text= "Purchases_Qty")
    monthly_fig_sp_one.update_traces(textposition = 'top center')
    monthly_fig_sp_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # B.21. Graphique en Bar qui affiche les models achate par les clients par ans
    model_years_sp = df_clients_1.groupby(["Years", "Products"], as_index= False)["Purchases_Qty"].sum()
    model_years_sp_fig = px.bar(model_years_sp, x="Years", y="Purchases_Qty", color="Products",text="Purchases_Qty", barmode= "group")
    model_years_sp_fig.update_traces(textposition = 'outside')
    model_years_sp_fig.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)


    # 4. Envoi simultané aux composants graphiques et métriques
    return (
        txt_qty_sd_sp_one,  #
        txt_achat_sd_sp_one, 
        moyenne_sd_sp_one, 
        mediane_sd_sp_one, 
        ecarT_dt_sp_one, 
        maximum_sd_sp_one, 
        minimum_sd_sp_one, 
        txt_qty_sd_sp_two, 
        txt_achat_sd_sp_two, 
        moyenne_sd_sp_two, 
        mediane_sd_sp_two, 
        ecarT_dt_sp_two, 
        maximum_sd_sp_two, 
        minimum_sd_sp_two,   
        sd_sp_monthly_fig_one, 
        bar_regions_sd_sp_one, 
        pie_region_sd_sp_one, 
        bar_series_sd_sp_one,  
        pie_series_sd_sp_one, 
        bar_models_sd_sp_one, 
        pie_models_sd_sp_one, 
        bar_clients_sd_sp_one, 
        pie_clients_sd_sp_one, #
        sd_sp_monthly_fig_two, 
        bar_regions_sd_sp_two, 
        pie_region_sd_sp_two, 
        bar_series_sd_sp_two, 
        pie_series_sd_sp_two, 
        bar_models_sd_sp_two, 
        pie_models_sd_sp_two, 
        bar_clients_sd_sp_two, 
        pie_clients_sd_sp_two, 
        yearly_fig_sp_one, 
        monthly_fig_sp_one, 
        model_years_sp_fig
        ) 
