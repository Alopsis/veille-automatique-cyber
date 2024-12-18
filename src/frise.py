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


def addFrise(nom):
    print("-à-ç-ç-ç-ç-ç-ç-")
    print(nom)
    print("-à-ç-ç-ç-ç-ç-ç-")
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
