from django.urls import path
from .views import *

urlpatterns = [
    path('', CreatePost.as_view()),
    path('list/', ListPost.as_view()),
    path('<payload_id>/', RetrievePost.as_view()),
    path('<payload_id>/replies/', ListReply.as_view()),
]
