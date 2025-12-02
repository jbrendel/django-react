from django.urls import path
from . import views

urlpatterns = [
    path("welcome-message/", views.welcome_message, name="welcome-message"),
]
