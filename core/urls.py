from django.urls import path
from .views import trophy_data

urlpatterns = [
   path('', trophy_data, name = 'home'),
]