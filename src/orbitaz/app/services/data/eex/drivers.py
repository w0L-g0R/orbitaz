from decouple import config
from dataclasses import dataclass

from orbitaz.app.services.data.interfaces.drivers import SFTPDriver

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////// EEX DRIVER
@dataclass(frozen=True)
class EEXDriver(SFTPDriver):
    host: str = "datasource.eex-group.com"
    username: str = config("EEX_USERNAME")
    password: str = config("EEX_PASSWORD")
    private_key: str = config("EEX_PRIVATE_KEY")
