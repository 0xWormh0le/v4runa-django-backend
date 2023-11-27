from django.urls import path
from . import views


urlpatterns = [
    path('', views.ReportView.as_view(), name='pump-report-list'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='pump-report-detail'),
]
