from abc import ABC, abstractmethod
from orbitaz.app.models.price import EEXManager
from orbitaz.app.services.data.eex.drivers import EEXDriver
from orbitaz.app.services.data.eex.clients import EEXClient
from orbitaz.app.services.data.eex.parsers import EEXParser
from orbitaz.app.services.data.eex.specifications import EEXSpecs
from orbitaz.app.services.data.interfaces.factories import DataFactory

# ______________________________________________________________________________
# ////////////////////////////////////////////////////////////////// EEX FACTORY
class EEXFactory(DataFactory):

    """
    Concrete factory which assembles the specific parts that are necessary to perform an EEX data transfer
    """

    # @property
    # @abstractmethod
    # def data(self):
    #     pass

    # @data.setter
    # @abstractmethod
    # def data(self, data):
    #     pass

    def create_client(self) -> EEXClient:
        return EEXClient(driver=EEXDriver, specs=EEXSpecs)

    def create_parser(self) -> EEXParser:
        pass

    def create_manager(self) -> EEXManager:
        return EEXManager
