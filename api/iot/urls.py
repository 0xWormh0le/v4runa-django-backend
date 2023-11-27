from django.urls import path
from . import views


urlpatterns = [
    path('sensor-data/', views.SensorDataView.as_view(), name='sensor-data'),
]
