from django.urls import path
# from campus_ambassador.models import campus_ambassador
from .views import payview,resp

atom_pay_urls = [
    path('merch' , payview , name='payView'),
    path('response', resp, name='response'),
]
