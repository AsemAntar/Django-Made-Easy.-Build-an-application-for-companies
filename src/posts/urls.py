from django.urls import path
from . import views


app_name = "posts"
urlpatterns = [
    path('', views.PostCreateView.as_view(), name='post_list'),
    path('<int:pk>/detail/', views.GeneralDetailPost.as_view(), name='gp-detail'),
    path('<int:pk1>/<int:pk>/detail/',
         views.ProblemDetailView.as_view(), name='pp-detail'),
    path('like/', views.like_post, name='post_like'),

]
