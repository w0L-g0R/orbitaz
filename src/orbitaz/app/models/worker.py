from django.db import models

# from django_q.models import Schedule

from orbitaz.app.models.entso.data import EntsoData
from orbitaz.app.models.meta.timestamp import TimeStampMixin
from orbitaz.app.models.entso.data import EntsoData
from orbitaz.app.models.jao.data import JaoData
from orbitaz.app.models.forecast import Forecast


class Worker(TimeStampMixin):
    entso_data = models.ForeignKey(EntsoData, models.DO_NOTHING, null=True)
    jao_data = models.ForeignKey(JaoData, models.DO_NOTHING, null=True)
    forecast = models.ForeignKey(Forecast, models.DO_NOTHING, null=True)
    # schedule = models.Schedule()