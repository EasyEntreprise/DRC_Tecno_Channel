from sqlalchemy import text
from connectDB import engine

with engine.connect() as conn:

    # Creation table ST_tecno_SP_data

    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS ST_tecno_SP_data(
            Id INTEGER PRIMARY KEY,
            City TEXT NOT NULL,
            Products TEXT NOT NULL,
            Categories TEXT NOT NULL,
            SERIES TEXT NOT NULL,
            Weeks TEXT NOT NULL,
            Date TEXT NOT NULL,
            Months TEXT NOT NULL,
            Years TEXT NOT NULL,
            Purchased_Qty INTEGER,
            Prices_usd REAL
        )
    """
    ))

    # Creation table ST_tecno_FP_data
    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS ST_tecno_FP_data(
            Id INTEGER PRIMARY KEY,
            City TEXT NOT NULL,
            Products TEXT NOT NULL,
            Weeks TEXT NOT NULL,
            Date TEXT NOT NULL,
            Months TEXT NOT NULL,
            Years TEXT NOT NULL,
            Purchased_Qty INTEGER,
            Prices_usd REAL,
            B_Price_usd REAL,
            R_Price_usd REAL,
            A_B_Profit_usd REAL,
            A_R_Profit_usd REAL,
            B_R_Profit_usd REAL
            )
        """))

    # Creation table ST_tecno_FP_data
    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS SD_tecno_SP_data(
            Id INTEGER PRIMARY KEY,
            Country TEXT NOT NULL,
            Cities TEXT NOT NULL,
            Customers_Name TEXT NOT NULL,
            Market TEXT,
            Products TEXT NOT NULL,
            Categories TEXT NOT NULL,
            SERIES TEXT NOT NULL,
            Purchases_Qty INTEGER,
            Prices_usd REAL NULL,
            Investments_usd REAL,
            Date TEXT NOT NULL,
            Months TEXT NOT NULL,
            Years TEXT NOT NULL
        )
        """))
    
    # Creation table SD_tecno_FP_data
    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS SD_tecno_FP_data(
            Id INTEGER PRIMARY KEY,
            Country TEXT NOT NULL,
            Cities TEXT NOT NULL,
            Customers_Name TEXT NOT NULL,
            Market TEXT,
            Products TEXT NOT NULL,
            Purchases_Qty INTEGER,
            Prices_usd REAL,
            Investments_usd REAL,
            Date TEXT NOT NULL,
            Months TEXT NOT NULL,
            Years TEXT NOT NULL
        )
        """))
    
    # Creation table tecno_Shops_data
    conn.execute(text(
        """
        CREATE TABLE IF NOT EXISTS tecno_Shops_data(
            Id INTEGER PRIMARY KEY,
            Country TEXT NOT NULL,
            Shops_Name TEXT NOT NULL,
            Shop_Id TEXT NOT NULL,
            Region TEXT,
            Market TEXT,
            Shop_Type TEXT NOT NULL,
            Regional_Manager TEXT NOT NULL,
            Supervisor_Name TEXT NOT NULL,
            Models TEXT NOT NULL,
            Sales_Qty INTEGER,
            SP_FP TEXT NOT NULL,
            Months TEXT NOT NULL,
            Years TEXT NOT NULL
            
        )
        """))
    conn.commit()

print("Tables created successfully !")