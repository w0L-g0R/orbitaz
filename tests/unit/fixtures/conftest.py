# import pytest
# from orbitaz.utils.fixtures_handler import FixtureHandler
# import shutil
# from pathlib import Path


# @pytest.fixture(scope="session")
# def test_fixture_handler():
#     """
#     Mocks an instance of the FixtureHandler class
#     """

#     return FixtureHandler


# @pytest.fixture(scope="session")
# def test_temp_folder(tmpdir_factory):
#     tmpdir = Path(tmpdir_factory.mktemp("fixtures"))
#     yield tmpdir
#     shutil.rmtree(str(tmpdir))