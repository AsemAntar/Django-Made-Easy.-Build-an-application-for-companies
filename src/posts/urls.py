from django.urls import path
from . import views


app_name = "posts"
urlpatterns = [
    path('board/', views.PostCreateView.as_view(), name='post_list'),
]
