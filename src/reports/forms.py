from django import forms
from .models import Report, ProblemReported


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = "__all__"


class ProblemReportedForm(forms.ModelForm):
    class Meta:
        model = ProblemReported
        # fields = "__all__"
        exclude = ('user', 'report',)
