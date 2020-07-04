from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, FormView

from .forms import ReportForm, ProblemReportedForm, SelectReportForm, ReportResultForm
from .models import Report
from areas.models import ProductionLine


@login_required
def main_report_summary(request):
    try:
        day = request.session.get('day' or None)
        print(day)
    except:
        pass

    return render(request, 'reports/summary.html', {})


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
        self.request.session['day'] = self.request.POST.get('day' or None)
        print(self.request.session['day'])
        return super(SelectView, self).form_valid(form)


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
