import configparser
from settings import Base, ENGINE
from sqlalchemy import create_engine, MetaData
from create_db import create_tables

config = configparser.ConfigParser()
config.read("config.ini")
config_root = config["admin"]
password = config_root["password"]
engine = create_engine(f"postgresql+psycopg2://admin:{password}@localhost/epic_events")

def drop_all_tables():
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(engine)
    print("Toutes les tables de la base de données ont été supprimées avec succès.")

if __name__ == "__main__":
    confirmation = input("Êtes-vous sûr de vouloir supprimer toutes les tables de la base de données ? (oui/non): ")
    if confirmation.lower() == "oui":
        drop_all_tables()
        create_tables()
    else:
        print("Opération annulée.")
