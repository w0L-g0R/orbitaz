from pysftp import Connection, CnOpts
from pathlib import Path
import datetime
from orbitaz.core.settings import EEX_FILES_DIR
from orbitaz.app.services.data.interfaces.drivers import SFTPDriver
from orbitaz.app.services.data.interfaces.clients import (
    FileTransferClient,
    BulkFileTransferClient,
)
from orbitaz.app.services.data.utils import (
    check_if_sftp_remotepath_exists,
)

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// LOGGER
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////// EEX CLIENT
class EEXClient(FileTransferClient, BulkFileTransferClient):
    def __init__(self, driver: SFTPDriver, specs: CnOpts):
        self.driver = driver
        self.specs = specs
        self.localpath = EEX_FILES_DIR

    def download(
        self,
        date: datetime.date,
    ) -> None:
        """
        Docstring
        ---------
            Parameters
            ----------
                localpath : str

                    Define local path where the file will be saved
                    TODO: Replace this with temp folder

                remotepath : str

                    Define the path to the file you want to download from the remote's directory

            Raises
            ------
                paramiko.ssh_exception.SSHException:
                    Bad host key from server, reconfigure the public-private key authentication with the command "ssh-keyscan datasource.eex-group.com" from an anaconda terminal
        """

        with Connection(
            host=self.driver.host,
            username=self.driver.username,
            password=self.driver.password,
            cnopts=self.driver.conncection_options,
        ) as sftp:

            # status = self.check_if_remotepath_exists(
            #     sftp=sftp, remotepath=self.driver.remote_xml_base + remotepath
            # )
            # logger.info(f"status: {status}")

            # exists = sftp.isdir(
            #     remotepath="/market_data/power/at/derivatives/csv/2019/20191206/PowerFutureResults_AT_20191206.csv",
            # )

            remotepath = "/market_data/power/at/derivatives/csv/2020/20201230/PowerFutureResults_AT_20201230.csv"

            wrong_remotepath = "/market_data/power/at/derivatives/csv/2020/20201230/PowerFutureResults_AT_20201230.csv"

            isfile = sftp.exists(remotepath=remotepath)

            logger.info(f"exists: {isfile}")
            # sftp.chdir(
            #     "/market_data/power/at/derivatives/csv/2020/20201230/PowerFutureResults_AT_20201230.csv"
            # )
            # for attr in sftp.listdir_attr():
            #     logger.info(f"{attr.filename}")
            #     logger.info(f"{attr}")

            # sftp.walktree()
            # logger.info(sftp.walktree())

            sftp.get(remotepath=remotepath, localpath=local_file_path)

        # logger.info(f"Successfully fetched EEX Data from {remotepath}")

        return


# class SFTPClient(FileTransferClient):
#     def __init__(self, sftp_driver: SFTPDriver):
#         self._client = sftp_driver

#     def download(self, target: str) -> bytes:
#         with self._client.Connection() as sftp:
#             return sftp.get(target)
