from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/send/", views.receive_encrypted, name="receive_encrypted"),
]
