from django.db import models


class PointOfOrigin(models.Model):
    country = models.CharField(max_length=75)
    country_acronym = models.CharField(max_length=10)
    eu = models.BooleanField()

    def __str__(self):
        return f"Country: {self.country}"
