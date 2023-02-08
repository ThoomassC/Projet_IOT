# Récupération des données dans la BDD
import os
import sqlite3
from sqlite3 import Error
from flask import Flask, jsonify, request

app = Flask(__name__)

# Création du fichier de BDD
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

# Pour récupérer le json de l'ESP
@app.route("/api/data", methods=['POST'])
def insertDatas():
    json : dict = request.json
    cursor = conn.cursor()
    cursor.execute(
        f"""INSERT INTO Meteo (heure, jour, pression, temperature, humidite) 
        VALUES (\'{json.get('heure')}\', {json.get('jour')}, {json.get('pression')}, {json.get('temperature')}, {json.get('humidite')});""")
    conn.commit()
    return jsonify(True)

# pour lancer le server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)