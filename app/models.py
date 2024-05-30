from sqlalchemy import Column, Integer, Float, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional
from app.database import Base  # Utilizando la Base definida en app.database
from sqlalchemy.orm import relationship
from .database import Base


# Autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relación con Estudiante
    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    
    # Relación con Docente
    docente = relationship("Docente", back_populates="usuario")
    
    # Relación con Acudiente
    acudiente = relationship("Acudiente", back_populates="usuario")


# Docente
class Docente(Base):
    __tablename__ = "docente"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)

    usuario = relationship("Usuario", back_populates="docente")


class Materia(Base):
    __tablename__ = "materias"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    grado_academico = Column(String(50), nullable=False)
    
    notas = relationship("Nota", back_populates="materia")


class Nota(Base):
    __tablename__ = "notas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), nullable=False)
    materia_id = Column(Integer, ForeignKey('materias.id'), nullable=False)
    valor = Column(Float, nullable=False)
    fecha_asignacion = Column(Date, nullable=False)

    estudiante = relationship("Estudiante", back_populates="notas")
    materia = relationship("Materia", back_populates="notas")

#Estudiantes
class Estudiante(Base):
    __tablename__ = "estudiantes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    grado_academico = Column(String(50), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False, unique=True)
    acudiente_id = Column(Integer, ForeignKey('acudiente.id'))  # Clave foránea para relacionarse con Acudiente

    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="estudiante")
    acudiente = relationship("Acudiente", back_populates="estudiantes")
    notas = relationship("Nota", back_populates="estudiante")



#Acudiente
class Acudiente(Base):
    __tablename__ = "acudiente"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)

    usuario = relationship("Usuario", back_populates="acudiente")
    estudiantes = relationship("Estudiante", back_populates="acudiente")


