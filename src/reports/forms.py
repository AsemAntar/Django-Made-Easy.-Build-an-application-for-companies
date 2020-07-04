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


class SelectReportForm(forms.Form):
    production_line = forms.ModelChoiceField(
        queryset=ProductionLine.objects.none(), label='')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SelectReportForm, self).__init__(*args, **kwargs)
        self.fields['production_line'].queryset = ProductionLine.objects.filter(
            team_leader__user__username=self.user)


class ReportResultForm(forms.Form):
    production_line = forms.ModelChoiceField(
        queryset=ProductionLine.objects.all(), label='')
    day = forms.CharField(widget=forms.DateTimeInput(
        attrs={'class': 'datepicker'}
    ))
