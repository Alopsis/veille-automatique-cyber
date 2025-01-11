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
def getArticlesListePerso(idListe,dateMin, dateMax):
    connection = connectDatabase()
    cursor = connection.cursor()
    articlesId = []
    articles = []
    query = "SELECT * FROM linkListeArticle WHERE id_liste = %s"
    cursor.execute(query, (idListe,))
    results = cursor.fetchall()
    print(results)
    for row in results:
        articlesId.append(row[1])
    for articleId in articlesId:
        print(articleId)
        query = "SELECT * FROM articles WHERE id = %s AND date >= %s AND date <= %s"
        parameters = [articleId, dateMin, dateMax]
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        for row in results:
            articles.append({"id": row[0], "title": row[1], "date": row[2], "source": row[3], "link":row[4]})

    articles.sort(key=lambda x: x['date'], reverse=True)
    cursor.close()
    connection.close()
    print(articles)
    return articles
def addArticleListePerso(idListePerso, idArticle):
    connection = connectDatabase()
    cursor = connection.cursor()
    try:
        # Vérifier si la liste existe
        query = "SELECT * FROM liste_perso WHERE id = %s"
        cursor.execute(query, (idListePerso,))
        element = cursor.fetchone()

        if not element:
            print(f"Erreur : La liste avec l'ID {idListePerso} n'existe pas.")
            return False

        print("La liste existe, vérification des doublons...")

        query = "SELECT * FROM linkListeArticle WHERE id_article = %s AND id_liste = %s"
        cursor.execute(query, (idArticle, idListePerso))
        element = cursor.fetchone()

        if element:
            print(f"Doublon détecté : L'article {idArticle} est déjà lié à la liste {idListePerso}.")
            return False
        print("Aucun doublon trouvé, insertion en cours...")
        query = "INSERT INTO linkListeArticle (id_article, id_liste) VALUES (%s, %s)"
        cursor.execute(query, (idArticle, idListePerso))
        connection.commit()

        print(f"Insertion réussie : Article {idArticle} ajouté à la liste {idListePerso}.")
        return True

    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
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
