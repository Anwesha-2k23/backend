from django.http import JsonResponse
from typing import Any
from .models import User
from requests import post
import jwt
import datetime
from anwesha.settings import COOKIE_ENCRYPTION_SECRET ,EMAIL_MICROSERVICE_ENDPOINT

class Autherize:
    def __init__(self, mode = 1) -> None:
        self.mode = mode

    def __call__(self, func) -> Any:
        def wrapper(*args, **kwargs):
            request = args[1]
            token = request.COOKIES.get('jwt')
            if not token:
                return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

            try:
                payload = jwt.decode(token,COOKIE_ENCRYPTION_SECRET , algorithms = 'HS256')
                
            except jwt.ExpiredSignatureError:
                return JsonResponse({"message":"Your token is expired please login again"},status=409)
        
            user = User.objects.get(anwesha_id = payload["id"]) 

            if not user:
                return JsonResponse({"message":"User not found"},status=404)
            
            kwargs["user"] = user

            return func(*args, **kwargs)
        return wrapper
        
"""
this is a utility function to generate content for the mail

## type == 1

    it will create template for user email verification 
        it will require email id , anwesha ID and full name in kwargs
"""
def mail_content(type , *args ,**kwargs):
    if(type == 1):
        email = kwargs['email_id']
        user = kwargs['full_name']
        anwesha_id = kwargs['anwesha_id'] 
        payload = {
            'email':email,
            'id':anwesha_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(
            payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
        link = "https://backend.anwesha.live/user/verifyemail/"+token
        body = f'''Hello {user},\n\nThank you for being part of Anwesha 2023 \nYour Anwesha ID is :- {anwesha_id} \nPlease click on the link below to verify your email address for anwesha login:\n{link}\n\nThanks,\nTeam  Anwesha
        '''
    else:
        return None
    return body

def send_email_using_microservice(email_id , subject , text):
    PARAM = {
        "to": email_id,
        "subject":subject,
        "text":text
    }
    r = post(url = EMAIL_MICROSERVICE_ENDPOINT , data = PARAM)
