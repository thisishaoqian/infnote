from django.urls import path
from .views import *

urlpatterns = [
    # path('', UserDetail.as_view()),
    path('info/<id>/', UserDetail.as_view()),
    # path('info/', UpdateInfo.as_view()),
    path('create/', CreateUser.as_view()),
    # path('nonce/', Token.as_view()),
]
