"""Module for resource"""
from typing import Optional

class Resource:
    """Class for resource sub-type within dataset"""

    file_name: str
    file_type: str
    asset_url: str
    date_created: Optional[str]
    date_updated: Optional[str]
    file_size_unit: Optional[str]
    file_size: Optional[float]
    num_records: Optional[int]

    def __init__(
        self,
        file_name: str,
        file_type: str,
        asset_url: str,
        date_created: Optional[str],
        date_updated: Optional[str],
        file_size_unit: Optional[str],
        file_size: Optional[float],
        num_records: Optional[int],
    ) -> None:
        self.file_name = file_name
        self.file_type = file_type
        self.asset_url = asset_url
        self.date_created = date_created
        self.date_updated = date_updated
        self.file_size_unit = file_size_unit
        self.file_size = file_size
        self.num_records = num_records
