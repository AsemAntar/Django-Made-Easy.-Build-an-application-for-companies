from django.urls import path
from . import views


app_name = "reports"
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('reports/', views.SelectView.as_view(), name="select_report"),
    path('reports/summary', views.main_report_summary, name="report_summary"),
    path('reports/<str:production_line>/',
         views.report_view, name='report_view'),
    path('reports/delete/<int:pk>/', views.delete_report, name='delete_report'),
    path('reports/<str:production_line>/<int:pk>/update',
         views.UpdateReportView.as_view(), name="update_report"),
]
