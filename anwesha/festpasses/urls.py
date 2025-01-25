from django.urls import path
from .views import *

festpasses_urls = [
    path('atompay',payview,name="payview"),
    path('response',resp,name="response"),
    path('register',festpasses.as_view(),name="festpasses")
]