from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from . import crud, database, models, schemas, auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import requests

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
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
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/users/", response_model=schemas.User)
def create_user(user_create: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user_create.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
   #hashed_password = auth.get_password_hash(user_create.hashed_password)  # Corregir el acceso al atributo
    # Crear un nuevo objeto UserCreate con el atributo hashed_password actualizado
    #new_user_create = schemas.UserCreate(username=user_create.username, hashed_password=hashed_password)
    # Pasar el objeto UserCreate actualizado al crear usuario
    #return crud.create_user(db=db, user=new_user_create)
    return crud.create_user(db=db, user=user_create)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/get-token/")
async def get_access_token(username: str = Body(...), password: str = Body(...)):
    token_url = "http://localhost:8000/token"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return {"access_token": response.json()["access_token"]}
    else:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener el token de acceso")




# Rutas CRUD para Materias
@app.post("/materias/", response_model=schemas.Materia)
def create_materia(materia: schemas.MateriaCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    return crud.create_materia(db=db, materia=materia)

@app.get("/materias/{materia_id}", response_model=schemas.Materia)
def read_materia(materia_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    db_materia = crud.get_materia(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=404, detail=f"Materia con ID {materia_id} no encontrada")
    return db_materia

@app.put("/materias/{materia_id}", response_model=schemas.Materia)
def update_materia(materia_id: int, materia: schemas.MateriaCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    db_materia = crud.get_materia(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=404, detail=f"Materia con ID {materia_id} no encontrada")
    return crud.update_materia(db=db, materia_id=materia_id, materia=materia)

@app.delete("/materias/{materia_id}")
def delete_materia(materia_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    db_materia = crud.get_materia(db, materia_id=materia_id)
    if db_materia is None:
        raise HTTPException(status_code=404, detail=f"Materia con ID {materia_id} no encontrada")
    crud.delete_materia(db=db, materia_id=materia_id)
    return {"message": f"Materia con ID {materia_id} eliminada exitosamente"}

# Rutas CRUD para Notas
@app.post("/notas/", response_model=schemas.Nota)
def create_nota(nota: schemas.NotaCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    return crud.create_nota(db=db, nota=nota)

@app.get("/notas/{nota_id}", response_model=schemas.Nota)
def read_nota(nota_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    db_nota = crud.get_nota(db, nota_id=nota_id)
    if db_nota is None:
        raise HTTPException(status_code=404, detail=f"Nota con ID {nota_id} no encontrada")
    return db_nota

@app.get("/notas/estudiante/{estudiante_id}", response_model=List[schemas.Nota])
def read_notas_by_estudiante(estudiante_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    return crud.get_notas_by_estudiante(db, estudiante_id=estudiante_id)

@app.put("/notas/{nota_id}", response_model=schemas.Nota)
def update_nota(nota_id: int, nota: schemas.NotaCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    db_nota = crud.get_nota(db, nota_id=nota_id)
    if db_nota is None:
        raise HTTPException(status_code=404, detail=f"Nota con ID {nota_id} no encontrada")
    return crud.update_nota(db=db, nota_id=nota_id, nota=nota)

@app.delete("/notas/{nota_id}")
def delete_nota(nota_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    db_nota = crud.get_nota(db, nota_id=nota_id)
    if db_nota is None:
        raise HTTPException(status_code=404, detail=f"Nota con ID {nota_id} no encontrada")
    crud.delete_nota(db=db, nota_id=nota_id)
    return {"message": f"Nota con ID {nota_id} eliminada exitosamente"}

# Rutas CRUD para Estudiantes
@app.post("/estudiantes/", response_model=schemas.Estudiante)
def create_estudiante(estudiante: schemas.EstudianteCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    return crud.create_estudiante(db=db, estudiante=estudiante)

@app.get("/estudiantes/{estudiante_id}", response_model=schemas.Estudiante)
def read_estudiante(estudiante_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    db_estudiante = crud.get_estudiante(db, estudiante_id=estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID {estudiante_id} no encontrado")
    return db_estudiante

@app.get("/estudiantes/", response_model=List[schemas.Estudiante])
def read_estudiantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    return crud.get_estudiantes(db, skip=skip, limit=limit)

@app.put("/estudiantes/{estudiante_id}", response_model=schemas.Estudiante)
def update_estudiante(estudiante_id: int, estudiante: schemas.EstudianteCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    db_estudiante = crud.get_estudiante(db, estudiante_id=estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID {estudiante_id} no encontrado")
    return crud.update_estudiante(db=db, estudiante_id=estudiante_id, estudiante=estudiante)

@app.delete("/estudiantes/{estudiante_id}")
def delete_estudiante(estudiante_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(auth.get_current_user)):
    db_estudiante = crud.get_estudiante(db, estudiante_id=estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID {estudiante_id} no encontrado")
    crud.delete_estudiante(db=db, estudiante_id=estudiante_id)
    return {"message": f"Estudiante con ID {estudiante_id} eliminado exitosamente"}
