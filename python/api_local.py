from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime, timedelta
from mysql.connector import Error
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import hashlib
import jwt
from settings import settings

# --- Configuración general ---
app = FastAPI()
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 120

# --- Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos de datos ---
class movieStructure(BaseModel):
    Nombre: str
    Director: str
    Duracion: str
    Genero: str
    FechaLanzamiento: date
    ClasificacionId: int

class levelStructure(BaseModel):
    ClasificacionDesc: str

class LoginRequest(BaseModel):
    username: str
    password: str

# --- Conexión a MySQL ---
def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=settings.db_user,
            password=settings.db_pass,
            database="codecrafters",
            port=3306
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None

# --- Función para crear token ---
def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# --- Validar token ---
def verify_token(Authorization: Optional[str] = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    token = Authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# --- Endpoint de login ---
@app.post("/login")
def login(credentials: LoginRequest):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión con la base de datos")

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (credentials.username,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        hashed_password = hashlib.sha256(credentials.password.encode()).hexdigest()
        if hashed_password != user["password"]:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        token = create_token(credentials.username)
        return {"access_token": token, "token_type": "Bearer", "expires_in": TOKEN_EXPIRE_MINUTES * 60}
    finally:
        cursor.close()
        conn.close()

# --- Endpoints protegidos ---
@app.post("/insert_movie")
def insert_movie(structure: movieStructure, username: str = Depends(verify_token)):
    conn = get_connection()
    if conn is None:
        return JSONResponse(status_code=500, content={"error": "No se pudo conectar a la base de datos"})

    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        INSERT INTO peliculas (Nombre, Director, Duracion, Genero, FechaLanzamiento, ClasificacionId)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            structure.Nombre, structure.Director, structure.Duracion,
            structure.Genero, structure.FechaLanzamiento, structure.ClasificacionId
        ))
        conn.commit()
        return JSONResponse(status_code=201, content={"mensaje": "Película registrada correctamente"})
    except Error as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.post("/registrar_clasificaciones")
def insert_level(structure: levelStructure, username: str = Depends(verify_token)):
    conn = get_connection()
    if conn is None:
        return JSONResponse(status_code=500, content={"error": "No se pudo conectar a la base de datos"})

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO clasificaciones (ClasificacionDesc) VALUES (%s)", (structure.ClasificacionDesc,))
        conn.commit()
        return JSONResponse(status_code=201, content={"mensaje": "Clasificación registrada correctamente"})
    except Error as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    finally:
        cursor.close()
        conn.close()


@app.get("/get_movies/")
def get_movies(username: str = Depends(verify_token)):
    conn = get_connection()
    if conn is None:
        return {"status": 400, "error": "No se pudo conectar a la base de datos"}

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM peliculas ORDER BY PeliculaId DESC;")
        rows = cursor.fetchall()
        return {"status": 200, "data": rows}
    except Exception as e:
        return {"status": 400, "error": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.get("/obtener_clasificaciones/")
def get_level(username: str = Depends(verify_token)):
    conn = get_connection()
    if conn is None:
        return {"status": 400, "error": "No se pudo conectar a la base de datos"}

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM clasificaciones ORDER BY ClasificacionId DESC;")
        rows = cursor.fetchall()
        return {"status": 200, "data": rows}
    except Exception as e:
        return {"status": 400, "error": str(e)}
    finally:
        cursor.close()
        conn.close()

