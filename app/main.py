from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from . import crud, database, models, schemas, auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8000/docs",  # Agrega la URL de Swagger UI
    "http://localhost:8000/redoc",  # Agrega la URL de Redoc
    # Agrega aquí las URLs que necesites permitir
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la base de datos
models.Base.metadata.create_all(bind=database.engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuración de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/users/", response_model=schemas.User)
def create_user(user_create: schemas.UserCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.verify_admin_or_administrador)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    db_user = crud.get_user_by_username(db, username=user_create.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(user_create.password)
    new_user_create = schemas.UserCreate(username=user_create.username, password=hashed_password, role_id=user_create.role_id)
    return crud.create_user(db=db, user=new_user_create)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, expire = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expire.strftime('%Y-%m-%d %H:%M:%S')
    }

# Rutas CRUD para Materias
@app.post("/materias/", response_model=schemas.Materia)
def create_materia(materia: schemas.MateriaCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.verify_admin_or_administrador)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return crud.create_materia(db=db, materia=materia)

@app.get("/materias/{materia_id}", response_model=schemas.Materia)
def read_materia(materia_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    db_materia = crud.get_materia(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Materia no encontrada")
    return db_materia

@app.put("/materias/{materia_id}", response_model=schemas.Materia)
def update_materia(materia_id: int, materia: schemas.MateriaCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.verify_admin_or_administrador)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    db_materia = crud.get_materia(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Materia no encontrada")
    return crud.update_materia(db=db, materia_id=materia_id, materia=materia)

@app.delete("/materias/{materia_id}")
def delete_materia(materia_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.verify_admin_or_administrador)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    db_materia = crud.get_materia(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Materia no encontrada")
    crud.delete_materia(db=db, materia_id=materia_id)
    return {"message": "Materia eliminada exitosamente"}

@app.post("/notas/", response_model=schemas.Nota)
def create_nota(nota: schemas.NotaCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.verify_docente)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return crud.create_nota(db=db, nota=nota)

@app.get("/notas/{nota_id}", response_model=schemas.Nota)
def read_nota(nota_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    db_nota = crud.get_nota(db, nota_id=nota_id)
    if db_nota is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada")
    return db_nota

@app.get("/notas/estudiante/{estudiante_id}", response_model=List[schemas.Nota])
def read_notas_estudiante(estudiante_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return crud.get_notas_by_estudiante(db, estudiante_id=estudiante_id)

# Crear un enrutador para las rutas de administrador
admin_router = APIRouter()

# Definir el endpoint para crear un usuario administrador
@admin_router.post("/create-admin")
def create_admin(username: str, password: str, db: Session = Depends(get_db)):
    # Verificar si ya existe un usuario administrador
    admin_user = db.query(models.User).join(models.Role).filter(models.Role.name == "admin").first()
    if admin_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario administrador ya existe.")

    # Crear el rol de administrador si no existe
    admin_role = db.query(models.Role).filter(models.Role.name == "admin").first()
    if not admin_role:
        admin_role = models.Role(name="admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    # Crear el usuario administrador
    admin_user = models.User(
        username=username,
        hashed_password=auth.get_password_hash(password),
        role_id=admin_role.id,
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    # Eliminar la ruta después de su uso
    remove_create_admin_route()

    return {"message": "Usuario administrador creado con éxito."}

def remove_create_admin_route():
    app.router.routes = [route for route in app.router.routes if route.path != "/create-admin"]

# Incluir el enrutador de administrador en la aplicación principal
app.include_router(admin_router)

# Añadir esto al final de tu main.py
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    roles = ["administrador", "estudiante", "docente", "acudiente"]
    for role_name in roles:
        role = crud.get_role_by_name(db, name=role_name)
        if role is None:
            role = schemas.RoleCreate(name=role_name)
            crud.create_role(db, role)

    # Verificar si ya existe un usuario administrador
    admin_user = db.query(models.User).join(models.Role).filter(models.Role.name == "admin").first()
    if admin_user:
        # Eliminar la ruta create-admin si el administrador ya existe
        remove_create_admin_route()
