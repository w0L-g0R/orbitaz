from typing import List, Dict, TypeVar
import pandas as pd
import json
from pathlib import Path
from orbitaz.utils.models import get_field_names
from orbitaz.core.settings import (
    FIXTURES_DIR_XLSX,
    FIXTURES_DIR_JSON,
)
from orbitaz.validation.filesystem import (
    is_xlsx_file_name_in_array_class_name,
    is_file,
    is_xlsx_suffix_valid,
    is_fixture_source_valid,
)

from orbitaz.files.arrays.commodity_products import (
    CommodityProductArray,
    RecordsArray,
)

from orbitaz.utils.filesystem import (
    reformat_snake_to_camel_case,
)

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// LOGGER
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

# ______________________________________________________________________________
# ////////////////////////////////////////////////////////////// FIXTURE HANDLER


class FixtureHandler:
    """
    Docstring
    ---------

        Summary
        -------
            Fixtures provides initial data for the database.
            This handler provides the following fixture related functionalities:

                1) Converting of commodity products from python arrays to xlsx files.

                2) Extracting of fixture information from fixture xlsx files and converting it into applicable 'blueprints' for json formatted files (used for django's loaddata command).

                3) Dumps fixture 'blueprints' to json files

            The handler gets applied as part of the module "create_fixture.py", which invokes the handler as part of the its handle function.

        Raises
        ------

            FileNotFoundError:
                @ is_file()
                    in create_dataframe_fixtures_from_xlsx_files()
                    in setup_fixtures()

            ValueError:
                @ is_xlsx_file_name_in_array_class_name()
                @ is_fixture_source_valid()
                    in setup_fixtures()
    """

    # __________________________________________________________________________
    # /////////////////////////////////////////////////////////// XLSX FROM LIST
    @staticmethod
    def create_xlsx_from_record_array(
        model_field_names: List,
        array: RecordsArray,
        xlsx_fixtures_file_path: Path,
    ) -> None:

        """
        Docstring
        ---------
            Summary
            ----------
                This method parses a nested list data structure into dataframes and uses pandas' to_excel() to export the records as excel files to a fixtures excel file folder.

            Parameters
            ----------
                model_field_names : List
                    Field names of a django ORM database model

                array : RecordsArray
                    A class instance that serves a list of lists via its classmethod get_all(). Each of inner list object stores one record with data for one or several fields.

                xlsx_fixtures_file_path : Path, optional
                    Determine here where to store the derived excel files.
                    By default the initialized instance variable gets used.

            Notes
            -----
                I) Assure upfront that the passed records array class matches your model class name

                -> call is_xlsx_file_name_in_array_class_name() outside

                II) Check that the xlsx column names matches your model field names. This one is cumbersome to catch here, so its delegated to the users responsibility to pass the right model field names.

        """

        # First convert native python lists to a dataframe
        df = pd.DataFrame.from_records(data=array.get_all(), columns=model_field_names)

        # Then export them to a xlsx file in the xlsx fixture folder
        df.to_excel(excel_writer=xlsx_fixtures_file_path, index=False)

        return

    # __________________________________________________________________________
    # //////////////////////////////////////////////////// DF FIXTURES FROM XLSX
    @staticmethod
    def create_dataframe_with_fixtures_from_xlsx_files(
        xlsx_fixtures_file_path: Path,
        json_fixtures_folder_path: Path,
    ) -> Dict[Path, pd.DataFrame]:
        """
        Summary
        -------
            Extracts model records from excel files and converts them to dataframes.
            The columns of the dataframe are equal to the corresponding django models class fields.

            We then apply a dictionary as intermediate storage (fixture_cache), to pass dataframe to the the actual json dumping method.

        Parameters
        ----------
            xlsx_fixtures_folder_path : Path
                Path of xlsx fixture storage

            json_fixtures_folder_path : Path
                Path of json fixture storage

        Returns
        -------
            Dict[Path, pd.DataFrame]
                We use file pathes (json_fixtures_folder_path django + model name (lowercased)) as keys, and store the corresponding model record dataframes as values.
        """

        # Extract model name from path
        model_name = xlsx_fixtures_file_path.stem

        # First convert the xlsx files to pandas df
        df = pd.read_excel(
            xlsx_fixtures_file_path,
            header=0,
            # index_col=0,
            dtype=str,
        )

        # Create path to export the json file to
        json_file_path = json_fixtures_folder_path / ".".join([model_name, "json"])

        # Use an a dictionary to pass dataframe formatted fixtures around
        fixtures_cache = {}

        # Json_file_path gets used a key for in-memory-cache of the df
        fixtures_cache[json_file_path] = df

        return fixtures_cache

    # __________________________________________________________________________
    # //////////////////////////////////////////////////////// FIXTURE STRUCTURE
    @staticmethod
    def create_fixtures_blueprints(
        app_name: str,
        model_class_name_in_lower_case: str,
        fixtures_cache: Dict[Path, pd.DataFrame],
    ) -> Dict[Path, List[Dict]]:
        """
        Summary
        -------
            Converts a dataframe into a 'blueprint' for json fixtures.
            The actual json dumping is not part of this function.

        Parameters
        ----------
            app_name : str
                We need to pass the name of our app (NOTE: we called it just 'app')

            model_class_name_in_lower_case : str
                The class name needs to be in lowerCase for the right 'blueprint'

            fixtures_cache : Dict[Path, pd.DataFrame]
                This data structure comes (dict) holds the file path where we later store our fixtures at (key), alongside the data records for the fixtures (values).

        Returns
        -------
            Dict[Path, List[Dict]]
                Wraps the incoming fixtures_cache dict with newly transformed values. Gets passed to the json dumping method.

        Notes
        -----
            The row index number of the dataframe determines the primary key.
            But remember, there's one excel file per database table,
            and since the dataframe gets derived from that excel file, actually the order of the entries in the excel file defines the order of the primary keys.

        """

        # Storage for fixtures that gets json dumped
        fixtures_blueprint = {}

        # Iter over file paths and dataframes
        for file_path, df in fixtures_cache.items():

            # Applies the structure needed for django's loaddata command
            fixtures_blueprint[file_path] = [
                {
                    "model": ".".join([app_name, model_class_name_in_lower_case]),
                    "pk": i,
                    "fields": {
                        j: row[j]
                        # Filter stringified booleans out
                        if row[j] not in ["true", "false"]
                        # This assures that "true" and "false" becomes true and false in the json file
                        else json.loads(row[j])
                        for j in df.columns
                    },
                }
                for i, row in df.iterrows()
            ]

        return fixtures_blueprint

    # __________________________________________________________________________
    # ///////////////////////////////////////////////// JSON DUMP FROM DATAFRAME
    @staticmethod
    def dump_json_fixtures_from_blueprint(
        fixtures_blueprint: Dict[Path, List[Dict]]
    ) -> None:
        """
        Summary
        -------
            This method dumps django model record fixtures as json files, such that they can be loaded with django's loaddata command.

        Parameters
        ----------
            fixtures_blueprint : Dict[Path, List[Dict]]
                This data structure provides a list of dumpable fixtures in dictionary format.
        """

        # Iter over file paths and dataframes
        for file_path, lists_with_records in fixtures_blueprint.items():

            # Dump to json file
            with open(file_path, "w") as file:
                json.dump(lists_with_records, file, ensure_ascii=True, indent=4)

        return

    # __________________________________________________________________________
    # /////////////////////////////////////////////////////////// SETUP FIXTURES
    @staticmethod
    def setup_fixtures(
        app_name: str,
        fixture_source: str,
        model_name_in_snake_case: Path,
    ) -> None:

        # Fixture path for xlsx formatted fixtures
        xlsx_fixtures_file_name = ".".join([model_name_in_snake_case, "xlsx"])

        # Fixture path for xlsx formatted fixtures
        xlsx_fixtures_file_path = FIXTURES_DIR_XLSX / ".".join(
            [model_name_in_snake_case, "xlsx"]
        )

        # Reformatted model name
        model_name_in_camel_case = reformat_snake_to_camel_case(
            model_name_in_snake_case
        )

        # Should be either "arrays" or "xlsx", otherwise code breaks
        is_fixture_source_valid(fixture_source=fixture_source)

        # If fixture source is not xlsx, parse the hard-coded model records
        # Or if excel file does not exist
        if "arrays" in fixture_source or is_file(xlsx_fixtures_file_path) == False:

            # We use this path to get a database class model and its field names
            model_import_path = ".".join(
                [
                    "orbitaz.app.models",
                    model_name_in_snake_case,
                ]
            )

            model_field_names = get_field_names(
                model_import_path=model_import_path,
                model_class_name_in_camel_case=model_name_in_camel_case,
            )

            # Assure that the xlsx file names matches your model names.
            is_xlsx_file_name_in_array_class_name(
                array=CommodityProductArray,
                xlsx_fixtures_file_path=xlsx_fixtures_file_path,
            )

            # Storing python lists with records as excel file
            FixtureHandler.create_xlsx_from_record_array(
                array=CommodityProductArray,
                xlsx_fixtures_file_path=xlsx_fixtures_file_path,
                model_field_names=model_field_names,
            )

            logger.info(
                f"\nSuccessfully stored xlsx fixtures @files/fixtures/xlsx/commodity_products.xlsx"
            )

        # Make sure you created a parseable xlsx file
        is_file(target_file_path=xlsx_fixtures_file_path)

        # Creating an intermediate storage for path and record information
        fixtures_cache = FixtureHandler.create_dataframe_with_fixtures_from_xlsx_files(
            xlsx_fixtures_file_path=xlsx_fixtures_file_path,
            json_fixtures_folder_path=FIXTURES_DIR_JSON,
        )

        # Create a dict datastructure with model field data
        fixtures_blueprint = FixtureHandler.create_fixtures_blueprints(
            app_name=app_name,
            model_class_name_in_lower_case=model_name_in_snake_case.replace("_", ""),
            fixtures_cache=fixtures_cache,
        )

        # Dump model field data as json, which can be used as the actual fixture
        FixtureHandler.dump_json_fixtures_from_blueprint(
            fixtures_blueprint=fixtures_blueprint
        )

        logger.info(
            f"\nSuccessfully stored json fixtures @app/fixtures/{model_name_in_snake_case}.json"
        )

        return