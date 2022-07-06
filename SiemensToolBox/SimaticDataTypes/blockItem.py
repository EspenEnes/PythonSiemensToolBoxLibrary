from dataclasses import dataclass, field
import re

@dataclass
class BlockItem:
    row: str = field(init=True, repr=False)
    byte: int = field(init=True, default=None, repr=False)
    bit: int = field(init=True, default=None, repr=False)
    name: str = field(init=True, default=None, repr=True)
    type_: any = field(init=True, default=None, repr=True)
    typeValue: any = field(init=True, default=None, repr=False)
    actualValue: any = field(init=True, default=None, repr=False)
    comment: str = field(init=True, default=None, repr=True)

    def __post_init__(self):
        self.parseRow(self.row)

    @property
    def adress(self):
        return f"{self.byte}.{self.bit}"


    def parseRow(self, row):
        comment = re.compile(".*\/\/(.*$)").search(row)
        if comment:
            self.comment = comment.group(1)
            row = row[:comment.start(1) - 2]

        typeValue = re.compile(".*:=(.*)").search(row)
        if typeValue:
            self.typeValue = typeValue.group(1)
            row = row[:typeValue.start(1) - 2]

        _type = re.compile("^(\w+)\s+:\s+(.*)").search(row)
        if _type:
             self.type_ = _type.group(2).replace(";","").strip()
             row = _type.group(1)
        self.name = row



