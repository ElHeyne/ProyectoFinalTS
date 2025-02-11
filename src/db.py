# --- Fichero de configuracion de Data Base ---

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database/main.db', connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
