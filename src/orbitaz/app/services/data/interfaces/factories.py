from abc import ABC, abstractmethod
from django.db.models import Manager as DatabaseManager

from orbitaz.app.services.data.interfaces.drivers import Driver
from orbitaz.app.services.data.interfaces.specifications import TransferSpecifications
from orbitaz.app.services.data.interfaces.clients import TransferClient
from orbitaz.app.services.data.eex.parsers import DataParser

# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////// ABSTRACT FACTORY
class DataFactory(ABC):

    """
    Abstract factory interface provides three methods that need to be implemented in its subclasses:
    create_client, create_parser and create_manager.
    """

    # @property
    # @abstractmethod
    # def data(self):
    #     pass

    # @data.setter
    # @abstractmethod
    # def data(self, data):
    #     pass

    @abstractmethod
    def create_client(
        self, driver: Driver, specs: TransferSpecifications
    ) -> TransferClient:
        pass

    @abstractmethod
    def create_parser(self) -> DataParser:
        pass

    @abstractmethod
    def create_manager(self) -> DatabaseManager:
        """ Django model manager that provides a tailored interface to interact with the database"""
        pass
