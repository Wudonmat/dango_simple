from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.profile_update, name="profile_update"),
    path("dog/update/", views.dog_update, name="dog_update"),
]