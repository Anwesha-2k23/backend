import hashlib
import uuid
import jwt
import qrcode
from django.core.files import File
from io import BytesIO
from django.core.mail import send_mail
from anwesha.settings import EMAIL_HOST_USER ,COOKIE_ENCRYPTION_SECRET
import datetime
from django.template.loader import render_to_string 
from django.utils.html import strip_tags
import csv
from django.http import HttpResponse ,JsonResponse
import bcrypt

def verification_mail(email , user):
    payload = {
        'email':email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(
        payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
    link = "https://backend.anwesha.live/campasambassador/verifyemail/"+token
    localhost_link = "http://127.0.0.1:8000/campasambassador/verifyemail/"+token
    subject = "No replay"
    # html_content = render_to_string('mail_template.html', {'varname':'value'}) # render with dynamic value
    # text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.
    body = f'''
    Hello {user},\n
        Please click on the link below to verify your email address for anwesha login:
         \n{link}
        \n\nThanks,
        \nTeam  Anwesha
    '''
    recipient_list = []
    recipient_list.append(email)
    res = send_mail(subject, body, EMAIL_HOST_USER, recipient_list)
    return res

def hashpassword(password):
    return hashlib.sha256(password.encode()).hexdigest()


def createId(prefix, length):
    """
    Utility function to create a random id of given length
    prefix : prefix of the id ( ex : "TEAM", "ANW" )
    length : length of the id excluding the prefix
    """

    id = str(uuid.uuid4()).replace("-", "")
    return prefix + id[:length]


def checkPhoneNumber(phone_number: str):
    """
    Utility function to check if the given phone number is valid or not
    """
    pass


def isemail(email_id: str):
    """
    Utility function to check if the given email id is valid or not
    """
    if "@" in email_id:
        return True
    return False


def get_anwesha_id(request):
    """
    Utility function to get the anwesha_id of the user from the cookie
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


def generate_qr(anwesha_id):
    img = qrcode.make(anwesha_id)
    blob = BytesIO()
    img.save(blob, "PNG")
    qr = File(blob, name = anwesha_id + "-qr.png")
    return qr
    # img.save(anwesha_id+".png")

def generate_jwt_token(anwesha_id):
    return anwesha_id


def export_as_csv(self, request, queryset):
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

    print(field_names)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

def check_token(request):
    '''
    :TODO: Find a more efficient way to check token and return errors messages
    '''
    token = request.COOKIES.get('jwt')

    if not token:
        return JsonResponse({"message": "you are unauthenticated , Please Log in First"} , status=401)

    try:
        payload = jwt.decode(token,COOKIE_ENCRYPTION_SECRET , algorithms = 'HS256')
        return payload
    except jwt.ExpiredSignatureError:
        return JsonResponse({"message":"Your token is expired please login again"},status=409) 
    

def hash_password(password: str):
    """
    Hash a password for storing.
    :param password: The password to hash.
    :return: A string of length 60, containing the algorithm used and the hashed password.
    """
    return str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))[2:-1]

def check_password(password1: str, password2: str):
    """
    Check a hashed password. Uses bcrypt, the salt is saved into the hash itself
    :param password1: The password to check.
    :param password2: The hash to check the password against.
    :return: True if the password matched, False otherwise.
    """
    result =  bcrypt.checkpw(password1.encode('utf-8'), password2.encode('utf-8'))
    return result

