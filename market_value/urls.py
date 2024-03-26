from django.urls import path, include

from .views import market_value

urlpatterns = [
    path('', market_value, name = 'market_value'),
]