from django.urls import path
from .views import *

urlpatterns = [
    path('new_block/', BlockUpdated.as_view()),
]
