from django.shortcuts import render

from django.db import IntegrityError
from django.http import JsonResponse
from .models import Book
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

# DJANGO REST FRAMEWORK (DRF) Imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# Create your views here.

# @csrf_exempt
# def books(request):
#     if request.method == 'GET':
#         books = Book.objects.all().values()
#         return JsonResponse({'books': list(books)})

#     elif request.method == 'POST':
#         title = request.POST.get('title')
#         author = request.POST.get('author')
#         price = request.POST.get('price')
#         book = Book.object(title=title, author=author, price=price)

#         try:
#             book.save()
#         except IntegrityError as e:
#             return JsonResponse({'error':'true','message': e},status=400)
    
    # return JsonResponse(model_to_dict(books), status=400)

@api_view(['POST'])
def books(request):
    return Response('List of the books', 
                    status=status.HTTP_200_OK)