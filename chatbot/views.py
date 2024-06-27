from django.shortcuts import render
from numpy import VisibleDeprecationWarning
from accounts.models import User,PDFFile,PDFView
from .utils import get_pdf_text, get_text_chunks, get_vector_store, user_input
from django.http import HttpResponse,JsonResponse
from django.conf import settings
import requests
import os

# Create your views here.



def process_pdf(request):
    path = request.POST.get('path')
    path = path[1:]
    raw_text=get_pdf_text(path)
    text_chunks=get_text_chunks(raw_text)
    get_vector_store(text_chunks)
    data = {'status':'pdf load successful'}
    return JsonResponse(data, safe=False)



def pdfview(request,string,int):
    response = None
    subject_name=string
    id=int
    requested_pdf=PDFFile.objects.get(id=id)
    path=requested_pdf.pdf_file.url[1:]

    if request.user.is_authenticated and request.user.is_student:
        if not PDFView.objects.filter(user=request.user, pdf=requested_pdf).exists():
            requested_pdf.views_count += 1
            requested_pdf.save()
            PDFView.objects.create(user=request.user, pdf=requested_pdf)

    answers=" "
    try:
        with open("my_file.txt", 'r') as file:
            answers = file.read()
    except FileNotFoundError:
        pass

    if request.method == 'POST':
        question = request.POST.get('question')
        marks = request.GET.get('marks', '2')
        response = user_input(question,marks)
        answers += question+"\n"+response + "\n"

        with open("my_file.txt", 'w') as file:
            file.write(answers)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'response': response})
        else:
            return render(request, 'chatbot/pdfview.html', {
                'pdf': requested_pdf,
                'question': question,
                'response': response,
            })
    open('my_file.txt','w').close()
    return render(request, 'chatbot/pdfview.html', {'pdf': requested_pdf, 'subject_name': subject_name })


def download_file(request):
    file_path = "my_file.txt"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="responses.txt"'
            return response
    else:
        return HttpResponse("File not found", status=404)
    

def youtube_search(request):
    query = request.GET.get('query', '')
    if query:
        api_key = 'AIzaSyDe5wciQ_9A-rMqCJ13ALwvjEoZ0A6fvR0'  # Ensure you have this in your settings
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        search_params = {
            'part': 'snippet',
            'q': query,
            'key': api_key,
            'maxResults': 5,  # You can adjust the number of results here
            'type': 'video'
        }
        
        response = requests.get(search_url, params=search_params)
        results = response.json().get('items', [])
        
        video_data = [
            {
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'thumbnail': item['snippet']['thumbnails']['default']['url']
            }
            for item in results
        ]
        # print(video_data)
        
        return JsonResponse({'videos': video_data, 'query': query})
    
    return JsonResponse({'videos': []})