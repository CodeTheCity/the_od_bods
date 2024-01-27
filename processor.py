import urllib.error
from urllib import request, parse
from urllib.error import HTTPError, URLError
import csv
import json
import os

# TODO: Move this to the classes folder at some point
class Processor:
    USER_AGENT = (
        "Open Data Scotland Scraper - https://github.com/OpenDataScotland/the_od_bods"
    )

    # Type should be one of the following: 'dcat', 'arcgis', 'usmart'
    def __init__(self, type):
        self.type = type
        self.header = [
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
        self.urls = {}

    def get_urls(self):
        with open("sources.csv", "r", encoding="utf-8") as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                if row["Processor"] == self.type:
                    self.urls[row["Name"]] = row["Source URL"]
            for r in csv_file:
                print("r", r)

    def get_json(self, url):
        req = request.Request(url)
        try:
            return json.loads(request.urlopen(req).read().decode())
        except HTTPError as err1:
            print(url, "cannot be accessed. The URL returned:", err1.code, err1.reason)
            error_dict = {
                "url": url,
                "error_code": err1.code,
                "error_reason": err1.reason,
            }
        except URLError as err2:
            print(type(err2))
            print(url, "cannot be accessed. The URL returned:", err2.reason)
            error_dict = {
                "url": url,
                "error_code": "",
                "error_reason": str(err2.reason),
            }
        with open("log.json", "a") as f:
            json.dump(error_dict, f)
        with open("log.md", "a") as file:
            file.write(
                f'| {error_dict["url"]} | {error_dict["error_code"]} | {error_dict["error_reason"]} | \n'
            )

        return "NULL"

    def get_html(self, url):
        """Performs an HTTP request to get the HTML content of the portal page"""
        headers = {"User-Agent": self.USER_AGENT}
        req = request.Request(url, headers=headers)
        try:
            return request.urlopen(req).read().decode()
        except HTTPError as err1:
            print(url, "cannot be accessed. The URL returned:", err1.code, err1.reason)
            error_dict = {
                "url": url,
                "error_code": err1.code,
                "error_reason": err1.reason,
            }
        except URLError as err2:
            print(type(err2))
            print(url, "cannot be accessed. The URL returned:", err2.reason)
            error_dict = {
                "url": url,
                "error_code": "",
                "error_reason": str(err2.reason),
            }

    def get_html_head(self, url):
        """Performs an HTTP HEAD request"""
        headers = {"User-Agent": self.USER_AGENT}
        req = request.Request(url, headers=headers)
        try:
            return request.urlopen(req).info()
        except HTTPError as err1:
            print(url, "cannot be accessed. The URL returned:", err1.code, err1.reason)
            error_dict = {
                "url": url,
                "error_code": err1.code,
                "error_reason": err1.reason,
            }
        except URLError as err2:
            print(type(err2))
            print(url, "cannot be accessed. The URL returned:", err2.reason)
            error_dict = {
                "url": url,
                "error_code": "",
                "error_reason": str(err2.reason),
            }

    def get_http_content_length(self, url):
        """Tries to get file content length without downloading by using a HEAD request"""
        try:
            response_headers = self.get_html_head(url)
            return response_headers["Content-Length"]
        except:            
            return None

    def get_license(self, dataset):
        try:
            # Known Licenses info
            allLicenses = [
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
            ]

            # Return License info, If License 'url' key available
            if "url" in dataset["attributes"]["structuredLicense"]:
                return dataset["attributes"]["structuredLicense"]["url"]
            # Check for License in 'text' key and return the license info, if license 'url' key not available
            elif "text" in dataset["attributes"]["structuredLicense"]:
                for license in allLicenses:
                    if license in dataset["attributes"]["structuredLicense"]["text"]:
                        return license
                return ""
            # Return '', if 'url' & 'text' key not available
            else:
                return ""
        except:
            return ""

    def write_csv(self, fname, prepped):
        with open(fname, "w", newline="", encoding="utf-8") as csvf:
            w = csv.writer(csvf, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
            w.writerow(self.header)
            for r in prepped:
                if r[-1]:
                    r[-1] = r[-1].replace("\n", " ")
                w.writerow(r)

    def write_json(self, fname, prepped):
        with open(fname, "w", encoding="utf8") as json_file:
            json.dump(prepped, json_file, indent=4, default=vars)

    def get_datasets(self, owner, url, fname):
        print("Override this method")

    def process(self, file_type="csv"):
        self.get_urls()

        for name, url in self.urls.items():
            print(name)
            self.get_datasets(
                name, url, os.path.join("data", self.type, f"{name}.{file_type}")
            )
