from orbitaz.app.services.data.eex.specifications import EEXSpecs
from typing import Annotated, Union


# ______________________________________________________________________________
# //////////////////////////////////////////////////////////////////// TYPE HINT
# Parent class annotation for FileTransferClient and BulkFileTransferClient
TransferSpecifications = Annotated[Union[EEXSpecs], "Specs"]