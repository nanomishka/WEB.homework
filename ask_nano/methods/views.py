from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    output = "Hello world in Django!!!\n"
    output +='<form method="post">'
    output +='<input type="text" name="test">'
    output +='<input type="submit">'
    output +='</form>'
	
    if len(request.GET.items()):
        output += '<h1>GET</h1>'
        for key, value in request.GET.items():
            output += str(key) + ' = ' + str(value) + " | "
            output += '\n'
    if request.method == 'POST':
        output += '<h1>POST</h1>'
        for key, value in request.POST.items():
            output += str(key) + ' = ' + str(value) + " | "
    return HttpResponse(output)