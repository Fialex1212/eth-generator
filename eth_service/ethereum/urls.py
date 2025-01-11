from django.urls import path
from . import views

urlpatterns = [
    path('generate_keys/', views.generate_keys, name='generate_keys'),
    path('download_keys/', views.download_keys, name='download_keys'),
]