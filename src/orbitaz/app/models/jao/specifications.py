from django.db import models


class JaoSpecs(models.Model):

    domain = models.CharField(max_length=10)
    bidding_zone = models.CharField(max_length=10)
    start = models.DateField()
    end = models.DateField()
    resolution = models.DurationField()
    unit = models.CharField(max_length=10)