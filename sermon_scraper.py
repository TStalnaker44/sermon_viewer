
import requests, json, os
import sqlite3, time, re
from bs4 import BeautifulSoup

DATA_BASE = "audio.db"

pattern = pattern = "[A-Za-z]+ (\d+)(:(\d+)(-(\d+)(:(\d+))?)?)?"

base_url = "https://www.cfcwilliamsburg.org/podcast-sermons/"
insert_query = "INSERT INTO sermons (title, short_title, book, speaker, " +\
               "square_url, year, month, day, duration, start_chapter, " +\
               "end_chapter, start_verse, end_verse) " + \
               "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

def getBooks():
    with open("books.txt", "r", encoding="utf-8") as file:
        books = file.read().split()
        return books

def saveHTML(book, response):
    path = os.path.join("books", book+".html")
    with open(path, "w", encoding="utf-8") as file:
        file.write(response)

def bookExists(book):
    path = os.path.join("books", book+".html")
    return os.path.exists(path)

def getSermonsOnPage(book):
    if not bookExists(book):
        time.sleep(5)
        url = base_url + book
        response = requests.get(url).text
        saveHTML(book, response)
    else:
        path = os.path.join("books", book+".html")
        with open(path, "r", encoding="utf-8") as file:
            response = file.read()
    soup = BeautifulSoup(response, 'html.parser')
    sermons = soup.find_all("div", attrs={"class":"sqs-audio-embed"})
    return sermons

def getSermonData(s, book):
    book = book.replace("-", " ").title()
    title = s.get("data-title")
    short_title = title.split("-")[-1].strip()
    speaker = s.get("data-author")
    url = s.get("data-url")
    duration = s.get("data-duration-in-ms")
    year, month, day = title.split()[0].split(".")
    sc, sv, ec, ev = parseVerses(title)
    data = (title, short_title, book, speaker, url,
            year, month, day, duration, sc, ec, sv, ev)
    return data

def parseVerses(string):
    a = re.search(pattern, string)
    if not a:
        return (0,0,0,0)
    hits = len([x for x in a.groups() if x != None])
    if hits == 1:
        start_chap = a.group(1)
        start_verse = 1
        end_chap = start_chap
        end_verse = start_verse
        return (start_chap,start_verse,
                start_chap,start_verse)
    elif hits == 3:
        start_chap = a.group(1)
        start_verse = a.group(3)
        end_chap = start_chap
        end_verse = start_verse
    elif hits == 5:
        start_chap = a.group(1)
        start_verse = a.group(3)
        end_chap = start_chap
        end_verse = a.group(5)
    elif hits == 7:
        start_chap = a.group(1)
        start_verse = a.group(3)
        end_chap = a.group(5)
        end_verse = a.group(7)
    return (start_chap,start_verse,end_chap,end_verse)

def insertIntoDatabase(data, conn):
    cursor = conn.cursor()
    cursor.execute(insert_query, data)
    
def main():
    conn = sqlite3.connect(DATA_BASE)
    for book in getBooks():
        sermons = getSermonsOnPage(book)
        for s in sermons:
            data = getSermonData(s, book)
            insertIntoDatabase(data, conn)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()


