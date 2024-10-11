import feedparser
import requests
import argparse
from datetime import datetime, timedelta, timezone
from database import Database 
database = Database()


urls = database.chargeUrl()

# permet de faire les small url 

def shorten(url):
  base_url = 'http://tinyurl.com/api-create.php?url='
  response = requests.get(base_url+url)
  short_url = response.text
  return short_url


def printLine(domain_only):
    for i in range (0 , len(domain_only) + 12 , 1):
        print("-", end ="")
    print()
    


def includeNewArticle():
    for id, url in urls: 
        try:
            feedParser = feedparser.parse(url)
            if feedParser.bozo: 
                print(f"Erreur de parsing pour l'URL : {url}")
                continue
            
            domain_only = feedParser.feed.link.split("//")[-1].split("/")[0]  
            printLine(feedParser.feed.link)
            printLine(domain_only)
            
            for entry in feedParser.entries:
                if 'published' in entry:
                    try:
                        pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                        database.addArticle(entry.title, entry.description, shorten(entry.link), pub_date, id)
                    except ValueError as e:
                        print(f"Erreur de conversion de date pour l'entrée : {entry.title}, erreur : {e}")
                else:
                    print(f"L'entrée n'a pas de date publiée : {entry.title}")

        except Exception as e:
            print(f"Erreur lors du traitement de l'URL {url} : {e}")









parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-c', '--config', type=str, help="Chemin du fichier de configuration")

parser.add_argument('-db','--day-before',type=int)
parser.add_argument('-dmax','--date-max',type=str)
parser.add_argument('-dmin','--date-min',type=str)
parser.add_argument('-l', '--list-source', action='store_true', help="Liste les sources")
args = parser.parse_args()


#################################
# Gestion des arguments de date #
#################################
if args.list_source:
    database.listSource()
    exit(1)

# Recherche des nouveaux articles....
includeNewArticle()
date_start = ""
date_end = ""
if args.day_before:  
    date_today = datetime.now(timezone.utc)
    date_start = date_today - timedelta(days=args.day_before) 


if not args.date_max:
    date_end = datetime.now(timezone.utc)
if args.date_min:
    if re.search(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$', args.date_min):
        date_start = datetime.strptime(args.date_min, '%Y-%m-%d')
        print(f"Date minimale valide : {date_start}")
    else:
        print("Le format de la date minimale est incorrect. Utilisez le format YYYY-MM-DD.")
        exit(1)

#################################
#################################



database.printArticle()




# recuperation des champs en bdd
# for url in urls:
#     feedParser = feedparser.parse(url)
#     domain_only = feedParser.feed.link.split("//")[-1].split("/")[0]  
#     print()
#     print()
#     printLine(domain_only)
#     print(" ---- " + domain_only + " ---- " )
#     printLine(domain_only)
#     print()
#     print()

#     for entry in feedParser.entries:
#         if 'published' in entry:
#             pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')

#             # comparer avec la date en argument
#             if pub_date >= date_start and pub_date < date_end:
#                 print(entry.title)
#                 print(" - " + pub_date.strftime('%Y-%m-%d %H:%M:%S'))
#                 print(" - " + shorten(entry.link))
#                 print()