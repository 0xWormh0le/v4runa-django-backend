from django.urls import path
from . import views


urlpatterns = [
    path('', views.WaterUtilityListView.as_view(), name='utilities'),
    path('search/', views.WaterUtilitySearchView.as_view(), name='utilities-search'),
    path('<int:pk>/assets-finances/', views.AssetFinanceListView.as_view(), name='assets-finances'),
    path('<int:pk>/water-quality-history/', views.WaterQualityHistoryView.as_view(), name='water-quality-history'),
    path('<int:pk>/water-quality-history/all', views.WaterQualityAllHistoryView.as_view(), name='water-quality-all-history'),
    path('<int:pk>/sensors', views.SensorListView.as_view(), name='sensors'),
    path('<int:pk>/', views.WaterUtilityDetailsView.as_view(), name='water-utility-details'),
    path('autocomplete/', views.WaterUtilityAutoCompleteListView.as_view(), name='utilities-autocomplete')
]
