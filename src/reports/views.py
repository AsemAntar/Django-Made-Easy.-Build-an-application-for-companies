from django.shortcuts import render

from .forms import ReportForm, ProblemReportedForm
from .models import Report


def report_view(request, production_line):
    form = ReportForm()
    pform = ProblemReportedForm()

    queryset = Report.objects.filter(production_line__name=production_line)

    context = {
        'form': form,
        'pform': pform,
        'report_list': queryset,
    }

    return render(request, 'reports/report.html', context)
