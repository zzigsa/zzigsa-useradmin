from django.urls import path
from . import views

app_name = "photographers"

urlpatterns = [path("<int:pk>", views.photographer_detail, name="detail")]
