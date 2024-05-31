from pydantic import BaseModel
from typing import List, Optional

# Esquema para Role
class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True  # Reemplaza orm_mode

# Esquema para User
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role_id: int

class User(UserBase):
    id: int
    is_active: bool
    role: Role

    class Config:
        from_attributes = True  # Reemplaza orm_mode

# Esquema para Materia
class MateriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class MateriaCreate(MateriaBase):
    pass

class Materia(MateriaBase):
    id: int

    class Config:
        from_attributes = True  # Reemplaza orm_mode

# Esquema para Nota
class NotaBase(BaseModel):
    estudiante_id: int
    materia_id: int
    calificacion: int

class NotaCreate(NotaBase):
    pass

class Nota(NotaBase):
    id: int
    estudiante: User
    materia: Materia

    class Config:
        from_attributes = True  # Reemplaza orm_mode

# Esquema para Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
