from django.urls import path
from . import views
from photographer import views as photographer_views

app_name = "core"

urlpatterns = [
    path("", photographer_views.HomeView.as_view(), name="home")
]