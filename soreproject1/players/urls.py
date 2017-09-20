__author__ = 'Crashmotilda'
from django.conf.urls import url

from . import views
app_name = "players"
urlpatterns = [
    # /players/
    #url(r'results/', views.player_search, name="player_search")
    url(r'results', views.SearchView.as_view(), name="player_search"),
    # /players/<player_id>
    url(r'^(?P<player_id>[0-9]+)/', views.player_detail, name='player_detail'),
    #url(r'^$', views.index, name='index'),
    url(r'^', views.IndexView.as_view(), name='index'),





]


