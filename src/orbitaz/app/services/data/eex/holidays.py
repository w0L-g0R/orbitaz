from datetime import date, datetime

import holidays

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////// TODO TESTS

"""
    Test subsequent years, assure only valid EEX holiday dates appear.
"""

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// LOGGER
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////////////////// BASE


class EEXHolidaysGasFutures(holidays.UnitedKingdom):

    """
    Docstring
    ---------

        Summary
        -------
            This acts as our base class, since the Gas Futures exchange has the most holidays.
            We inherit from the UK holiday data, since this includes all of the Bank Holidays.
            Note, that we additionally included "Labour Day" from the austrian dataset.

            The following holidays are included:

                New Year – 1st January
                Good Friday
                Easter Monday
                Labour Day – 1st May
                Early May Bank Holiday – first Monday of May (UK dataset == May-Day)
                Spring Bank Holiday – last Monday of May
                Summer Bank Holiday – last Monday of August
                Christmas Day – 25th December
                Boxing Day – 26th December

        See
        ---
            https://www.eex.com/fileadmin/EEX/Downloads/Market_Data/EEX_Group_DataSource/sFTP_Server/EEX_Group_DataSource_SFTP_CSV_Interface_Specification_v016_09_11_2020.pdf, Page 23

        Note
        ----
            To see a list of applied holidays call:
            e.g.: EEXHolidaysGasFutures(years=2022)._print(years=2022)

    """

    def _populate(cls, year):

        # Exclude the observed day of a holiday that falls on a weekend
        cls.observed = False

        # Populate the holiday list with the default UK holidays
        super()._populate(year)

        # Remove UK holidays which are not needed
        cls.pop_named("New Year Holiday [Scotland]")
        cls.pop_named("St. Patrick's Day [Northern Ireland]")
        cls.pop_named("Battle of the Boyne [Northern Ireland]")
        cls.pop_named("St. Andrew's Day [Scotland]")

        # Add 1st of may sinc its not in the UK dataset
        labour_day = holidays.Austria(years=datetime.now().year).get_named(
            name="Staatsfeiertag"
        )
        cls[labour_day[0]] = "Labour Day"

        # Catch extra-ordinary holiday from UK dataset
        if holidays.Austria(years=datetime.now().year).get_named(
            name="Platinum Jubilee of Elizabeth II"
        ):
            cls.pop_named("Platinum Jubilee of Elizabeth II")

        return

    @classmethod
    def _print(cls, years: int):

        logger.info(f"{cls.__name__}")

        for date, name in sorted(cls(years=years).items()):
            logger.info(f"{date}, {name}")

        return


class EEXHolidaysGasSpot(EEXHolidaysGasFutures):
    """
    Docstring
    ---------

        Summary
        -------
            We exclude "Labour Day" for the Gas Spot exchange.

            The following holidays are included:

                New Year – 1st January
                Good Friday
                Easter Monday
                Early May Bank Holiday – first Monday of May (UK dataset == May Day)
                Spring Bank Holiday – last Monday of May
                Summer Bank Holiday – last Monday of August
                Christmas Day – 25th December
                Boxing Day – 26th December
    """

    def _populate(cls, year):

        # Populate the holiday list with the superclass' holidays
        super()._populate(year)

        # Remove Labour Day
        cls.pop_named("Labour Day")

        return


class EEXHolidaysDerivativesAndEmissionSpot(EEXHolidaysGasFutures):

    """
    Docstring
    ---------

        Summary
        -------
            We exclude all the "Bank Holidays" here, but add "Christmas Eve".

            The following holidays are included:

                New Year – 1st January
                Good Friday
                Easter Monday
                Christmas Day – 25th December
                Boxing Day – 26th December
    """

    def _populate(cls, year):

        # Populate the holiday list with the superclass' holidays
        super()._populate(year)

        # Hacky workaround due to inheritance issues
        # BUG: Inheritance from "EEXHolidaysGasFutures" leads to doubling the attributes of this class, such that poping holidays throws an KeyError. You can check this with "pprint(cls.__dict__)".
        try:
            cls.pop_named("May Day")
            cls.pop_named("Summer Bank Holiday [Scotland]")
            cls.pop_named("Late Summer Bank Holiday [England, Wales, Northern Ireland]")
        except KeyError:
            pass

        # Only adds christmas eve for current year
        cls[f"{datetime.now().year}-12-24"] = "Christmas Eve"

        return
