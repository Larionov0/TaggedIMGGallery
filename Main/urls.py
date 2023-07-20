from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('cards/', card_list, name='card_list'),
]
