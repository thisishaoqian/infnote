from django.urls import path
# from .wallet import *
from .views import *

urlpatterns = [
    # path('unspent/', Unspent.as_view()),
    path('balance/', Balance.as_view()),
    path('coins/', GetCoin.as_view()),
]
