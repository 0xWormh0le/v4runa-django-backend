from django.urls import path
from . import views


urlpatterns = [
    path('', views.ResourceAllocationListView.as_view(), name='resource-allocations'),
    path('search/', views.ResourceAllocationSearchView.as_view(), name='resource-allocations-search'),
    path('<int:pk>/calendar/', views.ResourceAllocationCalendarView.as_view(), name='resource-allocation-calendar'),
]
