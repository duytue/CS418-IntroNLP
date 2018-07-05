import unicodedata
from bs4 import BeautifulSoup
from google import google
from urllib2 import urlopen


num_pages = 1
urls = google.search("What is a prism?", 1)
print urls[0].description

# url = next(urls)
# print url
# response = urlopen(url)
# html = response.read()

