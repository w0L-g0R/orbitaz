# Create fixture with django commands
from django.core.management.base import BaseCommand
from django.utils import timezone
from orbitaz.utils.fixtures_handler import FixtureHandler


class Command(BaseCommand):
    help = "Creates django model fixtures from xlxs files"

    def add_arguments(self, parser):

        parser.add_argument(
            "fixture_source",
            type=str,
            nargs="?",
            default="xlsx",
            help="Selects a source to create 'commodity products' fixtures from. Could be either 'xlsx' or 'arrays', whereas 'xlsx' is the default",
        )

        parser.add_argument(
            "-cp",
            "--commodity-product",
            action="store_true",
            help="Selects 'commodity products' fixtures to be created",
        )

        parser.add_argument(
            "-u",
            "--unit",
            action="store_true",
            help="Selects 'units fixtures' to be created",
        )

        parser.add_argument(
            "-poo",
            "--point-of-origin",
            action="store_true",
            help="Selects 'points of origin fixtures' to be created",
        )

    def handle(self, *args, **options):

        if options["commodity_product"]:

            # Returns True in case of
            FixtureHandler.setup_fixtures(
                app_name="app",
                fixture_source=options["fixture_source"],
                model_name_in_snake_case="commodity_product",
            )

        if options["unit"]:

            # Returns True in case of
            FixtureHandler.setup_fixtures(
                app_name="app",
                fixture_source=options["fixture_source"],
                model_name_in_snake_case="unit",
            )

        if options["point_of_origin"]:

            # Returns True in case of
            FixtureHandler.setup_fixtures(
                app_name="app",
                fixture_source=options["fixture_source"],
                model_name_in_snake_case="point_of_origin",
            )

        # if successful_setup:
        #     self.stdout.write(
        #         self.style.SUCCESS(
        #             f"Successfully stored fixtures @files/fixtures/{fixture_source}/commodity_products.json"
        #         )
        #     )

        # self.stdout.write(f"Model '{options}' has been selected")
        # self.stdout.write(f"Model '{args}' has been selected")