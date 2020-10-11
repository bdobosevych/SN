from django.urls import path, include

from .views import feed

urlpatterns = [
    path('', feed, name='feed'),

]