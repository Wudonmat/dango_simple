from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("blog/", views.blog_home, name='home'), # 첫번째 URL패턴
    path("blog/post/<int:post_id>/", views.blog_post_view, name="post"),
    path("blog/post-delete/<int:post_id>/", views.blog_post_delete, name="delete"),
    path("blog/post-edit/<int:post_id>/", views.blog_post_edit, name="edit"),
]