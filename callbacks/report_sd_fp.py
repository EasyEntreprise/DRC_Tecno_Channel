# IMPORTATION
from dash import callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_mantine_components as dmc
from datetime import datetime
from database.connectDB import engine
from database.data import sd_data_fp

# Convertir en date
sd_data_fp["Date"] = pd.to_datetime(sd_data_fp["Date"], errors="coerce")


# ==========================================
# LE CALLBACK LISTE DEROULANTE 4
# ==========================================
@callback(
    [ 
        Output('dropdown_sd_fp_old', 'data'),
        Output('dropdown_sd_fp_old', 'value'),
    ],

    [
        Input('date-picker-rep-date1', 'start_date'),
        Input('date-picker-rep-date2', 'end_date'),
    ]
)

def maj_liste_deroulanteFour(debut, fin):
    if not debut or not fin :
        subD_uniques_fp = sd_data_fp["Customers_Name"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date_one = pd.to_datetime(debut)
        end_date_two   = pd.to_datetime(fin)
        df_temp        = sd_data_fp[(sd_data_fp["Date"] >= start_date_one) & (sd_data_fp["Date"] <= end_date_two)]
        subD_uniques_fp = df_temp["Customers_Name"].unique()


    # Formater les options pour le dmc.Select de Mantine
    options_subD_fp = [{"value": prod, "label": prod} for prod in subD_uniques_fp]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    subD_par_defaut_fp = subD_uniques_fp[0] if len(subD_uniques_fp) > 0 else None

    return options_subD_fp, subD_par_defaut_fp

################################################
### CallBack General SD-FP
################################################
@callback(
    [
        ################
        ##### Metric ###
        ################
        # SD-FEATURE PHONE 1
        Output('sd-qty_sd_fp_old', 'children'),
        Output('total-purchase_sd_fp_old', 'children'),
        Output('average-sd-fp-old', 'children'),
        Output('median-sd-fp-old', 'children'),
        Output('ecartT-sd-fp-old', 'children'),
        Output('maxim-sd-fp-old', 'children'),
        Output('minim-sd-fp-old', 'children'),
        

        # SD-FEATURE PHONE 2
        Output('sd-qty_sd_fp_new', 'children'),
        Output('total-purchase_sd_fp_new', 'children'),
        Output('average-sd-fp-new', 'children'),
        Output('median-sd-fp-new', 'children'),
        Output('ecartT-sd-fp-new', 'children'),
        Output('maxim-sd-fp-new', 'children'),
        Output('minim-sd-fp-new', 'children'),

        ########################    
        ###### Graphic #########
        ########################
        # SD-FEATURE 1
        Output('monthly-purchase_sd_fp_old', 'figure'),
        Output('regions_bar_sd_fp_old', 'figure'),
        Output('regions_pie_sd_fp_old', 'figure'),
        Output('models_bar_sd_fp_old', 'figure'),
        Output('models_pie_sd_fp_old', 'figure'),
        Output('SD_bar_sd_fp_old', 'figure'),
        Output('SD_pie_sd_fp_old', 'figure'),

        # SD-FEATURE 2
        Output('monthly-purchase_sd_fp_new', 'figure'),
        Output('regions_bar_sd_fp_new', 'figure'),
        Output('regions_pie_sd_fp_new', 'figure'),
        Output('models_bar_sd_fp_new', 'figure'),
        Output('models_pie_sd_fp_new', 'figure'),
        Output('SD_bar_sd_fp_new', 'figure'),
        Output('SD_pie_sd_fp_new', 'figure'),
        Output('sd_fp_year_fig', 'figure'),
        Output('sd_fp_month_fig', 'figure'),
        Output('sd_fp_model_years_fig', 'figure'),
    ],

    [
        Input('date-picker-rep-date1', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-rep-date1', 'end_date'),
        Input('date-picker-rep-date2', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-rep-date2', 'end_date'),
        Input('dropdown_sd_fp_old', 'value'),
    ]
)

def filter_data_sd_fp(debut_one, fin_one, debut_two, fin_two, clients_2):

    # 1. Sécurité : si une des deux dates est effacée par l'utilisateur

    #######################
    #### SD FEATURE

    if not debut_one or not fin_one:
        df_sd_fp_one = sd_data_fp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date_one = pd.to_datetime(debut_one)
        end_date_one   = pd.to_datetime(fin_one)
        df_sd_fp_one   = sd_data_fp[(sd_data_fp['Date'] >= start_date_one) & (sd_data_fp['Date'] <= end_date_one)]


    if not debut_two or not fin_two:
        df_sd_fp_two = sd_data_fp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date_two = pd.to_datetime(debut_two)
        end_date_two   = pd.to_datetime(fin_two)
        df_sd_fp_two   = sd_data_fp[(sd_data_fp['Date'] >= start_date_two) & (sd_data_fp['Date'] <= end_date_two)]


    if not debut_one or not fin_two:
        df_sd_fp_four = sd_data_fp.copy()

    else:
        start_date_one = pd.to_datetime(debut_one)
        end_date_two   = pd.to_datetime(fin_two)
        df_sd_fp_four  = sd_data_fp[(sd_data_fp['Date'] >= start_date_one) & (sd_data_fp['Date'] <= end_date_two)]


    #############################
    #########

    # SD-FP
    if clients_2 :
        df_clients_2 = df_sd_fp_four[df_sd_fp_four["Customers_Name"] == clients_2]
    else :
        df_clients_2 = df_sd_fp_four.copy()

    if clients_2 :
        df_clients_2_full = sd_data_fp[sd_data_fp["Customers_Name"] == clients_2]
    else :
        df_clients_2_full = sd_data_fp.copy()
    


    ####################
    ### METRIC
    ####################
    #########################
    ### A.4. SD FEATURE PHONE

    # Partie One
    qty_sd_fp_one   = df_sd_fp_one["Customers_Name"].nunique()
    achat_sd_fp_one = df_sd_fp_one["Purchases_Qty"].sum()
    
    txt_qty_sd_fp_one    = f"{qty_sd_fp_one} A Sub-Dealers"
    txt_achat_sd_fp_one  = f"{achat_sd_fp_one:,.2f} Pcs"

    ## Statistiques #####
    statis_sd_fp_one    = df_sd_fp_one.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    
    moyenne_sd_fp_one   = statis_sd_fp_one["Purchases_Qty"].mean()
    mediane_sd_fp_one   = statis_sd_fp_one["Purchases_Qty"].median()
    ecarT_dt_fp_one     = statis_sd_fp_one["Purchases_Qty"].std()
    maximum_sd_fp_one   = statis_sd_fp_one["Purchases_Qty"].max()
    minimum_sd_fp_one   = statis_sd_fp_one["Purchases_Qty"].min()

    # Partie Two
    qty_sd_fp_two   = df_sd_fp_two["Customers_Name"].nunique()
    achat_sd_fp_two = df_sd_fp_two["Purchases_Qty"].sum()
    
    txt_qty_sd_fp_two    = f"{qty_sd_fp_two} A Sub-Dealers"
    txt_achat_sd_fp_two  = f"{achat_sd_fp_two:,.2f} Pcs"

    ## Statistiques #####
    statis_sd_fp_two    = df_sd_fp_two.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    
    moyenne_sd_fp_two   = statis_sd_fp_two["Purchases_Qty"].mean()
    mediane_sd_fp_two   = statis_sd_fp_two["Purchases_Qty"].median()
    ecarT_dt_fp_two     = statis_sd_fp_two["Purchases_Qty"].std()
    maximum_sd_fp_two   = statis_sd_fp_two["Purchases_Qty"].max()
    minimum_sd_fp_two   = statis_sd_fp_two["Purchases_Qty"].min()


    #####################################################################
    #####################################################################
    ########################### GRAPHIC #################################
    #####################################################################
    ########################
    ## E. SD FEATURE PHONE
    ##########
    # Partie One
    # E.1. Vente mensuelle de SD
    sd_fp_monthly_one = df_sd_fp_one.groupby("Date", as_index= False)["Purchases_Qty"].sum()
    sd_fp_monthly_fig_one = px.line(sd_fp_monthly_one , x="Date", y="Purchases_Qty", text= "Purchases_Qty")
    sd_fp_monthly_fig_one.update_traces(textposition = 'top center')
    sd_fp_monthly_fig_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 300)

    # E.2. Vente par regions de SD
    regions_sd_fp_one = df_sd_fp_one.groupby("Cities", as_index= False)["Purchases_Qty"].sum()
    bar_regions_sd_fp_one = px.bar(regions_sd_fp_one, x="Cities", y="Purchases_Qty", color="Cities", text="Purchases_Qty")
    bar_regions_sd_fp_one.update_traces(textposition = 'outside')
    bar_regions_sd_fp_one.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # E.3. Graphique en Pie pour regions 
    pie_region_sd_fp_one = go.Figure(data = [go.Pie(labels = regions_sd_fp_one["Cities"], values= regions_sd_fp_one["Purchases_Qty"], opacity=0.5)])
    pie_region_sd_fp_one.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_region_sd_fp_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # E.4. Vente par models de SD
    models_sd_fp_one = df_sd_fp_one.groupby("Products", as_index= False)["Purchases_Qty"].sum()
    bar_models_sd_fp_one = px.bar(models_sd_fp_one, x="Products", y="Purchases_Qty", color="Products", text="Purchases_Qty")
    bar_models_sd_fp_one.update_traces(textposition = 'outside')
    bar_models_sd_fp_one.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # E.5. Graphique en Pie pour models 
    pie_models_sd_fp_one = go.Figure(data = [go.Pie(labels = models_sd_fp_one["Products"], values= models_sd_fp_one["Purchases_Qty"], opacity=0.5)])
    pie_models_sd_fp_one.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_models_sd_fp_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # E.6. Vente par clients de SD
    clients_sd_fp_one = df_sd_fp_one.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    bar_clients_sd_fp_one = px.bar(clients_sd_fp_one, x="Customers_Name", y="Purchases_Qty", color="Customers_Name", text="Purchases_Qty")
    bar_clients_sd_fp_one.update_traces(textposition = 'outside')
    bar_clients_sd_fp_one.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # E.7. Graphique en Pie pour clients 
    pie_clients_sd_fp_one = go.Figure(data = [go.Pie(labels = clients_sd_fp_one["Customers_Name"], values= clients_sd_fp_one["Purchases_Qty"], opacity=0.5)])
    pie_clients_sd_fp_one.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_clients_sd_fp_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)


    # Partie Two
    # E.8. Vente mensuelle de SD
    sd_fp_monthly_two = df_sd_fp_two.groupby("Date", as_index= False)["Purchases_Qty"].sum()
    sd_fp_monthly_fig_two = px.line(sd_fp_monthly_two , x="Date", y="Purchases_Qty", text= "Purchases_Qty", title="Monthly Sell for SD-FP")
    sd_fp_monthly_fig_two.update_traces(textposition = 'top center')
    sd_fp_monthly_fig_two.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 300)

    # E.9. Vente par regions de SD
    regions_sd_fp_two = df_sd_fp_two.groupby("Cities", as_index= False)["Purchases_Qty"].sum()
    bar_regions_sd_fp_two = px.bar(regions_sd_fp_two, x="Cities", y="Purchases_Qty", color="Cities", text="Purchases_Qty")
    bar_regions_sd_fp_two.update_traces(textposition = 'outside')
    bar_regions_sd_fp_two.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # E.10. Graphique en Pie pour regions 
    pie_region_sd_fp_two = go.Figure(data = [go.Pie(labels = regions_sd_fp_two["Cities"], values= regions_sd_fp_two["Purchases_Qty"], opacity=0.5)])
    pie_region_sd_fp_two.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_region_sd_fp_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 300)


    # E.11. Vente par models de SD
    models_sd_fp_two = df_sd_fp_two.groupby("Products", as_index= False)["Purchases_Qty"].sum()
    bar_models_sd_fp_two = px.bar(models_sd_fp_two, x="Products", y="Purchases_Qty", color="Products", text="Purchases_Qty")
    bar_models_sd_fp_two.update_traces(textposition = 'outside')
    bar_models_sd_fp_two.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # E.12. Graphique en Pie pour models 
    pie_models_sd_fp_two = go.Figure(data = [go.Pie(labels = models_sd_fp_two["Products"], values= models_sd_fp_two["Purchases_Qty"], opacity=0.5)])
    pie_models_sd_fp_two.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_models_sd_fp_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 300)

    # E.13. Vente par clients de SD
    clients_sd_fp_two = df_sd_fp_two.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
    bar_clients_sd_fp_two = px.bar(clients_sd_fp_two, x="Customers_Name", y="Purchases_Qty", color="Customers_Name", text="Purchases_Qty")
    bar_clients_sd_fp_two.update_traces(textposition = 'outside')
    bar_clients_sd_fp_two.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 370, height = 300)
    
    # E.14. Graphique en Pie pour clients 
    pie_clients_sd_fp_two = go.Figure(data = [go.Pie(labels = clients_sd_fp_two["Customers_Name"], values= clients_sd_fp_two["Purchases_Qty"], opacity=0.5)])
    pie_clients_sd_fp_two.update_traces (textinfo = "none", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    pie_clients_sd_fp_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 150, height = 280)

    # E.15. Graphique en Line qui affiche les achats annuel du client choisi 
    yearlySD_clients_fp = df_clients_2_full.groupby("Years", as_index= False)["Purchases_Qty"].sum()
    yearly_fig_fp_one = px.line(yearlySD_clients_fp , x="Years", y="Purchases_Qty", text= "Purchases_Qty")
    yearly_fig_fp_one.update_traces(textposition = 'top center')
    yearly_fig_fp_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # E.16. Graphique en Line qui affiche les achats mensuel du clients chois
    monthlySD_clients_fp = df_clients_2.groupby("Date", as_index= False)["Purchases_Qty"].sum()
    monthly_fig_fp_one = px.line(monthlySD_clients_fp , x="Date", y="Purchases_Qty", text= "Purchases_Qty")
    monthly_fig_fp_one.update_traces(textposition = 'top center')
    monthly_fig_fp_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # E.17. Graphique en Bar qui affiche les models achate par les clients par ans
    model_years_fp = df_clients_2.groupby(["Years", "Products"], as_index= False)["Purchases_Qty"].sum()
    model_years_fp_fig = px.bar(model_years_fp, x="Years", y="Purchases_Qty", color="Products",text="Purchases_Qty", barmode= "group")
    model_years_fp_fig.update_traces(textposition = 'outside')
    model_years_fp_fig.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 1180, height = 300)

    # 4. Envoi simultané aux composants graphiques et métriques
    return ( 
        txt_qty_sd_fp_one, 
        txt_achat_sd_fp_one, 
        moyenne_sd_fp_one, 
        mediane_sd_fp_one, 
        ecarT_dt_fp_one, 
        maximum_sd_fp_one, 
        minimum_sd_fp_one, 
        txt_qty_sd_fp_two, 
        txt_achat_sd_fp_two, 
        moyenne_sd_fp_two, 
        mediane_sd_fp_two, 
        ecarT_dt_fp_two, 
        maximum_sd_fp_two, 
        minimum_sd_fp_two,  
        sd_fp_monthly_fig_one, 
        bar_regions_sd_fp_one, 
        pie_region_sd_fp_one, 
        bar_models_sd_fp_one, 
        pie_models_sd_fp_one, 
        bar_clients_sd_fp_one, 
        pie_clients_sd_fp_one, 
        sd_fp_monthly_fig_two, 
        bar_regions_sd_fp_two, 
        pie_region_sd_fp_two, 
        bar_models_sd_fp_two, 
        pie_models_sd_fp_two, 
        bar_clients_sd_fp_two, 
        pie_clients_sd_fp_two, 
        yearly_fig_fp_one, 
        monthly_fig_fp_one, 
        model_years_fp_fig
        ) 