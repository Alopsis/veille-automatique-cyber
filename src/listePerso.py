from src.database import connectDatabase
import feedparser
import bcrypt 

from datetime import datetime, timedelta, timezone
import requests
from src.misc import shorten

def getListes(userId):
    connection = connectDatabase()
    cursor = connection.cursor()
    try:
        listes = []
        listeRet = []
        query = "SELECT * FROM linkUserListe WHERE id_user = %s"
        cursor.execute(query, (userId,))
        linkUserListes = cursor.fetchall()
        for row in linkUserListes:
            listes.append(row[2])
        for liste in listes:
            listeRet.append(getListe(liste))
        return listeRet

    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")
        return None

    finally:
        cursor.close()
        connection.close()


def getListe(idListe):
    connection = connectDatabase()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM liste_perso WHERE id = %s"
        cursor.execute(query, (idListe,))
        element = cursor.fetchone()
        if element:
            return {"id": element[0], "nom": element[1]} 
    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")
        return None

    finally:
        cursor.close()
        connection.close()


def insertListe(nom,userId):
    connection = connectDatabase()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO liste_perso (nom) VALUES (%s)"
        cursor.execute(query, (nom,))
        connection.commit()
        if cursor.rowcount >= 1:
            last_inserted_id = cursor.lastrowid
            print(f"Utilisateur enregistré avec l'ID: {last_inserted_id}")
            query = "INSERT INTO linkUserListe (id_user,id_liste_perso) VALUES (%s, %s)"
            cursor.execute(query,(userId, last_inserted_id))
            connection.commit()

        else:
            print("Erreur lors de l'enregistrement")
    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")
        return None

    finally:
        cursor.close()
        connection.close()
