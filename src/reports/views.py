from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, FormView
from django.template.loader import render_to_string

from .forms import ReportForm, ProblemReported, ProblemReportedForm, SelectReportForm, ReportResultForm
from .models import Report
from areas.models import ProductionLine

from weasyprint import HTML
import tempfile


def get_generated_problems_in_pdf(request):
    problems = ProblemReported.objects.problems_from_today()
    context = {
        'problems': problems,
    }

    # render
    html_string = render_to_string('reports/problems.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # http response
    response = HttpResponse(content_type='application/pdf;')
    response['content-Disposition'] = 'inline; filename=problem_list.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


class HomeView(FormView):
    template_name = 'reports/home.html'
    form_class = SelectReportForm

    # get the current logged in user
    def get_form_kwargs(self):
        kwargs = super(HomeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, *args, **kwargs):
        prod_line = self.request.POST.get('prod_line')
        return redirect('reports:report_view', production_line=prod_line)


class SelectView(FormView):
    template_name = 'reports/select.html'
    form_class = ReportResultForm
    success_url = reverse_lazy('reports:report_summary')

    def form_valid(self, form):
        # get the selected date from the datepicker
        self.request.session['day'] = self.request.POST.get('day' or None)
        # get the id of the production line selected from the form
        self.request.session['production_line'] = self.request.POST.get(
            'production_line' or None)
        return super(SelectView, self).form_valid(form)


@login_required
def main_report_summary(request):
    try:
        day = request.session.get('day' or None)
        prod_id = request.session.get('production_line' or None)
        production_line = ProductionLine.objects.get(id=prod_id)
        execution_qs = Report.objects.filter_by_line_and_day(
            day, prod_id).aggregate_execution()['execution__sum']
        plan_qs = Report.objects.filter_by_line_and_day(
            day, prod_id).aggregate_plan()['plan__sum']
        problems = ProblemReported.objects.get_problem_by_day_and_line(
            day, production_line)
    except:
        pass
    context = {
        'execution_qs': execution_qs,
        'plan_qs': plan_qs,
        'day': day,
        'production_line': production_line,
        'problems': problems,
    }
    return render(request, 'reports/summary.html', context)


@login_required
def report_view(request, production_line):
    form = ReportForm(request.POST or None, production_line=production_line)
    pform = ProblemReportedForm(request.POST or None)
    queryset = Report.objects.filter(production_line__name=production_line)
    # return the production line or 404 if not created yet
    line = get_object_or_404(ProductionLine, name=production_line)

    if "submitbtn1" in request.POST:
        r_id = request.POST.get("report_id")
        if pform.is_valid():
            report = Report.objects.get(id=r_id)
            new_problem = pform.save(commit=False)
            new_problem.user = request.user
            new_problem.report = report
            new_problem.save()
            # form = ReportForm()
            # pform = ProblemReportedForm()
            return redirect(request.META.get('HTTP_REFERER'))
    elif "submitbtn2" in request.POST:
        if form.is_valid():
            new_report = form.save(commit=False)
            new_report.user = request.user
            new_report.production_line = line
            new_report.save()
            # form = ReportForm()
            # pform = ProblemReportedForm()
            return redirect(request.META.get('HTTP_REFERER'))

    context = {
        'form': form,
        'pform': pform,
        'report_list': queryset,
    }

    return render(request, 'reports/report.html', context)


@login_required
def delete_report(request, *args, **kwargs):
    r_id = kwargs.get('pk')
    report = Report.objects.get(id=r_id)
    report.delete()
    return redirect(request.META.get('HTTP_REFERER'))


class UpdateReportView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/update.html'

    def get_success_url(self):
        return self.request.path
