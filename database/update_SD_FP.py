from sqlalchemy import create_engine, text
import pandas as pd

# Connexion à la base SQLite
engine = create_engine("sqlite:///data/tecno_database.db")

# Lecture du fichier Excel
df = pd.read_excel("data/Tecno_FP_SD_dataset.xlsx")

with engine.begin() as conn:

    for _, row in df.iterrows():

        conn.execute(
            text("""
                INSERT INTO SD_tecno_FP_data (
                    Id,
                    Country,
                    Cities,
                    Customers_Name,
                    Market,
                    Products,
                    Purchases_Qty,
                    Prices_usd,
                    Investments_usd,
                    Date,
                    Months,
                    Years
                )
                VALUES (
                    :Id,
                    :Country,
                    :Cities,
                    :Customers_Name,
                    :Market,
                    :Products,
                    :Purchases_Qty,
                    :Prices_usd,
                    :Investments_usd,
                    :Date,
                    :Months,
                    :Years
                )

                ON CONFLICT(Id)
                DO UPDATE SET
                    Country = excluded.Country,
                    Cities = excluded.Cities,
                    Customers_Name = excluded.Customers_Name,
                    Market = excluded.Market,
                    Products = excluded.Products,
                    Purchases_Qty = excluded.Purchases_Qty,
                    Prices_usd = excluded.Prices_usd,
                    Investments_usd = excluded.Investments_usd,
                    Date = excluded.Date,
                    Months = excluded.Months,
                    Years = excluded.Years
            """),
            row.to_dict()
        )


print("Update executed successfully !")