"""Module for dataset"""
from typing import List
import json
from .resource import Resource


class Dataset:
    """Class for dataset"""

    title: str
    owner: str
    page_url: str
    date_created: str
    date_updated: str
    licence: str
    description: str
    tags: List[str]
    resources: List[Resource]

    def __init__(
        self,
        title: str,
        owner: str,
        page_url: str,
        date_created: str,
        date_updated: str,
        licence: str,
        description: str,
        tags: List[str],
        resources: List[Resource],
    ) -> None:
        self.title = title
        self.owner = owner
        self.page_url = page_url
        self.date_created = date_created
        self.date_updated = date_updated
        self.licence = licence
        self.description = description
        self.tags = tags
        self.resources = resources
