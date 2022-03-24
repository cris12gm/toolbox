from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'result', views.result, name="srnacons"),
<<<<<<< HEAD
    url(r'^ajax_species$', views.querySpecies, name='ajax_species'),
=======
>>>>>>> upstream/develop
    url(r'^$', views.sRNAcons.as_view(), name="SRNACONS")
]