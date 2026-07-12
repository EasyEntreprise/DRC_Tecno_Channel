from sqlalchemy import create_engine, text
import pandas as pd

# Connexion à la base SQLite
engine = create_engine("sqlite:///data/tecno_database.db")

# Lecture du fichier Excel
df = pd.read_excel("data/Tecno_SP_ST_dataset.xlsx")

with engine.begin() as conn:

    for _, row in df.iterrows():

        conn.execute(
            text("""
                INSERT INTO ST_tecno_SP_data (
                    Id,
                    City,
                    Products,
                    Categories,
                    SERIES,
                    Weeks,
                    Date,
                    Months,
                    Years,
                    Purchased_Qty,
                    Prices_usd

                )
                VALUES (
                    :Id,
                    :City,
                    :Products,
                    :Categories,
                    :SERIES,
                    :Weeks,
                    :Date,
                    :Months,
                    :Years,
                    :Purchased_Qty,
                    :Prices_usd

                )

                ON CONFLICT(Id)
                DO UPDATE SET
                    City = excluded.City,
                    Products = excluded.Products,
                    Categories = excluded.Categories,
                    SERIES = excluded.SERIES,
                    Weeks = excluded.Weeks,
                    Date = excluded.Date,
                    Months = excluded.Months,
                    Years = excluded.Years,
                    Purchased_Qty = excluded.Purchased_Qty,
                    Prices_usd = excluded.Prices_usd
                )
                                     
            """),
            row.to_dict()
        )


print("Update executed successfully !")