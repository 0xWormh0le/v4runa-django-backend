from django.urls import path
from . import views


urlpatterns = [
    path('', views.SensorListView.as_view(), name='sensors'),
    path('search/', views.SensorSearchView.as_view(), name='sensors-search'),

    path('<int:pk>/records/all/', views.SensorDataRecordAllListView.as_view(), name='sensor-data-records-all'),
    path('<int:pk>/records/<str:chemical>/all/', views.SensorDataRecordAllListView.as_view(), name='sensor-data-records-chemical-all'),

    path('<int:pk>/records/<str:chemical>/latest/', views.SensorDataRecordLatestView.as_view(), name='sensor-data-records-chemical-latest'),
    
    path('<int:pk>/records/<str:chemical>/', views.SensorDataRecordListView.as_view(), name='sensor-data-records-chemical-hourly'),
    path('<int:pk>/records/<str:chemical>/<str:interval>/', views.SensorDataRecordListView.as_view(), name='sensor-data-records-chemical-interval'),
    
    path('<str:chemical>/', views.SensorCurrentDataListView.as_view(), name='sensors-current-chemical'),
    path('<str:chemical>/search/', views.SensorCurrentDataSearchView.as_view(), name='sensors-search-current-chemical'),
]
