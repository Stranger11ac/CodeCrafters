from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import mysql.connector
from mysql.connector import Error

from pydantic import BaseModel
from datetime import date

# --- Configurar API ---
app = FastAPI()

# --- Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelo de datos ---
class movieStructure(BaseModel):
    Nombre: str
    Director: str
    Duracion: str
    Genero: str
    FechaLanzamiento: date
    ClasificacionId: int

class levelStructure(BaseModel):
    ClasificacionDesc: str

# --- Conexión a MySQL ---
def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="L0c4lP$SS",
            database="codecrafters",
            port=3306
        )
        if connection.is_connected():
            print("✅ Conexión exitosa a MySQL")
            return connection
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None

get_connection()

@app.post("/insert_movie")
def insert_movie(structure: movieStructure):
    conn = get_connection()
    if conn is None:
        # Devuelve realmente HTTP 500
        return JSONResponse(status_code=500, content={"error": "No se pudo conectar a la base de datos"})

    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        INSERT INTO peliculas (Nombre, Director, Duracion, Genero, FechaLanzamiento, ClasificacionId)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (structure.Nombre, structure.Director, structure.Duracion, structure.Genero, structure.FechaLanzamiento, structure.ClasificacionId))
        conn.commit()
        return JSONResponse(status_code=201, content={"mensaje": "Película registrada correctamente"})
    except Error as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.post("/registrar_clasificaciones")
def insert_level(structure: levelStructure):
    conn = get_connection()
    if conn is None:
        return JSONResponse(status_code=500, content={"error": "No se pudo conectar a la base de datos"})

    cursor = conn.cursor(dictionary=True)

    try:
        query = "INSERT INTO clasificaciones (ClasificacionDesc) VALUES (%s)"
        cursor.execute(query, (structure.ClasificacionDesc,))
        conn.commit()
        return JSONResponse(status_code=201, content={"mensaje": "Clasificación registrada correctamente"})
    except Error as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.get("/get_movies/")
def get_movies():
    conn = get_connection()
    if conn is None:
        return {"status":400, "error": "No se pudo conectar a la base de datos"}

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM peliculas ORDER BY PeliculaId DESC;")
        rows = cursor.fetchall()
        return {"status":200, "data": rows}
    except Exception as e:
        return {"status":400, "error": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.get("/obtener_clasificaciones/")
def get_level():
    conn = get_connection()
    if conn is None:
        return {"status":400, "error": "No se pudo conectar a la base de datos"}

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM clasificaciones ORDER BY ClasificacionId DESC;")
        rows = cursor.fetchall()
        return {"status":200, "data": rows}
    except Exception as e:
        return {"status":400, "error": str(e)}
    finally:
        cursor.close()
        conn.close()


# Para ejecutar la API...
# Dentro de la carpeta donde esta api_local.py
# uvicorn api_local:app --reload --host localhost --port 8220

# Ejecuta por modulo (-m)
# python -m uvicorn api_local:app --reload --host localhost --port 8220
