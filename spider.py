import requests
from bs4 import BeautifulSoup
import os
import sys
import validators

URL = ""
CLEANURL = ""
LINKSTOIMAGES = set()
LINKS = set()
VISITEDLINKS = set()
FILEPATH = "data"
DEPTH = 0


def URLclean(url2clean):
    global CLEANURL
    cleanURL = url2clean.replace("https://www.", '')
    CLEANURL = cleanURL

def getHTML(url):
    try:
        getURL = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(getURL.text, 'html.parser')
        return soup
    except:
        print("ERROR: Failed connecting to site Status code :", getURL.status_code)
        exit()

def downloadImages():
    folder_path = FILEPATH
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for image_url in LINKSTOIMAGES:
        if CLEANURL not in  image_url:
            image_url = URL + image_url
        file_name = image_url.split('/')[-1]
        file_name = file_name.split('?')[0]
        if not file_name or file_name == CLEANURL:
            continue
        print("Downloading", image_url, end='\r')
        file_path = os.path.join(folder_path, file_name)
        imageraw = requests.get(image_url)
        if imageraw.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(imageraw.content)
        else:
            print("ERROR: Downloading image, code ", imageraw.status_code)

def getURLS(cleanurl, soup, depth):
    global LINKS, VISITEDLINKS, LINKSTOIMAGES
    if depth == -1:
        return
    links = soup.find_all("a", href=True)
    images = soup.find_all('img')
    for image in images:
        src = image.get('src')
        if src not in LINKSTOIMAGES:
            LINKSTOIMAGES.add(requests.compat.urljoin(cleanurl, src))
    new_links = set()
    for link in links:
        src = link.get('href')
        if cleanurl in src:
            if src not in VISITEDLINKS and src not in LINKS:
                new_links.add(requests.compat.urljoin(cleanurl, src))
    print(depth, end='\r')    
    VISITEDLINKS.add(cleanurl)
    for recursiurl in new_links:
        soup = getHTML(recursiurl)
        LINKS.add(recursiurl)
        getURLS(recursiurl, soup, depth - 1)

def parsearg():
    global DEPTH
    global FILEPATH
    global URL
    for a in sys.argv[1:]:
        if a == "-r":
            DEPTH = 5
        if a == "-l":
            if sys.argv[sys.argv.index(a) + 1].isnumeric() == True:
                DEPTH = int(sys.argv[sys.argv.index(a) + 1])
            else:
                DEPTH = 5
        if a == "-p":
            FILEPATH = sys.argv[sys.argv.index(a) + 1]
        if validators.url(a) == True:
            URL = a

parsearg()
print("DEPTH:", DEPTH)
print("URL:", URL)
print("FILE PATH:", FILEPATH)

soup = getHTML(URL)
LINKS.add(URL)
URLclean(URL)
getURLS(CLEANURL, soup, DEPTH)
downloadImages()
