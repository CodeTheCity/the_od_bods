import validators
import pytest
import dateutil.parser


def is_valid_string(str_to_check):
    return isinstance(str_to_check, str)


def is_valid_filename(filename_to_check):
    return is_valid_string(filename_to_check)


def is_valid_date(date_to_check):
    if date_to_check:
        try:
            dateutil.parser.isoparse(date_to_check)
        except ValueError:
            return False
    return True


def is_valid_number(str_to_check):
    if str_to_check:
        return str_to_check.isnumeric()
    return True


def is_valid_file_size_unit(str_to_check):
    file_size_units = [
        "",  # blank
        "bytes",  # alt bytes
        "B",  # Bytes
        "kB",
        "MB",
        "GB",
        "TB",
        "PB",
        "EB",
        "ZB",
        "YB",
        "b",  # bits
        "kb",
        "Mb",
        "Gb",
        "Tb",
        "Pb",
        "Eb",
        "Zb",
        "Yb",
    ]
    return str_to_check in file_size_units


def is_valid_file_type(str_to_check):
    return is_valid_string(str_to_check)


def is_valid_tags(str_to_check):
    return is_valid_string(str_to_check)


def is_valid_tags_json(tags_to_check):
    for thistag in tags_to_check:
        if not is_valid_string(thistag):
            return False
    return True


def is_valid_licence(str_to_check):
    licences = [
        "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/",
        "http://opendatacommons.org/licenses/odbl/1-0/",
        "Open Data Commons Open Database License 1.0",
        "uk-ogl",
        "UK Open Government Licence (OGL)",
        "Open Government Licence 3.0 (United Kingdom)",
        "OGL3",
        "https://creativecommons.org/licenses/by/4.0/legalcode",
        "Creative Commons Attribution 4.0",
        "https://creativecommons.org/licenses/by-sa/3.0/",
        "",
    ]
    return str_to_check in licences


def is_valid_url(url_to_check):
    if url_to_check:
        return validators.url(url_to_check)
    return True


def csv_checker(csv_file):
    result = True
    csv_testers = [
        {"title": "Title", "test_func": is_valid_string},
        {"title": "Owner", "test_func": is_valid_string},
        {"title": "PageURL", "test_func": is_valid_url},
        {"title": "AssetURL", "test_func": is_valid_url},
        {"title": "FileName", "test_func": is_valid_filename},
        {"title": "DateCreated", "test_func": is_valid_date},
        {"title": "DateUpdated", "test_func": is_valid_date},
        {"title": "FileSize", "test_func": is_valid_number},
        {"title": "FileSizeUnit", "test_func": is_valid_file_size_unit},
        {"title": "FileType", "test_func": is_valid_file_type},
        {"title": "NumRecords", "test_func": is_valid_number},
        {"title": "OriginalTags", "test_func": is_valid_tags},
        {"title": "ManualTags", "test_func": is_valid_tags},
        {"title": "License", "test_func": is_valid_licence},
        {"title": "Description", "test_func": is_valid_string},
    ]
    header_row = 0
    for row_idx, row in enumerate(csv_file):
        if row_idx != header_row:
            for col_idx, cell in enumerate(row):
                assert csv_testers[col_idx]["test_func"](cell)
                # result = False
    return result


def json_checker(json_file):
    result = True

    json_testers = {
        "Title": is_valid_string,
        "Owner": is_valid_string,
        "PageURL": is_valid_url,
        "AssetURL": is_valid_url,
        "FileName": is_valid_filename,
        "DateCreated": is_valid_date,
        "DateUpdated": is_valid_date,
        "FileSize": is_valid_number,
        "FileSizeUnit": is_valid_file_size_unit,
        "FileType": is_valid_file_type,
        "NumRecords": is_valid_number,
        "OriginalTags": is_valid_tags_json,
        "ManualTags": is_valid_tags_json,
        "License": is_valid_licence,
        "Description": is_valid_string,
    }

    header_row = 0
    for row in json_file:
        for attribute_key in row.keys():
            this_test_function = json_testers[attribute_key]
            this_test_value = row[attribute_key]
            test_result = this_test_function(this_test_value)
            debug_output = f"{this_test_function.__name__}( {this_test_value} )"
            assert test_result, debug_output
    return result
