from django.shortcuts import render
from django.http import JsonResponse
from .models import City
from django.views import View

# Create your views here.

class Get_City(View):
    def get(self, request, city):
        try:
            city_name = City.objects.get(city_name=city)
            city_name = city_name.__dict__
            city_name.pop('_state')
            return JsonResponse(city_name, safe=False)
        except:
            response = JsonResponse({"message": "Error occured"})
            return response

class Get_All_Cities(View):
    def get(self,request):
        try:
            cities = City.objects.all()
            cities = list(cities.values("city_name","poster","date"))
            return JsonResponse(cities,safe=False)
        except:
            return JsonResponse({"message":"Error occured"},safe=False)
