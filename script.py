import feedparser
import requests
import argparse
import src.web.server
from datetime import datetime, timedelta, timezone
from src.web.server import *

runWebsite()
date = 2
urls = {
    "https://www.usine-digitale.fr/cybersecurite/rss",
    "https://thecyberexpress.com/feed/"
}

for url in urls:
    feedParser = feedparser.parse(url)
    domain_only = feedParser.feed.link.split("//")[-1].split("/")[0]  
    print()
    print()
    print(" ---- " + domain_only + " ---- " )
    print()
    print()
    date_today = datetime.now(timezone.utc)
    date_two_days_ago = date_today - timedelta(days=date) 

    for entry in feedParser.entries:
        if 'published' in entry:
            pub_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')

            # comparer avec la date en argument
            if pub_date >= date_two_days_ago:
                print(entry.title)
                print(" - " + pub_date.strftime('%Y-%m-%d %H:%M:%S'))
                print(" - " + shorten(entry.link))
                print()