from connectDB import engine

# Création automatique du fichier SQLite
conn = engine.connect()

print("Database file created successfully !")