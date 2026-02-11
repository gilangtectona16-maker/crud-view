from django.urls import path
from . import views
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='api_login'),
]