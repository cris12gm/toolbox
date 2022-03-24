# Create your views here.
import os
import time
from subprocess import Popen, PIPE
import json
from sRNAtoolboxweb.settings import STATIC_ROOT

from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from rest_framework import generics
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView
from progress.models import JobStatus, Status
from sRNAtoolboxweb.settings import CONF, SUB_SITE
from progress.serializers import JobStatusSerializer, StatusSerializer
from django.core.urlresolvers import reverse

def content(request):
    template = "content.html"

    fileContent = STATIC_ROOT+"toolboxDB.json"

    with open(fileContent) as json_file:
        data = json.load(json_file)

    header = ["Scientific name","Taxon ID","Assembly","miRNA","Other annotations"]
    results = {}

    table = []

    for element in data:
        values = data[element]
        values ['taxonID'] = element
        table.append(values)
    
    print (header)
    results["table"] = table
    results["header"] = header
    return render(request, template, results)