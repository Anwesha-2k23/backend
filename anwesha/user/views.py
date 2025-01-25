import shutil
from multiprocessing import AuthenticationError
from django.http import JsonResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from anwesha.settings import AWS_S3_CUSTOM_DOMAIN, COOKIE_ENCRYPTION_SECRET
import jwt
from utility import hashpassword, createId, isemail, generate_qr, EmailSending, hash_id,send_email_using_microservice,checkPhoneNumber
import time
from .utility import Autherize, mail_content
from anwesha.settings import  AWS_PUBLIC_MEDIA_LOCATION2
from django.shortcuts import redirect
from anwesha.settings import CONFIGURATION,BASE_DIR
import os
import re
import threading

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently=False) 


class Login(APIView):
    def get(self, request):
        # Retrieve the token from the request cookies
        token = request.COOKIES.get('jwt')

        if not token:
            # Return an error response if the token is not present
            return JsonResponse({"message": "You are unauthenticated. Please log in first."}, status=401)

        try:
            # Decode the token using the secret key
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            # Return an error response if the token has expired
            return JsonResponse({"message": "Your token is expired. Please generate a new one."}, status=409)

        try:
            # Retrieve the user based on the decoded token
            user = User.objects.get(anwesha_id=payload["id"])

            if user.is_email_verified:
                user.is_loggedin = True
                user.save()
                
                if CONFIGURATION == "local":
                    qr_code = str(os.path.join(BASE_DIR,""))+str(user.qr_code)
                else:
                    qr_code = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/' + AWS_PUBLIC_MEDIA_LOCATION2 + str(user.qr_code)
                
                # Create a response object
                response = Response()
                response.data = {
                    "mssg": "Welcome",
                    "full_name": user.full_name,
                    "anwesha_id": user.anwesha_id,
                    "user_type": user.user_type,
                    "status": "200",
                    "qr_code": qr_code
                }

                return response
            else:
                # Return an error response if the user's email is not verified
                return JsonResponse({"message": "Your email is not verified. Please verify your email to continue further."}, status=403)
        except:
            # Return an error response if the token is invalid or user does not exist
            return JsonResponse({"message": "Invalid token."}, status=409)

    def post(self, request):
        response = Response()

        try:
            # Retrieve the username and password from the request data
            username = request.data['username']
            password = request.data['password']
        except:
            # Return an error response if the input is incorrect
            response.data = {"status": "Incorrect input"}
            response.status = 404
            return response

        password = hashpassword(password)
        user = None

        if isemail(username):
            # Check if the username is an email address
            user = User.objects.filter(email_id=username, password=password)
        else:
            user = User.objects.filter(anwesha_id=username, password=password)

        this_user = user.first()

        if user:
            if this_user.is_email_verified:
                # Create a JWT token for the authenticated user
                payload = {
                    "id": this_user.anwesha_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
                    "iat": datetime.datetime.utcnow()
                }
                token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')

                this_user.is_loggedin = True
                this_user.save()
                
                if CONFIGURATION == "local":
                    qr_code = str(os.path.join(BASE_DIR,""))+str(this_user.qr_code)
                else:
                    qr_code = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/' + AWS_PUBLIC_MEDIA_LOCATION2 + str(this_user.qr_code)

                response.data = {
                    "success": True,
                    "name": this_user.full_name,
                    "anwesha_id": this_user.anwesha_id,
                    "user_type": this_user.user_type,
                    "qr_code": qr_code,
                    "status": 200,
                    "token":token
                }

                # Set the JWT token as a cookie in the response
                response.set_cookie(key='jwt', value=token, httponly=True, samesite="None",secure=True)
                return response
            else:
                # Return an error response if the user's email is not verified
                return JsonResponse({"message": "Please verify your email to log in to your account."}, status=403)
        else:
            # Return an error response if the credentials are incorrect
            return JsonResponse({"message": "Incorrect credentials."}, status=401)

    def options(self, request):
        # Return a success response for the OPTIONS request
        return Response("200")

class LogOut(APIView):
    def post(self, request):
        # Retrieve the token from the request cookies
        token = request.COOKIES.get('jwt')

        if not token:
            return Response({"message":"Unauthenticated"},status=401)
        else:
            try:
                # Decode the token using the secret key
                payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
            except jwt.ExpiredSignatureError:
                # Raise an AuthenticationError if the token has expired
                raise AuthenticationError("Cookie Expired")

            # Retrieve the user based on the decoded token
            user = User.objects.get(anwesha_id=payload["id"])

            # Update the user's logged-in status and save the user object
            user.is_loggedin = False
            user.save()

            # Create a response object
            response = Response()

            # Delete the 'jwt' cookie from the response
            response.delete_cookie(key='jwt',samesite='None')
            #response.delete_cookie('jwt')

            response.data = {'message': 'Logout Successful', "status": "200"}
            return response

class Register(APIView):
    def post(self, request):

        stime = time.time()
        
        try:
            # Retrieve data from the request
            password = request.data['password']
            email_id = request.data['email_id']
            full_name = request.data['full_name']
            phone_number = request.data['phone_number']
            college_name = request.data['college_name']
            user_type = request.data['user_type']

            """
            Data validation
            """
            if not isemail(email_id):
                return JsonResponse({"message": "Please enter a valid email"}, status=409)
            if not checkPhoneNumber(phone_number):
                return JsonResponse({"message":"Please enter a valid phone number"},status=409)
            if User.objects.filter(email_id=email_id).exists():
                return JsonResponse({'message': 'A user with the same email already exists', 'status': '409'}, status=409)

            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message': 'A user with the same phone number already exists', 'status': '409'}, status=409)

            """
            Assigning user types
            """
            if user_type == "iitp_student":
                user_type = User.User_type_choice.IITP_STUDENT
            elif user_type == "student":
                user_type = User.User_type_choice.STUDENT
            elif user_type == "non-student":
                user_type = User.User_type_choice.NON_STUDENT
            elif user_type == "alumni":
                user_type = User.User_type_choice.ALUMNI
            elif user_type == "faculty":
                user_type = User.User_type_choice.GUEST
            else:
                return JsonResponse({"message": "Please enter a proper user type"}, status=403)
            pattern = r"^[a-zA-Z0-9]+_\d{2}[a-zA-Z]\d{2}res\d+@iitp\.ac\.in$"
            if re.match(pattern, email_id):
                user_type = User.User_type_choice.STUDENT
        except KeyError:
            return JsonResponse({"message": "Required form data not received"}, status=401)

        # Create a new user object
        new_user = User.objects.create(
            full_name=full_name,
            email_id=email_id,
            password=password,
            phone_number=phone_number,
            is_email_verified=False,
            user_type=user_type,
            collage_name=college_name,
        )
        new_user.save()

        # Prepare and send an email
        text = mail_content(type=1, email_id=email_id, full_name=full_name, anwesha_id=new_user.anwesha_id)
        sendMail = EmailMessage(
                    "No reply",
                    text,
                    "anwesha.backed@gmail.com",
                    [email_id],
                    )
        EmailThread(sendMail).start()
        #send_email_using_microservice(
        #    email_id=email_id,
        #    subject="No reply",
        #    text=text
        #)

        return JsonResponse({'message': 'User created successfully!', "status": "201"})


class EditProfile(APIView):
    @Autherize()  # Apply the authentication decorator if applicable
    def get(self, request, **kwargs):
        user = kwargs['user']
        response = Response()
        
        if CONFIGURATION == "local":
            qr_code = str(os.path.join(BASE_DIR,""))+str(user.qr_code)
        else:
            qr_code = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/' + AWS_PUBLIC_MEDIA_LOCATION2 + str(user.qr_code)
        
        response.data = {
            "anwesha_id": user.anwesha_id,
            "full_name": user.full_name,
            "phone_number": user.phone_number,
            "email_id": user.email_id,
            "college_name": user.collage_name,
            "age": user.age,
            "is_email_verified": user.is_email_verified,
            "gender": user.gender,
            "is_profile_completed": user.is_profile_completed,
            "profile_picture": str(user.profile_photo),
            "user_type": user.user_type,
            "qr_code": qr_code
        }
        return response

    @Autherize()  # Apply the authentication decorator if applicable
    def post(self, request, **kwargs):
        user = kwargs['user']
        data = request.data

        # Update fields if provided, otherwise retain the current values
        full_name = data.get('full_name', user.full_name)
        college_name = data.get('college_name', user.collage_name)
        age = data.get('age', user.age)

        # Map the gender value to the corresponding enum value
        gender = user.gender
        if 'gender' in data:
            if data['gender'] == 'male':
                gender = User.Gender.MALE
            elif data['gender'] == 'female':
                gender = User.Gender.FEMALE
            elif data['gender'] == 'rather_not_say':
                gender = User.Gender.RATHER_NOT_SAY

        # Update social media IDs if provided, otherwise retain the current values
        instagram_id = data.get('instagram_id', user.instagram_id)
        facebook_id = data.get('facebook_id', user.facebook_id)

        # Update profile photo if provided, otherwise retain the current value
        profile_photo = data.get('profile_photo', user.profile_photo)

        # Update the user object with the new data
        user.full_name = full_name
        user.collage_name = college_name
        user.instagram_id = instagram_id
        user.facebook_id = facebook_id
        user.profile_photo = profile_photo
        user.age = age
        user.gender = gender
        user.save()

        response = Response()
        response.data = {
            'message': 'Profile successfully updated!'
        }
        return response

class SendVerificationEmail(APIView):
    def post(self, request):
        try:
            email = request.data["email_id"]

            # Check if the user with the provided email exists
            if User.objects.filter(email_id=email).exists():
                try:
                    # Generate a verification token with an expiration time
                    payload = {
                        "email": email,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=10),
                        "iat": datetime.datetime.utcnow()
                    }
                    token = jwt.encode(payload=payload, key=COOKIE_ENCRYPTION_SECRET, algorithm="HS256")
                    return JsonResponse({"token": token}, status=201)
                except:
                    return JsonResponse({"message": "Token cannot be generated"}, status=409)
            else:
                return JsonResponse({"message": "No such email exists"}, status=409)
        except:
            return JsonResponse({"message": "Bad request"}, status=400)


def verifyEmail(request, *args, **kwargs):
    if request.method == 'GET':
        token = kwargs['pk']

        try:
            # Decode the token using the provided encryption secret
            jwt_payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Token expired"}, status=409)
        except jwt.DecodeError:
            return JsonResponse({"message": "Invalid token"}, status=401)

        try:
            # Retrieve the user to be verified based on the decoded token
            user_to_verify = User.objects.get(anwesha_id=jwt_payload['id'])
            user_to_verify.is_email_verified = True
            user_to_verify.save()
        except User.DoesNotExist:
            return JsonResponse({"message": "Invalid token"}, status=401)

        return redirect('https://anwesha.iitp.ac.in/userLogin')


class ForgetPassword(APIView):
    def get(self, request):
        # This method is for clicking the sent link
        pass

    def post(self, request):
        # This method is for posting the email address and sending the reset password link via email

        if not request.data.get('email'):
            return Response({"message": "Email is missing"}, status=400)

        try:
            user = User.objects.get(email_id=request.data['email'])

            # Create a payload for the JWT token containing the user ID and expiration time
            payload = {
                'userid': user.anwesha_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10),
                "iat": datetime.datetime.utcnow()
            }

            # Encode the payload into a token using the provided encryption secret
            token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')

            # Create the reset password link with the token
            link = "http://anwesha.iitp.ac.in/user/reset_password/" + token

            # Compose the email text
            text = f'''Hello {user.full_name}!\nThis is the link to change your password. Click on it to update your password:\n{link}\nPS: Please don't share it with anyone.\nThanks,\nTeam Anwesha'''
            

            sendMail = EmailMessage(
                        "No reply",
                        text,
                        "anwesha.backed@gmail.com",
                        [user.email_id],
                    )
            EmailThread(sendMail).start()
            # Send the email with the reset password link
            #send_email_using_microservice(email_id=request.data['email'], subject="Change password", text=text)

            return Response({"message": "Reset link sent"}, status=200)
        except User.DoesNotExist:
            return Response({"message": "Email not found"}, status=404)

    def put(self, request):
        # This method is for changing the password using the provided token

        token = request.data['token']
        password = request.data['password']

        try:
            # Decode the token using the provided encryption secret
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"message": "Token expired"}, status=408)
        except jwt.DecodeError:
            return Response({"message": "Invalid token"}, status=400)

        try:
            # Retrieve the user based on the user ID from the token
            user = User.objects.get(anwesha_id=payload['userid'])
        except User.DoesNotExist:
            return Response({"message": "Invalid token"}, status=404)

        # Update the user's password and save it
        user.password = hashpassword(password)
        user.save()

        # Send email confirmation if necessary

        return Response({"message": "Password updated"}, status=200)


class RegenerateQR(APIView):
    @Autherize()
    def get(self, request, **kwargs):
        user = kwargs['user']
        user.secret = createId("secret",10)
        user.signature = hash_id(user.anwesha_id, user.secret)
        user.qr_code = generate_qr(user.anwesha_id,user.signature)
        user.save()
        return JsonResponse({
            "qr_code":'https://'+ AWS_S3_CUSTOM_DOMAIN +'/'+ AWS_PUBLIC_MEDIA_LOCATION2 + str(user.qr_code)
        },safe=False)



"""
:WARNING: OAuth login is not stable yet hence not in use
"""
class Oauth_Login(APIView):
    def get(self,request):
        username = request.user.username
        first_name = request.user.first_name
        email = request.user.email
        last_name = request.user.last_name
        full_name = first_name + last_name

        #registering user in custom user model
        if User.objects.filter(email_id=email).exists():
            user = User.objects.get(email_id=email)
            payload = {
                        "id" : user.anwesha_id,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
                        "iat": datetime.datetime.utcnow()
                    }
            response = Response()
            token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm = 'HS256')
            response.set_cookie(key='jwt', value=token, httponly=True)
            user.is_loggedin=True
            user.save()
            response.data={'user':'logged in','username':username,'first_name':first_name, 'last_name':last_name,'email':email}
            return response
        else:
            anwesha_id = createId("ANW", 7)
            password = uuid.uuid1()
            anwesha_id_hash = hash_id(anwesha_id)
            generate_qr(anwesha_id=anwesha_id_hash)
            # checking if the created id is not already present in the database
            check_exist = User.objects.filter(anwesha_id = anwesha_id)
            while check_exist:  # very unlikely to happen
                anwesha_id = createId("ANW", 7)
                check_exist = User.objects.filter(anwesha_id = anwesha_id)
            new_user = User.objects.create(full_name=full_name, password = password, email_id=email, anwesha_id=anwesha_id)
            new_user.qr_code="static/qrcode/"+anwesha_id+".png"
            shutil.move(anwesha_id+".png","static/qrcode/")
            new_user.is_loggedin=False
            new_user.save()
            user = User.objects.get(email_id=email)
            payload = {
                        "id" : user.anwesha_id,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                        "iat": datetime.datetime.utcnow()
                    }
            response = Response()
            token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm = 'HS256')
            response.set_cookie(key='jwt', value=token, httponly=True)
            user.is_loggedin=True
            user.save()
            response.data={'user':'registered','username':username,'first_name':first_name, 'last_name':last_name,'email':email}
            return response

    # return JsonResponse({'status':'success' },safe=False)

class Oauth_Logout(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationError("Unauthenticated")

        try:
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Cookie Expired")

        user = User.objects.get(anwesha_id = payload['id'])
        user.is_loggedin=False
        user.save()
        response = Response()
        response.delete_cookie('jwt')
        return response
