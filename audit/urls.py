from django.urls import path
from .views import home, analyze_url

urlpatterns = [
    path("", home, name="home"),
    path("analyze/", analyze_url, name="analyze"),
]