from django.shortcuts import render

# Create your views here.

def index(req):
    return render(req, 'index.html')

def login(req):
    return render(req, 'login.html')

def signup(req):
    return render(req, 'signup.html')