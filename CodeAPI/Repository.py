# Récupération des données dans la BDD
import os
import sqlite3
from sqlite3 import Error
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

db_file = r"Projet_IOT.db"

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

@app.route("/api/data", methods=['POST'])
def insertDatas():
    json = request.json
    cursor = conn.cursor()
    cursor.execute(
        f"""INSERT INTO Meteo (heure, jour, pression, temperature, humidite) 
        VALUES ({json.get('heure')}, {json.get('jour')}, {json.get('pression')}, {json.get('temperature')}, {json.get('humidite')});""")
    conn.commit()
    return jsonify(True)

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


@app.route('/getDatas/<int:temperature>/', methods=['GET'])
def getDatas(temperature):
    # récupérer les variables dans la route puis paramètre et faire un SELECT
    return True

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)