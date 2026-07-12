"""
Supprimer une table de la base des donnees
"""
from connectDB import engine
from create_table_users import Users

Users.__table__.drop(engine, checkfirst = True)