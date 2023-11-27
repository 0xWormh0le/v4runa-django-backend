from django.urls import path
from . import views


urlpatterns = [
    path('', views.TechnicianListView.as_view(), name='technicians'),
    path('search/', views.TechnicianSearchView.as_view(), name='technicians-search'),
    path('<int:pk>/', views.TechnicianDetailsView.as_view(), name='technician-details'),
]
