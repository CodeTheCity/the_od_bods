from bs4 import BeautifulSoup
from processor import Processor
from classes.dataset import Dataset
from classes.resource import Resource


class ProcessorStagecoach(Processor):
    """Processor for Stagecoach's open data portal"""

    ACCEPTED_REGIONS = [
        "stagecoach bluebird",
        "stagecoach east scotland",
        "stagecoach highlands",
        "stagecoach west scotland",
    ]
    # TODO: Find out licence info from Stagecoach
    DATASETS_LICENCE = "UNKNOWN"

    def __init__(self):
        """Base init for type and URL list"""
        super().__init__(type="bespoke_Stagecoach")

    def filter_rows(self, row):
        row_title = row.select_one("b")

        if row_title is None:
            return False

        return row_title.text.lower() in self.ACCEPTED_REGIONS

    def get_datasets(self, owner, url, fname):
        """Gets datasets from provided portal and outputs to JSON"""
        print(f"Processing {url}")

        portal_html = processor.get_html(url)

        # PATCH: This page contains an unclosed <style> tag so we're closing it
        # TODO: Contact Stagecoach and ask if they can fix their HTML
        portal_html = portal_html.replace("</style\n", "</style>\n")

        parsed_portal_html = BeautifulSoup(portal_html, features="html.parser")
        dataset_list_rows = parsed_portal_html.select(".rich-text .row")

        # Remove non-Scottish rows
        filtered_dataset_list_rows = list(filter(self.filter_rows, dataset_list_rows))

        print(f"Found {len(filtered_dataset_list_rows)} datasets")

        prepped_datasets = []

        for region in filtered_dataset_list_rows:
            region_title = region.select_one("b").text

            dataset_owner = owner
            dataset_page_url = url
            dataset_date_created = None
            dataset_date_updated = None
            dataset_licence = self.DATASETS_LICENCE
            dataset_tags = []

            # Check for presence of download buttons
            schedules_txc_2_1_button = region.select_one(
                "a:-soup-contains('Schedules (TXC 2.1)')"
            )
            schedules_txc_2_4_button = region.select_one(
                "a:-soup-contains('Schedules (TXC 2.4)')"
            )
            has_schedules = schedules_txc_2_1_button or schedules_txc_2_4_button
            fares_button = region.select_one("a:-soup-contains('Fares')")

            # Build title and description
            dataset_title = f"{region_title} - "
            dataset_description = None

            if has_schedules and fares_button:
                dataset_title += "Schedules and Fares"
                dataset_description = (
                    f"Schedules and Fares data for the {region_title} region"
                )
            elif has_schedules:
                dataset_title += "Schedules"
                dataset_description = f"Schedules data for the {region_title} region"
            elif fares_button:
                dataset_title += "Fares"
                dataset_description = f"Fares data for the {region_title} region"

            dataset_resources = []

            buttons = [
                button
                for button in [
                    schedules_txc_2_1_button,
                    schedules_txc_2_4_button,
                    fares_button,
                ]
                if button != None
            ]

            for button in buttons:
                asset_url = button["href"]
                file_size = processor.get_http_content_length(asset_url)
                dataset_resources.append(
                    Resource(
                        button.text,
                        "ZIP",
                        asset_url,
                        dataset_date_created,
                        dataset_date_updated,
                        "B",
                        file_size,
                        None,
                    )
                )

            prepped_datasets.append(
                Dataset(
                    dataset_title,
                    dataset_owner,
                    dataset_page_url,
                    dataset_date_created,
                    dataset_date_updated,
                    dataset_licence,
                    dataset_description,
                    dataset_tags,
                    dataset_resources,
                )
            )

        processor.write_json(fname, prepped_datasets)


processor = ProcessorStagecoach()

if __name__ == "__main__":
    processor.process("json")
