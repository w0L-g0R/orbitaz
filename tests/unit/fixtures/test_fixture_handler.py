import pytest
from pathlib import Path
from shutil import rmtree

from orbitaz.utils.models import get_field_names
from orbitaz.utils.fixtures_handler import FixtureHandler
from orbitaz.files.arrays.commodity_products import (
    CommodityProductArray,
    RecordsArray,
)

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// LOGGER
import coloredlogs, logging
from orbitaz.validation.filesystem import (
    is_xlsx_file_name_in_array_class_name,
    is_xlsx_suffix_valid,
)

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////////////////// INFO

"""
TEST INFO
    
    This module tests the methods of the FixtureHandler class, using commodity products as input data.
        
    NOTE: We use excel as our persistent storage (for readability reasons), 
        so we don't additionally store dataframes as pickles. The reason is  we'd have too much duplicates then, since we also need to store the database records as json file (the preferred django fixture format).
        
"""

# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////////// MODEL FIELDS
@pytest.mark.django_fixtures
def test_get_model_field_names():

    """
    Description:
    -----------
        Test wether the field names from commodity product database model getting received correctly.

    Expectation:
    -----------
        Matches the following field names:
        [
            "commodity",
            "product",
            "vat",
            "source",
            "start_time",
            "granularity",
            "point_of_origin",
            "unit",
        ]

    Fails:
    ------
        If model field names changes or new fields get added.

    """

    test_commodity_product_model_field_names = get_field_names(
        model_import_path="orbitaz.app.models.commodity_product",
        model_class_name_in_camel_case="CommodityProduct",
    )

    assert test_commodity_product_model_field_names == [
        "commodity",
        "product",
        "vat",
        "source",
        "start_time",
        "granularity",
        "point_of_origin",
        "unit",
    ]
    return


# ______________________________________________________________________________
# ///////////////////////////////////////////////////////// VALID XLSX FROM LIST
@pytest.mark.django_fixtures
def test_create_xlsx_from_record_array_with_valid_xlsx_name(
    test_fixture_handler: FixtureHandler,
    test_temp_folder: Path,
):

    """
    Description:
    -----------
        We use a nested list of model records and use pandas to create an excel file. We store it temporarily in /tests/temp.
        Passed xlsx file name is equal to RecordsArray's string representation.

    Expectation:
    -----------
        Test should create one file in /tests/temp, which gets deleted afterwards.

    Fails:
    ------

    """

    commodity_product_model_field_names = get_field_names(
        model_import_path="orbitaz.app.models.commodity_product",
        model_class_name_in_camel_case="CommodityProduct",
    )

    test_file_path = test_temp_folder / "commodity_product.xlsx"

    test_fixture_handler.create_xlsx_from_record_array(
        array=CommodityProductArray,
        xlsx_fixtures_file_path=test_file_path,
        model_field_names=commodity_product_model_field_names,
    )

    assert test_file_path.is_file() == True, "File not found"

    return


# ______________________________________________________________________________
# //////////////////////////////////////////////////////// DF FIXTURES FROM XLSX
@pytest.mark.django_fixtures
def test_create_dataframe_fixtures_from_xlsx_files(
    test_fixture_handler: FixtureHandler, test_temp_folder: Path
):

    """
    Description:
    -----------
        We test wether the columns from excel files are getting parsed correctly into dataframe columns.

    Expectation:
    -----------
        Dataframe gets parsed correctly and df columns matches the commodity product django model fields. Further, the fixture cache dict keys are equal to the assigned json fixtures folder path + model name.

    Fails:
    ------

    """
    commodity_product_model_field_names = get_field_names(
        model_import_path="orbitaz.app.models.commodity_product",
        model_class_name_in_camel_case="CommodityProduct",
    )

    test_fixture_handler.create_xlsx_from_record_array(
        array=CommodityProductArray,
        xlsx_fixtures_file_path=test_temp_folder / "commodity_product.xlsx",
        model_field_names=commodity_product_model_field_names,
    )

    test_dataframe_with_fixtures = (
        test_fixture_handler.create_dataframe_with_fixtures_from_xlsx_files(
            xlsx_fixtures_file_path=test_temp_folder / "commodity_product.xlsx",
            json_fixtures_folder_path=test_temp_folder,
        )
    )

    assert (
        list(test_dataframe_with_fixtures.keys())[0]
        == test_temp_folder / "commodity_product.json"
    ), "Fixture cache keys did not get assigned properly"

    assert set(
        test_dataframe_with_fixtures[
            test_temp_folder / "commodity_product.json"
        ].columns
    ) == set(
        [
            "commodity",
            "product",
            "vat",
            "source",
            "start_time",
            "granularity",
            "point_of_origin",
            "unit",
        ]
    ), "Columns did not get parsed right from excel to dataframe"

    return


# ______________________________________________________________________________
# /////////////////////// FIXTURE STRUCTURE + JSON DUMP FROM DATAFRAME FROM XLSX
@pytest.mark.django_fixtures
def test_dump_json_fixtures_from_blueprint(
    test_fixture_handler: FixtureHandler, test_temp_folder: Path
):

    """
    Description:
    -----------
        We test wether the fixture file gets dumped correctly.

    Expectation:
    -----------
        The temp json fixture folder contains a json file

    Fails:
    ------
    """

    commodity_product_model_field_names = get_field_names(
        model_import_path="orbitaz.app.models.commodity_product",
        model_class_name_in_camel_case="CommodityProduct",
    )

    test_fixture_handler.create_xlsx_from_record_array(
        array=CommodityProductArray,
        xlsx_fixtures_file_path=test_temp_folder / "commodity_product.xlsx",
        model_field_names=commodity_product_model_field_names,
    )

    test_fixtures_cache = (
        test_fixture_handler.create_dataframe_with_fixtures_from_xlsx_files(
            xlsx_fixtures_file_path=test_temp_folder / "commodity_product.xlsx",
            json_fixtures_folder_path=test_temp_folder,
        )
    )

    test_fixtures_blueprint = test_fixture_handler.create_fixtures_blueprints(
        app_name="app",
        model_class_name_in_lower_case="CommodityProduct",
        fixtures_cache=test_fixtures_cache,
    )
    test_fixture_handler.dump_json_fixtures_from_blueprint(
        fixtures_blueprint=test_fixtures_blueprint
    )

    test_json_fixtures_folder = test_temp_folder / "commodity_product.json"

    assert test_json_fixtures_folder.is_file() == True, "File not found"
    return
