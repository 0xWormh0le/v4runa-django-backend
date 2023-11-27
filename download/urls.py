from django.urls import include, path
from . import views

urlpatterns = [
	path('monthly-report/<int:pk>/', views.MonthlyReportView.as_view(), name='monthly-report-download'),
]
