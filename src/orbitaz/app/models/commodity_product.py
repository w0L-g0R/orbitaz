from django.db import models
from .unit import Unit
from .point_of_origin import PointOfOrigin
from django.core.exceptions import ValidationError


class CommodityProduct(models.Model):

    GRANULARITIES = (
        ("day", "Daily"),
        ("week", "Weekly"),
        ("month", "Monthly"),
        ("season", "Each quarter"),
    )

    commodity = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    vat = models.BooleanField()
    source = models.CharField(max_length=100)
    start_time = models.DateField()
    granularity = models.CharField(choices=GRANULARITIES, max_length=10)
    point_of_origin = models.ForeignKey(
        PointOfOrigin, on_delete=models.DO_NOTHING, null=True
    )
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.commodity} | {self.product} | {self.point_of_origin}"
