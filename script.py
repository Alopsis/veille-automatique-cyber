import feedparser
import requests
import src.web.server
from src.web.server import *
from src.article import *

runWebsite()
urls = {
    "https://www.usine-digitale.fr/cybersecurite/rss",
    "https://thecyberexpress.com/feed/"
}


addArticles()