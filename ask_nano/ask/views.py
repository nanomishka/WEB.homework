from django.shortcuts import render, redirect, HttpResponse
from django.template import RequestContext, loader
from ask.models import Profile, Question, Answer, Tags, Like, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login, logout
from django import forms
from django.core.files import File
import md5
from django.http import JsonResponse

# Create your views here.

class UploadFileForm(forms.Form):
    file = forms.FileField()

def index(req):
    num_page = req.GET.get('page')

    q = Question.objects.all().order_by('-id')
    p = Paginator(q, 10)
    if req.user.is_authenticated():
        prof = Profile.objects.get(user_id=req.user.id);
    else:
        prof = ""
    try:
        page = p.page(num_page)
    except PageNotAnInteger:
        page = p.page(1)
        num_page = 1;
    except EmptyPage:
        page = p.page(p.num_pages)
        num_page = p.num_pages
    for quest in page:
        quest.count = quest.answer_set.count()
        quest.tags = quest.tags_set.all()
        if prof != "":
            like = Like.objects.filter(question = quest, author  = prof)
            if like.exists():
                quest.voice = 0
            else:
                quest.voice = 1
        else:
            quest.voice = 1
    
    k = []
    for i in range(int(num_page)-4, int(num_page)+4):
        if i in p.page_range:
            k.append(i)

    context = {
        "profile": prof,
        "questions":  page,
        "paginators": k,
        "all_pages": p.num_pages
    }

    return render(req, 'index.html', context)

def question(req, quest):
    num_page = req.GET.get('page')

    question = Question.objects.all().get(id=int(quest))
    
    answers = Answer.objects.all().filter(question = int(quest))
    p = Paginator(answers, 5)
    try:
        page = p.page(num_page)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)

    if req.user.is_authenticated():
        prof = Profile.objects.get(user_id=req.user.id);
    else:
        prof = ""

    context = {
        "question": question,
        "count": question.answer_set.count(),
        "tags": question.tags_set.all(),
        "answers" : page,
        "profile" : prof,
        "likes" : question.like_set.count(),
    }

    if context["question"]:
        return render(req, 'question.html', context)
    else:
        return render(req, 'signup.html')

def login(req):
    if req.user.is_authenticated():
        logout(req)
        index(req)

    username = ""
    path = req.META.get('HTTP_REFERER', None) 
    refer = path
    try:
        username = req.POST.get('username', False)
        password = req.POST.get('password', False)
        path_get = req.GET.get('red', False)
        if path_get is not False:
            path = path_get
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(req, user)
                #if path_get is not None
                #    return redirect(path)
                #else
                #    index(req)

    except:
        return render(req, 'index.html')
    context = {
        "username":  username,
        "path" : path,
    }
    return render(req, 'login.html', context)


def signup(req):

    form = UploadFileForm(req.POST, req.FILES)

    username = ""
    email = ""
    path = req.META.get('HTTP_REFERER', None) 
    try:
        path_get = req.GET.get('red', False)
        if path_get is not False:
            path = path_get
        else:
            path = "/"
        username = req.POST.get('username', False)
        email = req.POST.get('email', False)
        password = req.POST.get('password', False)
        u = User.objects.create_user(username, email, password)
        p = Profile.objects.create(user_id=u.id, rating = 0, avatar_url="user"+str(u.id)+".jpeg")

        if req.method == 'POST':
            if form.is_valid():
                handle_uploaded_file(req.FILES['file'],u.id)
        return redirect(path)
    except:
        username = username
    context = {
        "username":  username,
        "email" : email,
        "path" : path,
        "check" : form,
    }
    return render(req, 'signup.html', context)


def add(req):
    if not req.user.is_authenticated():
        return login(req)

    text=""
    title=""

    try:
        title = req.POST.get('title', False)
        text = req.POST.get('text', False)
        if title and text:
            p = Profile.objects.get(user_id=req.user.id);
            q = Question.objects.create(title=title,text=text,author=p,rating=0)
        return redirect("/question/"+str(q.id))     
    except:
        title = title
        text = text
    context = {
        "title": title,
        "text" : text,
    }
    return render(req, 'add.html', context)

def response(req, quest):
    if not req.user.is_authenticated():
        return login(req)

    p = Profile.objects.get(user_id=req.user.id);
    q = Question.objects.get(id=int(quest))
    try:
        text = req.POST.get('text', False)
        q = Answer.objects.create(text=text,author=p, question=q )
    except:
        text = text
    return redirect("/question/"+quest) 

def profile(req):
    if not req.user.is_authenticated():
        return login(req)


    form = UploadFileForm(req.POST, req.FILES)
    p = Profile.objects.get(user_id=req.user.id);
    context = {}

    username = req.POST.get('username', False)
    if username != False and username != p.user.username:
        p.user.username = username
        p.user.save()
        context["stname"] = "changed"
    
    email = req.POST.get('email', False)
    if email != False and email != p.user.email:
        p.user.email = email
        p.user.save()
        context["stemail"] = "changed"

    oldpass = req.POST.get('oldpass', False)
    newpass = req.POST.get('pass2', False)
    if (username != "") and (newpass != ""):
        if p.user.check_password(oldpass):
            p.user.set_password(newpass)
            p.user.save()
            context["stpass"] = "changed"

    if req.method == 'POST':
        if form.is_valid():
            handle_uploaded_file(req.FILES['file'],req.user.id)
            context["stavatar"] = "changed"
            p.avatar_url = "user"+str(req.user.id)+".jpeg"
            p.save()

    context["profile"] = Profile.objects.get(user_id=req.user.id)
    context["check"] = form

    return render(req, 'profile.html', context)

def like(req):
    if not req.user.is_authenticated():
        status = "error"
        new_rating = 0;
    else:
        id = int(req.POST.get('id', False))
        type = req.POST.get('type', False)

        question = Question.objects.all().get(id=id)
        profile = Profile.objects.get(user_id=req.user.id);

        likes = Like.objects.filter(question = question, author  = profile)

        if likes.exists():
            status = "error"
            new_rating = 0;
        else:
            new_rating = question.rating
            status = "ok"
            if type == "like":
                value = True
                new_rating += 1
            else:
                value = False
                new_rating -= 1

            like = Like.objects.create(question = question, author  = profile, status = value)
            question.rating = new_rating
            question.save()

    context = JsonResponse({'status': status, 'new_rating': new_rating})

    return context

def handle_uploaded_file(f, id):
    with open('/home/nano/web/ask_nano/uploads/user'+str(id)+'.jpeg', 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)