from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_user, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout_user", views.logout_user, name="logout"),
    path("transcription", views.transcription, name="transcription")
]
