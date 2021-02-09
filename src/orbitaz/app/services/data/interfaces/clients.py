from abc import ABC, abstractmethod, abstractproperty
from typing import Annotated, Union


# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////// FTC SINGLE
class FileTransferClient(ABC):

    """
    Docstring
    ---------

        Summary
        -------
        Interface for clients that perform single downloads

        See
        ---
            https://dev.to/ezzy1337/a-pythonic-guide-to-solid-design-principles-4c8i
    """

    @abstractmethod
    def download(self, target: str) -> None:
        pass


# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////////////// FTC BULK
class BulkFileTransferClient(ABC):
    """
    Docstring
    ---------

        Summary
        -------
        Interface for clients that perform bulk downloads

        See
        ---
            https://dev.to/ezzy1337/a-pythonic-guide-to-solid-design-principles-4c8i
    """

    @abstractmethod
    def download_bulk(self, targets: list[str]):
        pass


# ______________________________________________________________________________
# //////////////////////////////////////////////////////////////////// TYPE HINT
# Parent class annotation for FileTransferClient and BulkFileTransferClient
TransferClient = Annotated[Union[FileTransferClient, BulkFileTransferClient], "Client"]