# Create your views here.
import datetime
import itertools
import os
import urllib

import django_tables2 as tables
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .forms import sRNAconsForm
from progress.models import JobStatus
from utils import pipeline_utils
from utils.sysUtils import make_dir
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from FileModels.sRNAconsParsers import sRNAconsParser
from .summary_plots import makesrnasPlot,makeSpeciesPlot
from django.http import JsonResponse

CONF = settings.CONF
FS = FileSystemStorage(CONF["sRNAtoolboxSODataPath"])

counter = itertools.count()


class TableResult(tables.Table):
    """
    Class to serialize table of results
    """

    class Meta:
        orderable = True
        attrs = {'class': 'table table-striped table-bordered table-hover dataTable no-footer',
                 "id": lambda: "table_%d" % next(counter)}
        empty_text = "Results not found!"
        order_by = ("percentage")


def define_table(columns, typeTable):
    """
    :param columns: Array with names of columns to show
    :return: a class of type TableResults
    """
    attrs = dict((c, tables.Column()) for c in columns)

    if typeTable == "TableResult":
        attrs['Meta'] = type('Meta', (),
                             dict(attrs={'class': 'table table-striped table-bordered table-hover dataTable no-footer',
                                         "id": lambda: "table_%d" % next(counter)},
                                  ordenable=True,
                                  empty_text="Results not found!",
                                  order_by=("Frequency",)))
    else:
        attrs['Meta'] = type('Meta', (),
                             dict(attrs={'class': 'table table-striped',
                                         "id": "notformattable"},
                                  ordenable=True,
                                  empty_text="Results not found!",
                                  order_by=("frequency",)))


    klass = type('TableResult', (tables.Table,), attrs)
    return klass

def querySpecies(request):
    if 'id' in request.GET and 'element' in request.GET:
        job_id = request.GET['id']
        selected = request.GET['element']

        try:
            new_record = JobStatus.objects.get(pipeline_key=job_id)
            fileTable = open(os.path.join(new_record.outdir, "sRNA2Species.txt"),'r')
            fileTable.readline()
            tableSRNA = {}
            tableSRNA['header'] = ["Species"]
            tableSRNA['content'] = []

            for element in fileTable:
                element = element.strip().split("\t")
                if element[0] == selected:
                    tableSRNA['name'] = selected
                    tableSRNA['percentage'] = element[1]
                    tableSRNA['frequency'] = element[2]
                    for sp in element[3].split(","):
                        sp = sp.split(";")
                        tableSRNA['content'].append(sp[0])

            results = {}
            results['tableSRNA'] = tableSRNA
            results['id'] = job_id
            return render(request, 'sRNAcons/srnacons_showmore.html', results)
        except:
            return redirect(settings.SUB_SITE)
    else:
        return redirect(settings.SUB_SITE)



class Result():
    """
    Class to manage tables results and meta-info
    """

    def __init__(self, name, table):
        self.name = name.capitalize()
        self.content = table
        self.id = name.replace(" ", "_")


def input(request):
    """
    :rtype : render
    :param request: posts and gets
    :return: html with main of functerms
    """
    return render(request, 'sRNAcons/srnacons_input.html', {})



def result(request):
    if 'id' in request.GET:
        job_id = request.GET['id']

        new_record = JobStatus.objects.get(pipeline_key=job_id)
        assert isinstance(new_record, JobStatus)

        results = {}
        results["id"] = job_id
        if new_record.job_status == "Finished":
            results["info"] = "Correct"
            results["date"] = new_record.start_time + datetime.timedelta(days=15)

            try:
                results["parameters"] = new_record.parameters
            except:
                pass

            if os.path.exists(os.path.join(new_record.outdir,"identicalSequenceRelation.tsv")):
                try:
                    fileTable = open(os.path.join(new_record.outdir, "sRNA2Species.txt"),'r')
                    tableSRNA = {}
                    fileTable.readline()
                    header = ["Name","Percentage","Frequency","Species"]
                    tableSRNA['header'] = header
                    tableSRNA['content'] = []
                    for element in fileTable:
                        element = element.split("\t")
                        new = []
                        for sp in element[3].split(","):
                            sp = sp.split(";")[0]
                            new.append(sp)
                        element[3] = new
                        
                        tableSRNA['content'].append(element)

                    results["srna2sp"] = tableSRNA

                except:
                    pass
     
                parser = sRNAconsParser(os.path.join(new_record.outdir, "species2SRNA.txt"), "species2srna", 1000)
                srna2sp = [obj for obj in parser.parse()]
                header = srna2sp[0].get_sorted_attr()
                blast_result = Result("sRNAs per species", define_table(header, 'TableResult')(srna2sp))
                results["sp2srna"] = blast_result

                try:
                    graphicSum = makesrnasPlot(os.path.join(new_record.outdir, "sRNA2Species.txt"))
                    results["graphicSum"] = graphicSum
                except:
                    pass

                try:
                    graphicSum_2 = makeSpeciesPlot(os.path.join(new_record.outdir, "species2SRNA.txt"))
                    results["graphicSum_2"] = graphicSum_2
                except:
                    pass
                try:
                    cmd = "zip -j -r "+os.path.join(new_record.outdir,"results.zip")+" "+os.path.join(new_record.outdir,"sRNA2Species.txt")+" "+os.path.join(new_record.outdir,"species2SRNA.txt")
                    os.system(cmd)
                    results["downloadAll"] =  (os.path.join(new_record.outdir,"results.zip")).replace(settings.MEDIA_ROOT,settings.MEDIA_URL)
                    results["downloadsRNA"] = (os.path.join(new_record.outdir,"sRNA2Species.txt")).replace(settings.MEDIA_ROOT,settings.MEDIA_URL)
                    results["downloadspecies"] = (os.path.join(new_record.outdir,"species2SRNA.txt")).replace(settings.MEDIA_ROOT,settings.MEDIA_URL)
                except:
                    results["downloadAll"]=""
                    results["downloadsRNA"] = ""
                    results["downloadspecies"] = ""
            else:
                results["error"] = "Some errors were detected, please email with the number of this jobID ("+job_id+") to the administrator of the website."
            return render(request, 'sRNAcons/srnacons_result.html', results)
        else:
            return redirect(reverse_lazy('progress', kwargs={"pipeline_id": job_id}))
    else:
        return redirect(settings.SUB_SITE)


class sRNAcons(FormView):
    template_name = 'sRNAcons/srnacons_input.html'
    form_class = sRNAconsForm

    success_url = reverse_lazy("srnacons")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        call, pipeline_id = form.create_call()
        os.system(call)
        js = JobStatus.objects.get(pipeline_key=pipeline_id)
        js.status.create(status_progress='sent_to_queue')
        js.job_status = 'sent_to_queue'
        js.save()
        self.success_url = reverse_lazy('srnacons') + '?id=' + pipeline_id
        return super(sRNAcons, self).form_valid(form)
