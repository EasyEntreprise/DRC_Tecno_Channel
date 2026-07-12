from sqlalchemy import create_engine, text
import pandas as pd

# Connexion à la base SQLite
engine = create_engine("sqlite:///data/tecno_database.db")

# Lecture du fichier Excel
df = pd.read_excel("data/Tecno Business Shops.xlsx")

with engine.begin() as conn:

    for _, row in df.iterrows():

        conn.execute(
            text("""
                INSERT INTO tecno_Shops_data (
                    Id,
                    Country,
                    Shops_Name,
                    Shops_Id,
                    Region,
                    Market,
                    Shop_Type,
                    Regional_Managers,
                    Supervisors_Name,
                    Models,
                    Sales_Qty,
                    SP_FP,
                    Months,
                    Years

                )
                VALUES (
                    :Id,
                    :Country,
                    :Shops_Name,
                    :Shops_Id,
                    :Region,
                    :Market,
                    :Shop_Type,
                    :Regional_Managers,
                    :Supervisors_Name,
                    :Models,
                    :Sales_Qty,
                    :SP_FP,
                    :Months,
                    :Years

                )

                ON CONFLICT(Id)
                DO UPDATE SET
                    Country = excluded.Country,
                    Shops_Name = excluded.Shops_Name,
                    Shops_Id = excluded.Shops_Id,
                    Region = excluded.Region,
                    Market = excluded.Market,
                    Shop_Type = excluded.Shop_Type,
                    Regional_Managers = excluded.Regional_Managers,
                    Supervisors_Name = excluded.Supervisors_Name,
                    Models = excluded.Models,
                    Sales_Qty = excluded.Sales_Qty,
                    SP_FP = excluded.SP_FP,
                    Months = excluded.Months,
                    Years = excluded.Years
                 
                )
                                     
            """),
            row.to_dict()
        )


print("Update executed successfully !")