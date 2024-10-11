import mysql.connector
from mysql.connector import Error
import json


class Database:
    def __init__(self):
        with open('credential.json') as config_file:
            config = json.load(config_file)
        try:
            self.connection = mysql.connector.connect(
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password']
            )
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
        except Error as e:
            print(f"Erreur lors de la connexion à MySQL ")
            self.connection = None

    def printArticle(self):
        if self.connection is not None and self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM article ORDER BY domain;")
                articles = cursor.fetchall()
                
                # Itération sur les résultats
                for article in articles:
                    id = article[0]
                    title = article[1]
                    content = article[2]
                    published_date = article[3]
                    
                    print(f"Title: {title}")
                    print(f"Content: {content}")
                    print(f"Published Date: {published_date}")
                    print("-" * 20)
            except Error as e:
                print(f"Erreur lors de l'exécution de la requête {e}")
            finally:
                cursor.close()

    def close(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
    def listSource(self):
        if self.connection is not None and self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM domain ORDER BY name ASC;")
                domains = cursor.fetchall()
                for domain in domains:
                    domainName = domain[1]
                    print(f"- {domainName}")
            except Error as e:
                print(f"Erreur lors de l'exécution de la requête {e}")
            finally:
                cursor.close()
    def addArticle(self, title,description,url,pub_date,domain):
        print(domain)
        if self.connection is not None and self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT * FROM article where name = {title} and description = {description};")
                elem = cursor.fetchone()
                if elem:
                    # on peut l'ajouter
                    cursor.execute(f"INSERT INTO article ('name','description','date','domain','url') VALUES ({title} , {description}, {date}, {domain},{url})")            
            except Error as e:
                print(f"Erreur lors de l'exécution de la requête {e}")
            finally:
                cursor.close()
