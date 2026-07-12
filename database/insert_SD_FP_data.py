"""
Dans ce script, nous allons insérer les données du fichier Excel "Tecno_FP_SD_dataset.xlsx" dans la table SQL "SD_tecno_FP_data". Nous allons d'abord lire les données du fichier Excel, puis vérifier quelles lignes sont nouvelles par rapport à ce qui existe déjà dans la base de données. Enfin, nous allons insérer uniquement les nouvelles lignes pour éviter les doublons.
"""

import pandas as pd
from sqlalchemy import text
from connectDB import engine

# Lecture du fichier Excel
df_excel = pd.read_excel("data/Tecno_FP_SD_dataset.xlsx")

#df_excel["Date"] = pd.to_datetime(df_excel["Date"]).dt.strftime("%Y-%m-%d")
#df_excel["Months"] = pd.to_datetime(df_excel["Months"]).dt.strftime("%Y-%m-%d")

# Lecture de la table SQL
try:
    df_sql = pd.read_sql(
        text("SELECT Id FROM SD_tecno_FP_data"),
        con=engine
    )
except:
    # Si la table n'existe pas
    df_excel.to_sql(
        "SD_tecno_FP_data",
        con=engine,
        if_exists="replace",
        index=False
    )
    print("Table créée.")
    exit()

# Colonnes à mettre à jour (toutes sauf Id)
colonnes = [c for c in df_excel.columns if c != "Id"]

with engine.begin() as conn:

    for _, row in df_excel.iterrows():

        ids_sql = set(df_sql["Id"])

        if row["Id"] in ids_sql:

            # Construction automatique du SET
            set_clause = ", ".join(
                [f"{col}=:{col}" for col in colonnes]
            )

            sql = text(f"""
                UPDATE SD_tecno_FP_data
                SET {set_clause}
                WHERE Id=:Id
            """)

            params = row.to_dict()

            if pd.notna(params["Date"]):
                params["Date"] = params["Date"].strftime("%Y-%m-%d")

            conn.execute(sql, params)

        else:

            pd.DataFrame([row]).to_sql(
                "SD_tecno_FP_data",
                con=conn,
                if_exists="append",
                index=False
            )

print("Synchronization complete !")
