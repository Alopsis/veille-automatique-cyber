from src.database import connectDatabase
import feedparser
import bcrypt 

from datetime import datetime, timedelta, timezone
import requests
from src.misc import shorten

def getUser(username, password):
    connection = connectDatabase()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user:
            stored_password = user[2]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return user
            else:
                return None
        else:
            return None

    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")
        return None

    finally:
        cursor.close()
        connection.close()



def insertUser(username, password):
    connection = connectDatabase()
    cursor = connection.cursor()
    try:
        # Vérifier si l'utilisateur existe déjà
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        results = cursor.fetchall()
        if len(results) >= 1:
            print("L'utilisateur existe déjà.")
        else:
            # Hachage du mot de passe avec bcrypt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            # Insertion dans la base de données
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, hashed_password))
            connection.commit()
            if cursor.rowcount >= 1:
                return username
            else:
                return None

    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")
        return None

    finally:
        cursor.close()
        connection.close()
