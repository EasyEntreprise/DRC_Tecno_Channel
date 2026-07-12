# IMPORTATION
from dash import callback
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_mantine_components as dmc
from datetime import datetime
from database.connectDB import engine
import pandas as pd
from database.data import st_data_sp

# Convertir en date
st_data_sp["Date"] = pd.to_datetime(st_data_sp["Date"])


#############
## CALLBACK
##############
# ==========================================
# LE CALLBACK LISTE DEROULANTE 1
# ==========================================
@callback(
    [
        Output('multiselect-modelST_Smart', 'data'),
        Output('multiselect-modelST_Smart', 'value'),
    ],

    [
        Input('date-picker-rep-date1', 'start_date'),
        Input('date-picker-rep-date2', 'end_date'),
    ]
)

def maj_liste_deroulanteOne(debut, fin):
    if not debut or not fin :
        models_uniques = st_data_sp["Products"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date_one = pd.to_datetime(debut)
        end_date_two   = pd.to_datetime(fin)
        df_temp        = st_data_sp[(st_data_sp["Date"] >= start_date_one) & (st_data_sp["Date"] <= end_date_two)]
        models_uniques = df_temp["Products"].unique()


    # Formater les options pour le dmc.Select de Mantine
    options_models = [{"value": prod, "label": prod} for prod in models_uniques]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    models_par_defaut = [models_uniques[0]] if len(models_uniques) > 0 else []

    return options_models, models_par_defaut

################################################
### CallBack General ST-SP
################################################
@callback(
    [
        ################
        ##### Metric ###
        ################
        # ST-SMART PHONE 1
        Output('total-purchaseST-old', 'children'),
        Output('best-ST-SP-old', 'children'),
        Output('bad-ST-SP-old', 'children'),
        Output('average-st-sp-one', 'children'),
        Output('median-st-sp-one', 'children'),
        Output('ecartT-st-sp-one', 'children'),
        Output('maxim-st-sp-one', 'children'),
        Output('minim-st-sp-one', 'children'),

        # ST-SMART PHONE 2
        Output('total-purchaseST-new', 'children'),
        Output('best-ST-SP-new', 'children'),
        Output('bad-ST-SP-new', 'children'),
        Output('average-st-sp-two', 'children'),
        Output('median-st-sp-two', 'children'),
        Output('ecartT-st-sp-two', 'children'),
        Output('maxim-st-sp-two', 'children'),
        Output('minim-st-sp-two', 'children'),

        ########################    
        ###### Graphic #########
        ########################
        # ST-SMART PHONE 1
        Output('monthly_ST_SP_Line_old', 'figure'),
        Output('weekly_ST_SP_Line_old', 'figure'),
        Output('Channel_ST_SP_Bar_old', 'figure'),
        Output('Channel_ST_SP_Pie_old', 'figure'),
        Output('series_ST_SP_Bar_old', 'figure'),
        Output('series_ST_SP_Pie_old', 'figure'),
        Output('models_ST_SP_Bar_old', 'figure'),
        Output('models_ST_SP_Pie_old', 'figure'),


        # ST-SMART PHONE 2
        Output('monthly_ST_SP_Line_new', 'figure'),
        Output('weekly_ST_SP_Line_new', 'figure'),
        Output('Channel_ST_SP_Bar_new', 'figure'),
        Output('Channel_ST_SP_Pie_new', 'figure'),
        Output('series_ST_SP_Bar_new', 'figure'),
        Output('series_ST_SP_Pie_new', 'figure'),
        Output('models_ST_SP_Bar_new', 'figure'),
        Output('models_ST_SP_Pie_new', 'figure'),
        Output('modelSelectBar-st-sp-old', 'figure'),
        Output('modelSelectPie-st-sp-old', 'figure'),
    ],

    [
        Input('date-picker-rep-date1', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-rep-date1', 'end_date'),
        Input('date-picker-rep-date2', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-rep-date2', 'end_date'),
        Input('multiselect-modelST_Smart', 'value'),
    ]
)

def filter_data_st_sp(debut_one, fin_one, debut_two, fin_two, produit):

    # 1. Sécurité : si une des deux dates est effacée par l'utilisateur

    #######################
    #### ST SMART
    if not debut_one or not fin_one:
        df_filtre_one = st_data_sp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date_one = pd.to_datetime(debut_one)
        end_date_one = pd.to_datetime(fin_one)
        df_filtre_one = st_data_sp[(st_data_sp['Date'] >= start_date_one) & (st_data_sp['Date'] <= end_date_one)]


    if not debut_two or not fin_two:
        df_filtre_two = st_data_sp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date_two = pd.to_datetime(debut_two)
        end_date_two = pd.to_datetime(fin_two)
        df_filtre_two = st_data_sp[(st_data_sp['Date'] >= start_date_two) & (st_data_sp['Date'] <= end_date_two)]

    if not debut_one or not fin_two:
        df_filtre_three = st_data_sp.copy()

    else:
        start_date_one = pd.to_datetime(debut_one)
        end_date_two = pd.to_datetime(fin_two)
        df_filtre_three = st_data_sp[(st_data_sp['Date'] >= start_date_one) & (st_data_sp['Date'] <= end_date_two)]
    


    #############################
    #########
    # ST-SP
    if produit :
        df_produits = df_filtre_three[df_filtre_three["Products"].isin(produit)]
    else :
        df_produits = df_filtre_three.copy()


    ####################
    ### METRIC
    ####################
    #########################
    ### A. ST SMART PHONE

    ## Parti 1
    total_achat_one  = df_filtre_one["Purchased_Qty"].sum()

    best_st_sp_one   = df_filtre_one.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    best_week_one    = best_st_sp_one["Purchased_Qty"].max()
    bad_week_one     = best_st_sp_one["Purchased_Qty"].min()
    
    txt_achat_one    = f"{total_achat_one:,.2f} Pcs"
    txt_bestWeek_one = f"{best_week_one :,.2f} Pcs"
    txt_badWeek_one  = f"{bad_week_one:,.2f} Pcs"

    ## Statistiques #####
    statis_st_sp_one    = df_filtre_one.groupby("Date", as_index= False)["Purchased_Qty"].sum()
    
    moyenne_st_sp_one   = statis_st_sp_one["Purchased_Qty"].mean()
    mediane_st_sp_one   = statis_st_sp_one["Purchased_Qty"].median()
    ecarT_st_sp_one     = statis_st_sp_one["Purchased_Qty"].std()
    maximum_st_sp_one   = statis_st_sp_one["Purchased_Qty"].max()
    minimum_st_sp_one   = statis_st_sp_one["Purchased_Qty"].min()
  

    ## Partie 2
    total_achat_two  = df_filtre_two["Purchased_Qty"].sum()

    best_st_sp_two   = df_filtre_two.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    best_week_two    = best_st_sp_two["Purchased_Qty"].max()
    bad_week_two     = best_st_sp_two["Purchased_Qty"].min()
    
    txt_achat_two    = f"{total_achat_two:,.2f} Pcs"
    txt_bestWeek_two = f"{best_week_two :,.2f} Pcs"
    txt_badWeek_two  = f"{bad_week_two:,.2f} Pcs"

    ## Statistiques #####
    statis_st_sp_two   = df_filtre_two.groupby("Date", as_index= False)["Purchased_Qty"].sum()
    
    moyenne_st_sp_two   = statis_st_sp_two["Purchased_Qty"].mean()
    mediane_st_sp_two   = statis_st_sp_two["Purchased_Qty"].median()
    ecarT_st_sp_two     = statis_st_sp_two["Purchased_Qty"].std()
    maximum_st_sp_two   = statis_st_sp_two["Purchased_Qty"].max()
    minimum_st_sp_two   = statis_st_sp_two["Purchased_Qty"].min()


    #####################################################################
    #####################################################################
    ########################### GRAPHIC #################################
    #####################################################################
    ########################
    ## B. ST SMART PHONE
    ##########


    # B.1. Graphique en Line sur la situation mensuelle
    monthly_one = df_filtre_one.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    monthly_fig_one = px.line(monthly_one , x="Months", y="Purchased_Qty", text= "Purchased_Qty", title="Monthly Sell FOR ST-SP")
    monthly_fig_one.update_traces(textposition = 'top center')
    monthly_fig_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.2. Graphique en Line sur la situation semestriel
    weekly_one = df_filtre_one.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    weekly_fig_one = px.line(weekly_one , x="Weeks", y="Purchased_Qty", text= "Purchased_Qty", title="Weekly Sell FOR ST-SP")
    weekly_fig_one.update_traces(textposition = 'top center')
    weekly_fig_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.3. Graphique en Bar pour channel Kin et Lushi
    channel_one = df_filtre_one.groupby("City", as_index= False)["Purchased_Qty"].sum()

    fig_bar_channel_one = px.bar(
        channel_one, 
        x="City", 
        y="Purchased_Qty", 
        color="City",
        text="Purchased_Qty",
        title="Channel-City situation for ST-SP"
    )
    fig_bar_channel_one.update_traces(textposition = 'outside')
    fig_bar_channel_one.update_layout(showlegend= False,margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.4. Graphique en Pie pour channel Kin et Lushi
    fig_pie_chan_one = go.Figure(data = [go.Pie(labels = channel_one["City"], values= channel_one["Purchased_Qty"], title = "Channel-City Proportions for ST-SP", opacity=0.5)])
    fig_pie_chan_one.update_traces (textinfo = "percent", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    fig_pie_chan_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 180, height = 280)

    # B.5. Graphique en Bar pour les series
    series_one = df_filtre_one.groupby("SERIES", as_index= False)["Purchased_Qty"].sum()
    fig_bar_series_one = px.bar(
        series_one, 
        x="SERIES", 
        y="Purchased_Qty", 
        color="SERIES",
        text="Purchased_Qty",
        title="Channel-Series situation for ST-SP"
    )
    fig_bar_series_one.update_traces(textposition = 'outside')
    fig_bar_series_one.update_layout(showlegend= False, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.6. Graphique en Pie pour les series
    fig_pie_series_one = go.Figure(data = [go.Pie(labels = series_one["SERIES"], values= series_one["Purchased_Qty"], title = "Channel-Series Proportions for ST-SP", opacity=0.5)])
    fig_pie_series_one.update_traces (textinfo = "percent", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    fig_pie_series_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 180, height = 280)

    # B.7. Graphique en Bar pour les modeles
    models_one = df_filtre_one.groupby("Products", as_index= False)["Purchased_Qty"].sum()
    fig_bar_models_one = px.bar(
        models_one, 
        x="Products", 
        y="Purchased_Qty", 
        color="Products",
        text="Purchased_Qty",
        title="Channel-models situation for ST-SP"
    )
    fig_bar_models_one.update_traces(textposition = 'outside', textfont_size=8)
    fig_bar_models_one.update_layout(showlegend= False, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.8. Graphique en Pie pour les modeles
    fig_pie_models_one = go.Figure(data = [go.Pie(labels = models_one["Products"], values= models_one["Purchased_Qty"], title = "Channel-models Proportions for ST-SP", opacity=0.5)])
    fig_pie_models_one.update_traces (hoverinfo='percent', textfont_size=15, textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2), hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>")
    fig_pie_models_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 180, height = 280)

    # B.9. Graphique en Bar qui affiche
    group_produits = df_produits.groupby(["Years", "Products"], as_index= False)["Purchased_Qty"].sum()

    fig_barx_one = px.bar(
        group_produits, 
        x="Years", 
        y="Purchased_Qty", 
        color="Products",
        text="Purchased_Qty",
        barmode= "group"
    )
    fig_barx_one.update_traces(textposition = 'outside', textfont_size=8)
    fig_barx_one.update_layout(showlegend= False, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor = '#F8F9FA', width = 780, height = 360)
    
    
    # B.10. Graphique en Histogram pour channel
    fig_piex_one = go.Figure(data = [go.Pie(labels = group_produits["Years"], values= group_produits["Purchased_Qty"], opacity=0.5)])
    fig_piex_one.update_traces (textinfo = "percent", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    fig_piex_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 360, height = 310)
    
    #############
    # Partie II
    # B.11. Graphique en Line sur la situation mensuelle
    monthly_two = df_filtre_two.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    monthly_fig_two = px.line(monthly_two , x="Months", y="Purchased_Qty", text= "Purchased_Qty", title="Monthly Sell FOR ST-SP")
    monthly_fig_two.update_traces(textposition = 'top center')
    monthly_fig_two.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.12. Graphique en Line sur la situation semestriel
    weekly_two = df_filtre_two.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    weekly_fig_two = px.line(weekly_two , x="Weeks", y="Purchased_Qty", text= "Purchased_Qty", title="Weekly Sell FOR ST-SP")
    weekly_fig_two.update_traces(textposition = 'top center')
    weekly_fig_two.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.13. Graphique en Bar pour channel Kin et Lushi
    channel_two = df_filtre_two.groupby("City", as_index= False)["Purchased_Qty"].sum()

    fig_bar_channel_two = px.bar(
        channel_two, 
        x="City", 
        y="Purchased_Qty", 
        color="City",
        text="Purchased_Qty",
        title="Channel-City situation for ST-SP"
    )
    fig_bar_channel_two.update_traces(textposition = 'outside')
    fig_bar_channel_two.update_layout(showlegend= False, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.14. Graphique en Pie pour channel Kin et Lushi
    fig_pie_chan_two = go.Figure(data = [go.Pie(labels = channel_two["City"], values= channel_two["Purchased_Qty"], title = "Channel-City Proportions for ST-SP", opacity=0.5)])
    fig_pie_chan_two.update_traces (hoverinfo='percent', textfont_size=15, textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2), hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>")
    fig_pie_chan_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 180, height = 280)

    # B.15. Graphique en Bar pour les series
    series_two = df_filtre_two.groupby("SERIES", as_index= False)["Purchased_Qty"].sum()
    fig_bar_series_two = px.bar(
        series_two, 
        x="SERIES", 
        y="Purchased_Qty", 
        color="SERIES",
        text="Purchased_Qty",
        title="Channel-Series situation for ST-SP"
    )
    fig_bar_series_two.update_traces(textposition = 'outside')
    fig_bar_series_two.update_layout(showlegend= False, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.16. Graphique en Pie pour les series
    fig_pie_series_two = go.Figure(data = [go.Pie(labels = series_two["SERIES"], values= series_two["Purchased_Qty"], title = "Channel-Series Proportions for ST-SP", opacity=0.5)])
    fig_pie_series_two.update_traces (hoverinfo='percent', textfont_size=15, textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2), hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>")
    fig_pie_series_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 180, height = 280)

    # B.17. Graphique en Bar pour les models
    models_two = df_filtre_two.groupby("Products", as_index= False)["Purchased_Qty"].sum()
    fig_bar_models_two = px.bar(
        models_two, 
        x="Products", 
        y="Purchased_Qty", 
        color="Products",
        text="Purchased_Qty",
        title="Channel-models situation for ST-SP"
    )
    fig_bar_models_two.update_traces(textposition = 'outside', textfont_size=8)
    fig_bar_models_two.update_layout(showlegend= False, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.18. Graphique en Pie pour les modeles
    fig_pie_models_two = go.Figure(data = [go.Pie(labels = models_two["Products"], values= models_two["Purchased_Qty"], title = "Channel-models Proportions for ST-SP", opacity=0.5)])
    fig_pie_models_two.update_traces (hoverinfo='percent', textfont_size=15, textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2), hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>")
    fig_pie_models_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 180, height = 280)


    # 4. Envoi simultané aux composants graphiques et métriques
    return (
        txt_achat_one, 
        txt_bestWeek_one, 
        txt_badWeek_one, 
        moyenne_st_sp_one, 
        mediane_st_sp_one, 
        ecarT_st_sp_one, 
        maximum_st_sp_one, 
        minimum_st_sp_one, 
        txt_achat_two, 
        txt_bestWeek_two, 
        txt_badWeek_two, 
        moyenne_st_sp_two, 
        mediane_st_sp_two, 
        ecarT_st_sp_two, 
        maximum_st_sp_two, 
        minimum_st_sp_two, 
        monthly_fig_one, 
        weekly_fig_one, 
        fig_bar_channel_one, 
        fig_pie_chan_one, 
        fig_bar_series_one, 
        fig_pie_series_one, #
        fig_bar_models_one, 
        fig_pie_models_one, 
        monthly_fig_two, 
        weekly_fig_two, 
        fig_bar_channel_two, 
        fig_pie_chan_two, 
        fig_bar_series_two, 
        fig_pie_series_two, 
        fig_bar_models_two, 
        fig_pie_models_two, 
        fig_barx_one, 
        fig_piex_one
        ) 