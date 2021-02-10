from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

from orbitaz.app.models.meta.timestamp import TimeStampMixin
from orbitaz.app.models.jao.specifications import JaoSpecs


class JaoData(TimeStampMixin):

    specification = models.ForeignKey(JaoSpecs, on_delete=models.DO_NOTHING, null=True)
    frame = models.JSONField(encoder=DjangoJSONEncoder)
