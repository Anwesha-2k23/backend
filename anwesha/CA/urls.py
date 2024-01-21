from django.urls import path
# from campus_ambassador.models import campus_ambassador
from .views import register , all_campas_ambassodor , leaderBoardData , verifyEmail , sendVerificationEmail , Login , LogOut , editProfile

campus_ambassador_urls = [
    path('allcampusambassadors' , all_campas_ambassodor , name='all_campas_ambassodor'),
    path('login', Login.as_view(), name='Login'),
    path('register' ,register.as_view(), name='register'),
    path('logout', LogOut.as_view() , name='logout'),
    path('editprofile' , editProfile.as_view() , name = 'editProfile'),
    path('leaderboarddata' ,leaderBoardData.as_view(), name='leaderBoardData'),
    path('verifyemail' , sendVerificationEmail.as_view(), name='send_verificaion_email'),
    path('verifyemail/<str:pk>' , verifyEmail , name='verifyEmail' ),
]