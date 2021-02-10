from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from orbitaz.app.models.luna import Luna


class MissionControl(models.Model):
    luna = models.ForeignKey(Luna, models.DO_NOTHING, null=True)
    scores = models.JSONField(encoder=DjangoJSONEncoder)

    # class Meta:

    #     # Assures that a get query with "latest()" argument returns the price with the greatest counter_update value (for a specific date)
    #     ordering = ["-counter_update"]

    #     # Assures that per date only one price entry for a commodity product can be saved
    #     # constraints = [
    #     #     models.UniqueConstraint(
    #     #         fields=["commodity_product", "date"], name="unique date"
    #     #     )
    #     # ]

    # def save(self, *args, **kwargs):
    #     # Custom logic (e.g. validation, logging, call third party service)
    #     # Run default save() method
    #     super(Price, self).save(*args, **kwargs)
    #     return

    # def delete(self, *args, **kwargs):
    #     # Custom logic (e.g. validation, logging, call third party service)
    #     # Run default save() method
    #     super(Price, self).save(*args, **kwargs)
    #     return
