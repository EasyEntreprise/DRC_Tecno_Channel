# IMPORTATION
import pandas as pd
from database.connectDB import engine

# Upload des databases
df_st_sp = pd.read_sql_table("ST_tecno_SP_data", con= engine)
df_st_fp = pd.read_sql_table("ST_tecno_FP_data", con= engine)
df_sd_sp = pd.read_sql_table("ST_tecno_SP_data", con= engine)
df_sd_sp = pd.read_sql_table("SD_tecno_SP_data", con= engine)
df_sd_fp = pd.read_sql_table("SD_tecno_FP_data", con= engine)

# Traitement des valeurs manquantes
st_data_sp = df_st_sp.dropna(subset="Purchased_Qty")
st_data_fp = df_st_fp.dropna(subset="Purchased_Qty")
sd_data_sp = df_sd_sp.dropna(subset="Purchases_Qty")
sd_data_fp = df_sd_fp.dropna(subset="Purchases_Qty")
