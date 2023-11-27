from django.urls import include, path


urlpatterns = [
	path('auth/', include('api.auth.urls')),
	path('users/', include('api.user.urls')),
	path('utilities/', include('api.utility.urls')),
	path('alerts/', include('api.alert.urls')),
	path('sensors/', include('api.sensor.urls')),
	path('settings/', include('api.settings.urls')),
	path('resource-allocations/', include('api.resource_allocation.urls')),
	path('technicians/', include('api.technician.urls')),
	path('legacy-reports/', include('api.temp_report.urls')),
	path('reports/', include('api.reports.urls')),
	path('pumps/compare-reports/', include('api.pumps.urls')),
	path('memo/', include('api.memo.urls')),
	# webhook endpoint
	path('devices/', include('api.iot.urls')),
]
