import tmdbsimple as tmdb
import os
import shutil


def StripFileType(title):
    if title.endswith(".mpeg") or title.endswith(".MPEG"):
        return title[:-5]

    return title[:-4]

def StripDate(title):
    if title.endswith(')'):
        return title[:-6]
    return title

def MovieSearch(title):
    search = tmdb.Search()
    title = StripFileType(title)
    title = StripDate(title)
    response = search.movie(query=title)
    for r in response['results']:
        if r['title'] == title:
            return r['title'] + " (" + r['release_date'][:4] + ')'
    return response['results'][0]['title'] + " (" + response['results'][0]['release_date'][:4] + ')'


def ReplaceBadChars(title):
    reservedChars = {'<', '>', ':', '"', '/', '/', '|', '?', '*'}
    res = ""
    for i in range(0, len(title)):
        if title[i] in reservedChars:
            res += ' '
            res += '-'
        else:
            res += title[i]
    return res


tmdb.API_KEY = '13a93ca90cf789141a57294fca994d41'

sourceDir = 'H:\\Videos\\Drop\\Movies\\'
movieDir = 'H:\\Videos\\Movies\\'
errorDir = 'H:\\Videos\\Issues\\Movies\\'

for filename in os.listdir(sourceDir):
    try:
        if os.path.isfile(os.path.join(sourceDir, filename)):
            title = MovieSearch(filename)
            title = ReplaceBadChars(title)
            if not os.path.exists(title):
                os.mkdir(title)
                source = movieDir + filename
                dst = movieDir + title + "\\" + filename
                shutil.move(source, dst)
            else:
                if not os.path.exists(errorDir):
                    os.mkdir(errorDir)
                source = sourceDir + filename
                dst = errorDir + filename
                shutil.move(source, dst)

    except FileExistsError:
        print("File Exists")

    except IndexError:
        print("Index Error on " + filename)
        if not os.path.exists(errorDir):
            os.mkdir(errorDir)
        source = movieDir + filename
        dst = errorDir + filename
        shutil.move(source, dst)

