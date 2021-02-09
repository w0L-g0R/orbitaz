from typing import NewType, List
import django
from django.conf import settings
from django.apps import apps
from importlib import import_module
import re
from typing import Annotated

# ______________________________________________________________________________
# /////////////////////////////////////////////////////////// CUSTOM ANNOTATIONS

ImportPath = Annotated[str, "ImportPath"]

# ______________________________________________________________________________
# ///////////////////////////////////////////////////////////////// MODEL FIELDS


def get_field_names(
    model_import_path: ImportPath, model_class_name_in_camel_case: str
) -> List[str]:
    """
    Docstring
    ---------
        Summary
        -------

            This functions gets the properties of a django db model class (as stored in the models folder).

            In order to import django database model field in standalone mode (-> without having a django server running) one has to invoke django's settings configuration as implemented within this method.

                # Kind a mocks a default settings setup
                settings.configure(DEBUG=True)

                # Makes django aware of the execution context
                django.setup()

        Parameters
        ----------
            model_import_path : NewType

                A string that contains an import address statements (e.g."orbitaz.app.models.commodity_products")

            model_class_name_in_camel_case : str
                The actual django class model name in CamelCase

        Returns
        -------
        List[str]
            Reveals a model's field as a list with strings

        Notes
        -----
            We use NewType from typing for the function annotation, in order to specify a python import statement (actually just a fancy wrapper for a str variable)

        See
        ---
        https://docs.djangoproject.com/en/1.11/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage
    """

    # To ensure that setup was already done we can check if apps are ready and settings are configured
    if not apps.ready and not settings.configured:

        # Mocks a default settings setup
        settings.configure(DEBUG=True)

        # Mocks a running django application
        django.setup()

    # Imports a database model class from an app
    # model_class = import_module(model_import_statement)
    model_class = getattr(
        import_module(model_import_path), model_class_name_in_camel_case
    )

    # Extract the models attributes, but leave out the "id" field
    model_field_names = [
        field.name for field in model_class._meta.fields if field.name != "id"
    ]

    return model_field_names
