from django.conf import settings
from django import setup

if not settings.configured:

    settings.configure(DEBUG=True)

    # This is needed since it is a standalone django package
    setup()

from orbitaz.app.models import CommodityProduct