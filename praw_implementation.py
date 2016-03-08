import praw
import os
import re
import urllib3

def folderCheck(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def deleteDoubles(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

"""
    TODO: Process files with no file extension in URL.
"""


http = urllib3.PoolManager();

user_agent = "Picture Scraper"
r = praw.Reddit(user_agent=user_agent)


Folder = "Pictures2/"
folderCheck(Folder)

pictureLinks = []

#r.login()

while True:
    UserInput = input('Enter a subreddit:')
    subreddit = r.get_subreddit(UserInput)

    print("Looking for subreddit...")

    for submission in subreddit.get_hot(limit=25):
        print(submission.url)
        matcher = re.match('http[s]?://(imgur.com|i.imgur.com)/\w+.(png|jpg|jpeg)', submission.url)

        if matcher:
            pictureLinks.append(submission.url)

    if len(pictureLinks) >= 0:
        print("Seems like there were no pictures. Try again with another subreddit!")
        continue

    print("Found submissions")
    print("Deleting doubles")
    pictureLinks = deleteDoubles(pictureLinks)

    imageCounter = 0
    print("Saving pictures...")
    for link in pictureLinks:
        image = http.request('GET', link)
        type=link[-4:]

        if type[0] != ".":
            ending=".jpg"
        else:
            ending=type

        with open(Folder + 'Picture_' + str(imageCounter) + ending, 'wb') as f:
            f.write(image.data)
            imageCounter += 1

    print("Done!")

