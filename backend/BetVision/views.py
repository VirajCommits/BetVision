from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


@api_view(['GET'])
def home(request):
    return JsonResponse({"message": "Welcome to the home page!"})  # Correct return type