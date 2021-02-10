from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

from orbitaz.app.models.meta.timestamp import TimeStampMixin


class Forecast(TimeStampMixin):
    series = models.JSONField(encoder=DjangoJSONEncoder)
    accuracy = models.FloatField()
    method = models.CharField(max_length=25)
