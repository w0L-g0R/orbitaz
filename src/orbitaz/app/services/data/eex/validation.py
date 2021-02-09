from datetime import date, datetime

from orbitaz.app.services.data.eex.holidays import (
    EEXHolidaysDerivativesAndEmissionSpot,
)

from orbitaz.validation.datetimes import (
    is_weekday,
)


# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// LOGGER
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////// VALID DATE


def is_date_valid_for_EEX_power_data_transfer(date: datetime.date) -> bool:

    """
    TODO TEST

    This function checks for a given date wether it's valid to perform a download, regarding the weekday and the list of official EEX holidays.
    """
    assert isinstance(
        date, datetime.date
    ), "Passed 'date' object is not a valid datetime.date object."

    if is_weekday(date=date):
        logger.info(
            f"CAUTION: {date} is not a weekday. EEX does not provide new data today."
        )
        return False

    elif date in EEXHolidaysDerivativesAndEmissionSpot(years=datetime.now().year):
        return False

    return True