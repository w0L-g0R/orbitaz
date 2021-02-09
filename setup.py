from setuptools import setup, find_packages

setup(
    name="orbitaz",
    version="0.1.0",
    author="Wolfgang Goritschnig",
    author_email="",
    package_dir={"": "src"},
    setup_requires=["black", "coloredlogs", "sphinx"],
    tests_require=[],
    license="LICENSE.md",
    description="orbitaz is a python package that provides data-driven energy analysis alongside related procedures to manage and host the results as a web service",
    long_description=open("README.md").read(),
    install_requires=[],
)
