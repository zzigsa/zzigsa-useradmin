from django.db import models
from django.urls import reverse
from core import models as core_models
# Create your models here.

class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    file = models.ImageField(upload_to="portfolio")
    zzigsa = models.ForeignKey("Photographer", related_name="photos", on_delete=models.CASCADE)


class Photographer(core_models.TimeStampedModel):

    """ Photographer Model Definition """

    zzigsa = models.ForeignKey("user.User", related_name="photographer", on_delete=models.CASCADE)
    introduction = models.CharField(max_length=150)
    title = models.CharField(max_length=80)
    description = models.TextField()
    location = models.CharField(max_length=140)
    equip = models.CharField(max_length=100)
    equip_picture = models.ImageField(upload_to="equip", blank=True)
    sns = models.URLField(blank=True)
    profile = models.ImageField(upload_to="profile", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photographers:detail', kwargs={'pk': self.pk})

    def first_photo(self):
        photo, = self.photos.all()[:1]
        return photo.file.url

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos