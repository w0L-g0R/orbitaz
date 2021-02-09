from pathlib import Path
from orbitaz.utils.filesystem import (
    reformat_camel_to_snake_case,
)
from orbitaz.files.arrays.commodity_products import (
    RecordsArray,
)

# ______________________________________________________________________________
# ////////////////////////////////////////////////////////////// XLSX NAME ERROR


def is_xlsx_file_name_in_array_class_name(
    array: RecordsArray, xlsx_fixtures_file_path: Path
) -> None:
    """
    Raises a ValueError in 'create_xlsx_from_record_array'
    if the xlsx file name is not equal to the corresponding django model class name
    """

    # Convert camel case class name and drop "array" suffix
    array_class_name = reformat_camel_to_snake_case(camel_case_string=array.__name__)

    # Remove 'array' from array_class_name
    model_class_name_in_snake_case = "_".join(array_class_name.split("_")[:-1])

    # Check if array name is equal to storage_destination_path
    if model_class_name_in_snake_case in Path(xlsx_fixtures_file_path).stem:
        pass
    else:
        raise ValueError(
            "Excel file name has to be equal to the django model name (in lowerCase)"
        )
    return


# ______________________________________________________________________________
# //////////////////////////////////////////////////////////// XLSX SUFFIX ERROR


def is_xlsx_suffix_valid(xlsx_fixtures_file_path: Path) -> None:
    """
    Raises file extension error in 'create_xlsx_from_record_array'
    if the file path suffix is not ".xlsx"
    """

    # Check if storage_destination_path has a valid xlsx suffix
    if Path(xlsx_fixtures_file_path).suffix == ".xlsx":
        pass
    else:
        raise ValueError("Provided file path does not contain '.xlsx' suffix")

    return


# ______________________________________________________________________________
# ///////////////////////////////////////////////////// MISSING XLSX FILES ERROR


def is_file(target_file_path: Path) -> bool:
    """
    Raises an FileNotFoundError if the target file does not exist.
    """

    # Raise an error if fixtures folder does not contain any files
    if not target_file_path.is_file():
        raise FileNotFoundError(f"Could not find {target_file_path}")
    return True


# ______________________________________________________________________________
# ///////////////////////////////////////////////////// MISSING XLSX FILES ERROR


def is_fixture_source_valid(fixture_source: str):
    """
    This function checks the valid options for the command argument "fixture_source", which gets called within the custom django command "create_fixture".
    """

    if fixture_source in ["xlsx", "arrays"]:
        pass
    else:
        raise ValueError(
            "Wrong argument passed, fixture source to convert from must be either 'xlsx' or 'arrays'."
        )