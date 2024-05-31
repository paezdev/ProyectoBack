from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional

# URL de la base de datos
DATABASE_URL = "mysql+pymysql://root:Z32pp23z1124@localhost/NotaProDB"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# SessionLocal para la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base para las clases de modelo
Base = declarative_base()

# Función para obtener una instancia de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



