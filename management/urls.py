from django.urls import path
from . import views

urlpatterns = [
    path("", views.manage_list, name="manage_list"),
    path("create/", views.manage_create, name="manage_create"),
    path("edit/<str:mode>/<int:pk>/", views.manage_edit, name="manage_edit"),
    path("delete/<str:mode>/<int:pk>/", views.manage_delete, name="manage_delete"),
    path("go-to-blog/", views.to_blog, name="to_blog"),
]
