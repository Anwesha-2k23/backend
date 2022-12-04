from django.shortcuts import render
from django.views import View
from utility import hashpassword, createId, isemail
from campus_ambassador.models import campus_ambassador
from django.http import JsonResponse
from rest_framework.views import APIView
# Create your views here.


def all_campas_ambassodor(request):
    if request.method == 'GET':
        events = campus_ambassador.objects.all()
        events = list(events.values())
        return JsonResponse(events, safe=False)
    return JsonResponse({'message': 'An Error occured'}) 


class register(APIView):
    def post(self, request):
        # anwesha_id=request.POST.get('anwesha_id')
        phone_number=request.data['phone_number']
        email_id=request.data['email_id']
        full_name=request.data['full_name']
        college_name=request.data['college_name']
        # college_city=request.POST.get('college_city')
        # college_state=request.POST.get('college_state')
        # degree=request.POST.get('degree')
        # years_of_study=request.POST.get('years_of_study')
        refferal_code=request.data['refferal_code']
        password=request.data['password']
        # intrests=request.POST.get('intrests')
        # instagram_id=request.POST.get('instagram_id')
        # facebook_id=request.POST.get('facebook_id')
        # linkdin_id=request.POST.get('linkdin_id')
        # twitter_id=request.POST.get('twitter_id')
        # date_of_birth=request.POST.get('date_of_birth')
        # time_of_registration=request.POST.get('time_of_registration')
        # score = request.POST.get('score')
        # anwesha_id=request.POST.get('anwesha_id')
        print("refferal code = ",phone_number)
        hpassword = hashpassword(password)

        new_campus_ambassador = campus_ambassador.objects.create(
            full_name=full_name,
            email_id=email_id, 
            password=hpassword, 
            # anwesha_id=anwesha_id , 
            phone_number = phone_number , 
            # college_city = college_city , 
            college_name = college_name , 
            # college_state = college_state , 
            # degree = degree , 
            # years_of_study = years_of_study , 
            refferal_code = refferal_code , 
            # intrests = intrests , 
            # instagram_id = instagram_id , 
            # facebook_id = facebook_id , 
            # linkdin_id = linkdin_id , 
            # twitter_id = twitter_id , 
            # date_of_birth = date_of_birth , 
            # time_of_registration = time_of_registration
            )
        new_campus_ambassador.save()
        return JsonResponse({'message': 'campus ambassador created successfully!'})

class leaderBoardData(View):
    def get(self , request):
        leaderBoard = campus_ambassador.objects.all().order_by('score')
        leaderBoard = list(leaderBoard.values().reverse())
        return JsonResponse ({"leaderBoardData" : leaderBoard })