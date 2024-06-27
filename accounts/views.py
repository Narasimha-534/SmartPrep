from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import User , PDFFile 
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
import re

def home(request):
    return render(request,"accounts/Home.html")

def recent_uploads(username):
    pdf_objects = PDFFile.objects.filter(uploadedBy = username)
    return pdf_objects

def student_home(username):
    arr=PDFFile.objects.values('subject').distinct()
    arr2=[]
    for i in arr:
        arr2.append(i['subject'])
    return arr2

def login_signup(request):
    if request.method == 'POST':
        form_identifier = request.POST.get("form_identifier")
        if form_identifier == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request,username = username,password = password)
                
            if user is not None and user.is_teacher:
                # print(pdf_object.pdf_file)
                login(request, user)
                return redirect('/faculty')
            elif user is not None and user.is_student:
                
                login(request, user)
                return redirect('/student')
            else:
                msg= 'invalid credentials'
            
        if form_identifier == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'email already exists'})
            elif User.objects.filter(username=username).exists():
                return JsonResponse({'message':'Username already exists'})
            else:
                if re.match(r'.+_.+@mvsrec.edu.in', email):  # Example pattern for teachers

                    user = User.objects.create_user(username, email, password1)
                    user.is_teacher = True
                    user.save()
                    return render(request,'accounts/login.html')

                elif re.match(r'\d+@mvsrec.edu.in', email):  # Example pattern for students    
                    user = User.objects.create_user(username, email, password1)
                    user.is_student = True
                    user.save()
                    return render(request,'accounts/login.html')      
                else:
                    print('email', 'Invalid email format for either teacher or student.')
                    return redirect('login_signup')
    return render(request,'accounts/login.html')


def Student(request):
    user = request.user
    subjects = student_home(user.username)
    return render(request, 'accounts/Student.html' , {'username' :user.username , 'subjects' : subjects})

# @login_required(login_url = 'accounts:login_signup')
def Faculty(request):
    user = request.user
    pdf_object = recent_uploads(user.id)
    return render(request, "accounts/Faculty.html", {'username':user.username , 'contents' : pdf_object })

def logout(request):
    return render(request,'accounts/login.html')

def upload(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        chapter_name = request.POST.get('chapter_name')
        chapter_number = request.POST.get('chapter_number')
        pdfs = request.FILES.getlist('pdfs')
        # print(request.user.username)
        for pdf in pdfs:
            PDFFile.objects.create(chapter_name=chapter_name, chapter_number=chapter_number, pdf_file=pdf ,uploadedBy = request.user,subject = subject)
    return render(request, 'accounts/Upload.html')

def pdf_view(request, string,int):
    id = int
    requested_pdf = PDFFile.objects.get(id = id)
    path = requested_pdf.pdf_file.url[1:]
    # print(path)
    return FileResponse(open(path, 'rb'), content_type='application/pdf')

def resources(request,string):
    subject=string
    pdfs_objects=PDFFile.objects.filter(subject=subject)
    # print(pdfs_objects)
    chapter_numbers=PDFFile.objects.filter(subject=subject).values('chapter_number').distinct()
    arr=[]
    for i in chapter_numbers:
        arr.append(i['chapter_number'])
    arr.sort()
    # print(arr)
    return render(request, 'accounts/resources.html',{'contents':pdfs_objects,'chapters':arr })