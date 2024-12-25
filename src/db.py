# --- Fichero de configuracion de Data Base ---

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Creamos el motor para gestionar la conexion del DB
engine = create_engine('sqlite:///database/main.db', connect_args={'check_same_thread': False}) # TODO Separar las bases de datos. Login - Productos

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()