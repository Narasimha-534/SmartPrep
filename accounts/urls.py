from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('',home, name="home"),
    path('login/', login_signup, name = "login_signup"),
    path('logout/', logout , name = "logout"),
    path('student/', Student , name = "Student"),
    path('faculty/', Faculty , name = "Faculty"),
    path('faculty/upload/', upload , name = "upload"),
    path('faculty/resources/<string>/<int>/', pdf_view , name = "pdf_view"),
    path('student/resources/<string>/', resources, name = "resources"),
    path('', include('chatbot.urls'))
]