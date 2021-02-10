from django.db import models
from .mappings import DOMAIN_MAPPINGS, BIDDING_ZONES, BSNTYPE, PSRTYPE


class EntsoSpecs(models.Model):

    domain = models.CharField(choices=DOMAIN_MAPPINGS, max_length=10)
    bidding_zone = models.CharField(choices=BIDDING_ZONES, max_length=10)
    power_source = models.CharField(choices=BSNTYPE, max_length=10)
    allocation_type = models.CharField(choices=PSRTYPE, max_length=10)
    start = models.DateField()
    end = models.DateField()
    resolution = models.DurationField()
    unit = models.CharField(max_length=10)