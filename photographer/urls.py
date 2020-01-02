from django.urls import path
from . import views

app_name = "photographers"

urlpatterns = [
    path("create/", views.ApplyZzigsaView.as_view(), name="create"),
    path("<int:pk>", views.PhotographerDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditPhotographerView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.PhotographerPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add/", views.AddPhotoView.as_view(), name="add-photo"),
    path("<int:photographer_pk>/photos/<int:photo_pk>/delete/", views.delete_photo, name="delete-photo"),
]
