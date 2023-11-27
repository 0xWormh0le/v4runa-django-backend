from django.urls import path
from . import views


urlpatterns = [
    path('', views.MemoView.as_view(), name='memo'),
]
