# IMPORTATION LIBRAIRIES
from dash import html
from dash import dcc, dash_table
import pandas as pd
from database.connectDB import engine, SessionLocal
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import dash_mantine_components as dmc
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
st_data_sp["Date"] = pd.to_datetime(st_data_sp["Date"], errors="coerce").dt.date
st_data_fp["Date"] = pd.to_datetime(st_data_fp["Date"], errors="coerce").dt.date
sd_data_sp["Date"] = pd.to_datetime(sd_data_sp["Date"], errors="coerce").dt.date
sd_data_fp["Date"] = pd.to_datetime(sd_data_fp["Date"], errors="coerce").dt.date

# Extraire le mois
st_data_sp["Monthly"] = pd.to_datetime(st_data_sp["Months"], errors="coerce").dt.month
st_data_fp["Monthly"] = pd.to_datetime(st_data_fp["Months"], errors="coerce").dt.month
sd_data_sp["Monthly"] = pd.to_datetime(sd_data_sp["Date"], errors="coerce").dt.month
sd_data_fp["Monthly"] = pd.to_datetime(sd_data_fp["Date"], errors="coerce").dt.month

# Considerons seulement les donnees pour l'annee en cours pour nos ST et SD
year_st_sp = st_data_sp[st_data_sp["Years"] == annee_str]
year_st_fp = st_data_fp[st_data_fp["Years"] == annee_str]
year_sd_sp = sd_data_sp[sd_data_sp["Years"] == annee_str]
year_sd_fp = sd_data_fp[sd_data_fp["Years"] == annee_str]

# Considerons seulement les donnees pour le mois en cours pour nos ST et SD
month_st_sp = st_data_sp[st_data_sp["Monthly"] == mois_str]
month_st_fp = st_data_fp[st_data_fp["Monthly"] == mois_str]
month_sd_sp = sd_data_sp[sd_data_sp["Monthly"] == mois_str]
month_sd_fp = sd_data_fp[sd_data_fp["Monthly"] == mois_str]


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
    )

# 2. Graphic SD for SP
sd_sp_year = sd_data_sp.groupby("Years", as_index= False)["Purchases_Qty"].sum()
sd_sp_year_fig = px.line(sd_sp_year, x="Years", y="Purchases_Qty", text= "Purchases_Qty", title="A SUB-DEALERS FOR SP")
sd_sp_year_fig.update_traces(textposition = 'top center')
sd_sp_year_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA')

# 3. Graphic ST for FP
st_fp_year = st_data_fp.groupby("Years", as_index= False)["Purchased_Qty"].sum()
st_fp_year_fig = px.line(st_fp_year, x="Years", y="Purchased_Qty", text= "Purchased_Qty", title="SELL THROUGH FOR FP")
st_fp_year_fig.update_traces(textposition = 'top center')
st_fp_year_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA')

# 4. Graphic SD for FP
sd_fp_year = sd_data_fp.groupby("Years", as_index= False)["Purchases_Qty"].sum()
sd_fp_year_fig = px.line(sd_fp_year, x="Years", y="Purchases_Qty", text= "Purchases_Qty", title="A SUB-DEALERS FOR FP")
sd_fp_year_fig.update_traces(textposition = 'top center')
sd_fp_year_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA') # t(Top/Haut), b(Bottom/bas), l(left), r(right)

###########################
# B. This Years
########
# B.1. SELL THROUGH
# 5. Graphic monthly pour ST SP
monthly_st_sp = year_st_sp.groupby("Months", as_index= False)["Purchased_Qty"].sum()
monthly_st_sp_fig = px.line(monthly_st_sp, x="Months", y="Purchased_Qty", text= "Purchased_Qty", title=f"ST-{annee} for SMART PHONE (Monthly Situation)")
monthly_st_sp_fig.update_traces(textposition = 'top center')
monthly_st_sp_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 880, height = 280)


# 6. Graphic weekly pour ST SP
weekly_st_sp = year_st_sp.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
weekly_st_sp_fig = px.line(weekly_st_sp, x="Weeks", y="Purchased_Qty", text= "Purchased_Qty", title=f"ST-{annee} for SMART PHONE (Weekly Situation)")
weekly_st_sp_fig.update_traces(textposition = 'top center')
weekly_st_sp_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 880, height = 280)

channel_st_sp = year_st_sp.groupby("City", as_index= False)["Purchased_Qty"].sum()
channel_st_sp_pie = go.Figure(data = [go.Pie(labels = channel_st_sp["City"], values= channel_st_sp["Purchased_Qty"], title = "Channel Proportions for SP", opacity=0.5)])
channel_st_sp_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
channel_st_sp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 338, height = 300)

channel_st_sp_bar = px.bar(channel_st_sp, x="City", y="Purchased_Qty", color="City", title="Channel Situation for SP", text = "Purchased_Qty",)
channel_st_sp_bar.update_traces(textposition = 'outside')
channel_st_sp_bar.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 490, height = 300)

# 7. Graphic weekly pour ST FP
monthly_st_fp = year_st_fp.groupby("Months", as_index= False)["Purchased_Qty"].sum()
monthly_st_fp_fig = px.line(monthly_st_fp, x="Months", y="Purchased_Qty", text= "Purchased_Qty", title=f"ST-{annee} for FEATURE PHONE (Monthly Situation)")
monthly_st_fp_fig.update_traces(textposition = 'top center')
monthly_st_fp_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 880, height = 280)

weekly_st_fp = year_st_fp.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
weekly_st_fp_fig = px.line(weekly_st_fp, x="Weeks", y="Purchased_Qty", text= "Purchased_Qty", title=f"ST-{annee} for FEATURE PHONE")
weekly_st_fp_fig.update_traces(textposition = 'top center')
weekly_st_fp_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 880, height = 280)

channel_st_fp = year_st_fp.groupby("City", as_index= False)["Purchased_Qty"].sum()
channel_st_fp_pie = go.Figure(data = [go.Pie(labels = channel_st_fp["City"], values= channel_st_fp["Purchased_Qty"], title = "Channel Proportions for FP", opacity=0.5)])
channel_st_fp_pie.update_traces (hoverinfo='label+percent', textfont_size=15,textinfo= 'label+percent', pull= [0.05, 0, 0, 0, 0],marker_line=dict(color='#FFFFFF', width=2))
channel_st_fp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 338, height = 300)

channel_st_fp_bar = px.bar(channel_st_fp, x="City", y="Purchased_Qty", color="City", title="Channel Situation for FP", text = "Purchased_Qty",)
channel_st_fp_bar.update_traces(textposition = 'outside')
channel_st_fp_bar.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 490, height = 300)

# B.2. SUB-DEALERS
# 8. Graphic monthly pour SD SP
monthly_sd_sp = year_sd_sp.groupby("Date", as_index= False)["Purchases_Qty"].sum()
monthly_sd_sp_fig = px.line(monthly_sd_sp, x="Date", y="Purchases_Qty", text= "Purchases_Qty", title=f"SD-{annee} for SMART PHONE (Monthly Situation)")
monthly_sd_sp_fig.update_traces(textposition = 'top center')
monthly_sd_sp_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 880, height = 280)

# 9. Graphic Bar pour SD SP
cities_sd_sp = year_sd_sp.groupby("Cities", as_index= False)["Purchases_Qty"].sum()
cities_sd_sp_fig = px.bar(cities_sd_sp, x="Cities", y="Purchases_Qty", color="Cities", title="Sub-Dealers Situation for SP", text = "Purchases_Qty",)
cities_sd_sp_fig.update_traces(textposition = 'outside')
cities_sd_sp_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 280)

# 10. Graphic Pie pour SD SP
cities_sd_sp_pie = go.Figure(data = [go.Pie(labels = cities_sd_sp["Cities"], values= cities_sd_sp["Purchases_Qty"], title = "SD Proportions for SP", opacity=0.5)])
cities_sd_sp_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
cities_sd_sp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 300, height = 300)

# 11. Graphic Line monthly pour SD FP
monthly_sd_fp = year_sd_fp.groupby("Date", as_index= False)["Purchases_Qty"].sum()
monthly_sd_fp_fig = px.line(monthly_sd_fp, x="Date", y="Purchases_Qty", text= "Purchases_Qty", title=f"SD-{annee} for FEATURE PHONE (Monthly Situation)")
monthly_sd_fp_fig.update_traces(textposition = 'top center')
monthly_sd_fp_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 880, height = 280)

# 12. Graphic Bar pour SD FP
cities_sd_fp = year_sd_fp.groupby("Cities", as_index= False)["Purchases_Qty"].sum()
cities_sd_fp_fig = px.bar(cities_sd_fp, x="Cities", y="Purchases_Qty", color="Cities", title="Sub-Dealers Situation for FP", text = "Purchases_Qty",)
cities_sd_fp_fig.update_traces(textposition = 'outside')
cities_sd_fp_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 580, height = 280)

# 13. Graphic Pie pour SD FP
cities_sd_fp_pie = go.Figure(data = [go.Pie(labels = cities_sd_fp["Cities"], values= cities_sd_fp["Purchases_Qty"], title = "SD Proportions for FP", opacity=0.5)])
cities_sd_fp_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
cities_sd_fp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 300, height = 300)

# C. THIS MONTH
""" En ce basant de l'annee en cours, nous allons considerer que les donnees du mois en cours """
this_month_st_sp = year_st_sp[year_st_sp["Monthly"] == mois]
this_month_st_fp = year_st_fp[year_st_fp["Monthly"] == mois]
this_month_sd_sp = year_sd_sp[year_sd_sp["Monthly"] == mois]
this_month_sd_fp = year_sd_fp[year_sd_fp["Monthly"] == mois]


# C.A. SMART PHONE
# C.A.1. Graphic line line de ST SP par semaine
sp_line_st = this_month_st_sp.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
sp_line_st_fig = px.line(sp_line_st, x="Weeks", y="Purchased_Qty", text= "Purchased_Qty", title=f"ST-{annee}-{mois} for SMART PHONE (Weekly Situation)")
sp_line_st_fig.update_traces(textposition = 'top center')
sp_line_st_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 290)

# C.A.2. Le graphic en bar pour Channel ST SP
sp_line_st_bar = this_month_st_sp.groupby("City", as_index= False)["Purchased_Qty"].sum()
sp_line_st_bar_fig = px.bar(sp_line_st_bar, x= "City", y= "Purchased_Qty", color="City", title="Channel Situation for SP", text = "Purchased_Qty",)
sp_line_st_bar_fig.update_traces(textposition = 'outside')
sp_line_st_bar_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 390, height = 280)

# C.A.3. Le graphic en Pie pour Channel ST SP
chan_sd_sp_pie = go.Figure(data = [go.Pie(labels = this_month_st_sp["City"], values= this_month_st_sp["Purchased_Qty"], title = "Channel Proportions for SP", opacity=0.5)])
chan_sd_sp_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
chan_sd_sp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 360, height = 300)

# C.A.4. Le graphic en Pie pour City SP
sp_line_sd = this_month_sd_sp.groupby("Cities", as_index= False)["Purchases_Qty"].sum()
citi_sd_sp_pie = go.Figure(data = [go.Pie(labels = sp_line_sd["Cities"], values= sp_line_sd["Purchases_Qty"], title = "Cities Proportions for SD-SP", opacity=0.5)])
citi_sd_sp_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
citi_sd_sp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 360, height = 300)

# C.A.5. Le graphic en bar pour model SP
sp_model_sd_bar = this_month_sd_sp.groupby("Products", as_index= False)["Purchases_Qty"].sum()
sp_model_sd_bar_fig = px.bar(sp_model_sd_bar, x= "Products", y= "Purchases_Qty", color="Products", title="Models Situation for SP", text = "Purchases_Qty",)
sp_model_sd_bar_fig.update_traces(textposition = 'outside')
sp_model_sd_bar_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 800, height = 280)

# C.A.6. Le graphic en Pie pour serie SP
sp_serie_sd = this_month_sd_sp.groupby("SERIES", as_index= False)["Purchases_Qty"].sum()
series_sd_fp_pie = go.Figure(data = [go.Pie(labels = sp_serie_sd["SERIES"], values= sp_serie_sd["Purchases_Qty"], title = "Series Proportions for SP", opacity=0.5)])
series_sd_fp_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
series_sd_fp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 380, height = 280)

# C.A.7. Le graphic en bar pour clients SP
sp_subD_bar = this_month_sd_sp.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
sp_subD_bar_fig = px.bar(sp_subD_bar, x= "Customers_Name", y= "Purchases_Qty", color="Customers_Name", title="Sub-Dealers Situation for SP", text = "Purchases_Qty",)
sp_subD_bar_fig.update_traces(textposition = 'outside')
sp_subD_bar_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 14), font= dict(size= 5), width = 800, height = 380)

# C.B.8. Le graphic en Pie pour clients SP
clients_sd_sp_pie = go.Figure(data = [go.Pie(labels = sp_subD_bar["Customers_Name"], values= sp_subD_bar["Purchases_Qty"], title = "Sub-Dealers Proportions for FP", opacity=0.5)])
clients_sd_sp_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
clients_sd_sp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 380, height = 380)

# C.B. FEAUTRE PHONE
# C.B.1. Graphic line line de ST FP par semaine
fp_line_st = this_month_st_fp.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
fp_line_st_fig = px.line(fp_line_st, x="Weeks", y="Purchased_Qty", text= "Purchased_Qty", title=f"ST-{annee}-{mois} for FEATURE PHONE (Weekly Situation)")
fp_line_st_fig.update_traces(textposition = 'top center')
fp_line_st_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 1180, height = 290)

# C.B.2. Le graphic en bar pour Channel ST FP
fp_line_st_bar = this_month_st_fp.groupby("City", as_index= False)["Purchased_Qty"].sum()
fp_line_st_bar_fig = px.bar(fp_line_st_bar, x= "City", y= "Purchased_Qty", color="City", title="Channel Situation for SP", text = "Purchased_Qty",)
fp_line_st_bar_fig.update_traces(textposition = 'outside')
fp_line_st_bar_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 390, height = 280)

# C.B.3. Le graphic en Pie pour Channel ST FP
chan_sd_fp_pie = go.Figure(data = [go.Pie(labels = this_month_st_fp["City"], values= this_month_st_fp["Purchased_Qty"], title = "Channel Proportions for FP", opacity=0.5)])
chan_sd_fp_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
chan_sd_fp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 300, height = 300)

# C.B.4. Le graphic en Pie pour City FP
fp_line_sd = this_month_sd_fp.groupby("Cities", as_index= False)["Purchases_Qty"].sum()
citi_sd_fp_pie = go.Figure(data = [go.Pie(labels = fp_line_sd["Cities"], values= fp_line_sd["Purchases_Qty"], title = "Cities Proportions for SD-FP", opacity=0.5)])
citi_sd_fp_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
citi_sd_fp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 300, height = 300)

# C.B.5. Le graphic en bar pour model FP
fp_model_sd_bar = this_month_sd_fp.groupby("Products", as_index= False)["Purchases_Qty"].sum()
fp_model_sd_bar_fig = px.bar(fp_model_sd_bar, x= "Products", y= "Purchases_Qty", color="Products", title="Models Situation for FP", text = "Purchases_Qty",)
fp_model_sd_bar_fig.update_traces(textposition = 'outside')
fp_model_sd_bar_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 800, height = 280)

# C.B.6. Le graphic en Pie pour model FP
fp_model_sd_pie_fig = go.Figure(data = [go.Pie(labels = fp_model_sd_bar["Products"], values= fp_model_sd_bar["Purchases_Qty"], title = "Models Proportions for SD-FP", opacity=0.5)])
fp_model_sd_pie_fig.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
fp_model_sd_pie_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', width = 340, height = 300)

# C.B.7. Le graphic en bar pour clients FP
fp_subD_bar = this_month_sd_fp.groupby("Customers_Name", as_index= False)["Purchases_Qty"].sum()
fp_subD_bar_fig = px.bar(fp_subD_bar, x= "Customers_Name", y= "Purchases_Qty", color="Customers_Name", title="Sub-Dealers Situation for FP", text = "Purchases_Qty",)
fp_subD_bar_fig.update_traces(textposition = 'outside')
fp_subD_bar_fig.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 800, height = 280)

# C.B.8. Le graphic en Pie pour clients FP
clients_sd_fp_pie = go.Figure(data = [go.Pie(labels = fp_subD_bar["Customers_Name"], values= fp_subD_bar["Purchases_Qty"], title = "Sub-Dealers Proportions for FP", opacity=0.5)])
clients_sd_fp_pie.update_traces (hoverinfo='percent', textfont_size=15,textinfo= 'percent', pull= [0.05, 0, 0, 0, 0],textposition= 'inside', marker_line=dict(color='#FFFFFF', width=2))
clients_sd_fp_pie.update_layout(margin = dict(l=10, r=10, t=30, b=10), paper_bgcolor = '#F8F9FA', title_font= dict(size= 16), font= dict(size= 8), width = 380, height = 280)


##################################################
##### METRIC #####################################
##################################################
#####################
## A. This Yeras
###############
## Metric ST SP
## 1. Total Achat  pour ST SP annee en cours
achat_st_sp = year_st_sp["Purchased_Qty"].sum()


## 2. Total Investisement  pour ST SP annee en cours
year_st_sp["Investisment"] = year_st_sp["Purchased_Qty"] * year_st_sp["Prices_usd"]
inest_st_sp = year_st_sp["Investisment"].sum()

## 3. Best week  pour ST SP annee en cours
best_st_sp = year_st_sp.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
best_week_st_sp = best_st_sp["Purchased_Qty"].max()

## 4. Bad week  pour ST SP annee en cours
bad_week_st_sp = best_st_sp["Purchased_Qty"].min()

###############
## Metric ST FP

## Comparaison annuelle
# 1. Annee recente
total_annee_st_sp = year_st_sp["Purchased_Qty"].sum()
total_annee_st_fp = year_st_fp["Purchased_Qty"].sum()
total_annee_sd_sp = year_sd_sp["Purchases_Qty"].sum()
total_annee_sd_fp = year_sd_fp["Purchases_Qty"].sum()

# 2. Annee precedente
annee_prec = annee -1
annee_prec_str = str(annee_prec) 
total_annee_old_st_sp = st_data_sp[st_data_sp["Years"] == annee_prec_str]
total_annee_old_st_fp = st_data_fp[st_data_fp["Years"] == annee_prec_str]
total_annee_old_sd_sp = sd_data_sp[sd_data_sp["Years"] == annee_prec_str]
total_annee_old_sd_fp = sd_data_fp[sd_data_fp["Years"] == annee_prec_str]

# Si l'annee n'existe pas
if total_annee_old_st_sp["Purchased_Qty"].sum() == 0 :
    total_annee_old_st_sp["Purchased_Qty"].sum() == 1

elif total_annee_old_st_fp["Purchased_Qty"].sum() == 0 :
    total_annee_old_st_fp["Purchased_Qty"].sum() == 1

elif total_annee_old_sd_sp["Purchases_Qty"].sum() == 0 :
    total_annee_old_sd_sp["Purchases_Qty"].sum() == 1

elif total_annee_old_sd_fp["Purchases_Qty"].sum() == 0 :
    total_annee_old_sd_fp["Purchases_Qty"].sum() == 1

# Calcul du pourcentage d'Evolution
variation_y_st_sp = (
    (total_annee_st_sp / total_annee_old_st_sp["Purchased_Qty"].sum())
) * 100

variation_y_st_fp = (
    (total_annee_st_fp / total_annee_old_st_fp["Purchased_Qty"].sum())
) * 100

variation_y_sd_sp = (
    (total_annee_sd_sp / total_annee_old_sd_sp["Purchases_Qty"].sum())
) * 100

variation_y_sd_fp = (
    (total_annee_sd_fp / total_annee_old_sd_fp["Purchases_Qty"].sum())
) * 100

#############################
## Comparaison mensuel
# 1. Mois recent
total_mois_st_sp = this_month_st_sp["Purchased_Qty"].sum()
total_mois_st_fp = this_month_st_fp["Purchased_Qty"].sum()
total_mois_sd_sp = this_month_sd_sp["Purchases_Qty"].sum()
total_mois_sd_fp = this_month_sd_fp["Purchases_Qty"].sum()

# 2. Mois precedent
mois_prec = mois -1
mois_prec_str = str(mois_prec)
total_mois_old_st_sp = year_st_sp[year_st_sp["Monthly"] == mois_prec]
total_mois_old_st_fp = year_st_fp[year_st_fp["Monthly"] == mois_prec]
total_mois_old_sd_sp = year_sd_sp[year_sd_sp["Monthly"] == mois_prec]
total_mois_old_sd_fp = year_sd_fp[year_sd_fp["Monthly"] == mois_prec]

#"""
# Si le mois n'existe pas
if total_mois_old_st_sp["Purchased_Qty"].sum() == 0 :
    total_mois_old_st_sp["Purchased_Qty"].sum() == 1

elif total_mois_old_st_fp["Purchased_Qty"].sum() == 0 :
    total_mois_old_st_fp["Purchased_Qty"].sum() == 1

elif total_mois_old_sd_sp["Purchases_Qty"].sum() == 0 :
    total_mois_old_sd_sp["Purchases_Qty"].sum() == 1

elif total_mois_old_sd_fp["Purchases_Qty"].sum() == 0 :
    total_mois_old_sd_fp["Purchases_Qty"].sum() == 1

# Calcul du pourcentage d'Evolution
variation_m_st_sp = (
    (total_mois_st_sp / total_mois_old_st_sp["Purchased_Qty"].sum())
) * 100

variation_m_st_fp = (
    (total_mois_st_fp / total_mois_old_st_fp["Purchased_Qty"].sum())
) * 100

variation_m_sd_sp = (
    (total_mois_sd_sp / total_mois_old_sd_sp["Purchases_Qty"].sum())
) * 100

variation_m_sd_fp = (
    (total_mois_sd_fp / total_mois_old_sd_fp["Purchases_Qty"].sum())
) * 100
#"""


########################################################
## 1. Total Achat  pour ST SP annee en cours
achat_st_sp = year_st_sp["Purchased_Qty"].sum()

## 2. Total Investisement  pour ST SP annee en cours
year_st_sp["Investisment"] = year_st_sp["Purchased_Qty"] * year_st_sp["Prices_usd"]
inest_st_sp = year_st_sp["Investisment"].sum()

## 3. Best week  pour ST SP annee en cours
best_st_sp = year_st_sp.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
best_week_st_sp = best_st_sp["Purchased_Qty"].max()

## 4. Bad week  pour ST SP annee en cours
bad_week_st_sp = best_st_sp["Purchased_Qty"].min()

## 5. Total Achat  pour ST FP annee en cours
achat_st_fp = year_st_fp["Purchased_Qty"].sum()

## 6. Total Investisement  pour ST FP annee en cours
year_st_fp["Investisment"] = year_st_fp["Purchased_Qty"] * year_st_fp["Prices_usd"]
inest_st_fp = year_st_fp["Investisment"].sum()

## 7. Best week  pour ST FP annee en cours
best_st_fp = year_st_fp.groupby("Weeks", as_index= False)["Purchased_Qty"].sum()
best_week_st_fp = best_st_fp["Purchased_Qty"].max()

## 8. Bad week  pour ST FP annee en cours
bad_week_st_fp = best_st_fp["Purchased_Qty"].min()

###############################################################
## Metric SD
# 1. Nombre des Sub-dealers pour SP
nbr_sd_sp = year_sd_sp["Customers_Name"].nunique()

# 2. Total Achat SD pour SP
achat_sd_sp = year_sd_sp["Purchases_Qty"].sum()

# 3. Nombre des SD pour FP
nbr_sd_fp = year_sd_fp["Customers_Name"].nunique()

# 4. Total achat SD pour FP
achat_sd_fp = year_sd_fp["Purchases_Qty"].sum()


######################
## Metric This month
month_st_sp_y = year_st_sp[year_st_sp["Monthly"] == mois]
month_st_fp_y = year_st_fp[year_st_fp["Monthly"] == mois]
month_sd_sp_y = year_sd_sp[year_sd_sp["Monthly"] == mois]
month_sd_fp_y = year_sd_fp[year_sd_fp["Monthly"] == mois]

# 1. Total ST SP
achat_st_sp_tt = month_st_sp_y["Purchased_Qty"].sum()
# 2. Total SD SP
achat_sd_sp_tt = month_sd_sp_y["Purchases_Qty"].sum()
# 3. Total SD FP
achat_st_fp_tt = month_st_fp_y["Purchased_Qty"].sum()
# 4. Total SD FP
achat_sd_fp_tt = month_sd_fp_y["Purchases_Qty"].sum()

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

def layout(): # Fonction principale se trouvant dans chaque page lors d'un multipage Dash, elle retourne le layout de la page qui contient les composants Dash à afficher

    return dmc.Container(
        fluid= True, 
        children=[

              
        dmc.Title("DASHBOARD", order= 1, style={"marginTop": 20}), # order = 1, correspond a H1
        html.Hr(),

        # Un espaceur vertical pour aerer (optionnel mais tres propre avec Mantine)
        dmc.Space(h= "xl"),

        #html.Pre(st_data_sp),


        ###############################
        ## YEARLY SITUATION
        ###############################
        dmc.Title("I. YEARLY SITUATION", order= 3, style={"marginBottom": 15}),

        dmc.Grid(
            gutter= "xs", # Remplace className = "g-1"
            styles= {
                "backgroundColor" : "#F8F9FA",
                "borderRadius" : "8px",
                "padding" : "10px",
                "boxShadow": "0px 1px 3px rgba(0, 0, 0, 0.05)" # Optionnel pour embellir
            }, 
            children= [
                # Graphic 1 : ST SP (width = 3 devient span=3)
                dmc.GridCol(
                    span= 3,
                    children= dcc.Graph(figure= st_sp_year_fig, id = "figure ST SP")
                ),

                # Graphic 2
                dmc.GridCol(
                    span = 3,
                    children= dcc.Graph(figure= sd_sp_year_fig, id = "figure SD SP")
                ),

                # Graphic 3
                dmc.GridCol(
                    span = 3,
                    children= dcc.Graph(figure= st_fp_year_fig, id = "figure ST FP")
                ),

                # Graphic 4
                dmc.GridCol(
                    span = 3,
                    children= dcc.Graph(figure= sd_fp_year_fig, id = "figure SD FT")
                ),
            ], style={'backgroundColor': '#F8F9FA', 'borderRadius': '8px', 'padding': '10px', 'boxShadow':'0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'}
        ),

        html.Hr(),

        ###############################
        ## THIS YEARL SITUATION
        ###############################
        html.H3("II. THIS YEARL SITUATION"),

        html.H4("II.1. SELL THROUGH (ST)"),
        html.H5("II.1.1. SELL THROUGH FOR SMART PHONE"),

        dmc.Grid(
            gutter = "md",
            children = [
                # --- Colonne de gauche (Graphic)
                dmc.GridCol(
                    span = 9,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [
                            # 1. Le grand graphique du haut
                            dmc.GridCol(
                                span = 12,
                                children = dmc.Paper(dcc.Graph(figure= monthly_st_sp_fig), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),
                            # 2. Le grand graphique du haut
                            dmc.GridCol(
                                span = 12,
                                children = dmc.Paper(dcc.Graph(figure= weekly_st_sp_fig), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            # 3. Le graphic en bas 
                            dmc.GridCol(
                                span = 7,
                                children = dmc.Paper(dcc.Graph(figure= channel_st_sp_bar), withBorder=True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # 4. Le graphique en bas à droite (ex: Pie)
                            dmc.GridCol(
                                span = 5,
                                children = dmc.Paper(dcc.Graph(figure= channel_st_sp_pie), withBorder=True, p="md", style={**style_boite, "height": "300px"})
                            ),

                        ]
                    )
                ),

                # ---- Colonne de droite Metric ---
                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children = dmc.Stack(
                            gap = "md",
                            children = [
                                # Grille pour aligner plusieurs cartes de manière responsive
                                create_metric_card("Total Purchase ST SP", f"{achat_st_sp} Pcs", f"{variation_y_st_sp}", is_positive= True, icon_name= "fluent:archive-24-regular"),
                                create_metric_card2("Revenue ST-SP", f"{inest_st_sp:.2f} $", is_positive= True, icon_name="fluent:money-24-regular"),
                                create_metric_card2("Best Week ST-SP", f"{best_week_st_sp} Pcs", is_positive= True, icon_name="fluent:storage-24-regular"),
                                create_metric_card2("Bad Week ST-SP", f"{bad_week_st_sp} Pcs", is_positive= True, icon_name="fluent:storage-24-regular"),
                            ]
                        ),
                        withBorder =  True,
                        p= "md",
                        style= {**style_boite, "height": "935px"} # Calculé pour correspondre à la hauteur de gauche + gutter
                    )
                )
            ]
        ),

        # ST FOR FP

        html.H5("II.1.2. SELL THROUGH FOR FEATURE PHONE"),

        dmc.Grid(
            gutter = "md",
            children = [
                # --- Colonne de gauche (Graphic)
                dmc.GridCol(
                    span = 9,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [
                            # 1. Le grand graphique du haut
                            dmc.GridCol(
                                span = 12,
                                children = dmc.Paper(dcc.Graph(figure= monthly_st_fp_fig), withBorder= True, p= "md", style={**style_boite, "height": "300px"})

                            ),

                            # 2. Le grand graphique du haut
                            dmc.GridCol(
                                span = 12,
                                children = dmc.Paper(dcc.Graph(figure= weekly_st_fp_fig), withBorder= True, p= "md", style={**style_boite, "height": "300px"})

                            ),

                            # 3. Le graphic en bas 
                            dmc.GridCol(
                                span = 7,
                                children = dmc.Paper(dcc.Graph(figure= channel_st_fp_bar), withBorder=True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # 4. Le graphique en bas à droite (ex: Pie)
                            dmc.GridCol(
                                span = 5,
                                children = dmc.Paper(dcc.Graph(figure= channel_st_fp_pie), withBorder=True, p="md", style={**style_boite, "height": "300px"})
                            ),

                        ]
                    )
                ),

                # ---- Colonne de droite Metric ---
                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children = dmc.Stack(
                            gap = "md",
                            children = [
                                # Grille pour aligner plusieurs cartes de manière responsive
                                create_metric_card("Total Purchase ST FP", f"{achat_st_fp} Pcs", f"{variation_y_st_fp}", is_positive= True, icon_name= "fluent:archive-24-regular"),
                                create_metric_card2("Revenue ST-FP", f"{inest_st_fp :.2f} $", is_positive= True, icon_name="fluent:money-24-regular"),
                                create_metric_card2("Best Week ST-FP", f"{best_week_st_fp} Pcs", is_positive= True, icon_name="fluent:storage-24-regular"),
                                create_metric_card2("Bad Week ST-FP", f"{bad_week_st_fp} Pcs", is_positive= True, icon_name="fluent:storage-24-regular"),
                            ]
                        ),
                        withBorder =  True,
                        p= "md",
                        style= {**style_boite, "height": "935px"} # Calculé pour correspondre à la hauteur de gauche + gutter
                    )
                )
            ]
        ),

        html.Br(),
        html.Br(),

        # SUB-DEALERS
        html.H4("II.2. SUB-DEALERS"),
        
        dmc.Grid(
            gutter = "md",
            children = [
                # --- Colonne de gauche (Metric)---
                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children = dmc.Stack(
                            gap = "md",
                            children = [
                                # Grille pour aligner plusieurs cartes de manière responsive
                                create_metric_card2("A SD-SP Qty", f"{nbr_sd_sp} A SD", is_positive= True, icon_name= "fluent:person-24-regular"),
                                create_metric_card2("Total Purchase ST-SP", f"{achat_sd_sp} Pcs", is_positive= True, icon_name="fluent:storage-24-regular"),
                                create_metric_card2("A SD-FP Qty", f"{nbr_sd_fp} A SD", is_positive= True, icon_name="fluent:person-24-regular"),
                                create_metric_card2("Total Purchase ST-FP", f"{achat_sd_fp} Pcs", is_positive= True, icon_name="fluent:storage-24-regular"),
                            ]
                        ),
                        withBorder= True,
                        p = "md",
                        style = {**style_boite, "height": "935px"}
                    )
                ),


                # --- Colonne de droite (Graphic)
                dmc.GridCol(
                    span = 9,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [
                            # Le grand graphic du haut
                            dmc.GridCol(
                                span = 12,
                                children = dmc.Paper(dcc.Graph(figure= monthly_sd_sp_fig), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic du millieu
                            dmc.GridCol(
                                span = 8,
                                children = dmc.Paper(dcc.Graph(figure= cities_sd_sp_fig), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic du milieu de pie
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= cities_sd_sp_pie), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            # Le grand graphic du bas pour FP
                            dmc.GridCol(
                                span = 12,
                                children = dmc.Paper(dcc.Graph(figure= monthly_sd_fp_fig ), withBorder= True, p= "md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic bas de line pour SD de FP
                            dmc.GridCol(
                                span = 8,
                                children = dmc.Paper(dcc.Graph(figure= cities_sd_fp_fig), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic bas de pie pour SD de FP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= cities_sd_fp_pie), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),
                        ]
                    )
                )
            ]
        ),

        html.Hr(),

        ###############################
        ## THIS MONTH SITUATION
        ###############################
        html.H3("III. THIS MONTH SITUATION"),

        ####################
        ### SMART PHONE
        #######
        #dmc.Title("III.1. SMART PHONE", order = 4, style={"marginBottom": 15}),
        dmc.Grid(
            gutter = "md",
            children = [
                # Metric pour ST SP
                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children = dmc.Stack(
                            gap = "md",
                            children = [
                                # Grille pour aligner plusieurs cartes de manière responsive
                                create_metric_card4("Total Purchase ST-SP", f"{achat_st_sp_tt} Pcs", is_positive= True, icon_name= "fluent:storage-24-regular"),
                            ]
                        ), 
                        withBorder= True, p="md", style={**style_boite, "height": "100px"})
                ),

                # Metric pour SD SP
                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children = dmc.Stack(
                            gap = "md",
                            children = [
                                # Grille pour aligner plusieurs cartes de manière responsive
                                create_metric_card4("Total Purchase SD-SP", f"{achat_sd_sp_tt} Pcs", is_positive= True, icon_name="fluent:storage-24-regular"),
                            ]
                        ), 
                        withBorder= True, p="md", style={**style_boite, "height": "100px"})
                ),

                # Metric pour ST FP
                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children = dmc.Stack(
                            gap = "md",
                            children = [
                                # Grille pour aligner plusieurs cartes de manière responsive
                                create_metric_card4("Total Purchase ST-FP", f"{achat_st_fp_tt} Pcs", is_positive= True, icon_name="fluent:storage-24-regular"),
                            ]
                        ), 
                        withBorder= True, p="md", style={**style_boite, "height": "100px"})
                ),

                # Metric pour SD FP
                dmc.GridCol(
                    span = 3,
                    children = dmc.Paper(
                        children = dmc.Stack(
                            gap = "md",
                            children = [
                                # Grille pour aligner plusieurs cartes de manière responsive
                                create_metric_card4("Total Purchase SD-FP", f"{achat_sd_fp_tt} Pcs", is_positive= True, icon_name="fluent:storage-24-regular"),
                            ]
                        ), 
                        withBorder= True, p="md", style={**style_boite, "height": "100px"})
                ),

                dmc.Title("III.1. SMART PHONE", order = 4, style={"marginBottom": 15}),

                # Graphic line line de ST SP par semaine
                dmc.GridCol(
                    span = 12,
                    children= dmc.Paper(dcc.Graph(figure= sp_line_st_fig), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                ),

                dmc.GridCol(
                    span = 12,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [
                            # Le graphic en bar pour ST SP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= sp_line_st_bar_fig), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en Pie pour ST SP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= chan_sd_sp_pie), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en Pie pour City SP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= citi_sd_sp_pie), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en bar pour models SP
                            dmc.GridCol(
                                span = 8,
                                children = dmc.Paper(dcc.Graph(figure= sp_model_sd_bar_fig), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en Pie pour serie SP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= series_sd_fp_pie), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en Pie pour clients SP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= clients_sd_sp_pie), withBorder= True, p="md", style={**style_boite, "height": "400px"})
                            ),

                            # Le graphic en bar pour clients SP
                            dmc.GridCol(
                                span = 8,
                                children = dmc.Paper(dcc.Graph(figure= sp_subD_bar_fig), withBorder= True, p="md", style={**style_boite, "height": "400px"})
                            )

                        ]
                    )
                )
            ]

        ),


        ####################
        ### FEATURE PHONE
        #######
        html.Br(),
        html.Br(),
        dmc.Title("III.2. FEATURE PHONE", order = 4, style={"marginBottom": 15}),

        dmc.Grid(
            gutter = "md",
            children = [

                # Graphic line line de ST FP par semaine
                dmc.GridCol(
                    span = 12,
                    children= dmc.Paper(dcc.Graph(figure= fp_line_st_fig), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                ),

                dmc.GridCol(
                    span = 12,
                    children = dmc.Grid(
                        gutter = "md",
                        children = [
                            # Le graphic en bar pour ST FP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= fp_line_st_bar_fig), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en Pie pour ST FP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= chan_sd_fp_pie), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en Pie pour City FP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= citi_sd_fp_pie ), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en bar pour models FP
                            dmc.GridCol(
                                span = 8,
                                children = dmc.Paper(dcc.Graph(figure= fp_model_sd_bar_fig), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en Pie pour model FP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= fp_model_sd_pie_fig), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en Pie pour clients FP
                            dmc.GridCol(
                                span = 4,
                                children = dmc.Paper(dcc.Graph(figure= clients_sd_fp_pie), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            ),

                            # Le graphic en bar pour clients FP
                            dmc.GridCol(
                                span = 8,
                                children = dmc.Paper(dcc.Graph(figure= fp_subD_bar_fig), withBorder= True, p="md", style={**style_boite, "height": "300px"})
                            )
                        ]
                    )
                )
            ]
        ),
        html.Hr(),

        #html.Pre(f"Type de la colonne Monthly : {achat_st_sp_tt}"),
        #html.Pre(f"Le resultat est : {variation_m_sd_fp}, old : {total_mois_old_sd_fp["Purchases_Qty"].sum()}, recent : {total_mois_sd_fp}"),

        #dash_table.DataTable(
            #data = month_st_sp_y.to_dict("records"),
            #columns=[
                #{"name": c, "id" : c} for c in month_st_sp_y.columns
            #], page_size= 10
            
        #)
        
    ]
)

