import pytest
from pathlib import Path
from shutil import rmtree

from src.orbitaz.utils.filesystem import (
    reformat_snake_to_camel_case,
)
from src.orbitaz.utils.models import get_field_names
from src.orbitaz.utils.fixtures_handler import FixtureHandler
from src.orbitaz.validation.filesystem import (
    is_fixture_source_valid,
    is_file,
    is_xlsx_file_name_in_array_class_name,
)
from orbitaz.files.arrays.commodity_products import (
    CommodityProductArray,
)
from src.orbitaz.core.settings import (
    FIXTURES_DIR_JSON,
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
    
    This module tests the setup fixtures methods of the FixtureHandler class, using commodity products as input data.

    The procedure runs as follows:
        
        0) First we need to get the field names from the database model we are testing against.
        
        1) Then we create an excel file from the python list with commodity products records and store it temporarily. 
        
        We use a dataframe as a middleware to store excel files. We do this out of convenience, instead of using a separate excel library. 

        2) Next, we convert from excel files back to a dataframe.
        
        NOTE: We use excel as our persistent storage (for readability reasons), 
        so we don't additionally store the dataframes as pickle. The reason is  we'd have too much duplicates then, since we also need to store the database records as json file (the preferred django fixture format) later.
        
        3) We further pass this dataframe to a function that converts it in a suitable format that can be dumped as a json file
        
        4) In the subsequent step, we dump the commodity records as a json file and test its records against the native python list with commodity products records.     
        
    This procedure could have been written as an integration test, using cached intermediate data, that gets passed from test to test.  
    But since we prefer try to have a testing pyramid with fundament made from unit tests, we went for a smaller scope mostly, where functions can get tested in a more atomistic manner. To this end, we do repeated function calls and accept some more boilerplate.
"""

# __________________________________________________________________________
# /////////////////////////////////////////////////////////// SETUP FIXTURES
def test_setup_commodity_fixtures(
    test_fixture_handler: FixtureHandler,
    test_temp_folder: Path,
):

    """
    This function mimics the internals of the function setup_fixtures.
    It allows to reproduce, test and alter the function's logic on an integral basis.
    """

    # Inputs for the function setup_fixtures
    test_fixture_source = "arrays"
    test_model_name_in_snake_case = "commodity_product"
    test_app_name = "app_name"

    # Parsed inputs
    test_model_xlsx_fixtures_file_name = "commodity_product.xlsx"
    test_xlsx_fixtures_file_path = test_temp_folder / test_model_xlsx_fixtures_file_name

    test_json_fixtures_folder_path = (
        test_temp_folder / test_model_xlsx_fixtures_file_name
    )

    test_model_name_in_camel_case = reformat_snake_to_camel_case(
        test_model_name_in_snake_case
    )

    is_fixture_source_valid(fixture_source=test_fixture_source)

    # If fixture source is not xlsx, parse the hard-coded model records
    # Or if excel file does not exist
    if "arrays" in test_fixture_source or not is_file(test_xlsx_fixtures_file_path):

        model_import_path = ".".join(
            [
                "orbitaz.app.models",
                test_model_name_in_snake_case,
            ]
        )

        model_field_names = get_field_names(
            model_import_path=model_import_path,
            model_class_name_in_camel_case=test_model_name_in_camel_case,
        )

        # Assure that the xlsx file names matches your model names.
        is_xlsx_file_name_in_array_class_name(
            array=CommodityProductArray,
            xlsx_fixtures_file_path=test_xlsx_fixtures_file_path,
        )

        FixtureHandler.create_xlsx_from_record_array(
            array=CommodityProductArray,
            xlsx_fixtures_file_path=test_xlsx_fixtures_file_path,
            model_field_names=model_field_names,
        )

    # Make sure you created a parseable xlsx file
    is_file(target_file_path=test_xlsx_fixtures_file_path)

    fixtures_cache = FixtureHandler.create_dataframe_with_fixtures_from_xlsx_files(
        xlsx_fixtures_file_path=test_xlsx_fixtures_file_path,
        json_fixtures_folder_path=FIXTURES_DIR_JSON,
    )

    fixtures_blueprint = FixtureHandler.create_fixtures_blueprints(
        app_name=test_app_name,
        model_class_name_in_lower_case=test_model_name_in_snake_case.replace("_", ""),
        fixtures_cache=fixtures_cache,
    )

    FixtureHandler.dump_json_fixtures_from_blueprint(
        fixtures_blueprint=fixtures_blueprint
    )

    logger.debug(
        f"Successfully stored fixtures @files/fixtures/{test_fixture_source}/commodity_products.json"
    )
    return