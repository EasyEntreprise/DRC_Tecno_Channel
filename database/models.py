"""

"""
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. Configuration de la classe de base

class Base(DeclarativeBase):
    pass

# 2. Definition de la table Users
class Utilisateurs(Base):
    __tablename__ = "Users"

    Id       : Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement= True)
    Username : Mapped[str] = mapped_column(String, nullable= False)
    Password : Mapped[str] = mapped_column(String, nullable= False)
    Role     : Mapped[str] = mapped_column(String, nullable= False)


# 3. Definition de la table ST_tecno_SP_data
class STTecnoSPData(Base):
    __tablename__ = "ST_tecno_SP_data"

    Id            : Mapped[int]   = mapped_column(Integer, primary_key= True)
    City          : Mapped[str]   = mapped_column(String, nullable= False)
    Products      : Mapped[str]   = mapped_column(String, nullable= False)
    Categories    : Mapped[str]   = mapped_column(String, nullable= False) 
    SERIES        : Mapped[str]   = mapped_column(String, nullable= False)
    Weeks         : Mapped[str]   = mapped_column(String, nullable= False)
    Date          : Mapped[str]   = mapped_column(String, nullable= False)
    Months        : Mapped[str]   = mapped_column(String, nullable= False)
    Years         : Mapped[str]   = mapped_column(String, nullable= False)
    Purchased_Qty : Mapped[int]   = mapped_column(Integer, nullable= True)
    Prices_usd    : Mapped[float] = mapped_column(Float, nullable= True)

# 4. Definition de la table ST_tecno_FP_data
class STTecnoFPData(Base):
    __tablename__ = "ST_tecno_FP_data"

    Id             : Mapped[int]   = mapped_column(Integer, primary_key= True)
    City           : Mapped[str]   = mapped_column(String, nullable= False)
    Products       : Mapped[str]   = mapped_column(String, nullable= False)
    Weeks          : Mapped[str]   = mapped_column(String, nullable= False)
    Date           : Mapped[str]   = mapped_column(String, nullable= False)
    Months         : Mapped[str]   = mapped_column(String, nullable= False)
    Years          : Mapped[str]   = mapped_column(String, nullable= False)
    Purchased_Qty  : Mapped[int]   = mapped_column(Integer, nullable= True)
    Prices_usd     : Mapped[float] = mapped_column(Float, nullable= True)
    B_Price_usd    : Mapped[float] = mapped_column(Float, nullable= True)
    R_Price_usd    : Mapped[float] = mapped_column(Float, nullable= True)
    A_B_Profit_usd : Mapped[float] = mapped_column(Float, nullable= True)
    A_R_Profit_usd : Mapped[float] = mapped_column(Float, nullable= True) 
    B_R_Profit_usd : Mapped[float] = mapped_column(Float, nullable= True)

# 5. Definition de la table SD_tecno_SP_data
class SDTecnoSPData(Base):
    __tablename__ = "SD_tecno_SP_data"

    Id               : Mapped[int]   = mapped_column(Integer, primary_key= True)
    Country          : Mapped[str]   = mapped_column(String, nullable= False) 
    Cities           : Mapped[str]   = mapped_column(String, nullable= False) 
    Customers_Name   : Mapped[str]   = mapped_column(String, nullable= False)
    Market           : Mapped[str]   = mapped_column(String, nullable= False)
    Products         : Mapped[str]   = mapped_column(String, nullable= False)
    Categories       : Mapped[str]   = mapped_column(String, nullable= False) 
    SERIES           : Mapped[str]   = mapped_column(String, nullable= False)
    Purchases_Qty    : Mapped[int]   = mapped_column(Integer, nullable= True)
    Prices_usd       : Mapped[float] = mapped_column(Float, nullable= True)
    Investments_usd  : Mapped[float] = mapped_column(Float, nullable= True)
    Date             : Mapped[str]   = mapped_column(String, nullable= False)
    Months           : Mapped[str]   = mapped_column(String, nullable= False)
    Years            : Mapped[str]   = mapped_column(String, nullable= False)

# 6. Definition de la table SD_tecno_FP_data
class SDTecnoFPData(Base):
    __tablename__ = "SD_tecno_FP_data"

    Id              : Mapped[int] = mapped_column(Integer, primary_key= True)
    Country         : Mapped[str] = mapped_column(String, nullable= False)
    Cities          : Mapped[str] = mapped_column(String, nullable= False)
    Customers_Name  : Mapped[str] = mapped_column(String, nullable= False)
    Market          : Mapped[str] = mapped_column(String, nullable= False)
    Products        : Mapped[str] = mapped_column(String, nullable= False)
    Purchases_Qty   : Mapped[int] = mapped_column(Integer, nullable= True)
    Prices_usd      : Mapped[float] = mapped_column(Float, nullable= True)
    Investments_usd : Mapped[float] = mapped_column(Float, nullable= True)
    Date            : Mapped[str] = mapped_column(String, nullable= False) 
    Months          : Mapped[str] = mapped_column(String, nullable= False)
    Years           : Mapped[str] = mapped_column(String, nullable= False)


# --- EXECUTION / CREATION DES TABLES ---

# Remplacez l'URL par celle de votre base de donnees 
engine = create_engine("sqlite:///data/tecno_database.db", echo = True)

# Cette ligne remplace la "CREATE TABLE IF NOT EXISTS" pour toutes les tables difinies ci-dessus
Base.metadata.create_all(engine)