import os
import sqlite3
from sqlite3 import Error
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Création du fichier de BDD
db_file = r"Projet_IOT.db"

def init_database(connection):
    cursor = connection.cursor()
    cursor.execute(
    "CREATE TABLE Projet_IOT.Meteo (id INT(100) AUTO INCREMENT PRIMARY KEY NOT NULL,date varchar(100) NOT NULL,pressure INT(100) NOT NULL,temperature INT(100) NOT NULL,humidity INT(100) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
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
    cursor.execute(f"INSERT INTO Meteo (date, pressure, temperature, humidity) VALUES (\'{json.get('date')}\', {json.get('pressure')}, {json.get('temperature')}, {json.get('humidity')});")
    conn.commit()
    return jsonify(True)

# Pour le front
@app.route("/front/data/", methods=['GET'])
def getData():
    cursor = conn.cursor()
    cursor.execute("SELECT date, humidity, pressure, temperature FROM Meteo ORDER BY id Desc LIMIT 1;")
    queries = cursor.fetchall()
    result = []
    for query in queries:
        result.append({
            'date': query[0],
            'humidity': query[1],
            'pressure': query[2],
            'temperature': query[3]
        })
    data = jsonify(result)

    return data

@app.route("/front/datas/", methods=['GET'])
def getDatas():
    cursor = conn.cursor()
    cursor.execute("SELECT date, humidity, pressure, temperature FROM Meteo ORDER BY id Desc LIMIT 30;")
    queries = cursor.fetchall()
    results = []
    for query in queries:
        results.append({
            'date': query[0],
            'humidity': query[1],
            'pressure': query[2],
            'temperature': query[3]
        })
    datas = jsonify(results)

    return datas

# pour lancer le server
if __name__ == "__main__":
    app.run(host='0.0.0.0')