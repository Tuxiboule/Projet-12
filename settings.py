import configparser
import typing
import enum
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, Enum


config = configparser.ConfigParser()
config.read("config.ini")
config_root = config["admin"]
password = config_root["password"]
config_jwt = config["jwt"]
SECRET = config_jwt["secret"]
ALGORITHME = config_jwt["algorithme"]
config_sentry = config["sentry"]
DSN = config_sentry["dsn"]

# utilisateur admin est un compte mysql avec une limitation des privilèges :
# accès uniquement à la BD epic_events
# Le paramètre echo=True indique que le SQL émis par les connexions sera affiché sur la sortie standard.
ENGINE = create_engine(
    f"postgresql+psycopg2://admin:{password}@localhost/epic_events",
    echo=False
)
Session = sessionmaker(bind=ENGINE)
SESSION = Session()


class Base(DeclarativeBase):
    type_annotation_map = {
        enum.Enum: Enum(enum.Enum),
        typing.Literal: Enum(enum.Enum),
    }
