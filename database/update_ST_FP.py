from sqlalchemy import create_engine, text
import pandas as pd

# Connexion à la base SQLite
engine = create_engine("sqlite:///data/tecno_database.db")

# Lecture du fichier Excel
df = pd.read_excel("data/Tecno_FP_ST_dataset.xlsx")

with engine.begin() as conn:

    for _, row in df.iterrows():

        conn.execute(
            text("""
                INSERT INTO ST_tecno_FP_data (
                    Id,
                    City,
                    Products,
                    Weeks,
                    Date,
                    Months,
                    Years,
                    Purchased_Qty,
                    Prices_usd,
                    B_Price_usd,
                    R_Price_usd,
                    A_B_Profit_usd,
                    A_R_Profit_usd,
                    B_R_Profit_usd

                )
                VALUES (
                    :Id,
                    :City,
                    :Products,
                    :Weeks,
                    :Date,
                    :Months,
                    :Years,
                    :Purchased_Qty,
                    :Prices_usd,
                    :B_Price_usd,
                    :R_Price_usd,
                    :A_B_Profit_usd,
                    :A_R_Profit_usd,
                    :B_R_Profit_usd

                )

                ON CONFLICT(Id)
                DO UPDATE SET
                    City = excluded.City,
                    Products = excluded.Products,
                    Weeks = excluded.Weeks,
                    Date = excluded.Date,
                    Months = excluded.Months,
                    Years = excluded.Years,
                    Purchased_Qty = excluded.Purchased_Qty,
                    Prices_usd = excluded.Prices_usd,
                    B_Price_usd = excluded.B_Price_usd,
                    R_Price_usd = excluded.R_Price_usd,
                    A_B_Profit_usd = excluded.A_B_Profit_usd,
                    A_R_Profit_usd = excluded.A_R_Profit_usd,
                    B_R_Profit_usd = excluded.B_R_Profit_usd
            """),
            row.to_dict()
        )


print("Update executed successfully !")