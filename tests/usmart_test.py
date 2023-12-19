import filecmp
import os
from os.path import isfile, join
import csv
import pytest
from .conftest import csv_checker
from .conftest import json_checker
from ..usmart import ProcessorUSMART
import json
import pandas as pd

test_proc = ProcessorUSMART()

EXPECTED_COLUMNS = [
    "Title",
    "Owner",
    "PageURL",
    "AssetURL",
    "FileName",
    "DateCreated",
    "DateUpdated",
    "FileSize",
    "FileSizeUnit",
    "FileType",
    "NumRecords",
    "OriginalTags",
    "ManualTags",
    "License",
    "Description",
]


def list_sources(dir):
    sources_path = os.path.abspath(dir)
    sources = [
        f.split(".")[0]
        for f in os.listdir(sources_path)
        if isfile(join(sources_path, f))
    ]
    return sources


@pytest.mark.parametrize("sources", list_sources("tests/mock_data/usmart"))
def test_get_datasets(sources):
    owner = "test_owner"
    outputdir = "tests/mock_data/output/usmart/"
    start_url = "file:///" + os.path.abspath(
        "tests/mock_data/usmart/" + sources + ".json"
    )
    fname = outputdir + sources + ".json"
    expected_fname = "tests/mock_data/usmart/expected/" + sources + ".json"
    if os.path.exists(fname):
        os.remove(fname)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    test_proc.get_datasets(owner, start_url, fname)

    # Check load of JSON into pandas
    df = pd.read_json(fname)

    test_columns = df.columns

    # Check number of columns matches expected
    assert len(test_columns) == len(
        EXPECTED_COLUMNS
    ), f"Expected {len(EXPECTED_COLUMNS)} columns but USMART JSON actually has {len(test_columns)}"

    # test columns are in expected order
    for ci in range(len(EXPECTED_COLUMNS)):
        expectedc = EXPECTED_COLUMNS[ci]
        testc = test_columns[ci]
        assert expectedc == testc, f"Expected column {expectedc} but got column {testc}"

    # Read JSON from file into json object and check it matches expected output
    with open(fname, "r", newline="", encoding="utf-8") as check_file:
        json_check_file = json.load(check_file)
        assert json_checker(json_check_file)

    assert filecmp.cmp(fname, expected_fname)
