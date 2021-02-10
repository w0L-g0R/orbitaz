from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

from orbitaz.app.models.meta.timestamp import TimeStampMixin
from orbitaz.app.models.entso.specifications import EntsoSpecs


class EntsoData(TimeStampMixin):

    specification = models.ForeignKey(
        EntsoSpecs, on_delete=models.DO_NOTHING, null=True
    )
    frame = models.JSONField(encoder=DjangoJSONEncoder)
