from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account/", include("account.urls")),
    path("admin/", admin.site.urls),
]
