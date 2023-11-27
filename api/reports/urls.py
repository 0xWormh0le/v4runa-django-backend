from django.urls import path
from . import views


urlpatterns = [
    path('monthly-reports/', views.MonthlyReportListView.as_view(), name='monthly-reports'),
    path('weekly-reports/', views.WeeklyReportView.as_view(), name='weekly-reports'),
]
