from passlib.hash import pbkdf2_sha256
import sqlite3

from config import *


class User:

    def __init__(self, id, nombre, contrasena):
        self.id = id
        self.nombre = nombre
        self.contrasena = contrasena

    def verificarContrasena(self, contrasena, contrasena_encriptada):
        verificacion = pbkdf2_sha256.verify(
            contrasena, contrasena_encriptada)

        return verificacion


class DBManager:
    """
    Clase para interactuar con la base de datos SQLite
    """
    CAMPOS = '''id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                fecha TEXT NO NULL,
                hora TEXT NOT NULL,
                origen TEXT NOT NULL,
                invertido NUMERIC NOT NULL,
                destino TEXT NOT NULL,
                obtenido NUMERIC NOT NULL,
                unitario NUMERIC NOT NULL'''

    def __init__(self, ruta):
        self.ruta = ruta

    def comprobarUsuario(self, user):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        peticion = f"SELECT * FROM usuarios WHERE usuario = '{user.nombre}'"

        cursor.execute(peticion)
        result = cursor.fetchone()

        if result != None:
            contrasena_encriptada = result[2]
            contrasena = user.contrasena
            verificacion = User.verificarContrasena(
                0, contrasena, contrasena_encriptada)
            usuario = User(result[0], result[1], verificacion)
            return usuario

        else:
            return None

    def crearTabla(self, usuario):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        peticion = f'''CREATE TABLE {usuario} ({self.CAMPOS})'''
        cursor.execute(peticion)
        conexion.commit()
        conexion.close()

    def guardarDatos(self, tabla, datos):
        campos = ', '.join(datos.keys())
        valores = ', '.join(['?'] * len(datos))
        consulta = f"INSERT INTO {tabla} ({campos}) VALUES ({valores})"
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute(consulta, list(datos.values()))
            conexion.commit()
            conexion.close()
            return True

        except Exception as ex:
            print("Error al guardar los datos: ", ex)
            return False

    def consultaSQL(self, consulta, page=1, per_page=5):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        # Calcular el número de elementos para saltar (OFFSET)
        offset = (page - 1) * per_page

        # Agregar la cláusula LIMIT y OFFSET a la consulta SQL
        consulta_paginada = consulta + " LIMIT ? OFFSET ?"
        parametros = (per_page, offset)

        cursor.execute(consulta_paginada, parametros)
        datos = cursor.fetchall()

        activos = []
        nombres_columna = []
        for columna in cursor.description:
            nombres_columna.append(columna[0])

        for dato in datos:
            indice = 0
            activo = {}
            for nombre in nombres_columna:
                activo[nombre] = dato[indice]
                indice += 1

            activos.append(activo)

        conexion.close()

        return activos
