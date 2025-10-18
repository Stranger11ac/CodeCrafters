from settings import settings
import mysql.connector
import hashlib

# Datos del nuevo usuario
username = input("Nombre de usuario: ").strip()
password = input("Contraseña: ").strip()

# Hashear la contraseña (SHA256)
hashed_password = hashlib.sha256(password.encode()).hexdigest()

# Conexión a la BD
conn = mysql.connector.connect(
    host="localhost",
    user=settings.db_user,
    password=settings.db_pass,
    database="codecrafters",
    port=3306
)

cursor = conn.cursor()

# Insertar usuario
query = "INSERT INTO users (username, password) VALUES (%s, %s)"
cursor.execute(query, (username, hashed_password))
conn.commit()

print("✅ Usuario registrado correctamente con hash SHA256")
cursor.close()
conn.close()
