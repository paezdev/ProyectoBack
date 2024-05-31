from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)  # Añade longitud a VARCHAR

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # Añade longitud a VARCHAR
    hashed_password = Column(String(255))  # Añade longitud a VARCHAR
    role_id = Column(Integer, ForeignKey('roles.id'))
    is_active = Column(Boolean, default=True)

    role = relationship("Role", back_populates="users")

class Materia(Base):
    __tablename__ = 'materias'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, index=True)  # Añade longitud a VARCHAR
    descripcion = Column(String(255), nullable=True)  # Añade longitud a VARCHAR

class Nota(Base):
    __tablename__ = 'notas'
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey('users.id'))
    materia_id = Column(Integer, ForeignKey('materias.id'))
    calificacion = Column(Integer)

    estudiante = relationship("User")
    materia = relationship("Materia")

