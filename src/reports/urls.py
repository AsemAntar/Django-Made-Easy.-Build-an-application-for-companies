from django.urls import path
from . import views


app_name = "reports"
urlpatterns = [
    path('<str:production_line>/', views.report_view, name='report_view'),
    path('delete/<int:pk>/', views.delete_report, name='delete_report'),
    path('<str:production_line>/<int:pk>/update',
         views.UpdateReportView.as_view(), name="update_report"),
]
