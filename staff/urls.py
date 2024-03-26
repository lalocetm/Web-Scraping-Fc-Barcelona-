from django.urls import path

from .views import staff_view

urlpatterns = [
    path('staff_view', staff_view, name = 'staff_view'),
]