from django import forms
from . import models


class CreatePhotoForm(forms.ModelForm):

    class Meta:
        model = models.Photo
        fields = ("file",)

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        photographer = models.Photographer.objects.get(pk=pk)
        photo.photographer = photographer
        photo.save()


class ApplyZzigsaForm(forms.ModelForm):
    class Meta:
        model = models.Photographer
        fields = (
            "introduction",
            "title",
            "description",
            "location",
            "equip",
            "equip_picture",
            "sns",
            "profile",
        )