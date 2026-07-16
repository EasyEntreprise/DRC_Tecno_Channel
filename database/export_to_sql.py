# Dans un fichier nommé 'insertion_helpers.py' ou directement dans ton app.py
import pandas as pd
from database.connectDB import engine
from sqlalchemy import text
from datetime import datetime



################################
## TECNO SUB-DEALERS FP DATA
################################

def insert_sd_fp_data():
    try:
        # Lecture du fichier Excel
        df_excel_sd_fp = pd.read_excel("data/Tecno_FP_SD_dataset.xlsx")

        # Lecture de la table SQL
        try:
            df_sql_sd_fp = pd.read_sql(
                text("SELECT Id FROM SD_tecno_FP_data"),
                con=engine
            )
        except:
            # Si la table n'existe pas
            df_excel_sd_fp.to_sql(
                "SD_tecno_FP_data",
                con=engine,
                if_exists="replace",
                index=False
            )
            print("Table créée.")
            exit()

        # Colonnes à mettre à jour (toutes sauf Id)
        colonnes = [c for c in df_excel_sd_fp.columns if c != "Id"]

        with engine.begin() as conn:

            for _, row in df_excel_sd_fp.iterrows():

                ids_sql = set(df_sql_sd_fp["Id"])

                if row["Id"] in ids_sql:

                    # Construction automatique du SET
                    set_clause = ", ".join(
                        [f"{col}=:{col}" for col in colonnes]
                    )

                    sql_sd_fp = text(f"""
                        UPDATE SD_tecno_FP_data
                        SET {set_clause}
                        WHERE Id=:Id
                    """)

                    params = row.to_dict()

                    #if pd.notna(params["Date"]):
                        #params["Date"] = params["Date"].strftime("%Y-%m-%d")

                    if "Date" in params and pd.notna(params["Date"]):
                        # Si c'est déjà un Timestamp ou un datetime
                        if isinstance(params["Date"], (pd.Timestamp, datetime)):
                            params["Date"] = params["Date"].strftime("%Y-%m-%d")
                        
                        else:
                            # Si c'est une chaîne venant d'Excel
                            params["Date"] = pd.to_datetime(params["Date"]).strftime("%Y-%m-%d")


                    conn.execute(sql_sd_fp, params)

                else:

                    pd.DataFrame([row]).to_sql(
                        "SD_tecno_FP_data",
                        con=conn,
                        if_exists="append",
                        index=False
                    )

        return True

    except Exception as e:
        return f"Erreur lors de l'insertion : {str(e)}"
        # Si la table n'existe pas encore, on prend tout le fichier Excel



################################
## TECNO SUB-DEALERS SP DATA
################################
def insert_sd_sp_data():

    try:
        # Lecture du fichier Excel
        df_excel_sd_sp = pd.read_excel("data/Tecno_SP_SD_dataset.xlsx")

        #df_excel["Date"] = pd.to_datetime(df_excel["Date"]).dt.strftime("%Y-%m-%d")

        # Lecture de la table SQL
        try:
            df_sql_sd_sp = pd.read_sql(
                text("SELECT Id FROM SD_tecno_SP_data"),
                con=engine
            )
        except:
            # Si la table n'existe pas
            df_excel_sd_sp.to_sql(
                "SD_tecno_SP_data",
                con=engine,
                if_exists="replace",
                index=False
            )
            print("Table créée.")
            exit()

        # Colonnes à mettre à jour (toutes sauf Id)
        colonnes = [c for c in df_excel_sd_sp.columns if c != "Id"]

        with engine.begin() as conn:

            for _, row in df_excel_sd_sp.iterrows():

                ids_sql_sd_sp = set(df_sql_sd_sp["Id"])

                if row["Id"] in ids_sql_sd_sp:

                    # Construction automatique du SET
                    set_clause = ", ".join(
                        [f"{col}=:{col}" for col in colonnes]
                    )

                    sql_sd_sp = text(f"""
                        UPDATE SD_tecno_SP_data
                        SET {set_clause}
                        WHERE Id=:Id
                    """)

                    params = row.to_dict()

                    #if pd.notna(params["Date"]):
                        #params["Date"] = params["Date"].strftime("%Y-%m-%d")

                    if "Date" in params and pd.notna(params["Date"]):
                        # Si c'est déjà un Timestamp ou un datetime
                        if isinstance(params["Date"], (pd.Timestamp, datetime)):
                            params["Date"] = params["Date"].strftime("%Y-%m-%d")
                        
                        else:
                            # Si c'est une chaîne venant d'Excel
                            params["Date"] = pd.to_datetime(params["Date"]).strftime("%Y-%m-%d")

                    conn.execute(sql_sd_sp, params)

                else:

                    pd.DataFrame([row]).to_sql(
                        "SD_tecno_SP_data",
                        con=conn,
                        if_exists="append",
                        index=False
                    )

        return True

    except Exception as e:
        return f"Erreur lors de l'insertion : {str(e)}"


####################################
## TECNO SELL THROUGH FP DATA
###################################
def insert_st_fp_data():
    try:
        # Lecture du fichier Excel
        df_excel = pd.read_excel("data/Tecno_FP_ST_dataset.xlsx")

        # Lecture de la table SQL
        try:
            df_sql = pd.read_sql(
                text("SELECT Id FROM ST_tecno_FP_data"),
                con=engine
            )
        except:
            # Si la table n'existe pas
            df_excel.to_sql(
                "ST_tecno_FP_data",
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
                        UPDATE ST_tecno_FP_data
                        SET {set_clause}
                        WHERE Id=:Id
                    """)

                    params = row.to_dict()
        
                    #if pd.notna(params["Date"]):
                        #params["Date"] = params["Date"].strftime("%Y-%m-%d")

                    if "Date" in params and pd.notna(params["Date"]):
                        # Si c'est déjà un Timestamp ou un datetime
                        if isinstance(params["Date"], (pd.Timestamp, datetime)):
                            params["Date"] = params["Date"].strftime("%Y-%m-%d")
                        
                        else:
                            # Si c'est une chaîne venant d'Excel
                            params["Date"] = pd.to_datetime(params["Date"]).strftime("%Y-%m-%d")

                    if "Months" in params and pd.notna(params["Months"]):
                        params["Months"] = params["Months"].strftime("%Y-%m-%d")

                    conn.execute(sql, params)

                else:

                    pd.DataFrame([row]).to_sql(
                        "ST_tecno_FP_data",
                        con=conn,
                        if_exists="append",
                        index=False
                    )

        return True

        print("Synchronization complete !")
    except Exception as e:
        return f"Erreur lors de l'insertion : {str(e)}"


####################################
## TECNO SELL THROUGH SP DATA
###################################
def insert_st_sp_data():


    try:
        # Lecture du fichier Excel
        df_excel_st_sp = pd.read_excel("data/Tecno_SP_ST_dataset.xlsx")

        # Lecture de la table SQL
        try:
            df_sql_st_sp = pd.read_sql(
                text("SELECT Id FROM ST_tecno_SP_data"),
                con=engine
            )
        except:
            # Si la table n'existe pas
            df_excel_st_sp.to_sql(
                "ST_tecno_SP_data",
                con=engine,
                if_exists="replace",
                index=False
            )
            print("Table créée.")
            exit()

        # Colonnes à mettre à jour (toutes sauf Id)
        colonnes = [c for c in df_excel_st_sp.columns if c != "Id"]

        with engine.begin() as conn:

            for _, row in df_excel_st_sp.iterrows():

                ids_sql_st_sp = set(df_sql_st_sp["Id"])

                if row["Id"] in ids_sql_st_sp:

                    # Construction automatique du SET
                    set_clause = ", ".join(
                        [f"{col}=:{col}" for col in colonnes]
                    )

                    sql_st_sp = text(f"""
                        UPDATE ST_tecno_SP_data
                        SET {set_clause}
                        WHERE Id=:Id
                    """)

                    params = row.to_dict()

                    #if pd.notna(params["Date"]):
                        #params["Date"] = params["Date"].strftime("%Y-%m-%d")

                    if "Date" in params and pd.notna(params["Date"]):
                        # Si c'est déjà un Timestamp ou un datetime
                        if isinstance(params["Date"], (pd.Timestamp, datetime)):
                            params["Date"] = params["Date"].strftime("%Y-%m-%d")
                        
                        else:
                            # Si c'est une chaîne venant d'Excel
                            params["Date"] = pd.to_datetime(params["Date"]).strftime("%Y-%m-%d")

                    if pd.notna(params["Months"]):
                        params["Months"] = params["Months"].strftime("%Y-%m-%d")

                    conn.execute(sql_st_sp, params)

                else:

                    pd.DataFrame([row]).to_sql(
                        "ST_tecno_SP_data",
                        con=conn,
                        if_exists="append",
                        index=False
                    )
        return True
    
    except Exception as e:
        return f"Erreur lors de l'insertion : {str(e)}"