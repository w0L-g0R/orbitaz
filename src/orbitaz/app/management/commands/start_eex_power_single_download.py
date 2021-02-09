# Create fixture with django commands
from django.core.management.base import BaseCommand
from django.utils import timezone
from orbitaz.app.services.data.transfers import DataTransfer
from orbitaz.app.services.data.eex.factories import EEXFactory
from orbitaz.app.services.data.eex.validation import (
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
            "--start_date",
            type=str,
            help="Select the start date for the download of power futures from EEX. The format has to be: YYYY-MM-DD. As a default value, the current date gets used.",
        )

    def handle(self, *args, **options):

        # TODO: Replace with task function "start_eex_power_single_download()" later

        # assert

        # datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

        logger.info(options)
        # if options["start_date"]:
        #     start_date = datetime.date.today()
        # logger.info(f"\nCommand 'start_eex_transfer' executed.")

        # eex_transfer = DataTransfer(factory=EEXFactory())

        # if is_date_valid_for_EEX_power_data_transfer(date=options["start-date"]):

        #     eex_transfer.download(start_date=options["start-date"])
