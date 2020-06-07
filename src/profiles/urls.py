from django.urls import path
from . import views


app_name = "profiles"
urlpatterns = [
    path('', views.profile, name="profile"),
    path('test/', views.test_user, name="test_user"),
]
