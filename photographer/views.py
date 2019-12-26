from django.views.generic import ListView
from django.shortcuts import render
from . import models

# Create your views here.
class HomeView(ListView):

    """ HomeView Definition """

    model = models.Photographer
    paginate_by = 10
    # paginate_orphans = ??
    ordering = "created"
    context_object_name = "photographers"


def photographer_detail(request, pk):
    photographer = models.Photographer.objects.get(pk=pk)
    return render(request, "photographer/detail.html", {'photographer': photographer})