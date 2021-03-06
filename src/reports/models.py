from datetime import datetime
import random
import string


from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from areas.models import ProductionLine
from categories.models import Category
from products.models import Product


# custom variables to be used in models
HOURS = ((str(i), str(i)) for i in range(1, 25))
HOURS2 = ((str(i), str(i)) for i in range(1, 25))
el = [i for i in string.ascii_uppercase] + [i for i in range(10)]


# define a custom  report queryset to add some methods to use them in the custom manager
class ReportQuerySet(models.QuerySet):
    def filter_by_line_and_day(self, day, line_id):
        return self.filter(day=day, production_line__id=line_id)

    def aggregate_execution(self):
        return self.aggregate(Sum('execution'))

    def aggregate_plan(self):
        return self.aggregate(Sum('plan'))


# define custom  report manager
class ReportManager(models.Manager):
    # using the custome queryset inside the custom manager
    def get_queryset(self):
        return ReportQuerySet(self.model, using=self._db)

    def filter_by_line_and_day(self, day, line_id):
        return self.get_queryset().filter_by_line_and_day(day, line_id)

    def aggregate_execution(self):
        return self.get_queryset().aggregate_execution()

    def aggregate_plan(self):
        return self.get_queryset().aggregate_plan()


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    production_line = models.ForeignKey(
        ProductionLine, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    day = models.DateField(default=timezone.now)
    start_hour = models.CharField(max_length=2, choices=HOURS)
    end_hour = models.CharField(max_length=2, choices=HOURS2)
    # The amount you want to produce
    plan = models.PositiveIntegerField()
    # The actual produced quantity
    execution = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # instantiate the ReportManager
    objects = ReportManager()

    # define a function for customly formatting date
    def get_day(self):
        return self.day.strftime('%d/%m/%Y')

    def get_absolute_url(self):
        return reverse("reports:update_report", kwargs={"production_line": self.production_line, "pk": self.pk})

    def __str__(self):
        return f"{self.start_hour}-{self.end_hour}-{self.production_line}"

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'


def random_code():
    random.shuffle(el)
    code = [str(x) for x in el[:12]]
    str_code = ''.join(code)
    return str_code


# define custom  report manager
class ProblemReportedManager(models.Manager):
    def get_problem_by_day_and_line(self, day, line):
        return super().get_queryset().filter(report__day=day, report__production_line__name=line)

    # get problems of the current day
    def problems_from_today(self):
        now = datetime.now().strftime('%Y-%m-%d')
        return super().get_queryset().filter(report__day=now)


class ProblemReported(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    description = models.TextField()
    problem_id = models.CharField(
        max_length=12, unique=True, blank=True, default=random_code)
    # how much time does it take to solve the problem
    breakdown = models.PositiveIntegerField()
    public = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # custom manager
    objects = ProblemReportedManager()

    def __str__(self):
        return f"{self.category.name}-{self.description[:20]}"

    class Meta:
        verbose_name = 'problem reported'
        verbose_name_plural = 'problems reported'
