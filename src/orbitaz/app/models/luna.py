from django.db import models

from orbitaz.app.models.meta.timestamp import TimeStampMixin
from orbitaz.app.models.worker import Worker


class Luna(TimeStampMixin):

    STATUS_TYPES = (
        ("active", "Active"),
        ("lost_in_space", "Inactive"),
    )

    captain = models.CharField(max_length=50)
    contact = models.EmailField()
    status = models.CharField(choices=STATUS_TYPES, max_length=15)
    worker = models.ForeignKey(Worker, models.DO_NOTHING, null=True)
    max_workers = models.IntegerField()
    score = models.FloatField()
