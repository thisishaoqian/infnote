from django.urls import path
from .views import *

urlpatterns = [
    path('id/<user_id>/', UserInfoID.as_view()),
    path('pk/<public_key>/', UserInfoPK.as_view()),
    path('create/', CreateUser.as_view()),
]
