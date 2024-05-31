from sqlalchemy.orm import Session
from . import models, schemas

def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        hashed_password=user.password,  # Asegúrate de hashar el password antes de guardarlo
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_materia(db: Session, materia: schemas.MateriaCreate):
    db_materia = models.Materia(
        nombre=materia.nombre,
        descripcion=materia.descripcion
    )
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia

def get_materia(db: Session, materia_id: int):
    return db.query(models.Materia).filter(models.Materia.id == materia_id).first()

def update_materia(db: Session, materia_id: int, materia: schemas.MateriaCreate):
    db_materia = get_materia(db, materia_id)
    if db_materia:
        db_materia.nombre = materia.nombre
        db_materia.descripcion = materia.descripcion
        db.commit()
        db.refresh(db_materia)
    return db_materia

def delete_materia(db: Session, materia_id: int):
    db_materia = get_materia(db, materia_id)
    if db_materia:
        db.delete(db_materia)
        db.commit()

def create_nota(db: Session, nota: schemas.NotaCreate):
    db_nota = models.Nota(
        estudiante_id=nota.estudiante_id,
        materia_id=nota.materia_id,
        calificacion=nota.calificacion
    )
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota

def get_nota(db: Session, nota_id: int):
    return db.query(models.Nota).filter(models.Nota.id == nota_id).first()

def get_notas_by_estudiante(db: Session, estudiante_id: int):
    return db.query(models.Nota).filter(models.Nota.estudiante_id == estudiante_id).all()
