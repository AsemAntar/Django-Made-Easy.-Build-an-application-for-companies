from django.urls import path
from . import views


app_name = "reports"
urlpatterns = [
    path('<str:production_line>/', views.report_view, name='report_view'),
]
