import requests

def shorten(url):
  base_url = 'http://tinyurl.com/api-create.php?url='
  response = requests.get(base_url+url)
  short_url = response.text
  return short_url