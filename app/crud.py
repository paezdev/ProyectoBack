from . import models, schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from . import models, schemas, auth
from .database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_username(db: Session, username: str):
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.hashed_password)
    print(f"Creating user {user.username} with hashed password {hashed_password}")
    db_user = models.Usuario(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Usuarios
@router.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# Materias
def create_materia(db: Session, materia: schemas.MateriaCreate):
    db_materia = models.Materia(**materia.dict())
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia

def get_materia(db: Session, materia_id: int):
    return db.query(models.Materia).filter(models.Materia.id == materia_id).first()

def update_materia(db: Session, materia_id: int, materia: schemas.MateriaCreate):
    db_materia = db.query(models.Materia).filter(models.Materia.id == materia_id).first()
    if db_materia:
        for key, value in materia.dict().items():
            setattr(db_materia, key, value)
        db.commit()
        db.refresh(db_materia)
    return db_materia

def delete_materia(db: Session, materia_id: int):
    db_materia = db.query(models.Materia).filter(models.Materia.id == materia_id).first()
    if db_materia:
        db.delete(db_materia)
        db.commit()
    return db_materia


# Notas
def create_nota(db: Session, nota: schemas.NotaCreate):
    db_nota = models.Nota(**nota.dict())
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota

def get_nota(db: Session, nota_id: int):
    return db.query(models.Nota).filter(models.Nota.id == nota_id).first()

def get_notas_by_estudiante(db: Session, estudiante_id: int):
    return db.query(models.Nota).filter(models.Nota.estudiante_id == estudiante_id).all()

def update_nota(db: Session, nota_id: int, nota: schemas.NotaCreate):
    db_nota = db.query(models.Nota).filter(models.Nota.id == nota_id).first()
    if db_nota:
        for key, value in nota.dict().items():
            setattr(db_nota, key, value)
        db.commit()
        db.refresh(db_nota)
    return db_nota

def delete_nota(db: Session, nota_id: int):
    db_nota = db.query(models.Nota).filter(models.Nota.id == nota_id).first()
    if db_nota:
        db.delete(db_nota)
        db.commit()
    return db_nota

# Estudiantes
def create_estudiante(db: Session, estudiante: schemas.EstudianteCreate):
    db_estudiante = models.Estudiante(**estudiante.dict())
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante

def get_estudiante(db: Session, estudiante_id: int):
    return db.query(models.Estudiante).filter(models.Estudiante.id == estudiante_id).first()

def get_estudiantes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Estudiante).offset(skip).limit(limit).all()

def update_estudiante(db: Session, estudiante_id: int, estudiante: schemas.EstudianteCreate):
    db_estudiante = db.query(models.Estudiante).filter(models.Estudiante.id == estudiante_id).first()
    if db_estudiante:
        for key, value in estudiante.dict().items():
            setattr(db_estudiante, key, value)
        db.commit()
        db.refresh(db_estudiante)
    return db_estudiante

def delete_estudiante(db: Session, estudiante_id: int):
    db_estudiante = db.query(models.Estudiante).filter(models.Estudiante.id == estudiante_id).first()
    if db_estudiante:
        db.delete(db_estudiante)
        db.commit()
    return db_estudiante

# Docente
def create_docente(db: Session, docente: schemas.DocenteCreate):
    db_docente = models.Docente(**docente.dict())
    db.add(db_docente)
    db.commit()
    db.refresh(db_docente)
    return db_docente

def get_docente(db: Session, docente_id: int):
    return db.query(models.Docente).filter(models.Docente.id == docente_id).first()

def update_docente(db: Session, docente_id: int, docente: schemas.DocenteCreate):
    db_docente = db.query(models.Docente).filter(models.Docente.id == docente_id).first()
    if db_docente:
        for key, value in docente.dict().items():
            setattr(db_docente, key, value)
        db.commit()
        db.refresh(db_docente)
    return db_docente

def delete_docente(db: Session, docente_id: int):
    db_docente = db.query(models.Docente).filter(models.Docente.id == docente_id).first()
    if db_docente:
        db.delete(db_docente)
        db.commit()
    return db_docente

# Acudiente
def create_acudiente(db: Session, acudiente: schemas.AcudienteCreate):
    db_acudiente = models.Acudiente(**acudiente.dict())
    db.add(db_acudiente)
    db.commit()
    db.refresh(db_acudiente)
    return db_acudiente

def get_acudiente(db: Session, acudiente_id: int):
    return db.query(models.Acudiente).filter(models.Acudiente.id == acudiente_id).first()

def update_acudiente(db: Session, acudiente_id: int, acudiente: schemas.AcudienteCreate):
    db_acudiente = db.query(models.Acudiente).filter(models.Acudiente.id == acudiente_id).first()
    if db_acudiente:
        for key, value in acudiente.dict().items():
            setattr(db_acudiente, key, value)
        db.commit()
        db.refresh(db_acudiente)
    return db_acudiente

def delete_acudiente(db: Session, acudiente_id: int):
    db_acudiente = db.query(models.Acudiente).filter(models.Acudiente.id == acudiente_id).first()
    if db_acudiente:
        db.delete(db_acudiente)
        db.commit()
    return db_acudiente


