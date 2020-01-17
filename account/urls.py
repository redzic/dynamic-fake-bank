from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("transfer", views.transfer, name="transfer"),
    path("transactions", views.transactions, name="transactions"),
]
