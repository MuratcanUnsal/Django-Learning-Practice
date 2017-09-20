from django.shortcuts import render
from django.http import HttpResponse
from players.forms import PlayerSearchForm
# Create your views here.
from django.views.generic import ListView
from players.models import Player


def main_pa(request):
    form = PlayerSearchForm("")
    #return render(request, 'main_page/main.html', {"form": form})
    return render(request, 'main_page/main.html', {"form": form})

