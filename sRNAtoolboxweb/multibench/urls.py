#from sRNABench.views import Bench

__author__ = 'antonior'

from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'results', views.result_new, name='srnabench'),
    #url(r'results', views.result),
    #url(r'table/(.+)/(.+)/(.+)*', views.render_table, name='table_bench'),
    #url(r'align/(.+)/(.+)/(.+)', views.show_align, name='show_align'),
    # url(r'run$', views.run, name='run_bench'),
    url(r'^$', views.MultiBench.as_view(),  name="MULTI"),
    #url(r'test$', views.test),
]
