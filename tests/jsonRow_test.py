import pytest
from ..jsonRow import jsonRow


def test_json_conversion():
    # Test 1 - every attribute populated

    example_row1 = jsonRow()

    example_row1.Title = "Example title"
    example_row1.Owner = "Example owner"
    example_row1.PageURL = "Example original dataset link"
    example_row1.AssetURL = "Example resource link"
    example_row1.FileName = "Example filename"
    example_row1.DateCreated = "05/Nov/2023"
    example_row1.DateUpdated = "05/Dec/2023"
    example_row1.FileSize = "Example size"
    example_row1.FileSizeUnit = "Example size unit"
    example_row1.FileType = "Example file type"
    example_row1.NumRecords = "Example num records"
    example_row1.OriginalTags = "Example tags"
    example_row1.ManualTags = "Example manual tags"
    example_row1.License = "Example licence"
    example_row1.Description = "Example description"

    outputJson1 = example_row1.toJSON()

    expectedJson1 = '{"Title": "Example title", "Owner": "Example owner", "PageURL": "Example original dataset link", "AssetURL": "Example resource link", "FileName": "Example filename", "DateCreated": "05/Nov/2023", "DateUpdated": "05/Dec/2023", "FileSize": "Example size", "FileSizeUnit": "Example size unit", "FileType": "Example file type", "NumRecords": "Example num records", "OriginalTags": "Example tags", "ManualTags": "Example manual tags", "License": "Example licence", "Description": "Example description"}'

    assert outputJson1 == expectedJson1

    # Test 2 - some attributes left as defaults (blank)

    example_row2 = jsonRow()

    example_row2.Title = "Example title"
    example_row2.Owner = "Example owner"
    example_row2.PageURL = "Example original dataset link"
    example_row2.AssetURL = "Example resource link"
    example_row2.FileType = "Example file type"
    example_row2.OriginalTags = "Example tags"
    example_row2.ManualTags = "Example manual tags"
    example_row2.License = "Example licence"
    example_row2.Description = "Example description"

    outputJson2 = example_row2.toJSON()

    expectedJson2 = '{"Title": "Example title", "Owner": "Example owner", "PageURL": "Example original dataset link", "AssetURL": "Example resource link", "FileName": "", "DateCreated": "", "DateUpdated": "", "FileSize": "", "FileSizeUnit": "", "FileType": "Example file type", "NumRecords": "", "OriginalTags": "Example tags", "ManualTags": "Example manual tags", "License": "Example licence", "Description": "Example description"}'

    assert outputJson2 == expectedJson2
