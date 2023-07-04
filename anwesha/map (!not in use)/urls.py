from django.urls import path
# from campus_ambassador.models import campus_ambassador
from .views import Get_City,Get_All_Cities

map_urls = [
    path('allcities' , Get_All_Cities.as_view() , name='allcities'),
    path('<str:city>' ,Get_City.as_view(), name='get_city_by_name'),
]