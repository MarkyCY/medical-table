from django.urls import path
from .views import list_test

urlpatterns = [
    path('', list_test)
]