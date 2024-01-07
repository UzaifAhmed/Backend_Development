from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# from .models import Menu
# Create your views here.

def home(request):
    path = request.path
    request = HttpResponse(path, content_type='text/html', charset='utf-8')
    return request
    # return HttpResponse('Welcome to Little Lemon restaurant!')

def display_date(request):
    date_joined = datetime.today().year
    return HttpResponse(date_joined)

def menu(request):
    text = """<h1 style="color: #F4CE14"> This is Colored Little Lemon</h1>"""
    return HttpResponse(text)

def menuitems(request, dish):
    items = {
        'pasta': 'Pasta is a type of noodle',
        'falafel': 'Falafel are deep fried patties',
        'cheesecake': 'Cheesecake is a type of dessert'
    }
    description = items[dish]
    return HttpResponse(f'<h2 style="color: #B4CA64"> {dish} </h2>' +description)
# def menu_by_id(request, menu_by_id):
#     menu = Menu.objects.get(pk=menu_id)
#     # return HttpResponse(f"{menu.menu_item}: Type of {menu.cuisine} cuisine")
#     return render(request, 'menu_card.html', {'menu':menu})