import json
from django.http import JsonResponse
from .models import User
from utility import isemail


def register(request):
    """
    Register a new user.

    Endpoint: `{host}/slick/register`

    Args:
        request: The HTTP request object.
        header: Bearer token: "AnweshaIitpxSlick"
        ```json
        {
            "email_id": "johndoe@email.com",
            "full_name": "John Doe",
            "phone_number": "9876543210",
            "college_name": "IIT Patna",
            "user_type": "iitp_student"
        }
        ```

    Returns:
        A JSON response with the Anwesha ID of the newly registered user, or the Anwesha ID of the existing user if the user is already registered.
        ```json
        {
            "Anwesha_id": "ANWXXXXXX"
        }
        ```
        
        On token error
        ```json
        {
            "message": "you are unauthenticated , Please Log in First"
        }
        ```

    Raises:
        JsonResponse: If the request method is not POST or the user is unauthenticated.
    """
    if request.method == "POST":
        data = request.body
        payload = json.loads(data)

        # verify token
        token = request.META.get("HTTP_AUTHORIZATION")
        print(token)
        if token == None:
            return JsonResponse(
                {"message": "you are unauthenticated , Please Log in First"}, status=401
            )
        elif token != "Bearer AnweshaIitpxSlick":
            return JsonResponse(
                {"message": "you are unauthenticated , Please Log in First"}, status=401
            )

        password = request.data["email_id"]  # set password by default to email id
        email_id = request.data["email_id"]
        full_name = request.data["full_name"]
        phone_number = request.data["phone_number"]
        college_name = request.data["college_name"]
        user_type = request.data["user_type"]  # student or iitp_student
        """
                data validation
        """
        if isemail(email_id) == False:
            return JsonResponse({"message": "enter valid email"}, status=409)
        if User.objects.filter(email_id=email_id).exists():
            # return anwesha id of the user
            existing_user = User.objects.get(email_id=email_id)
            existing_user.is_email_verified = True
            existing_user.save()
            return JsonResponse(
                {
                    "Anwesha_id": existing_user.anwesha_id,
                },
                status=200,
            )
        if User.objects.filter(phone_number=phone_number).exists():
            existing_user = User.objects.get(phone_number=phone_number)
            existing_user.is_email_verified = True
            existing_user.save()
            return JsonResponse(
                {
                    "Anwesha_id": existing_user.anwesha_id,
                },
                status=200,
            )
        """
            assiging user types
        """
        if user_type == "iitp_student":
            user_type = User.User_type_choice.IITP_STUDENT
        elif user_type == "student":
            user_type = User.User_type_choice.STUDENT
        elif user_type == "non-student":
            user_type = User.User_type_choice.NON_STUDENT
        elif user_type == "non-student":
            user_type = User.User_type_choice.NON_STUDENT
        elif user_type == "alumni":
            user_type = User.User_type_choice.ALUMNI
        elif user_type == "faculty":
            user_type = User.User_type_choice.GUEST
        else:
            return JsonResponse({"message": "enter proper user type"}, status=403)
        print(full_name, email_id, password, college_name, user_type)
        new_user = User.objects.create(
            full_name=full_name,
            email_id=email_id,
            password=password,
            phone_number=phone_number,
            is_email_verified=True,
            user_type=user_type,
            collage_name=college_name,
        )
        print("New user created successfully")
        print(new_user)
        new_user.save()
        return JsonResponse({"Anwesha_id": new_user.anwesha_id}, status=201)
