from django.urls import path
from . import views

app_name = "dog"
urlpatterns = [
    path("list/", views.dog_list, name='list'), # 첫번째 URL패턴
    path("dog/profile/<int:user_id>/", views.dog_profile_view, name="profile"),
]