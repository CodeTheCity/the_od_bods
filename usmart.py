try:
    from processor import Processor
    from jsonProcessor import jsonProcessor
    from jsonRow import jsonRow
except:
    from .processor import Processor
    from .jsonProcessor import jsonProcessor
    from .jsonRow import jsonRow


class ProcessorUSMART(jsonProcessor):
    def __init__(self):
        super().__init__(type="USMART")

    def get_datasets(self, owner, start_url, fname):
        data = processor.get_json(start_url)
        if data != "NULL":
            datasets = data["dataset"]
            print("Number of datasets: ", str(len(datasets)))

            prepped = []

            for dataset in datasets:
                Title = dataset["title"]
                Owner = owner
                PageURL = dataset["landingPage"].replace(" ", "%20")
                filetypes = dict()
                for dist in dataset["distribution"]:
                    if "/" in dist["mediaType"]:
                        filetypes[dist["mediaType"].split("/")[1]] = [
                            dist["accessURL"].replace(" ", "%20"),
                            dist["title"],
                        ]
                    else:
                        filetypes[dist["mediaType"]] = [
                            dist["accessURL"].replace(" ", "%20"),
                            dist["title"],
                        ]
                DateCreated = dataset["createdAt"]
                DateUpdated = dataset["modified"]
                Description = '"' + dataset["description"] + '"'
                if (
                    dataset["licence"]
                    == "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
                ):
                    Licence = "OGL3"
                else:
                    Licence = dataset["licence"]
                OriginalTags = []
                for theme in dataset["theme"]:
                    OriginalTags.append(theme)
                ManualTags = []
                if "keyword" in dataset:
                    for kw in dataset["keyword"]:
                        ManualTags.append(kw)
                else:
                    ManualTags.append(" ")

                for item in filetypes:
                    print(filetypes[item][1])

                    # Create jsonRow
                    line = jsonRow()
                    line.Title = Title
                    line.Owner = Owner
                    line.PageURL = PageURL
                    line.AssetURL = filetypes[item][0]
                    line.FileName = filetypes[item][1]
                    line.DateCreated = DateCreated
                    line.DateUpdated = DateUpdated
                    line.FileType = item
                    line.OriginalTags = (" ".join(OriginalTags),)
                    line.ManualTags = (" ".join(ManualTags),)
                    line.license = Licence
                    line.Description = Description

                    prepped.append(line)

            processor.write_json(fname, prepped)

processor = ProcessorUSMART()

if __name__ == "__main__":
    processor.process()
