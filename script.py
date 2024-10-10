import feedparser
import requests
import argparse
from datetime import datetime, timedelta, timezone
from database import Database 

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-c', '--config', type=str, help="Chemin du fichier de configuration")

parser.add_argument('-db','--day-before',type=int)
parser.add_argument('-dmax','--date-max',type=str)
parser.add_argument('-dmin','--date-min',type=str)
args = parser.parse_args()



#################################
# Gestion des arguments de date #
#################################

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


# permet de faire les small url 
url = 'http://tinyurl.com/api-create.php?url='

def shorten(url):
  base_url = 'http://tinyurl.com/api-create.php?url='
  response = requests.get(base_url+url)
  short_url = response.text
  return short_url


def printLine(domain_only):
    for i in range (0 , len(domain_only) + 12 , 1):
        print("-", end ="")
    print()
    
database = Database()
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