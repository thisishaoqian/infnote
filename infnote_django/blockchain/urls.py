from django.urls import path
from .wallet import *

urlpatterns = [
    path('unspent/', Unspent.as_view()),
]