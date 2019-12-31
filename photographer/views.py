from django.views.generic import ListView, DetailView
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


class PhotographerDetail(DetailView):
    
    """ Photographer Detail Definition """

    model = models.Photographer
    