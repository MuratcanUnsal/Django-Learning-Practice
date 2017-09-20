
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_list_or_404
from .models import Player
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView
from .forms import PlayerSearchForm
import re


class IndexView(ListView):

    model = Player
    template_name = 'players/all_players.html'
    paginate_by = 40
    #queryset = Player.objects.all()

    '''def get_queryset(self):

        req = self.request.GET.get("group")
        if req is None or req == "all":
            return Player.objects.all()
        elif req == "attk":
            return Player.objects.filter(role__iexact="Attacker")
        elif req == "mid":
            return Player.objects.filter(role__iexact="Midfielder")
        elif req == "def":
            return Player.objects.filter(role__iexact="Defender")
        elif req == "gk":
            return Player.objects.filter(role__iexact="Goalkeeper")'''


    def get_context_data(self, **kwargs):

        context = super(ListView, self).get_context_data(**kwargs)
        form = PlayerSearchForm("")
        context["form"] = form

        
        x = self.request.META["QUERY_STRING"]
        context["full_path"] = x


        updated_params = self.param_maker(x)
        context["updated_param_list"] = updated_params

        return context


    def param_maker(self, query_str):

 
        params = [
            {"title": "Position", "section": "group", "values": ["all","attk","mid", "def","gk"], "sub_title": ["All Positions", "Attackers", "Midfielders", "Defenders", "Goalkeepers"]},
            {"title": "Level", "section": "level", "values": ["gold", "silver", "bronze"], "sub_title": ["Gold", "Silver", "Bronze"]},
            {"title": "Skills", "section": "skills", "values": ["all", "5", "4", "3", "2", "1"], "sub_title": ["All", "5", "4", "3", "2", "1"]},
            {"title": "Weak Foot", "section": "wf", "values": ["5", "4", "3", "2", "1"], "sub_title": ["5", "4", "3", "2", "1"]},
            {"title": "Work Rate", "section": "wr", "values": ["hh", "hm", "hl", "mh", "mm", "ml", "lh", "lm", "ll"],
                                                    "sub_title": ["High/High", "High/Medium", "High/Low",
                                                                  "Medium/High", "Medium/Medium", "Medium/Low",
                                                                  "Low/High", "Low/Medium", "Low/Low"]},
            {"title": "Foot", "section": "foot", "values": ["all", "left", "right"], "sub_title": ["All", "Left", "Right"]}]


        for k in range(len(params)):

             params[k]["values"] = self.inject_param(query_str, params[k]["section"], params[k]["values"])

        return params



    def inject_param(self, query_str, section, values):

        if len(query_str) == 0:
            response_ready_hrefs = list(map(lambda x: "?{0}={1}".format(section, x), values))

            return response_ready_hrefs
        if len(query_str) != 0:
            if query_str.find(section) != -1:

                y = re.search(r'({0}[^&]+)'.format(section), query_str).group()
                response_ready_hrefs = list(map(lambda x: "?" + query_str.replace(y, section + "=" + x), values))
                return response_ready_hrefs
            else:
                
                response_ready_hrefs = list(map(lambda x: '?' + query_str + '&' + section + '=' + x, values))
                return response_ready_hrefs



def player_detail(request, player_id):
    
    query_set = Player.objects.filter(id=player_id)

    return render(request, "players/player_det.html", {"query_set": query_set})



class SearchView(ListView):

    query = ""
    paginate_by = 30
    context_object_name = "players"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context["form"] = PlayerSearchForm(self.query)
        context["search_request"] = ("query="+self.query)
        return context

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get("query", "")
        return super(SearchView, self).get(request, *args, ** kwargs)

    def get_queryset(self):

        if not self.query:
            player_list = Player.objects.all()

        else:
            player_list = Player.objects.filter(query_helper__icontains=self.query)

        return player_list


