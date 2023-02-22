from django.http import JsonResponse
from typing import Any
from .models import User
import jwt
from anwesha.settings import COOKIE_ENCRYPTION_SECRET

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