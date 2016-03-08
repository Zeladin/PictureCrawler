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

"""
TODO:
-Add config file
-make more functions to keep the code cleaner
-deleted unnecessary stuff
-create a text based UI with commands
-find a way to get past nsfw question
"""


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

picLinks = deleteDoubles(picLinks)

imageCounter = 0

Folder = "Pictures/"

folderCheck(Folder)

"""TODO:
    Take link, if its a direct img link -> download image (change regex and add those with fileending to directlink array) Maybe 2 Regex?
    imgur site link -> take div post-image take img tag inside and open the link in the src -> download with correct file ending
    Gallery link -> download gallery

"""

for link in picLinks:
    image = http.request('GET', link + ".jpg")
    with open(Folder + 'Picture_' + str(imageCounter) + ".jpg", 'wb') as f:
        f.write(image.data)
        imageCounter += 1
