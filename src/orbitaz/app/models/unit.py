from django.db import models


class Unit(models.Model):
    currency = models.CharField(max_length=100)
    currency_acronym = models.CharField(max_length=5)
    measure = models.CharField(max_length=100)
    measure_acronym = models.CharField(max_length=10)

    def __str__(self):
        return f"Currency: {self.currency} - Measure: {self.measure}"
