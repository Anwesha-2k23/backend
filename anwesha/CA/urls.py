from django.urls import path
# from campus_ambassador.models import campus_ambassador
from .views import register , all_campas_ambassodor , leaderBoardData , verifyEmail , sendVerificationEmail

campus_ambassador_urls = [
    path('allcampusambassadors' , all_campas_ambassodor , name='all_campas_ambassodor'),
    path('register' ,register.as_view(), name='register'),
    path('leaderboarddata' ,leaderBoardData.as_view(), name='leaderBoardData'),
    path('verifyemail' , sendVerificationEmail.as_view(), name='send_verificaion_email'),
    path('verifyemail/<str:pk>' , verifyEmail , name='verifyEmail' ),
]