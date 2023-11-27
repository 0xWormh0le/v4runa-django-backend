from django.urls import include, path
from . import views

urlpatterns = [
	path('weekly-report-mail/', views.WeeklyReportMailView.as_view(), name='weekly-report-mail'),
	path('after-deploy/', views.AfterDeployView.as_view(), name='after-deploy'),
]
