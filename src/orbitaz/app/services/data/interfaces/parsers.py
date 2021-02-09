from abc import ABC, abstractmethod

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// PARSER


class DataParser(ABC):
    """An abstract product, that parses file content, in order to be used by a database manager.
    One of its subclasses will be created in factory methods."""

    @abstractmethod
    def process(self, content):
        pass
