import feedparser
import requests
import argparse
from datetime import datetime, timedelta, timezone

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('date',  type=int, 
                    help='jour avant')
args = parser.parse_args()

if args.date:
    print("ok")
else:
    print("non")
print(args.date)
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
    
urls = {
    "https://www.usine-digitale.fr/cybersecurite/rss",
    "https://thecyberexpress.com/feed/"
}

for url in urls:
    feedParser = feedparser.parse(url)
    domain_only = feedParser.feed.link.split("//")[-1].split("/")[0]  
    print()
    print()
    printLine(domain_only)
    print(" ---- " + domain_only + " ---- " )
    printLine(domain_only)
    print()
    print()
    date_today = datetime.now(timezone.utc)
    date_two_days_ago = date_today - timedelta(days=args.date) 

    for entry in feedParser.entries:
        if 'published' in entry:
            pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')

            # comparer avec la date en argument
            if pub_date >= date_two_days_ago:
                print(entry.title)
                print(" - " + pub_date.strftime('%Y-%m-%d %H:%M:%S'))
                print(" - " + shorten(entry.link))
                print()