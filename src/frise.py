from src.database import connectDatabase
import feedparser
from datetime import datetime, timedelta, timezone
import requests
from src.misc import shorten


def getFrise():
    connection = connectDatabase()
    cursor = connection.cursor()

    query = "SELECT * FROM frise "
    cursor.execute(query)
    frise = []
    results = cursor.fetchall()
    for row in results:
        frise.append({"id": row[0], "nom": row[1]})
    cursor.close()
    connection.close()
    return frise
def addItemToFrise(friseid, valeur, date):
    if not friseid or not valeur or not date:
        raise ValueError("friseid, valeur, et date sont obligatoires")
    
    connection = connectDatabase()
    cursor = connection.cursor()

    query = "SELECT * FROM frise WHERE id = %s"
    cursor.execute(query, (friseid,))
    results = cursor.fetchall()

    if len(results) >= 1:
        query = """
                INSERT INTO linkFrise (id_frise, valeur, date_publi)
                VALUES (%s, %s, %s)
            """
        cursor.execute(query, (friseid, valeur, date))
        connection.commit()
    else:
        raise ValueError("La frise avec l'ID spécifié n'existe pas")
    cursor.close()
    connection.close()

def getItemFrise(friseid):
    try:
        connection = connectDatabase()
        cursor = connection.cursor(dictionary=True)
        item = []
        query = "SELECT * FROM linkFrise WHERE id_frise = %s"
        cursor.execute(query, (friseid,))
        results = cursor.fetchall()
        for row in results:

            item.append({"id": row["id"], "valeur": row["valeur"], "date": row["date_publi"]})
        return item
    except Exception as e:
        print(f"Erreur : {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def getItem(itemId):
    try:
        connection = connectDatabase()
        cursor = connection.cursor()
        query = "SELECT id, valeur ,date_publi FROM linkFrise WHERE id = %s"
        cursor.execute(query, (itemId,))
        result = cursor.fetchone()
        if not result:
            print("L'item n'existe pas")
            return None
        item = {"id": result[0], "valeur": result[1], "date":result[2]}

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'accès à la base de données : {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return item
def get_specific_frise(id):
    try:
        connection = connectDatabase()
        cursor = connection.cursor()
        query = "SELECT id, nom FROM frise WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if not result:
            print("La frise n'existe pas")
            return None
        frise = {"id": result[0], "nom": result[1]}

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'accès à la base de données : {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return frise


def addFrise(nom):
    connection = connectDatabase()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM frise WHERE nom = %s"
        cursor.execute(query, (nom,))  # Ajout d'une virgule pour passer correctement le tuple
        results = cursor.fetchall()

        if results:  # Simplification de la vérification
            print("La frise existe déjà.")
        else:
            print("La frise n'existe pas.")
            query = "INSERT INTO frise (nom) VALUES (%s)"
            cursor.execute(query, (nom,)) 
            connection.commit()

            if cursor.rowcount >= 1:
                print("Frise enregistrée.")
            else:
                print("Erreur lors de l'enregistrement de la frise.")

    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")

    finally:
        # Fermeture des ressources
        if cursor:
            cursor.close()
        if connection:
            connection.close()
