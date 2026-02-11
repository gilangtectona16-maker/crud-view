from django.urls import path
from . import views
from .views import PostListView

urlpatterns = [
    path("", views.manage_list, name="manage_list"),
    path('form/<str:mode>/', views.manage_form, name='manage_create'),  
    path('form/<str:mode>/<uuid:item_id>/', views.manage_form, name='manage_edit'),
    path('delete/<str:mode>/<uuid:item_id>/', views.manage_delete, name='manage_delete'),
    path("go-to-blog/", views.to_blog, name="to_blog"),
    path('api/posts/', PostListView.as_view(), name='post_list_api'),
    path('logout/', views.logout_view, name='logout'),
]
