
import requests, json, os
import sqlite3, time
from bs4 import BeautifulSoup

DATA_BASE = "audio.db"

base_url = "https://www.cfcwilliamsburg.org/podcast-sermons/"
insert_query = "INSERT INTO sermons (title, short_title, book, speaker, " +\
               "square_url, year, month, day, duration) " + \
               "VALUES (?,?,?,?,?,?,?,?,?)"

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
    data = (title, short_title, book, speaker, url,
            year, month, day, duration)
    return data

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


