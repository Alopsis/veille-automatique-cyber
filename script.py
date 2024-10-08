import feedparser
import requests
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('date',  type=int, required=false,
                    help='jour avant')
args = parser.parse_args()
len(args.args)

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
    printLine(domain_only)
    print(" ---- " + domain_only + " ---- " )
    printLine(domain_only)

    for entry in feedParser.entries:
        
        print(entry.title)
        print(" - " +shorten(entry.link))