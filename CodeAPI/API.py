import os
import sqlite3
from sqlite3 import Error
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

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
def getDatas():
    cursor = conn.cursor()
    cursor.execute("SELECT pressure, temperature, humidity FROM Meteo ORDER BY id Desc LIMIT 1;")
    queries = cursor.fetchall()
    result = []
    results = []
    for query in queries:
        result.append({
            'temperature': query[0],
            'humidity': query[1],
            'pressure': query[2]
        })
    lastTemperature = result['temperature']
    lastHumidity = result['humidity']
    lastPressure = result['pressure']

    cursor.execute("SELECT temperature, humidity, pressure FROM Meteo ORDER BY id Desc LIMIT 30;")
    queryes = cursor.fetchone()
    for querys in queryes:
        results.append({
            'temperature': querys[0],
            'humidity': querys[1],
            'pressure': querys[2]
        })
    temperature = results['temperature']
    humidity = results['humidity']
    pressure = results['pressure']

    return render_template('../CodeWEB/Index.html', temperature=temperature, humidity=humidity, pressure=pressure,
                           lastTemperature=lastTemperature, lastHumidity=lastHumidity, lastPressure=lastPressure)

# pour lancer le server
if __name__ == "__main__":
    app.run(host='0.0.0.0')