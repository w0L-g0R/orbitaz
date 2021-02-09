from dataclasses import dataclass, field
from itertools import product
from pysftp import CnOpts
from pathlib import Path
import datetime


@dataclass(frozen=True)
class EEXSpecs:

    """
    Defines relevant information related to the downloading process EEX' sFTP server. Does not include

    Note
    ----
        Example Abbreviations: Power Future History Austria

        Derivatives Contained Data:
            ATBM    EEX Austrian Power Base Month Future
            ATBQ    EEX Austrian Power Base Quarter Future
            ATBY    EEX Austrian Power Base Year Future
            ATPM    EEX Austrian Power Peak Month Future
            ATPQ    EEX Austrian Power Peak Quarter Future
            ATPY    EEX Austrian Power Peak Year Future

    See
    ---
        https://www.eex.com/fileadmin/EEX/Downloads/Market_Data/EEX_Group_DataSource/sFTP_Server/EEX_Group_DataSource_SFTP_XLSX_Interface_Specification_v008_09_09_2020.pdf, Page 19
    """

    base_path_power_futures: Path = "/market_data/power/at/derivatives/csv"

    # TODO: Get ssh-pk from config via paramiko
    connection_options: CnOpts = CnOpts(
        knownhosts=Path(__file__).resolve().parent / "sshpk.txt"
    )

    countries: list = field(default_factory=lambda: ["AT", "DE", "FR", "NL", "BE"])

    contained_data_contracts: list = field(
        default_factory=lambda: ["BM", "PM", "BQ", "PQ", "BY", "PY"]
    )

    contract_country_codes: dict = field(
        default_factory=lambda: {
            "FR": "F7",
            "AT": "AT",
            "DE": "DE",
            "BE": "Q1",
            "NL": "Q0",
        }
    )

    def create_filename(date: datetime.date, country: str):
        return "PowerFutureResults_{}_{}.csv".format(country, date)

    def get_contained_data_codes_per_country(self, country: str):
        """
        Returns the cartesian product of a single a country and all considered EEX contract types

        Return
        ------

            TODO: Connect tuple items
            specs = EEXSpecs()
            specs.get_encoded_contracts_per_country("BE"))

            >> [('Q1', 'BM'), ('Q1', 'PM'), ('Q1', 'BQ'), ('Q1', 'PQ'), ('Q1', 'BY'), ('Q1', 'PY')]

        """

        return list(product([self.contract_country_codes[country]], self.contracts))
