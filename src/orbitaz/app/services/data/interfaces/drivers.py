from dataclasses import dataclass
from abc import ABC
from typing import Annotated, Union


# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////////////////// SFTP
@dataclass(frozen=True)
class SFTPDriver(ABC):

    """
    Includes basic configuration parameters for a sFTP connection
    """

    host: str
    username: str
    password: str

    def __post_init__(cls):
        """ Assures that this class never gets initiated as an object """
        if cls.__class__ == SFTPDriver:
            raise TypeError("Cannot instantiate abstract SFTPDriver base class.")


# ______________________________________________________________________________
# //////////////////////////////////////////////////////////////////// TYPE HINT
# Parent class annotation for different driver types
Driver = Annotated[Union[SFTPDriver], "Driver"]
