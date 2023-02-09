import os
import sqlite3
from sqlite3 import Error
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Création du fichier de BDD
db_file = r"Projet_IOT.db"

def init_database(connection):
    cursor = connection.cursor()
    cursor.execute(
    "CREATE TABLE Projet_IOT.Meteo (id INT(100) AUTO INCREMENT PRIMARY KEY NOT NULL,hour varchar(100),day varchar(100) NOT NULL,pressure INT(100) NOT NULL,temperature INT(100) NOT NULL,humidity INT(100) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
    connection.commit()


def create_connection():
    connection = None
    new = False
    if not os.path.isfile(db_file):
        new = True
    try:
        connection = sqlite3.connect(db_file, check_same_thread=False)
    except Error as e:
        print(e)
    finally:
        if connection:
            if new:
                init_database(connection)
            return connection

conn = create_connection()

# Pour récupérer le json de l'ESP
@app.route("/api/data", methods=['POST'])
def insertDatas():
    json : dict = request.json
    cursor = conn.cursor()
    cursor.execute(
        f"""INSERT INTO Meteo (hour, day, pressure, temperature, humidity) 
        VALUES (\'{json.get('hour')}\', {json.get('day')}, {json.get('pressure')}, {json.get('temperature')}, {json.get('humidity')});""")
    conn.commit()
    return jsonify(True)

# Pour le front
def get_datas():
    cursor = conn.cursor()
    cursor.execute("SELECT hour, day, pressure, temperature, humidity FROM Meteo;")
    queries = cursor.fetchall()
    result = []
    for query in queries:
        result.append({
            'heure': query[0],
            'jour': query[1],
            'pressure': query[3],
            'temperature': query[4],
            'humidity': query[5],
        })
    results = jsonify(result)
    return render_template('../CodeWEB/Index.html', results=results)

# pour lancer le server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)