import pytest
from pathlib import Path
from src.orbitaz.utils.fixtures_handler import FixtureHandler
from src.orbitaz.validation.filesystem import (
    is_xlsx_file_name_in_array_class_name,
    is_file,
    is_xlsx_suffix_valid,
    is_fixture_source_valid,
)
from orbitaz.files.arrays.commodity_products import (
    CommodityProductArray,
)

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// LOGGER
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////////////////// INFO

"""
TEST INFO
    
    This module tests common error functions that gets used for filesystem operations.
    
"""

# ______________________________________________________________________________
# //////////////////////////////////////////// XLSX NAME NOT IN ARRAY NAME ERROR
@pytest.mark.django_fixtures_errors
def test_check_if_array_class_name_contains_xlsx_file_name(
    test_fixture_handler: FixtureHandler,
):

    """
    Description:
    -----------
        Testing the error handling if passed xlsx file name is not equal to RecordsArray's string representation.

    Expectation:
    -----------
        Test throws a ValueError.

    Fails:
    ------
        If passed xlsx file name is equal to RecordsArray's string representation.
    """
    # Defining a fake invalid path with valid suffix
    fake_storage_destination_path = Path("a_filename_not_equal_to_array_name.xlsx")

    with pytest.raises(ValueError):
        is_xlsx_file_name_in_array_class_name(
            array=CommodityProductArray,
            xlsx_fixtures_file_path=fake_storage_destination_path,
        )

    return


# ______________________________________________________________________________
# //////////////////////////////////////////////////////////// XLSX SUFFIX ERROR
@pytest.mark.django_fixtures_errors
def test_check_valid_xlsx_suffix(
    test_fixture_handler: FixtureHandler,
):

    """
    Description:
    -----------
        Testing the error handling if passed xlsx file name has 'xlsx' suffix.

    Expectation:
    -----------
        Test throws a ValueError.

    Fails:
    ------
        If passed xlsx file name has valid xlsx suffix.
    """

    # Defining a fake invalid path with valid suffix
    fake_storage_destination_path = Path("a_filename_with_wrong_suffix.xls")

    with pytest.raises(ValueError):
        is_xlsx_suffix_valid(
            xlsx_fixtures_file_path=fake_storage_destination_path,
        )

    return


# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////// XLSX FILES ERROR
@pytest.mark.django_fixtures_errors
def test_check_if_file_exists(
    test_fixture_handler: FixtureHandler,
    test_temp_folder: Path,
):

    """
    Description:
    -----------
        Check if xlsx fixture files are available.

    Expectation:
    -----------
        Test throws a FileNotFoundError if xlsx fixtures directory is empty.

    Fails:
    ------
        If xlsx files have been found.
    """

    # Defining a fake invalid path with valid suffix
    fake_empty_xlsx_fixtures_folder_path = test_temp_folder / "commodity_products.xlsx"

    with pytest.raises(FileNotFoundError):
        is_file(
            target_file_path=fake_empty_xlsx_fixtures_folder_path,
        )

    return


# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////// XLSX FILES ERROR
@pytest.mark.django_fixtures_errors
def test_check_if_fixture_source_is_valid(
    test_fixture_handler: FixtureHandler,
    test_temp_folder: Path,
):

    """
    Description:
    -----------
        Check if xlsx fixture files are available.

    Expectation:
    -----------
        Test throws a FileNotFoundError if xlsx fixtures directory is empty.

    Fails:
    ------
        If xlsx files have been found.
    """

    # Defining an invalid source to parse fixtures from
    invalid_fixture_source = "a_not_valid_argument_like_yaml"

    with pytest.raises(ValueError):
        is_fixture_source_valid(
            fixture_source=invalid_fixture_source,
        )

    return
