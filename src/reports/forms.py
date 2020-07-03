from django import forms
from django.shortcuts import get_object_or_404
from .models import Report, ProblemReported
from areas.models import ProductionLine


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        # fields = "__all__"
        exclude = ('user', 'production_line',)

    def __init__(self, *args, **kwargs):
        production_line = kwargs.pop('production_line', None)
        super(ReportForm, self).__init__(*args, **kwargs)
        if production_line is not None:
            line = get_object_or_404(ProductionLine, name=production_line)
            self.fields['product'].queryset = line.products.all()


class ProblemReportedForm(forms.ModelForm):
    class Meta:
        model = ProblemReported
        # fields = "__all__"
        exclude = ('user', 'report', 'problem_id',)
