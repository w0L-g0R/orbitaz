# Create fixture with django commands
from django.core.management.base import BaseCommand
from django.utils import timezone
from orbitaz.app.services.data.eex.transfers import DataTransfer
from orbitaz.app.services.data.factories import EEXFactory
from orbitaz.app.utils.datetimes import (
    is_date_valid_for_EEX_power_data_transfer,
)

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// LOGGER
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)


class Command(BaseCommand):
    help = "Initiates a data transfer in order to fetch prices for commodities from different endpoints."

    def add_arguments(self, parser):

        parser.add_argument(
            "-start",
            "--start-date",
            type=str,
            help="Select the start date for the download of power futures from EEX. The format has to be: YYYY-MM-DD. As a default value, the current date gets used.",
        )

        parser.add_argument(
            "-end",
            "--end-date",
            type=str,
            help="Select the start date for the download of power futures from EEX. The format has to be: YYYY-MM-DD. As a default value, the current date gets used.",
        )

    def handle(self, *args, **options):

        # default=f"{datetime.date.today()}",

        if options["power"]:
            logger.info(f"\nCommand 'start_eex_transfer' executed.")

            eex_transfer = DataTransfer(factory=EEXFactory())

            if is_date_valid_for_EEX_power_data_transfer(date=options["start-date"]):

                eex_transfer.download(
                    start_date=options["start-date"], end_date=options["end-date"]
                )
