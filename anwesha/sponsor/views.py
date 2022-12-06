from django.shortcuts import render
from django.http import JsonResponse
from .models import Sponsors
from django.views import View


def allsponsors(request):
    if request.method == "GET":
        sponsors = Sponsors.objects.all()
        listed_sponsors = list(sponsors.values())
        return JsonResponse(listed_sponsors, safe=False)
    else:
        response = JsonResponse({"message": "inavalid method"})
        return response


class register(View):
    def get(self, request):
        response = JsonResponse({"message": "inavalid method"})
        return response

    def post(self, request):
        try:
            # spons logo not uploaded in register api
            sponsor_name = request.POST.get("sponsor_name ")
            sponsor_phone_number = request.POST.get("sponsor_phone_number")
            sponsor_email = request.POST.get("sponsor_email")
            sponsor_link = request.POST.get("sponsor_link")
            sponsor_instagram_id = request.POST.get("sponsor_instagram_id")
            sponsor_facebook_id = request.POST.get("sponsor_facebook_id")
            sponsor_linkdin_id = request.POST.get("sponsor_linkdin_id")

            new_sponsor = Sponsors.objects.create(
                sponsor_email=sponsor_email,
                sponsor_name=sponsor_name,
                sponsor_facebook_id=sponsor_facebook_id,
                sponsor_instagram_id=sponsor_instagram_id,
                sponsor_phone_number=sponsor_phone_number,
                sponsor_link=sponsor_link,
                sponsor_linkdin_id=sponsor_linkdin_id,
            )
            new_sponsor.save()
            return JsonResponse({"message": "Sponsor Successfully Added"})
        except:
            return JsonResponse({"message": "An Error Occured"})
