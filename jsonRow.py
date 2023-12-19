import json, dataclasses
from dataclasses import dataclass

@dataclass
class jsonRow:
    Title: str = ""
    Owner: str = ""
    PageURL: str = ""
    AssetURL: str = ""
    FileName: str = ""
    DateCreated: str = ""
    DateUpdated: str = ""
    FileSize: str = ""
    FileSizeUnit: str = ""
    FileType: str = ""
    NumRecords: str = ""
    OriginalTags: str = ""
    ManualTags: str = ""
    License: str = ""
    Description: str = ""

    def __init__(self):
        Title = ""
        Owner = ""
        PageURL = ""
        AssetURL = ""
        FileName = ""
        DateCreated = ""
        DateUpdated = ""
        FileSize = ""
        FileSizeUnit = ""
        FileType = ""
        NumRecords = ""
        OriginalTags = ""
        ManualTags = ""
        License = ""
        Description = ""

    class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

    def toJSON(self):
        return json.dumps(self, cls=self.EnhancedJSONEncoder)
