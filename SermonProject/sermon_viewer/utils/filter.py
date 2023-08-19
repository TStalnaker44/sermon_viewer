
from sermon_viewer.models import Sermons
from django.db.models import Q
from .book_order import book_ordering

def getSelections(field):
    selections = Sermons.objects.values(field).distinct()
    return [x[field] for x in selections]

def getPastors():
    return ["Peter Hess", "Bryce Rader", "Adam Messer", "Josiah Monfreda"]

def getGuestSpeakers():
    pastors = getPastors()
    speakers = getSelections("speaker")
    speakers = ["Unknown" if s == "" else s for s in speakers if s not in pastors]
    return sorted(speakers)


def getSermons(b, s, start=2013, end=2023, term="", minlen="", maxlen=""):
    sermons = Sermons.objects.all()
    if b != "Any":
        sermons = sermons.filter(book=b)
    if s != "Any":
        sermons = sermons.filter(speaker=s)
    if start:
        sermons = sermons.filter(year__gte=start)
    if end:
        sermons = sermons.filter(year__lte=end)
    if term:
        sermons = sermons.filter(short_title__contains=term)
    if minlen:
        sermons = sermons.filter(duration__gte=minlen)
    if maxlen:
        sermons = sermons.filter(duration__lte=maxlen)
    return sermons

def orderSermons(sermons, ordering):
    if ordering == 0:
        return sermons.order_by(book_ordering)
    elif ordering == 1: # New to Old
        return sermons.order_by('-year', "-month", "-day")
    elif ordering == 2: # Old to New
        return sermons.order_by('year', 'month', 'day')
    elif ordering == 3: # Alphabetically
        return sermons.order_by("book")

def querySetToList(sermons):
    return [s for s in sermons]