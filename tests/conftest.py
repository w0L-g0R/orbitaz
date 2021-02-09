from datetime import datetime
from tests.settings import SUMMARIES_BASE_DIR, TESTS_BASE_DIR
from src.orbitaz.utils.filesystem import (
    find_or_create_target_directory,
)

import pytest
from orbitaz.utils.fixtures_handler import FixtureHandler
import shutil
from pathlib import Path

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////////////////// LOGGER
import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////////////////// CONF
def pytest_configure(config) -> None:

    """
    This pytest built-in fixture function allows to set pytest terminal commands programatically on runtime.

    This specific implementation configures timestamps for excel summaries and takes care of storing excel test summaries at the right folder.

    In the course of that, it applies a recursive search function called 'get_or_create_target_directory' to find or make a path for the excel reports.
    """

    # We try to find a summary directory for the current year and month
    target_directory_path = (
        SUMMARIES_BASE_DIR
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%b")
    )

    # Use the current year and month as popable search keys
    search_keys = [datetime.now().strftime("%Y"), datetime.now().strftime("%b")]

    # Find the folder in the test summary directory, otherwise create one
    find_or_create_target_directory(
        path=SUMMARIES_BASE_DIR,
        search_keys=search_keys,
        target_directory_path=target_directory_path,
    )

    # Set the timestamp for the start of this test run
    timestamp = datetime.now().strftime("%d_%b_%Y_%Hh_%Mmin")

    # Create an excel test summary file
    config.option.excelpath = target_directory_path / f"test_summary_{timestamp}.xlsx"

    # Sets the temp directory for some tests that creates files
    # WARNING: All contents in this folder gets deleted afterwards, be careful!
    config.option.basetemp = TESTS_BASE_DIR / "temp"

    return


# ______________________________________________________________________________
# ////////////////////////////////////////////////////////////// FIXTURE HANDLER
@pytest.fixture(scope="session")
def test_fixture_handler():
    """
    Mocks an instance of the FixtureHandler class
    """

    return FixtureHandler


# ______________________________________________________________________________
# ////////////////////////////////////////////////////////////////// TEMP FOLDER
@pytest.fixture(scope="session")
def test_temp_folder(tmpdir_factory):
    tmpdir = Path(tmpdir_factory.mktemp("fixtures"))
    yield tmpdir
    shutil.rmtree(str(tmpdir))