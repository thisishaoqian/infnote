from django.urls import path
from .views import *

# TODO: 进一步限制路由的正则
urlpatterns = [
    path('create/', CreateUser.as_view()),
    path('send_code/', Verification.as_view()),
    path('<id>/', UserDetail.as_view()),
    path('', UserDetail.as_view()),
]
