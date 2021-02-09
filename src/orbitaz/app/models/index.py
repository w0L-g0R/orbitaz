from django.db import models
from .unit import Unit
from .point_of_origin import PointOfOrigin


class Index(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateField(max_length=5)
    base_year = models.CharField(max_length=100)
    granularity = models.CharField(max_length=10)
    unit = models.ForeignKey(Unit, models.DO_NOTHING, null=True)
    point_of_origin = models.ForeignKey(PointOfOrigin, models.DO_NOTHING, null=True)


class IndexValue(models.Model):
    value = models.CharField(max_length=100)
    date = models.DateField(max_length=5)
    index = models.ForeignKey(Index, models.DO_NOTHING, null=True)
