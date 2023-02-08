# Récupération des données dans la BDD
import os
import sqlite3
from sqlite3 import Error
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

db_file = r"Projet_IOT.db"

@app.route("/api/data", method=['POST'])
def getDatas():
    conn = http.client.HTTPConnection("localhost:80")
    response = requests.get(conn)

    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print("Error: la réponse a retourné un code d'erreur {}".format(response.status_code))

def init_database(connection):
    cursor = connection.cursor()
    cursor.execute(
    "CREATE TABLE Projet_IOT.Meteo ( id INT(100) AUTO INCREMENT PRIMARY KEY NOT NULL,heure varchar(100),jour varchar(100) NOT NULL,pression INT(100) NOT NULL,temperature INT(100) NOT NULL,humidite INT(100) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;")
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

@app.route('/get_Datas/')
def get_datas():
    cursor = conn.cursor()
    cursor.execute("SELECT id, heure, jour, pression, temperature, humidite FROM Meteo;")
    queries = cursor.fetchall()
    result = []
    for query in queries:
        result.append({
            'id': query[0],
            'date_prise': query[1],
            'pression': query[3],
            'temperature': query[4],
            'humidite': query[5],
        })
    return render_template('TemplateProjet_IOT.html', templateData=jsonify(result))

@app.route('/post_Datas/', method=['POST'])
def postDatas():
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Meteo (heure, jour, pression, temperature, humidite) VALUES ({heure}, {jour}, {pression}, {temperature}, {humidite});")
    cursor.commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)