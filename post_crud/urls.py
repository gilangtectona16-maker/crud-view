from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("read/<slug:slug>/", views.post_detail, name="post_detail"),
    path("create/", views.post_create, name="post_create"),
    path("edit/<int:post_id>/", views.post_edit, name="post_edit"),
    path("delete/<int:post_id>/", views.post_delete, name="post_delete"),
    path("go-to-manage/", views.to_manage, name="to_manage"),
]
