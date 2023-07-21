from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('cards/', card_list, name='card_list'),
    path('cards/<int:card_id>/', card_detail, name='card_detail'),
    path('cards/save/', save_card, name='save_card'),
    path('cards/create/', create_card, name='create_card'),
    path('cards/<int:card_id>/delete/', delete_card, name='delete_card'),
]
