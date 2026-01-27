from django.http import JsonResponse
from typing import Any
from .models import User,AppUsers
from requests import post
import jwt
import datetime
from anwesha.settings import COOKIE_ENCRYPTION_SECRET, EMAIL_MICROSERVICE_ENDPOINT,CONFIGURATION

class Autherize:
    """
    Authorization decorator class.

    Attributes:
        mode (int): Mode of the decorator.

    Methods:
        __init__(self, mode): Initializes the Autherize instance.
        __call__(self, func): Decorator method to authorize the function.
    """

    def __init__(self, mode=1) -> None:
        """
        Initializes the Autherize instance.

        Args:
            mode (int): Mode of the decorator.
        """
        self.mode = mode

    def __call__(self, func) -> Any:
        """
        Decorator method to authorize the function.

        Args:
            func: Function to be authorized.

        Returns:
            Any: Result of the function call or error response.

        Raises:
            jwt.ExpiredSignatureError: If the token is expired.
        """
        def wrapper(*args, **kwargs):
            request = args[1]
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({"message": "You are unauthenticated. Please log in first."}, status=401)
            token = auth_header.split(' ', 1)[1].strip()

            try:
                payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
            except jwt.ExpiredSignatureError:
                return JsonResponse({"message": "Your token is expired. Please login again."}, status=409)

            user = User.objects.get(anwesha_id=payload["id"])

            if not user:
                return JsonResponse({"message": "User not found."}, status=404)

            kwargs["user"] = user

            return func(*args, **kwargs)
        return wrapper

"""
This is a utility function to generate content for the email.

Parameters:
- type (int): Type of email content to generate.
- kwargs (dict): Additional keyword arguments based on the type of email.

Returns:
- str: Generated email content.

Precautions:
- Ensure that the appropriate kwargs are provided for the specified email type.
- Make sure to handle the return value of None when the email type is not supported.
"""
def mail_content(type, *args, **kwargs):
    if type == 1:
        email = kwargs['email_id']
        user = kwargs['full_name']
        anwesha_id = kwargs['anwesha_id']
        payload = {
            'email': email,
            'id': anwesha_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=7200),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
        if CONFIGURATION == 'local':
            link = "http://localhost:8000/user/verifyemail/"+token
        else:
            link = "https://anwesha.shop/user/verifyemail/" + token
        body = f'''Hello {user},

Thank you for being part of Anwesha 2025.
Your Anwesha ID is: {anwesha_id}.
Please click on the link below to verify your email address for Anwesha login:
{link}

The above link will be valid for 5 days.
Please ignore if already verified.

Thanks,
Team Anwesha
'''
    else:
        return None
    return body

def send_email_using_microservice(email_id, subject, text):
    """
    Sends an email using an external mail API.

    Parameters:
    - email_id (str): Email ID of the recipient.
    - subject (str): Subject of the email.
    - text (str): Content of the email.

    Precautions:
    - Ensure that the EMAIL_MICROSERVICE_ENDPOINT is properly configured.
    - Handle any exceptions or errors that may occur during the email sending process.
    """
    PARAM = {
        "to": email_id,
        "subject": subject,
        "text": text
    }
    r = post(url=EMAIL_MICROSERVICE_ENDPOINT, data=PARAM)



class AppAutherize:
    """
    Authorization decorator class.

    Attributes:
        mode (int): Mode of the decorator.

    Methods:
        __init__(self, mode): Initializes the Autherize instance.
        __call__(self, func): Decorator method to authorize the function.
    """

    def __init__(self, mode=1) -> None:
        """
        Initializes the Autherize instance.

        Args:
            mode (int): Mode of the decorator.
        """
        self.mode = mode

    def __call__(self, func) -> Any:
        """
        Decorator method to authorize the function.

        Args:
            func: Function to be authorized.

        Returns:
            Any: Result of the function call or error response.

        Raises:
            jwt.ExpiredSignatureError: If the token is expired.
        """
        def wrapper(*args, **kwargs):
            request = args[1]
            auth_header = request.headers.get('Authorization')
            # print("got token successfully")
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({"message": "You are unauthenticated. Please log in first."}, status=401)

            token = auth_header.split(' ', 1)[1].strip()

            try:
                payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
                # print("payload decoded .")
            except jwt.ExpiredSignatureError:
                return JsonResponse({"message": "Your token is expired. Please login again."}, status=409)

            user = AppUsers.objects.get(id=payload["id"])
            # print("user found")
            if not user:
                return JsonResponse({"message": "User not found."}, status=404)

            # kwargs["user"] = user

            return func(*args, **kwargs)
        return wrapper
