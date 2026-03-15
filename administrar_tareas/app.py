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


# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Endpoint POST /tareas
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    data = request.get_json()

    titulo = data.get('titulo')
    descripcion = data.get('descripcion')
    estado = data.get('estado')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tareas (titulo, descripcion, estado) VALUES (?, ?, ?)",
        (titulo, descripcion, estado)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "mensaje": "Tarea creada correctamente"
    }), 201


# Endpoint GET /tareas
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    conn = get_db_connection()
    tareas = conn.execute("SELECT * FROM tareas").fetchall()
    conn.close()

    lista_tareas = []

    for tarea in tareas:
        lista_tareas.append({
            "id": tarea["id"],
            "titulo": tarea["titulo"],
            "descripcion": tarea["descripcion"],
            "estado": tarea["estado"]
        })

    return jsonify(lista_tareas)


# Endpoint PUT /tareas/<id>
@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    data = request.get_json()

    titulo = data.get('titulo')
    descripcion = data.get('descripcion')
    estado = data.get('estado')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tareas SET titulo=?, descripcion=?, estado=? WHERE id=?",
        (titulo, descripcion, estado, id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "mensaje": "Tarea actualizada correctamente"
    })


# Endpoint DELETE /tareas/<id>
@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tareas WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "mensaje": "Tarea eliminada correctamente"
    })


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
