from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import filter
from .models import Sermons

def index(request):
    speaker = request.GET.get("speaker") or "Any"
    book = request.GET.get("book") or "Any"
    ordering = request.GET.get("ordering") or "0"
    if ordering.isdigit(): ordering = int(ordering)
    term = request.GET.get("term") or ""

    sermons = filter.getSermons(book, speaker, term=term)
    sermons = filter.orderSermons(sermons, ordering)
    print(len(sermons))
    books = ["Any"] + filter.getSelections("book")
    guest_speakers = filter.getGuestSpeakers()
    pastors = filter.getPastors()
    years = filter.getSelections("year")
    return render(request, 'index.html', {"books":books, "guest_speakers":guest_speakers, 
                                          "pastors":pastors, "years":years, "sermons":sermons,
                                          "book":book, "speaker":speaker, "ordering":ordering,
                                          "term":term})

@csrf_exempt
def update_content(request):
    if request.method == 'POST':
        book = request.POST.get('selected_book')
        speaker = request.POST.get('selected_speaker')
        start = request.POST.get('startdate')
        end = request.POST.get('enddate')
        term = request.POST.get('search')
        minlen = request.POST.get('mintime')
        maxlen = request.POST.get('maxtime')
        ordering = request.POST.get('selected_order')

        if start and start.isdigit():
            start = int(start)
        if end and end.isdigit():
            end = int(end)
        if minlen and minlen.isdigit():
            minlen = int(minlen) * 60000
        if maxlen and maxlen.isdigit():
            maxlen = int(maxlen) * 60000
        if ordering:
            ordering = int(ordering)

        sermons = filter.getSermons(book, speaker, start, end, term, minlen, maxlen)
        sermons = filter.orderSermons(sermons, ordering)
        sermons = filter.querySetToList(sermons)

        updated_content = f'<div class="results">{len(sermons)} Results</div><ul class="sermonList">'
        for sermon in sermons:
            title = sermon.title.replace("'", "")
            updated_content += f'<li onclick="downloadAudio(\'{sermon.square_url}?download=true\', \'{title}\')">'
            updated_content += f'<div class="header"><div class="title">{sermon.title}</div><div class="speaker">{sermon.speaker}</div></div>'
            updated_content += f'<audio controls><source src="{sermon.square_url}" controls><source type="audio/mpeg"></audio></li>'
        updated_content += "</ul>"

        return JsonResponse({'updated_content': updated_content})
