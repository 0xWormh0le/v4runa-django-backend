from django.urls import path
from . import views


urlpatterns = [
    path('', views.AlertListView.as_view(), name='alerts'),
    path('search/', views.AlertSearchView.as_view(), name='alerts-search'),
    path('sensors/<int:sensor_id>/search/', views.AlertSearchView.as_view(), name='alerts-sensor-search'),
]
