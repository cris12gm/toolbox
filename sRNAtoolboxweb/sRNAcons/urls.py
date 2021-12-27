from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'result', views.result, name='result'),
    url(r'^$', views.sRNAcons.as_view(), name="srnacons")
]
