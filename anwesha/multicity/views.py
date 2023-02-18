from django.shortcuts import render
from rest_framework.views import APIView
from .models import Multicity_Events ,Multicity_Participants 
from django.http import JsonResponse
from utility import isemail, createId

class register(APIView):
    def post(self, request):
        try:
            event_id = request.data['event_id']
            organisation_type = request.data['organisation_type']

            if organisation_type == 0:
                organisation_type = Multicity_Participants.Organisation_Type.SCHOOL
            elif organisation_type == 1:
                organisation_type = Multicity_Participants.Organisation_Type.COLLEGE
            else:   
                organisation_type = Multicity_Participants.Organisation_Type.OTHERS

            try:
                solo_team = request.data['solo_team']
            except:
                solo_team = True
            leader_name = request.data['leader_name']
            leader_email = request.data['leader_email']
            if(isemail(leader_email) == False):
                return JsonResponse({'message': 'Please enter valid email address', 'status': '409'} , status = 409)
            leader_phone_no = request.data['leader_phone_no']          
            leader_organisation = request.data['leader_organisation']

            if Multicity_Participants.objects.filter(leader_email = leader_email , event_id= event_id).exists():
                return JsonResponse({'message': 'You have already registered for this event', 'status': '409'} , status = 409)
            try:
               member_one_name = request.data['member_one_name']
               member_one_email = request.data['member_one_email']
               if(isemail(member_one_email) == False):
                   return JsonResponse({'message': 'Please enter valid email address', 'status': '409'} , status = 409)
               member_one_organisation = request.data['member_one_organisation'] 
               member_one_phone_no = request.data['member_one_phone_no']
            except:
               member_one_name = None
               member_one_email = None
               member_one_organisation = None
               member_one_phone_no = None

            try:
               member_two_name = request.data['member_two_name']
               member_two_email = request.data['member_two_email']
               if(isemail(member_two_email) == False):
                   return JsonResponse({'message': 'Please enter valid email address', 'status': '409'} , status = 409)
               member_two_organisation = request.data['member_two_organisation'] 
               member_two_phone_no = request.data['member_two_phone_no']
            except:
               member_two_name = None
               member_two_email = None
               member_two_organisation = None
               member_two_phone_no = None

            try:
               member_three_name = request.data['member_three_name']
               member_three_email = request.data['member_three_email']
               if(isemail(member_two_email) == False):
                   return JsonResponse({'message': 'Please enter valid email address', 'status': '409'} , status = 409)
               member_three_organisation = request.data['member_three_organisation'] 
               member_three_phone_no = request.data['member_three_phone_no']
            except:
               member_three_name = None
               member_three_email = None
               member_three_organisation = None
               member_three_phone_no = None

            registration_id = createId(prefix = "RST" , length = 6)
            check_exist = Multicity_Participants.objects.filter(registration_id=registration_id)
            while check_exist:  # very unlikely to happen
                    registration_id = createId(prefix = "RST" , length = 6)
                    check_exist = Multicity_Participants.objects.filter(registration_id=registration_id)
            try:
                new_registration = Multicity_Participants.objects.create(
                    event_id = Multicity_Events.objects.get(event_id = event_id) ,organisation_type = organisation_type , solo_team = solo_team,registration_id = registration_id,
                    leader_name = leader_name, leader_email = leader_email , leader_organisation = leader_organisation , leader_phone_no = leader_phone_no,
                    member_one_name = member_one_name ,member_one_email = member_one_email , member_one_organisation = member_one_organisation , member_one_phone_no = member_one_phone_no,
                    member_two_name = member_two_name ,member_two_email = member_two_email , member_two_organisation = member_two_organisation , member_two_phone_no = member_two_phone_no,
                    member_three_name = member_three_name ,member_three_email = member_three_email , member_three_organisation = member_three_organisation , member_three_phone_no = member_three_phone_no
                    )
            except:
                return JsonResponse({"message" : "Internal server side error , probably the event you registerings for does not exist"},status=500)
            return JsonResponse({"message" : "you are registered sucessfully","registration ID" : registration_id},status=200)

        except:
            return JsonResponse({"message":"Form data incomplete"})



        

