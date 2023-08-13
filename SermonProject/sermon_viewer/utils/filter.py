
from sermon_viewer.models import Sermons
from django.db.models import Q

def getSelections(field):
    selections = Sermons.objects.values(field).distinct()
    return ["Any"] + [x[field] for x in selections]

def getSermons(b, s, start=2013, end=2023, term=""):
    sermons = Sermons.objects.all()
    if b != "Any":
        sermons = sermons.filter(book=b)
    if s != "Any":
        sermons = sermons.filter(speaker=s)
    if start and end:
        sermons = sermons.filter(year__range=(start, end))
    if term:
        sermons = sermons.filter(short_title__contains=term)
    return [s for s in sermons]