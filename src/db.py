# --- Fichero de configuracion de Data Base ---

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

base_dir = Path(__file__).resolve().parent  # Obtiene la ruta absoluta del script actual
db_path = base_dir / "database" / "main.db"  # Construye la ruta absoluta al archivo DB

engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
