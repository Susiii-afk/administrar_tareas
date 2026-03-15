# administrar_tareas
Administrar tareas 

# API REST de Gestión de Tareas Personales

## Descripción

Este proyecto consiste en desarrollar una **API REST** para administrar tareas personales utilizando **Flask** y una base de datos **SQLite**.

La API permite realizar operaciones **CRUD** (Crear, Leer, Actualizar y Eliminar) sobre tareas.

Cada tarea contiene la siguiente información:

* **titulo**
* **descripcion**
* **estado** (por ejemplo: pendiente, en progreso o completada)

---

# Endpoints de la API

| Método | Endpoint     | Descripción                    |
| ------ | ------------ | ------------------------------ |
| POST   | /tareas      | Crear una nueva tarea          |
| GET    | /tareas      | Obtener todas las tareas       |
| PUT    | /tareas/<id> | Actualizar una tarea existente |
| DELETE | /tareas/<id> | Eliminar una tarea             |

---

# Estructura del Proyecto

```
administrar_tareas/
│
├── app.py
├── tareas.db
└── README.md
```

---

# Código de la API (app.py)

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "tareas.db"


# Crear tabla si no existe
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        estado TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# POST /tareas (Crear tarea)
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    data = request.get_json()

    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    estado = data.get("estado")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tareas (titulo, descripcion, estado) VALUES (?, ?, ?)",
        (titulo, descripcion, estado)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Tarea creada correctamente"}), 201


# GET /tareas (Consultar tareas)
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    conn = get_db_connection()
    tareas = conn.execute("SELECT * FROM tareas").fetchall()
    conn.close()

    lista = []

    for tarea in tareas:
        lista.append({
            "id": tarea["id"],
            "titulo": tarea["titulo"],
            "descripcion": tarea["descripcion"],
            "estado": tarea["estado"]
        })

    return jsonify(lista)


# PUT /tareas/<id> (Actualizar tarea)
@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    data = request.get_json()

    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
    estado = data.get("estado")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tareas SET titulo=?, descripcion=?, estado=? WHERE id=?",
        (titulo, descripcion, estado, id)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Tarea actualizada correctamente"})


# DELETE /tareas/<id> (Eliminar tarea)
@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tareas WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Tarea eliminada correctamente"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
```

---

# Ejecutar la API

Desde la terminal ejecutar:

```
python app.py
```

El servidor iniciará en:

```
http://127.0.0.1:5000
```

---

# Ejemplos de uso

## Crear tarea

POST `/tareas`

Body JSON:

```json
{
  "titulo": "Hacer tarea de programación",
  "descripcion": "Terminar la API REST de Flask",
  "estado": "pendiente"
}
```

---

## Consultar tareas

GET `/tareas`

Respuesta:

```json
[
  {
    "id": 1,
    "titulo": "Hacer tarea de programación",
    "descripcion": "Terminar la API REST de Flask",
    "estado": "pendiente"
  }
]
```

---

## Actualizar tarea

PUT `/tareas/1`

```json
{
  "titulo": "Hacer tarea de programación",
  "descripcion": "Terminar práctica de APIs",
  "estado": "completada"
}
```

---

## Eliminar tarea

DELETE `/tareas/1`

Respuesta:

```json
{
  "mensaje": "Tarea eliminada correctamente"
}
```

---

# Objetivos de aprendizaje

Con este ejercicio el estudiante aprende a:

* Crear una **API REST**
* Implementar un **CRUD completo**
* Conectar una API con una base de datos
* Manipular datos con **JSON**
* Usar diferentes métodos HTTP (POST, GET, PUT y DELETE)
* Comprender la estructura básica de un servicio REST
