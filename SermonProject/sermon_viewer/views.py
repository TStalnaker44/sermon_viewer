from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import filter
from .models import Sermons

def index(request):
    sermons = Sermons.objects.filter(book="Genesis")
    books = filter.getSelections("book")
    speakers = filter.getSelections("speaker")
    years = filter.getSelections("year")
    return render(request, 'index.html', {"books":books, "speakers":speakers, "years":years, "sermons":sermons})

@csrf_exempt
def update_content(request):
    if request.method == 'POST':
        book = request.POST.get('selected_book')
        speaker = request.POST.get('selected_speaker')
        start = request.POST.get('startdate')
        end = request.POST.get('enddate')
        term = request.POST.get('search')

        if start and start.isdigit():
            start = int(start)
        if end and end.isdigit():
            end = int(end)


        print("LOOK HERE: ", start, end, term)

        sermons = filter.getSermons(book, speaker, start, end, term)
        updated_content = f"{len(sermons)} results<br><ul>"
        for sermon in sermons:
            updated_content += f'<li>{sermon.title}, {sermon.speaker}</li> '
            updated_content += f'<audio controls><source src="{sermon.square_url}" controls><source type="audio/mpeg"></audio>'
        updated_content += "</ul>"

        return JsonResponse({'updated_content': updated_content})
