from django.urls import path, include
from .views import *

app_name = 'chatbot'

urlpatterns = [
    path('student/resources/<string>/<int>/', pdfview , name = "pdfview"),
    path('student/download/', download_file, name='download_file'),
    path('youtube_search/', youtube_search, name='youtube_search'),
    path('processpdf/', process_pdf, name="process_pdf")
]

