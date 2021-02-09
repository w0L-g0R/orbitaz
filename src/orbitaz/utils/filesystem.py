from pathlib import Path
from typing import List
import re

# ______________________________________________________________________________
# //////////////////////////////////////////////////////////// GET OR CREATE DIR


def find_or_create_target_directory(
    path: Path, search_keys: List[str], target_directory_path: Path
) -> Path:

    """
    Summary
    -------
        This function recursively searches for a target directory path, creating folders on the way (in case of a nested target directory path).

    Notes
    -----
        Gets used in conftest.py in the test suite, in order to create file structure for
    """

    # Base Case - we found what we were looking for
    if path == target_directory_path:
        return path

    else:
        # Try finding a directory with that includes the first search key
        try:

            # This raises an IndexError if the list is empty
            path = [
                directory_name
                for directory_name in path.iterdir()
                if search_keys[0] in str(directory_name)
            ][0]

        except IndexError as error:

            # If there's no directory for the first search key, create one
            path = path / search_keys[0]

            # Create a new directory
            path.mkdir()

        finally:

            # Delete the first search key
            del search_keys[0]

            find_or_create_target_directory(
                path=path,
                search_keys=search_keys,
                target_directory_path=target_directory_path,
            )


# ______________________________________________________________________________
# ////////////////////////////////////////////////////////// CAMEL TO SNAKE CASE


def reformat_camel_to_snake_case(camel_case_string: str) -> str:
    """ Converts CamelCase strings snake_case """

    # Splitting on UpperCase using re and lowercasing it
    array_with_lower_case_strings = [
        s.lower() for s in re.split("([A-Z][^A-Z]*)", camel_case_string) if s
    ]

    # Combine lower cased strings with underscores
    snake_cased_string = "_".join(array_with_lower_case_strings)

    return snake_cased_string


# ______________________________________________________________________________
# ////////////////////////////////////////////////////////// SNAKE TO CAMEL CASE


def reformat_snake_to_camel_case(snake_case_string: str) -> str:
    """ Converts snake_case strings to CamelCase """

    # Splitting camel case string and storing them as list
    array_with_capitalized_with_capitalized_strings = [
        s.capitalize() for s in snake_case_string.split("_")
    ]

    # Combine lower case strings underlines
    camel_case_string = "".join(array_with_capitalized_with_capitalized_strings)

    return camel_case_string