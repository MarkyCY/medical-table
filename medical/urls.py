from django.urls import path
from .views import base, create_task

urlpatterns = [
    path('', base),
    path('new/', create_task, name='create_task'),
]