from django.http import Http404
from django.views.generic import ListView, DetailView, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from user import mixins as user_mixins
from . import models, forms
from .filters import ZzigsaFilter

# Create your views here.
class HomeView(ListView):

    """ HomeView Definition """

    model = models.Photographer
    paginate_by = 10
    # paginate_orphans = ??
    ordering = "created"
    context_object_name = "photographers"

    def get_queryset(self):
        qs = self.model.objects.all()
        zzigsa_filtered_list = ZzigsaFilter(self.request.GET, queryset=qs)
        return zzigsa_filtered_list.qs


class PhotographerDetail(DetailView):
    
    """ Photographer Detail Definition """

    model = models.Photographer


class EditPhotographerView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Photographer
    template_name = "photographer/photographer_edit.html"
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
    
    def get_object(self, queryset=None):
        photographer = super().get_object(queryset=queryset)
        if photographer.zzigsa.pk != self.request.user.pk:
            raise Http404
        return photographer


class PhotographerPhotosView(user_mixins.LoggedInOnlyView, PhotographerDetail):    

    model = models.Photographer
    template_name = "photographer/photographer_photos.html"

    def get_object(self, queryset=None):
        photographer = super().get_object(queryset=queryset)
        if photographer.zzigsa.pk != self.request.user.pk:
            raise Http404
        return photographer


@login_required
def delete_photo(request, photographer_pk, photo_pk):
    user = request.user
    try:
        photographer = models.Photographer.objects.get(pk=photographer_pk)
        if photographer.zzigsa.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo deleted")
        return redirect(reverse("photographers:photos", kwargs={"pk": photographer_pk}))
    except models.Photographer.DoesNotExist:
        return redirect(reverse("core:home"))


class AddPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, FormView):

    template_name = "photographer/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("photographers:photos", kwargs={"pk": pk}))


class ApplyZzigsaView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.ApplyZzigsaForm
    template_name = "photographer/zzigsa_create.html"

    def form_valid(self, form, *args, **kwargs):
        pk = kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "찍사 신청되었습니다")
        return redirect(reverse("photographers:detail", kwargs={"pk": pk}))