from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'result', views.result, name="srnacons"),
    url(r'^show_species$', views.querySpecies, name='show_species'),
    url(r'^$', views.sRNAcons.as_view(), name="SRNACONS")
]
