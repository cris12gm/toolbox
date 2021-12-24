from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.sRNAcons.as_view(), name="srnacons"),
    url(r'result', views.result, name='result')
]
