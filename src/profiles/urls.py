from django.urls import path, include

from .views import view_profile

urlpatterns = [
    path('<str:username>/', view_profile, name='view_profile'),
    ]