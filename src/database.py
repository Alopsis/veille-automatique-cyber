import mysql.connector


def connectDatabase():

    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='veille-automatique-cyber'
        )
        if connection.is_connected():
            print("Connexion réussie")
        else:
            print("Connexion échouée")
        return connection
    except mysql.connector.Error as err:
        print(f"Erreur de connexion : {err}")
