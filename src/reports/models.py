from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from areas.models import ProductionLine
from categories.models import Category
from products.models import Product


HOURS = ((str(i), str(i)) for i in range(1, 25))
HOURS2 = ((str(i), str(i)) for i in range(1, 25))


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

    # define a function for customly formatting date
    def get_day(self):
        return self.day.strftime('%d/%m/%Y')

    def __str__(self):
        return f"{self.start_hour}-{self.end_hour}-{self.production_line}"

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'


class ProblemReported(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    description = models.TextField()
    problem_id = models.CharField(max_length=12, unique=True, blank=True)
    # how much time does it take to solve the problem
    breakdown = models.PositiveIntegerField()
    public = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name}-{self.description[:20]}"

    class Meta:
        verbose_name = 'problem reported'
        verbose_name_plural = 'problems reported'
