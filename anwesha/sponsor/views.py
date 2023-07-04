from django.http import JsonResponse
from .models import Sponsors
from django.views import View


def allsponsors(request):
    if request.method == "GET":
        # Retrieve all sponsors from the database
        sponsors = Sponsors.objects.all()
        # Convert the sponsor queryset to a list of dictionaries
        listed_sponsors = list(sponsors.values())
        # Return a JSON response with the list of sponsors
        return JsonResponse(listed_sponsors, safe=False, status=200)
    else:
        # Handle any HTTP method other than GET
        response = JsonResponse(
            {"message": "Invalid method", "status": "405"},
            status=405
        )
        return response
