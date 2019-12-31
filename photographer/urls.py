from django.urls import path
from . import views

app_name = "photographers"

urlpatterns = [path("<int:pk>", views.PhotographerDetail.as_view(), name="detail")]
