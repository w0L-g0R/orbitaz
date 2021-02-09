import datetime
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from orbitaz.app.services.data.eex.factories import DataFactory

# //////////////////////////////////////////////////////////////////// INTERFACE
class DataTransfer:
    """
    Docstring
    ---------

        Summary
        ---------
        Access class for clients (here: automated workers, terminal users).

        Parameter
        ---------
            factory: DataFactory
                Injects all "parts" for a specific data transfer
    """

    def __init__(self, factory: DataFactory):
        self._client = factory.create_client()
        self._manager = factory.create_manager()
        self._parser = factory.create_parser()

    def parse(self):
        self._parser.process()
        return

    def download(self, date: datetime.date):
        self._client.download(date=date)
        return

    def save(self):
        self._manager.save()
        return

    def update(self):
        self._manager.update()
        return