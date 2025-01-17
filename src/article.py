from src.database import connectDatabase
import feedparser
from datetime import datetime, timedelta, timezone
import requests
from src.misc import shorten
def getSources():
    connection = connectDatabase()
    cursor = connection.cursor()
    
    source_id = 1
    query = "SELECT * FROM sources"
    
    cursor.execute(query)
    sources = []
    results = cursor.fetchall()
    for row in results:
        sources.append({"id": row[0], "nom": row[1], "lien": row[2]})
    cursor.close()
    connection.close()
    return sources

def getArticles(dateMin, dateMax, sourceBan):
    connection = connectDatabase()
    cursor = connection.cursor()

    query = "SELECT * FROM articles WHERE date >= %s AND date <= %s"
    parameters = [dateMin, dateMax]
    cursor.execute(query, parameters)
    articles = []
    results = cursor.fetchall()
    for row in results:
        if str(row[3]) not in sourceBan:
            articles.append({"id": row[0], "title": row[1], "date": row[2], "source": row[3], "link":row[4]})
    articles.sort(key=lambda x: x['date'], reverse=True)
    cursor.close()
    connection.close()
    return articles


def addArticles():
    sources = getSources()
    for url in sources:
        feedParser = feedparser.parse(url["lien"])
        print("-----------------")
        print(url["nom"])
        print("------------------")
        domain_only = feedParser.feed.link.split("//")[-1].split("/")[0]  
        print()
        print()
        print(" ---- " + domain_only + " ---- " )
        print()
        print()
        date_today = datetime.now(timezone.utc)

        for entry in feedParser.entries:
            if 'published' in entry:
                pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                print(entry.title)
                print(" - " + pub_date.strftime('%Y-%m-%d'))
                print(" - " + shorten(entry.link))
                print()
                insertIfNotExist(entry.title,pub_date,url["id"], shorten(entry.link))


def insertIfNotExist(title, date, sourceId,link):
    date = date.strftime('%Y-%m-%d')
    connection = connectDatabase()
    cursor = connection.cursor()
    try:

        query = "SELECT * FROM articles WHERE title = %s AND date = %s AND source = %s"
        cursor.execute(query, (title, date, sourceId))  
        results = cursor.fetchall()
        if len(results) >= 1: 
            print("L'article existe déjà.")
        else:
            print("L'article n'existe pas.")
            title = title.replace("\"","'")
            query = "INSERT INTO articles (title,date,source, link) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (title,date,sourceId,link))
            connection.commit()
            if cursor.rowcount >= 1:
                print("Article enregistré")
            else:
                print("Erreur")

    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")
    finally:
        cursor.close()
        connection.close()
