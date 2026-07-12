import pandas as pd
from sqlalchemy import text
from connectDB import engine

# Lecture du fichier Excel
df_excel = pd.read_excel("data/Tecno_SP_SD_dataset.xlsx")

#df_excel["Date"] = pd.to_datetime(df_excel["Date"]).dt.strftime("%Y-%m-%d")

# Lecture de la table SQL
try:
    df_sql = pd.read_sql(
        text("SELECT Id FROM SD_tecno_SP_data"),
        con=engine
    )
except:
    # Si la table n'existe pas
    df_excel.to_sql(
        "SD_tecno_SP_data",
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
                UPDATE SD_tecno_SP_data
                SET {set_clause}
                WHERE Id=:Id
            """)

            params = row.to_dict()

            if pd.notna(params["Date"]):
                params["Date"] = params["Date"].strftime("%Y-%m-%d")

            conn.execute(sql, params)

        else:

            pd.DataFrame([row]).to_sql(
                "SD_tecno_SP_data",
                con=conn,
                if_exists="append",
                index=False
            )

print("Synchronization complete.")
