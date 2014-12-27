from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from ask.models import Profile, Question, Answer, Tags, Like, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login, logout

# Create your views here.

def index(req):
    num_page = req.GET.get('page')

    q = Question.objects.all()[:32]
    p = Paginator(q, 5)
    try:
        page = p.page(num_page)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)

    context = {
        "questions":  page.object_list,
        "paginators": p.page_range,
    }

    return render(req, 'index.html', context)

def login(req):
    if req.user.is_authenticated():
        logout(req)
        return render(req, 'login.html')

    username = ""
    path = req.META.get('HTTP_REFERER', None) 
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
                return redirect(path)
    except:
        return render(req, 'index.html')
    context = {
        "username":  username,
        "path" : path,
    }
    return render(req, 'login.html', context)


def signup(req):

    username = ""
    email = ""
    path = req.META.get('HTTP_REFERER', None) 
    try:
        path_get = req.GET.get('red', False)
        if path_get is not False:
            path = path_get
        username = req.POST.get('username', False)
        email = req.POST.get('email', False)
        password = req.POST.get('password', False)
        u = User.objects.create_user(username, email, password)
        p = Profile.objects.create(user_id=u.id, rating = 0)
        return redirect(path)
    except:
        username = username
    context = {
        "username":  username,
        "email" : email,
        "path" : path,
    }
    return render(req, 'signup.html', context)

def question(req, quest):
    num_page = req.GET.get('page')
    q = Answer.objects.all().filter(question = int(quest))
    p = Paginator(q, 5)
    try:
        page = p.page(num_page)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    context = {
        "question": Question.objects.all().get(id=int(quest)),
        "answers" : page.object_list,
        "paginators": p.page_range,
    }

    if context["question"]:
        return render(req, 'question.html', context)
    else:
        return render(req, 'signup.html')

def add(req):
    if not req.user.is_authenticated():
        return login(req)

    text= ""
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