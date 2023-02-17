from django.shortcuts import render
from django.views import View
from utility import hashpassword, createId, isemail
from CA.models import Campus_ambassador
from user.models import User
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from utility import generate_jwt_token , verification_mail , createId
from time import mktime

from datetime import datetime ,timedelta ,timezone
import jwt
from anwesha.settings import COOKIE_ENCRYPTION_SECRET



def all_campas_ambassodor(request):
    if request.method == 'GET':
        events = Campus_ambassador.objects.all()
        events = list(events.values('anwesha','email_id','full_name','college_name'))
        return JsonResponse(events, safe=False)
    return JsonResponse({'message': 'Invalid method', 'status': '405'}) 

class register(APIView):
    def post(self, request):
         try:
            phone_number=request.data['phone_number']
            email_id=request.data['email_id']
            full_name=request.data['full_name']
            college_name=request.data['college_name']
           
            password=request.data['password']
            hpassword = hashpassword(password)
            if(isemail(email_id) == False):
                return JsonResponse({'message': 'Please enter valid email address', 'status': '409'} , status = 409)
            if Campus_ambassador.objects.filter(email_id=email_id).exists():
                return JsonResponse({'message': 'An Campus Ambassador With same Email already exists', 'status': '409'},status = 409)
            if Campus_ambassador.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message': 'An Campus Ambassador With same Phone Number already exists', 'status': '409'},status = 409)
            else:
                ca_id = createId("CA",5)
                check_exist = Campus_ambassador.objects.filter(ca_id = ca_id)
                while check_exist:  # very unlikely to happen
                        ca_id = createId("CA",5)
                        check_exist = Campus_ambassador.objects.filter(ca_id = ca_id)
                
                refferal_code = createId(prefix="RF",length=4)
                check_refferal_code = Campus_ambassador.objects.filter(refferal_code = refferal_code)
                while check_refferal_code:  # very unlikely to happen
                    refferal_code = createId(prefix="RF",length=4)
                    check_refferal_code = Campus_ambassador.objects.filter(refferal_code = refferal_code)
            
                new_campus_ambassador = Campus_ambassador.objects.create(
                    full_name=full_name,
                    email_id=email_id, 
                    password=hpassword, 
                    phone_number = phone_number , 
                    college_name = college_name , 
                    refferal_code = refferal_code , 
                    ca_id = ca_id
                )
                new_campus_ambassador.save()
                #varification_mail(email=email_id)
                return JsonResponse({'message': 'Campus ambassador created successfully!' ,'status':'201'} ,status=201)
         except:
             return JsonResponse({'message': 'Campus ambassador registration failed', 'status': '400'},status=400)
        
class Login(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({"message": "you are unauthenticated"} , status=401)
        try:
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please generate new one"},status=409) 
        try:
            this_ca = Campus_ambassador.objects.get(ca_id = payload["id"])
            if(this_ca.validation == True):
                this_ca.is_loggedin = True
                this_ca.save()
                response = Response()
                response.data = {
                    "mssg": "welcome",
                    "full_name" : this_ca.full_name,
                    "status" : "200"
                }
                return response
            else:
                return JsonResponse({"message":"Your Email is not verified please verify email to continue further"},status=401)
        except:
            return JsonResponse({"message":"invalid token"},status=409)

    def post(self, request):
        response = Response()
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            response.data = { "status" : "Incorrrect input" }
            return response

        password = hashpassword(password)
        try:
            if isemail(username):
                ca = Campus_ambassador.objects.filter(email_id = username, password = password)
            else:
                ca = Campus_ambassador.objects.filter(ca_id = username , password=password)
        except:
            return JsonResponse({"message":"wrong credentaials provided"})
        this_ca = ca.first()
        
        if this_ca:
            if this_ca.validation == True :
                payload = {
                    "id" : this_ca.ca_id,
                    "exp": datetime.utcnow() + timedelta(minutes=60),
                    "iat": datetime.utcnow()
                }

                token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm = 'HS256')

                response.data = { "success" : True , "name" : this_ca.full_name}
                response.set_cookie(key='jwt', value=token, httponly=True)
            else:
                response.data = {
                    "message" : "Please verify email to log in to your account",
                    "success" : False
                }
            # code for linking cookie
        else:
            response.data = { "successs": False, "message": "incorrect id or password" }

        return response    

class LogOut(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({"message": "you are unauthenticated"} , status=401)
        else:
            try:
                payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms = 'HS256')
            except jwt.ExpiredSignatureError:
                return JsonResponse({"message":"Your token is expired please generate new one"},status=409) 
            try:
                this_ca = Campus_ambassador.objects.get(ca_id = payload["id"]) 
            except:
                return JsonResponse({"message":"Invalid Token value"},status=401)
            this_ca.is_loggedin = False
            this_ca.save()
            response = Response()
            response.delete_cookie('jwt')
            response.data = {'message': 'Logout Successful' , "status" : "200"}
            return response


class leaderBoardData(View):
    def get(self , request):
        try:
            leaderBoard = Campus_ambassador.objects.all().order_by('score')
            leaderBoard = list(leaderBoard.values('score','full_name','email_id').reverse())
            return JsonResponse ({"leaderBoardData" : leaderBoard , "status" : "200"},status=200)
        except:
            return JsonResponse({'message': 'Invalid method' , 'status': '405'},status=405)

class editProfile(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({"message": "you are unauthenticated"} , status=401)

        try:
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please generate new one"},status=409) 

        this_ca = Campus_ambassador.objects.get(ca_id = payload["id"]) 
        response = Response()
        response.data = {
            "ca_id": this_ca.ca_id ,
            "anwesha_id":this_ca.anwesha,
            "full_name" : this_ca.full_name ,
            "phone_number" : this_ca.phone_number,
            "email_id" : this_ca.email_id , 
            "college_name" : this_ca.college_name ,
            "college_city" : this_ca.college_city ,
            "age" : this_ca.age , 
            "gender" : this_ca.gender ,
            "instagram_id" : this_ca.instagram_id,
            "facebook_id":this_ca.facebook_id,
            "linkdin_id":this_ca.linkdin_id,
            "twitter_id":this_ca.twitter_id,
        }
        return response

    def post(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            return JsonResponse({"message": "you are unauthenticated"} , status=401)

        try:
            payload = jwt.decode(token, COOKIE_ENCRYPTION_SECRET, algorithms = 'HS256')
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"Your token is expired please generate new one"},status=409) 


        this_ca = Campus_ambassador.objects.get(ca_id = payload['id']) 
        data  = request.data
        try:
            full_name = data['full_name']
        except:
            full_name = this_ca.full_name

        try:
            provided_anwesha_id = data['anwesha_id']
            if User.objects.filter(anwesha_id = provided_anwesha_id).exists():
                user_object_of_ca  = User.objects.get(anwesha_id = provided_anwesha_id)
            else:
                return JsonResponse({"message" : "There is no user with provided Anwesha ID , Please provide correct Anwesha ID"},status=401)
            if user_object_of_ca.email_id == this_ca.email_id:
                anwesha_id = provided_anwesha_id
            else:
                return JsonResponse({"message":"The Anwesha ID you provided belongs to someone else , please ensure that email in both  the  places is same"}, status = 401)
        except:
            anwesha_id = this_ca.anwesha

        try:
            college_name = data['college_name']
        except:
            college_name = this_ca.collage_name

        try:
            college_city = data['college_city']
        except:
            college_city = this_ca.college_city

        try:
            age = data['age']
        except:
            age = this_ca.age

        try:
            profile_photo = data['profile_photo']
        except:
            profile_photo = this_ca.profile_photo

        try:
            instagram_id = data['instagram_id']
        except:
            instagram_id = this_ca.instagram_id

        try:
            facebook_id = data['facebook_id']
        except:
            facebook_id = this_ca.facebook_id
        
        try:
            linkdin_id = data['linkdin_id']
        except:
            linkdin_id = this_ca.linkdin_id
        
        try:
            twitter_id = data['twitter_id']
        except:
            twitter_id = this_ca.twitter_id

        try:
            gender = data['gender']
            if(gender == 'male'):
                gender = this_ca.Gender.MALE
            if(gender == 'female'):
                gender = this_ca.Gender.FEMALE
            if(gender == 'rather_not_say'):
                gender = this_ca.Gender.RATHER_NOT_SAY
            if(gender == 'others'):
                gender = this_ca.Gender.OTHERS
        except:
            gender = this_ca.gender
                
        this_ca.full_name = full_name
        this_ca.anwesha = anwesha_id
        this_ca.college_name = college_name
        this_ca.college_city = college_city
        this_ca.age = age
        this_ca.gender = gender
        this_ca.profile_photo = profile_photo
        this_ca.instagram_id = instagram_id
        this_ca.facebook_id = facebook_id
        this_ca.linkdin_id = linkdin_id
        this_ca.twitter_id = twitter_id
        this_ca.save()

        response = Response()
        response.data = {
            'message': 'Profile successfully updated!'
        }
        return response

class sendVerificationEmail(APIView):
    def post(self,request):
        try:
            email = request.data["email_id"]
            print(email)
            if Campus_ambassador.objects.filter(email_id = email).exists():
                try:
                    payload = {
                        "email":email ,
                        "exp": datetime.utcnow() + timedelta(days=1),
                        "iat": datetime.utcnow()
                    } 
                    token = jwt.encode( payload=payload, key=COOKIE_ENCRYPTION_SECRET , algorithm="HS256") # not working ?? 
                    return JsonResponse({"token": token},status=201)
                except:
                    return JsonResponse({"message":"Token cannot be generated"} , status=409)
            else:
                return JsonResponse({"message":"No such email exists"},status=409)
        except:
            return JsonResponse({"message":"bad request"},status=400 )


def verifyEmail(request , *arg , **kwarg):
    if request.method == 'GET':
        token = kwarg['pk']
        try:
            jwt_payload = jwt.decode(token,COOKIE_ENCRYPTION_SECRET,algorithms = 'HS256') # not working ?? 
        except:
            return JsonResponse({"message":"token expired"} , status=409)
        try:
            ca_to_verify = Campus_ambassador.objects.get(email_id = jwt_payload['email'])
            ca_to_verify.validation = True
            ca_to_verify.save()
        except:
            return JsonResponse({"message":"Invalid Token"} , status=401)
        return JsonResponse({"message" : "email verified succesfully" } , status=201)
