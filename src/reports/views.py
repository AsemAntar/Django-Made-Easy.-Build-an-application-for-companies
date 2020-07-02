from django.shortcuts import render

from .forms import ReportForm, ProblemReportedForm
from .models import Report


def report_view(request, production_line):
    form = ReportForm()
    pform = ProblemReportedForm(request.POST or None)
    queryset = Report.objects.filter(production_line__name=production_line)

    r_id = request.POST.get("report_id")

    if pform.is_valid():
        report = Report.objects.get(id=r_id)
        new_problem = pform.save(commit=False)
        new_problem.user = request.user
        new_problem.report = report
        new_problem.save()

    context = {
        'form': form,
        'pform': pform,
        'report_list': queryset,
    }

    return render(request, 'reports/report.html', context)
