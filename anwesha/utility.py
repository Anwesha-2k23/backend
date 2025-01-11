import hashlib
from typing import Any
import uuid
import jwt
import qrcode
from django.core.files import File
from io import BytesIO
from django.core.mail import send_mail
from anwesha.settings import EMAIL_HOST_USER, COOKIE_ENCRYPTION_SECRET
import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import csv
from django.http import HttpResponse, JsonResponse
import bcrypt
import hmac
import base64
from requests import post
from anwesha.settings import COOKIE_ENCRYPTION_SECRET, EMAIL_MICROSERVICE_ENDPOINT

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

def verification_mail(email, user):
    """
    Sends a verification email to the given email address.

    Args:
        email (str): Email address to send the email to.
        user (str): User's name.

    Returns:
        int: Number of successfully sent emails.
    """
    payload = {
        'email': email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(
        payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
    link = "https://backend.anwesha.live/campasambassador/verifyemail/" + token
    localhost_link = "http://127.0.0.1:8000/campasambassador/verifyemail/"
    subject = "No reply"
    body = f'''
    Hello {user},\n\n
        Please click on the link below to verify your email address for anwesha login:
         \n{localhost_link}
        \n\nThanks,
        \nTeam  Anwesha
    '''
    recipient_list = [email]
    # res = send_mail(subject, body, EMAIL_HOST_USER, recipient_list)
    send_email_using_microservice(email,subject,body)


def hashpassword(password):
    """
    Hashes the given password using SHA256 algorithm.

    Args:
        password (str): Password to hash.

    Returns:
        str: Hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def createId(prefix, length):
    """
    Utility function to create a random ID of given length.

    Args:
        prefix (str): Prefix of the ID (e.g., "TEAM", "ANW").
        length (int): Length of the ID excluding the prefix.

    Returns:
        str: Randomly generated ID.
    """
    id = str(uuid.uuid4()).replace("-", "")
    return prefix + id[:length]


def checkPhoneNumber(phone_number: str):
    """
    Checks if the given phone number is valid or not.

    Args:
        phone_number (str): Phone number to check.

    Returns:
        None
    """
    pass


def isemail(email_id: str):
    """
    Checks if the given email ID is valid or not.

    Args:
        email_id (str): Email ID to check.

    Returns:
        bool: True if the email ID is valid, False otherwise.
    """
    if "@" in email_id:
        return True
    return False


def get_anwesha_id(request):
    """
    Retrieves the anwesha_id of the user from the cookie.

    Args:
        request: Django request object.

    Returns:
        str: Anwesha ID of the user.
    """
    token = request.COOKIES.get("jwt")
    if not token:
        return None
    try:
        payload = jwt.decode(token, "ufdhufhufgefef", algorithms="HS256")
        id = payload["id"]
        return id
    except jwt.ExpiredSignatureError:
        return None


def generate_qr(anwesha_id,hash):
    """
    Generates a QR code for the given Anwesha ID.

    Args:
        anwesha_id (str): Anwesha ID.

    Returns:
        File: QR code image file.
    """
    img = qrcode.make(hash)
    blob = BytesIO()
    img.save(blob, "PNG")
    qr = File(blob, name=anwesha_id + "-qr.png")
    return qr


def generate_jwt_token(anwesha_id):
    """
    Generates a JWT token for the given Anwesha ID.

    Args:
        anwesha_id (str): Anwesha ID.

    Returns:
        str: JWT token.
    """
    return anwesha_id


def export_as_csv(self, request, queryset):
    """
    Exports the queryset as a CSV file.

    Args:
        self: Django model admin object.
        request: Django request object.
        queryset: Queryset to export.

    Returns:
        HttpResponse: HTTP response with the CSV file.
    """
    restricted_fields = [
        'password',
        'is_loggedin',
        'validation',
        'profile_photo',
        'intrests',
        'is_email_verified',
        'is_profile_completed',
        'is_locked',
    ]
    meta = self.model._meta
    field_names = []
    for field in meta.fields:
        if field.name not in restricted_fields:
            field_names.append(field.name)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


def check_token(request):
    """
    Checks the token from the request's cookie.

    Args:
        request: Django request object.

    Returns:
        JsonResponse: JSON response with the token payload or an error message.
    """
    token = request.COOKIES.get('jwt')

    if not token:
        return JsonResponse({"message": "you are unauthenticated, Please Log in First"}, status=401)

    try:
        payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        return JsonResponse({"message": "Your token is expired, please login again"}, status=409)


def hash_password(password: str):
    """
    Hashes a password for storing.

    Args:
        password (str): The password to hash.

    Returns:
        str: A string of length 60, containing the algorithm used and the hashed password.
    """
    return str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))[2:-1]


def check_password(password1: str, password2: str):
    """
    Checks a hashed password using bcrypt.

    Args:
        password1 (str): The password to check.
        password2 (str): The hash to check the password against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    result = bcrypt.checkpw(password1.encode('utf-8'), password2.encode('utf-8'))
    return result


class EmailSending:
    def __init__(self, user) -> None:
        self.address = user.email_id
        self.subject = None
        self.body = None
        self.user = user

    def email_varification(self):
        """
        Sends an email verification email.

        Returns:
        int: Number of successfully sent emails.
        """
        payload = {
            'id': self.user.anwesha_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(
            payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
        link = "https://backend.anwesha.live/user/verifyemail/" + token
        localhost_link = "http://127.0.0.1:8000/user/verifyemail/" + token
        subject = "No reply"
        body = f'''
        Hello {self.address},\n
            Please click on the link below to verify your email address for anwesha login:
             \n{link}
            \n\nThanks,
            \nTeam  Anwesha
        '''
        recipient_list = [self.address]
        res = send_mail(subject, body, EMAIL_HOST_USER, recipient_list)
        print(res)
        return res


def hash_id(anwesha_id, secret):
    """
    Hashes the given Anwesha ID using HMAC-SHA256.

    Args:
        anwesha_id (str): Anwesha ID to hash.
        secret (str): Secret key.

    Returns:
        str: Hashed ID.
    """
    anwesha_id = anwesha_id.encode('utf-8')
    secret = secret.encode('utf-8')
    digest = hmac.new(secret, msg=anwesha_id, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()
    return signature
