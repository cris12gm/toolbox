from . import views
from django.conf.urls import url


urlpatterns = [
    url('',views.content, name='content')
    ]