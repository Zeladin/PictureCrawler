import urllib3
# import ssl
import bs4
import re
import os

def folderCheck(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def deleteDoubles(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


url = 'http://www.reddit.com/r/funny'

http = urllib3.PoolManager();

redditPage = http.request('GET', url)

readPage = redditPage.data

soup = bs4.BeautifulSoup(readPage, "html.parser")

picLinks = []

for a in soup.find_all('a', href=True):

    matcher = re.match('http[s]?://(imgur.com|i.imgur.com)/\w+', a['href'])
    if matcher:
        picLinks.append(matcher.group(0))

# print(len(picLinks))
# print(picLinks)

picLinks=deleteDoubles(picLinks)

imageCounter=0

Folder="Pictures/"

folderCheck(Folder)

for link in picLinks[:10]:
    image = http.request('GET', link + ".jpg")
    with open(Folder+'Picture_'+str(imageCounter)+ ".jpg", 'wb') as f:
        f.write(image.data)
        imageCounter+=1


