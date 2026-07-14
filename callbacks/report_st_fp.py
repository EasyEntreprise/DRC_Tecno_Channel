# IMPORTATION
from dash import callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_mantine_components as dmc
from datetime import datetime
from database.connectDB import engine
from database.data import st_data_fp

# Convertir en date
st_data_fp["Date"] = pd.to_datetime(st_data_fp["Date"])


# ==========================================
# LE CALLBACK LISTE DEROULANTE 2
# ==========================================
@callback(
    [
        Output('multiselect-modelST_Feature', 'data'),
        Output('multiselect-modelST_Feature', 'value'),
    ],

    [
        Input('date-picker-rep-date1', 'start_date'),
        Input('date-picker-rep-date2', 'end_date'),
    ]
)

def maj_liste_deroulanteTwo(debut, fin):
    if not debut or not fin :
        models_uniques_2 = st_data_fp["Products"].unique()

    else :
        # Filtrer temporairement par date pour trouver les produits vendus sur cette periode
        start_date_one = pd.to_datetime(debut)
        end_date_two   = pd.to_datetime(fin)
        df_temp        = st_data_fp[(st_data_fp["Date"] >= start_date_one) & (st_data_fp["Date"] <= end_date_two)]
        models_uniques_2 = df_temp["Products"].unique()


    # Formater les options pour le dmc.Select de Mantine
    options_models_2 = [{"value": prod, "label": prod} for prod in models_uniques_2]

    # Valeur par defaut : on prend le premier produit de la liste s'il y en a un
    models_par_defaut_2 = [models_uniques_2[0]] if len(models_uniques_2) > 0 else []

    return options_models_2, models_par_defaut_2

################################################
### CallBack General ST-SP
################################################
@callback(
    [
        ################
        ##### Metric ###
        ################
        # ST-FEATURE PHONE 1
        Output('total-purchaseST-FP-old', 'children'),
        Output('best-ST-FP-old', 'children'),
        Output('bad-ST-FP-old', 'children'),
        Output('average-st-fp-one', 'children'),
        Output('median-st-fp-one', 'children'),
        Output('ecartT-st-fp-one', 'children'),
        Output('maxim-st-fp-one', 'children'),
        Output('minim-st-fp-one', 'children'),

        # ST-FEATURE PHONE 2
        Output('total-purchaseST-FP-new', 'children'),
        Output('best-ST-FP-new', 'children'),
        Output('bad-ST-FP-new', 'children'),
        Output('average-st-fp-two', 'children'),
        Output('median-st-fp-two', 'children'),
        Output('ecartT-st-fp-two', 'children'),
        Output('maxim-st-fp-two', 'children'),
        Output('minim-st-fp-two', 'children'),

        ########################    
        ###### Graphic #########
        ########################
        # ST-FEATURE PHONE 1
        Output('monthly_ST_FP_Line_old', 'figure'),
        Output('weekly_ST_FP_Line_old', 'figure'),
        Output('Channel_ST_FP_Bar_old', 'figure'),
        Output('Channel_ST_FP_Pie_old', 'figure'),
        Output('models_ST_FP_Bar_old', 'figure'),
        Output('models_ST_FP_Pie_old', 'figure'),

        # ST-FEATURE PHONE 2
        Output('monthly_ST_FP_Line_new', 'figure'),
        Output('weekly_ST_FP_Line_new', 'figure'),
        Output('Channel_ST_FP_Bar_new', 'figure'),
        Output('Channel_ST_FP_Pie_new', 'figure'),
        Output('models_ST_FP_Bar_new', 'figure'),
        Output('models_ST_FP_Pie_new', 'figure'),
        Output('modelSelectBar-st-fp-old', 'figure'),
        Output('modelSelectPie-st-fp-old', 'figure'),
    ],

    [
        Input('date-picker-rep-date1', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-rep-date1', 'end_date'),
        Input('date-picker-rep-date2', 'start_date'),  # Input 1 : Date de début
        Input('date-picker-rep-date2', 'end_date'),
        Input('multiselect-modelST_Feature', 'value'),
    ]
)

def filter_data_st_fp(debut_one, fin_one, debut_two, fin_two, produit_2):

    # 1. Sécurité : si une des deux dates est effacée par l'utilisateur
    
    #######################
    #### ST FEATURE
    if not debut_one or not fin_one:
        df_filtre_st_fp_one = st_data_fp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date_one = pd.to_datetime(debut_one)
        end_date_one = pd.to_datetime(fin_one)
        df_filtre_st_fp_one = st_data_fp[(st_data_fp['Date'] >= start_date_one) & (st_data_fp['Date'] <= end_date_one)]


    if not debut_two or not fin_two:
        df_filtre_st_fp_two = st_data_fp.copy()
    else:
        # 2. Filtrage strict du DataFrame Pandas avec vos variables 'debut' et 'fin'
        start_date_two = pd.to_datetime(debut_two)
        end_date_two = pd.to_datetime(fin_two)
        df_filtre_st_fp_two = st_data_fp[(st_data_fp['Date'] >= start_date_two) & (st_data_fp['Date'] <= end_date_two)]

    if not debut_one or not fin_two:
        df_filtre_four = st_data_fp.copy()

    else:
        start_date_one = pd.to_datetime(debut_one)
        end_date_two = pd.to_datetime(fin_two)
        df_filtre_four = st_data_fp[(st_data_fp['Date'] >= start_date_one) & (st_data_fp['Date'] <= end_date_two)]


    #############################
    #########
    # ST-FP
    if produit_2 :
        df_produits_2 = df_filtre_four[df_filtre_four["Products"].isin(produit_2)]
    else :
        df_produits_2 = df_filtre_four.copy()
    


    ####################
    ### METRIC
    ####################
    #########################
    ### A. ST FEATURE PHONE

    ## Parti 1
    total_achat_st_fp_one  = df_filtre_st_fp_one["Purchased_Qty"].sum()

    best_st_fp_one         = df_filtre_st_fp_one.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    best_week_st_fp_one    = best_st_fp_one["Purchased_Qty"].max()
    bad_week_st_fp_one     = best_st_fp_one["Purchased_Qty"].min()
    
    txt_achat_st_fp_one    = f"{total_achat_st_fp_one:,.2f} Pcs"
    txt_bestWeek_st_fp_one = f"{best_week_st_fp_one :,.2f} Pcs"
    txt_badWeek_st_fp_one  = f"{bad_week_st_fp_one:,.2f} Pcs"
 

    ## Statistiques #####
    statis_st_fp_one    = df_filtre_st_fp_one.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    
    moyenne_st_fp_one   = statis_st_fp_one["Purchased_Qty"].mean()
    mediane_st_fp_one   = statis_st_fp_one["Purchased_Qty"].median()
    ecarT_st_fp_one     = statis_st_fp_one["Purchased_Qty"].std()
    maximum_st_fp_one   = statis_st_fp_one["Purchased_Qty"].max()
    minimum_st_fp_one   = statis_st_fp_one["Purchased_Qty"].min()
  

    ## Partie 2
    total_achat_st_fp_two = df_filtre_st_fp_two["Purchased_Qty"].sum()

    best_st_fp_two         = df_filtre_st_fp_two.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    best_week_st_fp_two    = best_st_fp_two["Purchased_Qty"].max()
    bad_week_st_fp_two     = best_st_fp_two["Purchased_Qty"].min()
    
    txt_achat_st_fp_two    = f"{total_achat_st_fp_two:,.2f} Pcs"
    txt_bestWeek_st_fp_two = f"{best_week_st_fp_two :,.2f} Pcs"
    txt_badWeek_st_fp_two  = f"{bad_week_st_fp_two:,.2f} Pcs"

    ## Statistiques #####
    statis_st_fp_two    = df_filtre_st_fp_two.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    
    moyenne_st_fp_two   = statis_st_fp_two["Purchased_Qty"].mean()
    mediane_st_fp_two   = statis_st_fp_two["Purchased_Qty"].median()
    ecarT_st_fp_two     = statis_st_fp_two["Purchased_Qty"].std()
    maximum_st_fp_two   = statis_st_fp_two["Purchased_Qty"].max()
    minimum_st_fp_two   = statis_st_fp_two["Purchased_Qty"].min()

    #####################################################################
    #####################################################################
    ########################### GRAPHIC #################################
    #####################################################################
    ########################
    ## B. ST FEATURE PHONE
    ##########

    # B.1. Graphique en Line sur la situation mensuelle
    monthly_st_fp_one = df_filtre_st_fp_one.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    monthly_fig_st_fp_one = px.line(monthly_st_fp_one , x="Months", y="Purchased_Qty", text= "Purchased_Qty", title="Monthly Sell FOR ST-FP")
    monthly_fig_st_fp_one.update_traces(textposition = 'top center')
    monthly_fig_st_fp_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.2. Graphique en Line sur la situation semestriel
    weekly_st_fp_one = df_filtre_st_fp_one.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    weekly_fig_st_fp_one = px.line(weekly_st_fp_one , x="Weeks", y="Purchased_Qty", text= "Purchased_Qty", title="Weekly Sell FOR ST-FP")
    weekly_fig_st_fp_one.update_traces(textposition = 'top center')
    weekly_fig_st_fp_one.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.3. Graphique en Bar pour channel Kin et Lushi
    channel_st_fp_one = df_filtre_st_fp_one.groupby("City", as_index= False)["Purchased_Qty"].sum()

    fig_bar_channel_st_fp_one = px.bar(
        channel_st_fp_one, 
        x="City", 
        y="Purchased_Qty", 
        color="City",
        text="Purchased_Qty",
        title="Channel-City situation for ST-SP"
    )
    fig_bar_channel_st_fp_one.update_traces(textposition = 'outside')
    fig_bar_channel_st_fp_one.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.4. Graphique en Pie pour channel Kin et Lushi
    fig_pie_chan_st_fp_one = go.Figure(data = [go.Pie(labels = channel_st_fp_one["City"], values= channel_st_fp_one["Purchased_Qty"], title = "Channel-City Proportions for ST-FP", opacity=0.5)])
    fig_pie_chan_st_fp_one.update_traces (textinfo = "percent", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    fig_pie_chan_st_fp_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 180, height = 280)

    
    # B.5. Graphique en Bar pour les modeles
    models_st_fp_one = df_filtre_st_fp_one.groupby("Products", as_index= False)["Purchased_Qty"].sum()
    fig_bar_models_st_fp_one = px.bar(
        models_st_fp_one, 
        x="Products", 
        y="Purchased_Qty", 
        color="Products",
        text="Purchased_Qty",
        title="Channel-models situation for ST-FP"
    )
    fig_bar_models_st_fp_one.update_traces(textposition = 'outside', textfont_size=8)
    fig_bar_models_st_fp_one.update_layout(showlegend= False, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.6. Graphique en Pie pour les modeles
    fig_pie_models_st_fp_one = go.Figure(data = [go.Pie(labels = models_st_fp_one["Products"], values= models_st_fp_one["Purchased_Qty"], title = "Channel-models Proportions for ST-FP", opacity=0.5)])
    fig_pie_models_st_fp_one.update_traces (hoverinfo='percent', textfont_size=15, textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2), hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>")
    fig_pie_models_st_fp_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 180, height = 280)

    # B.7. Graphique en Bar qui affiche
    group_produits_2 = df_produits_2.groupby(["Years", "Products"], as_index= False)["Purchased_Qty"].sum()

    fig_barx_st_fp_one = px.bar(
        group_produits_2, 
        x="Years", 
        y="Purchased_Qty", 
        color="Products",
        text="Purchased_Qty",
        barmode= "group"
    )
    fig_barx_st_fp_one.update_traces(textposition = 'outside', textfont_size=8)
    fig_barx_st_fp_one.update_layout(showlegend= False, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor = '#F8F9FA', width = 780, height = 360)    
    
    # B.8. Graphique en Histogram pour channel
    fig_piex_st_fp_one = go.Figure(data = [go.Pie(labels = group_produits_2["Years"], values= group_produits_2["Purchased_Qty"], opacity=0.5)])
    fig_piex_st_fp_one.update_traces (textinfo = "percent", hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>", hoverinfo='percent', pull= [0.05, 0, 0, 0, 0], textfont_size=15)
    fig_piex_st_fp_one.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 360, height = 310)
    
    #############
    # Partie II
    # B.9. Graphique en Line sur la situation mensuelle
    monthly_st_fp_two = df_filtre_st_fp_two.groupby("Months", as_index= False)["Purchased_Qty"].sum()
    monthly_fig_st_fp_two = px.line(monthly_st_fp_two , x="Months", y="Purchased_Qty", text= "Purchased_Qty", title="Monthly Sell FOR ST-FP")
    monthly_fig_st_fp_two.update_traces(textposition = 'top center')
    monthly_fig_st_fp_two.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.10. Graphique en Line sur la situation semestriel
    weekly_st_fp_two = df_filtre_st_fp_two.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
    weekly_fig_st_fp_two = px.line(weekly_st_fp_two , x="Weeks", y="Purchased_Qty", text= "Purchased_Qty", title="Weekly Sell FOR ST-FP")
    weekly_fig_st_fp_two.update_traces(textposition = 'top center')
    weekly_fig_st_fp_two.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 290)

    # B.11. Graphique en Bar pour channel Kin et Lushi
    channel_st_fp_two = df_filtre_st_fp_two.groupby("City", as_index= False)["Purchased_Qty"].sum()

    fig_bar_channel_st_fp_two = px.bar(
        channel_st_fp_two, 
        x="City", 
        y="Purchased_Qty", 
        color="City",
        text="Purchased_Qty",
        title="Channel-City situation for ST-FP"
    )
    fig_bar_channel_st_fp_two.update_traces(textposition = 'outside')
    fig_bar_channel_st_fp_two.update_layout(showlegend= False, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.12. Graphique en Pie pour channel Kin et Lushi
    fig_pie_chan_st_fp_two = go.Figure(data = [go.Pie(labels = channel_st_fp_two["City"], values= channel_st_fp_two["Purchased_Qty"], title = "Channel-City Proportions for ST-FP", opacity=0.5)])
    fig_pie_chan_st_fp_two.update_traces (hoverinfo='percent', textfont_size=15, textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2), hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>")
    fig_pie_chan_st_fp_two.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), showlegend= False, font= dict(size= 8), width = 180, height = 280)

    
    # B.13. Graphique en Bar pour les models
    models_st_fp_two = df_filtre_st_fp_two.groupby("Products", as_index= False)["Purchased_Qty"].sum()
    fig_bar_models_st_fp_two = px.bar(
        models_st_fp_two, 
        x="Products", 
        y="Purchased_Qty", 
        color="Products",
        text="Purchased_Qty",
        title="Channel-models situation for ST-FP"
    )
    fig_bar_models_st_fp_two.update_traces(textposition = 'outside', textfont_size=8)
    fig_bar_models_st_fp_two.update_layout(showlegend= False, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor = '#F8F9FA', width = 380, height = 290)

    # B.14. Graphique en Pie pour les modeles
    fig_pie_models_st_fp_two = go.Figure(data = [go.Pie(labels = models_st_fp_two["Products"], values= models_st_fp_two["Purchased_Qty"], title = "Channel-models Proportions for ST-FP", opacity=0.5)])
    fig_pie_models_st_fp_two.update_traces (hoverinfo='percent', textfont_size=15, textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2), hovertemplate = "<b>%{label}</b><br>" "Ventes : %{value}<br>" "Pourcentage : %{percent}<extra></extra>")
    fig_pie_models_st_fp_two.update_layout(showlegend= False, margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 180, height = 280)


    # 4. Envoi simultané aux composants graphiques et métriques
    return (
        txt_achat_st_fp_one, 
        txt_bestWeek_st_fp_one, 
        txt_badWeek_st_fp_one, 
        moyenne_st_fp_one, 
        mediane_st_fp_one, 
        ecarT_st_fp_one, 
        maximum_st_fp_one, 
        minimum_st_fp_one, 
        txt_achat_st_fp_two, 
        txt_bestWeek_st_fp_two, 
        txt_badWeek_st_fp_two, 
        moyenne_st_fp_two, 
        mediane_st_fp_two, 
        ecarT_st_fp_two, 
        maximum_st_fp_two, 
        minimum_st_fp_two,
        monthly_fig_st_fp_one, 
        weekly_fig_st_fp_one, 
        fig_bar_channel_st_fp_one, 
        fig_pie_chan_st_fp_one, 
        fig_bar_models_st_fp_one, 
        fig_pie_models_st_fp_one, 
        monthly_fig_st_fp_two, 
        weekly_fig_st_fp_two, 
        fig_bar_channel_st_fp_two, 
        fig_pie_chan_st_fp_two, 
        fig_bar_models_st_fp_two, 
        fig_pie_models_st_fp_two, 
        fig_barx_st_fp_one, 
        fig_piex_st_fp_one
        ) 