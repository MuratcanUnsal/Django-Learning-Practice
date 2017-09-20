__author__ = 'Crashmotilda'
__author__ = 'Crashmotilda'
from django.conf.urls import url

from . import views

app_name = "main_page"

urlpatterns = [
    url(r'^$', views.main_pa, name='main_pa'),
    #url(r'^$', views.MainPageView.as_view(), name='main_pa'),

]