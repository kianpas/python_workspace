import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "https://kianpas.github.io/"
FILE_PATH = "C:\\Users\\1\\Documents"

# print(BASE_URL)
searched_links = []
broken_links = []

def getLinksFromHTML(html):
    def getLink(el):
        print(el)
        return el["href"]
    return list(map(getLink, BeautifulSoup(html, features="html.parser").select("a[href]")))

# print(certifi.where())

def find_broken_links(domainToSearch, URL, parentURL):
    # print(URL)
    is_searchable = (not (URL in searched_links)) and (not URL.startswith("mailto:")) and (not ("javascript:" in URL)) and (not URL.endswith((".png", ".jpg", ".jpeg")))
    if is_searchable:
        try:
            resetObj = requests.get(URL, verify=False)
            searched_links.append(URL)
            if(resetObj.status_code == 404):
                broken_links.append({
                    "url":URL,
                    "parent_url" : parentURL or 'Home',
                    "message" : resetObj.reason
                })
            else:
                if urlparse(URL).netloc == domainToSearch:
                    for link in getLinksFromHTML(resetObj.text):
                        find_broken_links(domainToSearch, urljoin(URL, link), URL)
        except Exception as e:
            print("ERROR: " + str(e))
            searched_links.append(domainToSearch)

# find_broken_links(urlparse(BASE_URL).netloc, BASE_URL, "")
print(searched_links)
print(broken_links)
govUrl = 'https://www.gov.kr/portal/service/serviceInfo/PTR000050333'
req = requests.get(govUrl, verify=False)
soup = BeautifulSoup(req.content, 'lxml')
go = soup.find('a', class_='directgo')
print(go)
# print(soup.select("a[href]"))