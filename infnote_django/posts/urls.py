from django.urls import path
from .views import *

urlpatterns = [
    path('', CreatePost.as_view()),
    path('list/', ListPost.as_view()),
    path('<id>/', RetrievePost.as_view()),
    path('<id>/replies/', ListReply.as_view()),
]
