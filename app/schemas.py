from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

# Autenticación
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: str  # Añadir el campo expires_in

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    hashed_password: str  # Cambiar 'password' por 'hashed_password'

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class LoginForm(BaseModel):
    username: str
    password: str



# Materia
class MateriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class MateriaCreate(MateriaBase):
    pass

class Materia(MateriaBase):
    id: int

    class Config:
        orm_mode = True

# Notas
class NotaBase(BaseModel):
    estudiante_id: int
    materia_id: int
    valor: float
    fecha_asignacion: date

class NotaCreate(NotaBase):
    pass

class Nota(NotaBase):
    id: int

    class Config:
        orm_mode = True


# Estudiantes
class EstudianteBase(BaseModel):
    nombre: str
    grado_academico: str
    usuario_id: int
    acudiente_id: Optional[int] = None

class EstudianteCreate(EstudianteBase):
    pass

class Estudiante(EstudianteBase):
    id: int

    class Config:
        orm_mode = True


# Docente
class DocenteBase(BaseModel):
    nombre: str

class DocenteCreate(DocenteBase):
    usuario_id: int

class Docente(DocenteBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True

# Acudientes
class AcudienteBase(BaseModel):
    nombre: str

class AcudienteCreate(AcudienteBase):
    usuario_id: int

class Acudiente(AcudienteBase):
    id: int
    usuario_id: int

    class Config:
        orm_mode = True

# AcudientesEstudiantes
class AcudienteEstudianteBase(BaseModel):
    acudiente_id: int
    estudiante_id: int

class AcudienteEstudianteCreate(AcudienteEstudianteBase):
    pass

class AcudienteEstudiante(AcudienteEstudianteBase):
    id: int

    class Config:
        orm_mode = True

# Definición de Usuario
class UsuarioBase(BaseModel):
    username: str
    hashed_password: str  # Cambiar 'password' por 'hashed_password'

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
